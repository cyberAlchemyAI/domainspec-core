#!/usr/bin/env node
"use strict";

/*
 * Deterministic offline audition mastering through the repository's shared
 * Playwright/Chromium runtime. The caller validates the profile and wraps the
 * derived WAV in a canonical receipt; this renderer owns only DSP and encoding.
 */

const fs = require("fs");


function fail(message) {
  process.stderr.write(`master-render-error: ${message}\n`);
  process.exitCode = 1;
}


async function main() {
  const [inputPath, outputPath, profilePath, playwrightModule, chromiumPath] =
    process.argv.slice(2);
  if (!inputPath || !outputPath || !profilePath || !playwrightModule || !chromiumPath) {
    throw new Error(
      "expected input, output, profile, Playwright module, and Chromium executable"
    );
  }
  if (fs.existsSync(outputPath)) {
    throw new Error("refusing to overwrite renderer output");
  }

  const profile = JSON.parse(fs.readFileSync(profilePath, "utf8"));
  const audioBase64 = fs.readFileSync(inputPath).toString("base64");
  const { chromium } = require(playwrightModule);
  const browser = await chromium.launch({
    executablePath: chromiumPath,
    headless: true,
  });
  try {
    const browserVersion = await browser.version();
    const page = await browser.newPage();
    const rendered = await page.evaluate(
      async ({ audioBase64, profile }) => {
        function linearFromDb(db) {
          return Math.pow(10, db / 20);
        }

        function dbFromLinear(value) {
          return value > 0 ? 20 * Math.log10(value) : null;
        }

        function seededNoise(seed) {
          let state = seed >>> 0;
          return () => {
            state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
            return state / 4294967296;
          };
        }

        function buildImpulse(context, settings) {
          const sampleRate = context.sampleRate;
          const length = Math.ceil(settings.rt60_seconds * sampleRate);
          const impulse = context.createBuffer(2, length, sampleRate);
          const seeds = [settings.seed_left, settings.seed_right];
          const reflectionGains = [0.90, 0.56, 0.34];

          for (let channel = 0; channel < 2; channel += 1) {
            const data = impulse.getChannelData(channel);
            const random = seededNoise(seeds[channel]);
            let smoothed = 0;
            for (let index = 0; index < length; index += 1) {
              const time = index / sampleRate;
              const decay = Math.exp((-6.907755278982137 * time) / settings.rt60_seconds);
              const noise = random() * 2 - 1;
              smoothed = 0.31 * noise + 0.69 * smoothed;
              data[index] = smoothed * decay * 0.15;
            }
            for (let tap = 0; tap < settings.early_reflections_ms.length; tap += 1) {
              const stereoOffset = channel === 0 ? tap * 0.7 : (2 - tap) * 0.9;
              const index = Math.round(
                ((settings.early_reflections_ms[tap] + stereoOffset) / 1000) * sampleRate
              );
              if (index < length) {
                data[index] += reflectionGains[tap];
              }
            }

            let energy = 0;
            for (let index = 0; index < length; index += 1) {
              energy += data[index] * data[index];
            }
            const scale = energy > 0 ? 1 / Math.sqrt(energy) : 1;
            for (let index = 0; index < length; index += 1) {
              data[index] *= scale;
            }
          }
          return impulse;
        }

        function writeAscii(view, offset, value) {
          for (let index = 0; index < value.length; index += 1) {
            view.setUint8(offset + index, value.charCodeAt(index));
          }
        }

        function encodePcm24Wav(left, right, sampleRate, gain) {
          const channels = 2;
          const bitsPerSample = 24;
          const bytesPerSample = 3;
          const blockAlign = channels * bytesPerSample;
          const dataSize = left.length * blockAlign;
          const bytes = new Uint8Array(44 + dataSize);
          const view = new DataView(bytes.buffer);
          writeAscii(view, 0, "RIFF");
          view.setUint32(4, 36 + dataSize, true);
          writeAscii(view, 8, "WAVE");
          writeAscii(view, 12, "fmt ");
          view.setUint32(16, 16, true);
          view.setUint16(20, 1, true);
          view.setUint16(22, channels, true);
          view.setUint32(24, sampleRate, true);
          view.setUint32(28, sampleRate * blockAlign, true);
          view.setUint16(32, blockAlign, true);
          view.setUint16(34, bitsPerSample, true);
          writeAscii(view, 36, "data");
          view.setUint32(40, dataSize, true);

          let offset = 44;
          for (let index = 0; index < left.length; index += 1) {
            for (const source of [left, right]) {
              const sample = Math.max(-1, Math.min(0.9999998807907104, source[index] * gain));
              let integer = sample < 0
                ? Math.round(sample * 0x800000)
                : Math.round(sample * 0x7fffff);
              if (integer < 0) integer += 0x1000000;
              bytes[offset] = integer & 0xff;
              bytes[offset + 1] = (integer >>> 8) & 0xff;
              bytes[offset + 2] = (integer >>> 16) & 0xff;
              offset += 3;
            }
          }
          return bytes;
        }

        function bytesToBase64(bytes) {
          const chunkSize = 0x8000;
          let binary = "";
          for (let offset = 0; offset < bytes.length; offset += chunkSize) {
            binary += String.fromCharCode(...bytes.subarray(offset, offset + chunkSize));
          }
          return btoa(binary);
        }

        const binary = atob(audioBase64);
        const encoded = new Uint8Array(binary.length);
        for (let index = 0; index < binary.length; index += 1) {
          encoded[index] = binary.charCodeAt(index);
        }
        const decodeContext = new OfflineAudioContext(
          1,
          1,
          profile.render.sample_rate_hz
        );
        const decoded = await decodeContext.decodeAudioData(encoded.buffer.slice(0));
        const sampleRate = profile.render.sample_rate_hz;
        const playbackRate = profile.performance?.playback_rate ?? 1;
        const performedSourceDuration = decoded.duration / playbackRate;
        const outputFrames = Math.ceil(
          (performedSourceDuration + profile.render.tail_seconds) * sampleRate
        );
        const context = new OfflineAudioContext(2, outputFrames, sampleRate);
        const source = context.createBufferSource();
        source.buffer = decoded;
        source.playbackRate.value = playbackRate;

        const dryHighpass = context.createBiquadFilter();
        dryHighpass.type = "highpass";
        dryHighpass.frequency.value = profile.cleanup.dry_highpass_hz;
        dryHighpass.Q.value = 0.707;

        const highShelf = context.createBiquadFilter();
        highShelf.type = "highshelf";
        highShelf.frequency.value = profile.tone?.high_shelf_frequency_hz ?? 3200;
        highShelf.gain.value = profile.tone?.high_shelf_gain_db ?? 0;

        const compressor = context.createDynamicsCompressor();
        compressor.threshold.value = profile.dynamics.threshold_db;
        compressor.knee.value = profile.dynamics.knee_db;
        compressor.ratio.value = profile.dynamics.ratio;
        compressor.attack.value = profile.dynamics.attack_ms / 1000;
        compressor.release.value = profile.dynamics.release_ms / 1000;

        const dryGain = context.createGain();
        dryGain.gain.value = 1;
        source
          .connect(dryHighpass)
          .connect(highShelf)
          .connect(compressor)
          .connect(dryGain)
          .connect(context.destination);

        const wetHighpass = context.createBiquadFilter();
        wetHighpass.type = "highpass";
        wetHighpass.frequency.value = profile.reverb.input_highpass_hz;
        wetHighpass.Q.value = 0.707;
        const wetLowpass = context.createBiquadFilter();
        wetLowpass.type = "lowpass";
        wetLowpass.frequency.value = profile.reverb.input_lowpass_hz;
        wetLowpass.Q.value = 0.707;
        const preDelay = context.createDelay(1);
        preDelay.delayTime.value = profile.reverb.pre_delay_ms / 1000;
        const convolver = context.createConvolver();
        convolver.normalize = false;
        convolver.buffer = buildImpulse(context, profile.reverb);
        const wetGain = context.createGain();
        wetGain.gain.value = linearFromDb(profile.reverb.wet_db);
        source
          .connect(wetHighpass)
          .connect(wetLowpass)
          .connect(preDelay)
          .connect(convolver)
          .connect(wetGain)
          .connect(context.destination);

        source.start(0);
        const result = await context.startRendering();
        const left = result.getChannelData(0);
        const right = result.getChannelData(1);
        let peakBefore = 0;
        let sumSquares = 0;
        for (let index = 0; index < left.length; index += 1) {
          peakBefore = Math.max(peakBefore, Math.abs(left[index]), Math.abs(right[index]));
          sumSquares += left[index] * left[index] + right[index] * right[index];
        }
        const rmsBefore = Math.sqrt(sumSquares / (left.length * 2));
        const ceiling = linearFromDb(profile.dynamics.target_peak_dbfs);
        let requestedGain = 1;
        if (typeof profile.dynamics.target_rms_dbfs === "number") {
          const targetRms = linearFromDb(profile.dynamics.target_rms_dbfs);
          const rmsGain = rmsBefore > 0 ? targetRms / rmsBefore : 1;
          const maxMakeup = linearFromDb(profile.dynamics.max_makeup_db);
          requestedGain = Math.min(rmsGain, maxMakeup);
        }
        const ceilingGain = peakBefore > 0 ? ceiling / peakBefore : 1;
        const ceilingLimited = ceilingGain < requestedGain;
        const gain = Math.min(requestedGain, ceilingGain);
        const peakAfter = peakBefore * gain;
        const rmsAfter = rmsBefore * gain;
        const wav = encodePcm24Wav(left, right, sampleRate, gain);
        return {
          audio_base64: bytesToBase64(wav),
          metrics: {
            applied_master_gain_db: dbFromLinear(gain),
            ceiling_limited: ceilingLimited,
            channels: 2,
            duration_seconds: result.duration,
            high_shelf_gain_db: profile.tone?.high_shelf_gain_db ?? 0,
            peak_dbfs: dbFromLinear(peakAfter),
            pitch_shift_cents: 1200 * Math.log2(playbackRate),
            pitch_shift_semitones: 12 * Math.log2(playbackRate),
            playback_rate: playbackRate,
            performed_source_duration_seconds: performedSourceDuration,
            rms_dbfs: dbFromLinear(rmsAfter),
            sample_rate_hz: sampleRate,
            source_duration_seconds: decoded.duration,
            source_sample_rate_hz: decoded.sampleRate,
          },
        };
      },
      { audioBase64, profile }
    );
    const output = Buffer.from(rendered.audio_base64, "base64");
    fs.writeFileSync(outputPath, output, { flag: "wx", mode: 0o600 });
    process.stdout.write(
      JSON.stringify({
        browser_version: browserVersion,
        metrics: rendered.metrics,
        output_size_bytes: output.length,
        status: "rendered",
      }) + "\n"
    );
  } finally {
    await browser.close();
  }
}


main().catch((error) => fail(error instanceof Error ? error.message : "unknown failure"));
