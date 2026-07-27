#!/usr/bin/env python3
"""Render the Agentic Music Studio live deck and Whisper review draft."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent
DEFAULT_SCHEMA = ROOT / "Agentic-Music-Studio-presentation.schema.yaml"
DEFAULT_HTML = ROOT / "Agentic-Music-Studio-presentation.html"
DEFAULT_REVIEW = ROOT / "Agentic-Music-Studio-presentation-review.md"


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def attr_words(values: list[str]) -> str:
    return " ".join(esc(value) for value in values)


def load_substrate(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise RuntimeError("Presentation schema must be a mapping.")
    substrate = loaded.get("text_intent_substrate")
    if not isinstance(substrate, dict):
        raise RuntimeError("Missing text_intent_substrate.")
    if substrate.get("human_gate", {}).get("status") != "approved":
        raise RuntimeError("Full generation is blocked until human_gate.status is approved.")
    presentation = substrate.get("presentation")
    if not isinstance(presentation, dict):
        raise RuntimeError("Missing presentation mapping.")
    slides = presentation.get("slides")
    if not isinstance(slides, list) or not slides:
        raise RuntimeError("Presentation must contain slides.")
    seen: set[str] = set()
    for index, slide in enumerate(slides, start=1):
        if not isinstance(slide, dict):
            raise RuntimeError(f"Slide {index} must be a mapping.")
        slide_id = str(slide.get("id", "")).strip()
        if not slide_id or slide_id in seen:
            raise RuntimeError(f"Slide {index} has a missing or duplicate id.")
        seen.add(slide_id)
        for field in (
            "projected_copy",
            "spoken_copy",
            "speaker_notes",
            "authoring_metadata",
            "lanes",
            "visual",
        ):
            if field not in slide:
                raise RuntimeError(f"Slide {slide_id} is missing {field}.")
    return substrate


def render_soundline(visual: dict[str, Any]) -> str:
    labels = visual.get("labels", ["hear", "find"])
    return f"""
      <div class="soundline" aria-hidden="true">
        <span>{esc(labels[0])}</span>
        <svg viewBox="0 0 760 180" role="img" aria-label="A sound wave becoming an editable path">
          <path class="soundline-ghost" d="M5 90 C45 10,75 170,115 90 S185 10,225 90 S295 170,335 90 S405 10,445 90 S515 170,555 90 S625 10,665 90 S725 170,755 90"/>
          <path class="soundline-main" d="M5 90 C45 10,75 170,115 90 S185 10,225 90 S295 170,335 90 S405 10,445 90 S515 170,555 90 S625 10,665 90 S725 170,755 90"/>
          <circle cx="555" cy="90" r="11"/>
          <circle cx="665" cy="90" r="11"/>
        </svg>
        <span>{esc(labels[1])}</span>
      </div>
    """


def render_contrast(visual: dict[str, Any]) -> str:
    sides = (("left", "contrast-fast"), ("right", "contrast-control"))
    cards = []
    for key, class_name in sides:
        item = visual[key]
        cards.append(
            f"""
            <article class="contrast-card {class_name}">
              <p class="card-label">{esc(item["label"])}</p>
              <p>{esc(item["text"])}</p>
            </article>
            """
        )
    return f'<div class="contrast-grid">{"".join(cards)}</div>'


def render_verb_loop(visual: dict[str, Any]) -> str:
    verbs = visual.get("verbs", [])
    items = []
    for index, verb in enumerate(verbs):
        arrow = '<span class="verb-arrow" aria-hidden="true">→</span>' if index < len(verbs) - 1 else ""
        items.append(f'<span class="verb">{esc(verb)}</span>{arrow}')
    return f'<div class="verb-loop">{"".join(items)}</div>'


def render_pipeline(visual: dict[str, Any]) -> str:
    stages = []
    for index, stage in enumerate(visual.get("stages", []), start=1):
        stages.append(
            f"""
            <article class="pipeline-stage">
              <span class="stage-number">{index:02d}</span>
              <h3>{esc(stage["label"])}</h3>
              <p>{esc(stage["text"])}</p>
            </article>
            """
        )
    return f'<div class="pipeline-grid">{"".join(stages)}</div>'


def render_audio_proof(visual: dict[str, Any]) -> str:
    audio = visual["audio"]
    facts = []
    for fact in visual.get("facts", []):
        facts.append(
            f"""
            <article class="fact">
              <strong>{esc(fact["value"])}</strong>
              <span>{esc(fact["label"])}</span>
            </article>
            """
        )
    return f"""
      <div class="proof-grid">
        <article class="audio-card">
          <p class="card-label">{esc(audio["label"])}</p>
          <div class="wave-bars" aria-hidden="true">
            {"".join(f'<i style="--h:{height}%"></i>' for height in (22, 48, 75, 38, 90, 56, 28, 68, 98, 46, 72, 32, 82, 52, 24, 64, 88, 42, 70, 30))}
          </div>
          <audio controls preload="metadata" src="{esc(audio["src"])}">
            Your browser does not support embedded audio.
          </audio>
        </article>
        <div class="fact-grid">{"".join(facts)}</div>
      </div>
    """


def render_evidence_split(visual: dict[str, Any]) -> str:
    cards = []
    for key, class_name in (("measured", "measured"), ("felt", "felt")):
        item = visual[key]
        cards.append(
            f"""
            <article class="evidence-card {class_name}">
              <p class="card-label">{esc(item["label"])}</p>
              <strong>{esc(item["value"])}</strong>
              <p>{esc(item["text"])}</p>
            </article>
            """
        )
    return f'<div class="evidence-grid">{"".join(cards)}</div>'


def render_tradeoff(visual: dict[str, Any]) -> str:
    columns = []
    for key in ("before", "after"):
        item = visual[key]
        columns.append(
            f"""
            <article class="trade-card">
              <p class="card-label">{esc(item["label"])}</p>
              <dl>
                <div><dt>centroid</dt><dd>{esc(item["centroid"])}</dd></div>
                <div><dt>dissonance</dt><dd>{esc(item["dissonance"])}</dd></div>
              </dl>
            </article>
            """
        )
    return f"""
      <div class="tradeoff">
        <div class="trade-grid">{"".join(columns)}</div>
        <p class="trade-consequence">{esc(visual["consequence"])}</p>
      </div>
    """


def render_timeline(visual: dict[str, Any]) -> str:
    steps = []
    for index, step in enumerate(visual.get("steps", []), start=1):
        steps.append(
            f"""
            <article class="timeline-step">
              <span>{index}</span>
              <h3>{esc(step["label"])}</h3>
              <p>{esc(step["text"])}</p>
            </article>
            """
        )
    return f'<div class="timeline">{"".join(steps)}</div>'


def render_roles(visual: dict[str, Any]) -> str:
    roles = []
    for role in visual.get("roles", []):
        roles.append(
            f"""
            <article class="role-card">
              <p class="card-label">{esc(role["label"])}</p>
              <h3>{esc(role["ask"])}</h3>
              <p>{esc(role["proof"])}</p>
            </article>
            """
        )
    return f'<div class="role-grid">{"".join(roles)}</div>'


def render_invitation(visual: dict[str, Any]) -> str:
    examples = "".join(f"<li>{esc(item)}</li>" for item in visual.get("examples", []))
    return f"""
      <div class="invitation-card">
        <p class="card-label">{esc(visual["prompt"])}</p>
        <ul>{examples}</ul>
        <p class="invitation-footer">{esc(visual["footer"])}</p>
      </div>
    """


VISUAL_RENDERERS = {
    "soundline": render_soundline,
    "contrast": render_contrast,
    "verb_loop": render_verb_loop,
    "pipeline": render_pipeline,
    "audio_proof": render_audio_proof,
    "evidence_split": render_evidence_split,
    "tradeoff": render_tradeoff,
    "timeline": render_timeline,
    "roles": render_roles,
    "invitation": render_invitation,
}


def render_visual(visual: dict[str, Any]) -> str:
    visual_type = visual.get("type")
    renderer = VISUAL_RENDERERS.get(str(visual_type))
    if renderer is None:
        raise RuntimeError(f"Unsupported visual type: {visual_type}")
    return renderer(visual)


def render_slide(slide: dict[str, Any], total: int) -> str:
    projected = slide["projected_copy"]
    heading_tag = "h1" if slide["number"] == 1 else "h2"
    support = projected.get("support")
    support_html = f'<p class="support">{esc(support)}</p>' if support else ""
    active = " is-active" if slide["number"] == 1 else ""
    return f"""
      <section
        class="slide layout-{esc(slide["layout"])}{active}"
        data-slide
        data-slide-id="{esc(slide["id"])}"
        data-lane="{attr_words(slide["lanes"])}"
        aria-hidden="{"false" if slide["number"] == 1 else "true"}"
      >
        <div class="slide-copy">
          <p class="eyebrow">{esc(projected["eyebrow"])}</p>
          <{heading_tag}>{esc(projected["headline"])}</{heading_tag}>
          {support_html}
        </div>
        <div class="slide-visual">
          {render_visual(slide["visual"])}
        </div>
        <footer class="slide-folio">
          <span>{slide["number"]:02d}</span>
          <span>Agentic Music Studio</span>
          <span>{total:02d}</span>
        </footer>
      </section>
    """


def render_html(substrate: dict[str, Any], schema_path: Path) -> str:
    presentation = substrate["presentation"]
    slides = presentation["slides"]
    theme = presentation["theme"]
    schema_digest = hashlib.sha256(schema_path.read_bytes()).hexdigest()[:12]
    notes = {
        slide["id"]: {
            "spoken_copy": slide["spoken_copy"],
            "speaker_notes": slide["speaker_notes"],
            "interaction_prompt": slide.get("interaction_prompt"),
        }
        for slide in slides
    }
    overview_items = "".join(
        f'<button type="button" data-overview-target="{esc(slide["id"])}"><span>{slide["number"]:02d}</span>{esc(slide["projected_copy"]["headline"])}</button>'
        for slide in slides
    )
    slides_html = "\n".join(render_slide(slide, len(slides)) for slide in slides)
    note_data = json.dumps(notes, ensure_ascii=True).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="presentation-schema" content="{esc(schema_path.name)}">
  <meta name="presentation-schema-digest" content="{schema_digest}">
  <title>{esc(presentation["title"])} — Collaborator Presentation</title>
  <style>
    :root {{
      color-scheme: light;
      --paper: {esc(theme["paper"])};
      --paper-deep: {esc(theme["paper_deep"])};
      --ink: {esc(theme["ink"])};
      --muted: {esc(theme["muted"])};
      --oxblood: {esc(theme["oxblood"])};
      --burgundy: {esc(theme["burgundy"])};
      --ochre: {esc(theme["ochre"])};
      --rust: {esc(theme["rust"])};
      --serif: {theme["serif"]};
      --sans: {theme["sans"]};
      --line: rgba(33, 27, 22, 0.18);
      --shadow: 0 24px 80px rgba(67, 45, 25, 0.16);
    }}

    * {{ box-sizing: border-box; }}

    html, body {{
      width: 100%;
      height: 100%;
    }}

    body {{
      margin: 0;
      overflow: hidden;
      background: #221d19;
      color: var(--ink);
      font-family: var(--sans);
    }}

    button, input, audio {{ font: inherit; }}

    button {{
      color: inherit;
      cursor: pointer;
    }}

    .xray-compatibility,
    .authoring-contract {{
      display: none !important;
    }}

    .presentation {{
      position: fixed;
      inset: 0;
      width: auto;
      height: auto;
      min-height: 540px;
      isolation: isolate;
      background:
        radial-gradient(circle at 16% 12%, rgba(180, 20, 34, 0.1), transparent 27%),
        radial-gradient(circle at 85% 82%, rgba(199, 173, 122, 0.2), transparent 31%),
        var(--paper);
    }}

    .presentation::before {{
      content: "";
      position: absolute;
      inset: 0;
      z-index: -1;
      pointer-events: none;
      opacity: 0.16;
      background-image:
        repeating-linear-gradient(0deg, rgba(33, 27, 22, 0.05) 0, rgba(33, 27, 22, 0.05) 1px, transparent 1px, transparent 4px);
      mix-blend-mode: multiply;
    }}

    .masthead {{
      position: absolute;
      inset: 0 0 auto;
      z-index: 20;
      height: 64px;
      padding: 0 clamp(24px, 4vw, 64px);
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--line);
      background: rgba(253, 250, 243, 0.88);
      backdrop-filter: blur(14px);
    }}

    .brand {{
      display: flex;
      align-items: baseline;
      gap: 12px;
      min-width: 0;
    }}

    .brand strong {{
      font-family: var(--serif);
      font-size: 1.05rem;
    }}

    .brand span {{
      color: var(--muted);
      font-size: 0.74rem;
      font-weight: 750;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }}

    .masthead-actions {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .counter {{
      min-width: 62px;
      text-align: center;
      font-variant-numeric: tabular-nums;
      color: var(--muted);
      font-size: 0.85rem;
      font-weight: 800;
    }}

    .icon-button {{
      width: 38px;
      height: 38px;
      display: grid;
      place-items: center;
      border: 1px solid var(--line);
      border-radius: 50%;
      background: rgba(253, 250, 243, 0.72);
    }}

    .icon-button:hover,
    .icon-button:focus-visible {{
      border-color: var(--oxblood);
      color: var(--oxblood);
      outline: none;
    }}

    .slides {{
      position: absolute;
      inset: 64px 0 0;
    }}

    .slide {{
      position: absolute;
      inset: 0;
      padding: clamp(44px, 7vh, 78px) clamp(36px, 7vw, 108px) clamp(50px, 8vh, 82px);
      display: grid;
      grid-template-columns: minmax(0, 0.95fr) minmax(420px, 1.05fr);
      grid-template-rows: 1fr auto;
      gap: clamp(24px, 4vw, 72px);
      opacity: 0;
      visibility: hidden;
      transform: translateY(18px);
      transition: opacity 260ms ease, transform 260ms ease, visibility 260ms;
      overflow: hidden;
    }}

    .slide.is-active {{
      opacity: 1;
      visibility: visible;
      transform: translateY(0);
    }}

    .slide-copy {{
      align-self: center;
      max-width: 760px;
    }}

    .eyebrow {{
      margin: 0 0 18px;
      color: var(--burgundy);
      font-size: clamp(0.72rem, 1vw, 0.9rem);
      font-weight: 850;
      letter-spacing: 0.15em;
      text-transform: uppercase;
    }}

    h1, h2 {{
      margin: 0;
      font-family: var(--serif);
      font-weight: 700;
      letter-spacing: -0.035em;
      text-wrap: balance;
    }}

    h1 {{
      font-size: clamp(3.6rem, 6.6vw, 7.2rem);
      line-height: 0.93;
    }}

    h2 {{
      font-size: clamp(3rem, 5.2vw, 5.9rem);
      line-height: 0.96;
    }}

    .support {{
      max-width: 680px;
      margin: 24px 0 0;
      color: var(--muted);
      font-family: var(--serif);
      font-size: clamp(1.08rem, 1.65vw, 1.5rem);
      line-height: 1.4;
    }}

    .slide-visual {{
      align-self: center;
      min-width: 0;
    }}

    .slide-folio {{
      grid-column: 1 / -1;
      display: grid;
      grid-template-columns: auto 1fr auto;
      gap: 14px;
      align-items: center;
      color: var(--muted);
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }}

    .slide-folio span:nth-child(2) {{
      text-align: center;
    }}

    .slide-folio::before {{
      content: "";
      position: absolute;
      left: clamp(36px, 7vw, 108px);
      right: clamp(36px, 7vw, 108px);
      bottom: calc(clamp(50px, 8vh, 82px) + 26px);
      height: 1px;
      background: var(--line);
    }}

    .layout-cover {{
      grid-template-columns: minmax(0, 1.1fr) minmax(360px, 0.9fr);
    }}

    .layout-cover h1 {{
      font-size: clamp(3.3rem, 5vw, 5.7rem);
      line-height: 0.95;
    }}

    .layout-manifesto {{
      grid-template-columns: minmax(0, 1.2fr) minmax(380px, 0.8fr);
    }}

    .card-label {{
      margin: 0;
      color: var(--burgundy);
      font-size: 0.76rem;
      font-weight: 850;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }}

    .soundline {{
      display: grid;
      grid-template-columns: auto 1fr auto;
      gap: 18px;
      align-items: center;
      color: var(--rust);
      font-family: var(--serif);
      font-size: 1.1rem;
      font-style: italic;
    }}

    .soundline svg {{
      width: 100%;
      overflow: visible;
    }}

    .soundline path {{
      fill: none;
      stroke-linecap: round;
    }}

    .soundline-ghost {{
      stroke: var(--ochre);
      stroke-width: 18;
      opacity: 0.26;
    }}

    .soundline-main {{
      stroke: var(--oxblood);
      stroke-width: 4;
    }}

    .soundline circle {{
      fill: var(--paper);
      stroke: var(--oxblood);
      stroke-width: 4;
    }}

    .contrast-grid,
    .evidence-grid,
    .trade-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
    }}

    .contrast-card,
    .evidence-card,
    .trade-card,
    .role-card,
    .audio-card,
    .fact,
    .invitation-card {{
      border: 1px solid var(--line);
      background: rgba(253, 250, 243, 0.78);
      box-shadow: var(--shadow);
    }}

    .contrast-card {{
      min-height: 240px;
      padding: 30px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .contrast-card > p:last-child {{
      margin: 42px 0 0;
      font-family: var(--serif);
      font-size: clamp(1.5rem, 2.5vw, 2.5rem);
      line-height: 1.08;
    }}

    .contrast-fast {{
      border-top: 8px solid var(--ochre);
    }}

    .contrast-control {{
      border-top: 8px solid var(--oxblood);
    }}

    .verb-loop {{
      display: flex;
      align-items: center;
      justify-content: center;
      flex-wrap: wrap;
      gap: 16px;
      padding: 46px 24px;
      border-top: 1px solid var(--line);
      border-bottom: 1px solid var(--line);
    }}

    .verb {{
      font-family: var(--serif);
      font-size: clamp(1.8rem, 3vw, 3.5rem);
      font-weight: 700;
    }}

    .verb:last-of-type {{
      color: var(--oxblood);
    }}

    .verb-arrow {{
      color: var(--ochre);
      font-size: 1.7rem;
    }}

    .layout-pipeline,
    .layout-timeline,
    .layout-roles {{
      grid-template-columns: 1fr;
      grid-template-rows: auto 1fr auto;
    }}

    .layout-pipeline .slide-copy,
    .layout-timeline .slide-copy,
    .layout-roles .slide-copy {{
      align-self: end;
      max-width: 1100px;
    }}

    .layout-pipeline .slide-visual,
    .layout-timeline .slide-visual,
    .layout-roles .slide-visual {{
      align-self: start;
    }}

    .pipeline-grid,
    .timeline {{
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 12px;
    }}

    .pipeline-stage,
    .timeline-step {{
      position: relative;
      min-height: 176px;
      padding: 22px 18px;
      border-top: 3px solid var(--ochre);
      border-bottom: 1px solid var(--line);
    }}

    .pipeline-stage:nth-child(5),
    .timeline-step:nth-child(5) {{
      border-top-color: var(--oxblood);
    }}

    .stage-number,
    .timeline-step > span {{
      color: var(--burgundy);
      font-size: 0.75rem;
      font-weight: 850;
      letter-spacing: 0.1em;
    }}

    .pipeline-stage h3,
    .timeline-step h3,
    .role-card h3 {{
      margin: 22px 0 10px;
      font-family: var(--serif);
      font-size: clamp(1.25rem, 1.6vw, 1.7rem);
      line-height: 1.1;
    }}

    .pipeline-stage p,
    .timeline-step p,
    .role-card p {{
      margin: 0;
      color: var(--muted);
      line-height: 1.45;
    }}

    .proof-grid {{
      display: grid;
      gap: 18px;
    }}

    .audio-card {{
      padding: 24px;
      border-top: 8px solid var(--oxblood);
    }}

    .audio-card audio {{
      width: 100%;
      margin-top: 20px;
    }}

    .wave-bars {{
      height: 86px;
      display: flex;
      gap: 7px;
      align-items: center;
      margin-top: 18px;
    }}

    .wave-bars i {{
      flex: 1;
      height: var(--h);
      min-width: 3px;
      background: linear-gradient(180deg, var(--oxblood), var(--rust));
      border-radius: 999px;
      opacity: 0.84;
    }}

    .fact-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }}

    .fact {{
      min-height: 132px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .fact strong {{
      color: var(--burgundy);
      font-family: var(--serif);
      font-size: 2.8rem;
      line-height: 1;
    }}

    .fact span {{
      color: var(--muted);
      font-size: 0.84rem;
      line-height: 1.3;
    }}

    .evidence-card {{
      min-height: 300px;
      padding: 28px;
    }}

    .evidence-card strong {{
      display: block;
      margin: 48px 0 16px;
      font-family: var(--serif);
      font-size: clamp(2.5rem, 4vw, 4.8rem);
      line-height: 1;
    }}

    .evidence-card > p:last-child {{
      margin: 0;
      color: var(--muted);
      font-size: 1rem;
      line-height: 1.5;
    }}

    .evidence-card.measured {{
      border-top: 8px solid var(--ochre);
    }}

    .evidence-card.felt {{
      border-top: 8px solid var(--oxblood);
    }}

    .tradeoff {{
      display: grid;
      gap: 16px;
    }}

    .trade-card {{
      padding: 24px;
    }}

    .trade-card dl {{
      margin: 28px 0 0;
      display: grid;
      gap: 16px;
    }}

    .trade-card dl div {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 18px;
      border-bottom: 1px solid var(--line);
      padding-bottom: 10px;
    }}

    .trade-card dt {{
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-size: 0.72rem;
    }}

    .trade-card dd {{
      margin: 0;
      font-family: var(--serif);
      font-size: 2rem;
      font-weight: 700;
    }}

    .trade-consequence {{
      margin: 0;
      padding: 18px 20px;
      color: var(--paper);
      background: var(--burgundy);
      font-family: var(--serif);
      font-size: 1.3rem;
      text-align: center;
    }}

    .role-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
    }}

    .role-card {{
      min-height: 230px;
      padding: 24px;
      border-top: 6px solid var(--ochre);
    }}

    .role-card:nth-child(2) {{
      border-top-color: var(--rust);
    }}

    .role-card:nth-child(3) {{
      border-top-color: var(--oxblood);
    }}

    .layout-invitation {{
      grid-template-columns: minmax(0, 1.15fr) minmax(360px, 0.85fr);
    }}

    .invitation-card {{
      padding: 28px;
      border-top: 8px solid var(--oxblood);
    }}

    .invitation-card ul {{
      margin: 28px 0;
      padding: 0;
      list-style: none;
      display: grid;
      gap: 12px;
    }}

    .invitation-card li {{
      padding-bottom: 12px;
      border-bottom: 1px solid var(--line);
      font-family: var(--serif);
      font-size: 1.2rem;
    }}

    .invitation-footer {{
      margin: 0;
      color: var(--muted);
      font-size: 0.76rem;
      font-weight: 800;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }}

    .progress {{
      position: absolute;
      z-index: 22;
      left: 0;
      right: 0;
      bottom: 0;
      height: 4px;
      background: rgba(33, 27, 22, 0.12);
    }}

    .progress span {{
      display: block;
      width: 10%;
      height: 100%;
      background: var(--oxblood);
      transition: width 220ms ease;
    }}

    .notes-panel {{
      position: absolute;
      z-index: 40;
      right: 24px;
      bottom: 28px;
      width: min(520px, calc(100vw - 48px));
      max-height: 72vh;
      padding: 22px;
      overflow: auto;
      border: 1px solid rgba(253, 250, 243, 0.22);
      background: rgba(33, 27, 22, 0.96);
      color: var(--paper);
      box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
      transform: translateY(22px);
      opacity: 0;
      visibility: hidden;
      transition: opacity 180ms ease, transform 180ms ease, visibility 180ms;
    }}

    body.show-notes .notes-panel {{
      opacity: 1;
      visibility: visible;
      transform: translateY(0);
    }}

    .notes-panel .card-label {{
      color: var(--ochre);
    }}

    .notes-panel h2 {{
      margin: 8px 0 12px;
      color: var(--paper);
      font-family: var(--serif);
      font-size: 1.35rem;
      letter-spacing: 0;
    }}

    .notes-panel p {{
      margin: 0 0 18px;
      color: rgba(253, 250, 243, 0.82);
      line-height: 1.55;
    }}

    .notes-panel .prompt {{
      padding: 12px 14px;
      border-left: 4px solid var(--oxblood);
      background: rgba(253, 250, 243, 0.08);
    }}

    .overview {{
      position: fixed;
      inset: 0;
      z-index: 60;
      display: grid;
      place-items: center;
      padding: 32px;
      background: rgba(33, 27, 22, 0.82);
      backdrop-filter: blur(12px);
      opacity: 0;
      visibility: hidden;
      transition: opacity 160ms ease, visibility 160ms;
    }}

    body.show-overview .overview {{
      opacity: 1;
      visibility: visible;
    }}

    .overview-card {{
      width: min(980px, 100%);
      max-height: 82vh;
      overflow: auto;
      padding: 28px;
      background: var(--paper);
      box-shadow: 0 28px 100px rgba(0, 0, 0, 0.42);
    }}

    .overview-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      margin-bottom: 20px;
    }}

    .overview-header h2 {{
      font-size: 2.2rem;
    }}

    .overview-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }}

    .overview-grid button {{
      min-height: 78px;
      display: grid;
      grid-template-columns: 42px 1fr;
      gap: 12px;
      align-items: center;
      text-align: left;
      border: 1px solid var(--line);
      background: transparent;
      padding: 14px;
    }}

    .overview-grid button:hover,
    .overview-grid button:focus-visible {{
      border-color: var(--oxblood);
      outline: none;
    }}

    .overview-grid button span {{
      color: var(--burgundy);
      font-weight: 850;
    }}

    @media (max-width: 1080px) {{
      .slide {{
        grid-template-columns: minmax(0, 1fr);
        grid-template-rows: auto 1fr auto;
        gap: 22px;
        overflow: auto;
      }}

      .slide-copy {{
        align-self: end;
      }}

      h1 {{ font-size: clamp(3.2rem, 8vw, 5.8rem); }}
      h2 {{ font-size: clamp(2.6rem, 6.4vw, 4.7rem); }}

      .slide-visual {{
        align-self: start;
      }}
    }}

    @media (max-width: 760px) {{
      body {{ overflow: auto; }}
      .presentation {{
        position: relative;
        inset: auto;
        width: 100%;
        height: auto;
        min-height: 100svh;
      }}
      .masthead {{ padding: 0 16px; }}
      .brand span {{ display: none; }}
      .slides {{ position: relative; min-height: calc(100svh - 64px); }}
      .slide {{
        padding: 32px 18px 72px;
        min-height: calc(100svh - 64px);
      }}
      .contrast-grid,
      .evidence-grid,
      .trade-grid,
      .fact-grid,
      .role-grid,
      .overview-grid {{
        grid-template-columns: 1fr;
      }}
      .pipeline-grid,
      .timeline {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}
      .pipeline-stage:last-child,
      .timeline-step:last-child {{
        grid-column: 1 / -1;
      }}
      .soundline {{ grid-template-columns: 1fr; }}
      .soundline span {{ display: none; }}
      .verb-loop {{ justify-content: flex-start; }}
      .slide-folio::before {{ left: 18px; right: 18px; }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      *, *::before, *::after {{
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
      }}
    }}

    @media print {{
      body {{ overflow: visible; background: white; }}
      .presentation {{ width: auto; height: auto; }}
      .masthead, .progress, .notes-panel, .overview {{ display: none !important; }}
      .slides {{ position: static; }}
      .slide {{
        position: relative;
        min-height: 100vh;
        opacity: 1;
        visibility: visible;
        transform: none;
        break-after: page;
      }}
    }}
  </style>
</head>
<body>
  <div class="xray-compatibility" aria-hidden="true">
    <input id="toggle-surface" type="checkbox" checked>
    <input id="toggle-flow" type="checkbox" checked>
    <input id="toggle-deps" type="checkbox" checked>
    <input id="toggle-risk" type="checkbox" checked>
  </div>
  <div class="authoring-contract" aria-hidden="true">
    source-backed · inference · L0 static HTML/SVG · reader terms · reader outcomes · why it matters
  </div>

  <main class="presentation">
    <header class="masthead">
      <div class="brand">
        <strong>{esc(presentation["title"])}</strong>
        <span>{esc(presentation["subtitle"])}</span>
      </div>
      <div class="masthead-actions">
        <button class="icon-button" id="previous" type="button" aria-label="Previous slide">←</button>
        <span class="counter" id="counter">01 / {len(slides):02d}</span>
        <button class="icon-button" id="next" type="button" aria-label="Next slide">→</button>
        <button class="icon-button" id="notes-toggle" type="button" aria-label="Toggle presenter notes" aria-pressed="false">N</button>
        <button class="icon-button" id="overview-toggle" type="button" aria-label="Open slide overview" aria-pressed="false">O</button>
      </div>
    </header>

    <div class="slides" id="slides">
      {slides_html}
    </div>

    <aside class="notes-panel" id="notes-panel" aria-label="Presenter notes">
      <p class="card-label">Spoken copy</p>
      <h2 id="spoken-copy"></h2>
      <p class="card-label">Speaker notes</p>
      <p id="speaker-notes"></p>
      <div id="interaction-wrap">
        <p class="card-label">Interaction prompt</p>
        <p class="prompt" id="interaction-prompt"></p>
      </div>
    </aside>

    <div class="progress" aria-hidden="true"><span id="progress"></span></div>
  </main>

  <div class="overview" id="overview" aria-hidden="true">
    <section class="overview-card">
      <header class="overview-header">
        <h2>Presentation map</h2>
        <button class="icon-button" id="overview-close" type="button" aria-label="Close slide overview">×</button>
      </header>
      <div class="overview-grid">{overview_items}</div>
    </section>
  </div>

  <script id="presentation-notes" type="application/json">{note_data}</script>
  <script>
    (() => {{
      const slides = Array.from(document.querySelectorAll("[data-slide]"));
      const notes = JSON.parse(document.getElementById("presentation-notes").textContent);
      const counter = document.getElementById("counter");
      const progress = document.getElementById("progress");
      const spoken = document.getElementById("spoken-copy");
      const speakerNotes = document.getElementById("speaker-notes");
      const promptWrap = document.getElementById("interaction-wrap");
      const prompt = document.getElementById("interaction-prompt");
      const notesToggle = document.getElementById("notes-toggle");
      const overviewToggle = document.getElementById("overview-toggle");
      const overview = document.getElementById("overview");
      let index = 0;

      function pad(value) {{
        return String(value).padStart(2, "0");
      }}

      function show(nextIndex, updateHash = true) {{
        index = Math.max(0, Math.min(slides.length - 1, nextIndex));
        slides.forEach((slide, slideIndex) => {{
          const active = slideIndex === index;
          slide.classList.toggle("is-active", active);
          slide.setAttribute("aria-hidden", String(!active));
        }});
        const slide = slides[index];
        const slideNotes = notes[slide.dataset.slideId];
        counter.textContent = `${{pad(index + 1)}} / ${{pad(slides.length)}}`;
        progress.style.width = `${{((index + 1) / slides.length) * 100}}%`;
        spoken.textContent = slideNotes.spoken_copy;
        speakerNotes.textContent = slideNotes.speaker_notes;
        prompt.textContent = slideNotes.interaction_prompt || "";
        promptWrap.hidden = !slideNotes.interaction_prompt;
        if (window.innerWidth > 760) window.scrollTo(0, 0);
        if (updateHash) history.replaceState(null, "", `#${{slide.dataset.slideId}}`);
      }}

      function toggleNotes(force) {{
        const nextState = typeof force === "boolean" ? force : !document.body.classList.contains("show-notes");
        document.body.classList.toggle("show-notes", nextState);
        notesToggle.setAttribute("aria-pressed", String(nextState));
      }}

      function toggleOverview(force) {{
        const nextState = typeof force === "boolean" ? force : !document.body.classList.contains("show-overview");
        document.body.classList.toggle("show-overview", nextState);
        overviewToggle.setAttribute("aria-pressed", String(nextState));
        overview.setAttribute("aria-hidden", String(!nextState));
      }}

      document.getElementById("previous").addEventListener("click", () => show(index - 1));
      document.getElementById("next").addEventListener("click", () => show(index + 1));
      notesToggle.addEventListener("click", () => toggleNotes());
      overviewToggle.addEventListener("click", () => toggleOverview());
      document.getElementById("overview-close").addEventListener("click", () => toggleOverview(false));

      document.querySelectorAll("[data-overview-target]").forEach((button) => {{
        button.addEventListener("click", () => {{
          const targetIndex = slides.findIndex((slide) => slide.dataset.slideId === button.dataset.overviewTarget);
          if (targetIndex >= 0) show(targetIndex);
          toggleOverview(false);
        }});
      }});

      window.addEventListener("hashchange", () => {{
        const targetId = window.location.hash.slice(1);
        const targetIndex = slides.findIndex((slide) => slide.dataset.slideId === targetId);
        if (targetIndex >= 0 && targetIndex !== index) show(targetIndex, false);
      }});

      document.addEventListener("keydown", (event) => {{
        if (event.key === "ArrowRight" || event.key === "PageDown" || event.key === " ") {{
          event.preventDefault();
          show(index + 1);
        }}
        if (event.key === "ArrowLeft" || event.key === "PageUp") {{
          event.preventDefault();
          show(index - 1);
        }}
        if (event.key === "Home") show(0);
        if (event.key === "End") show(slides.length - 1);
        if (event.key.toLowerCase() === "n") toggleNotes();
        if (event.key.toLowerCase() === "o") toggleOverview();
        if (event.key === "Escape") {{
          toggleNotes(false);
          toggleOverview(false);
        }}
      }});

      const requestedId = window.location.hash.slice(1);
      const requestedIndex = slides.findIndex((slide) => slide.dataset.slideId === requestedId);
      show(requestedIndex >= 0 ? requestedIndex : 0, false);
    }})();
  </script>
</body>
</html>
"""


def review_paragraph(label: str, text: str) -> str:
    return f"**{label}** — {text.strip()}"


def render_review_markdown(substrate: dict[str, Any]) -> str:
    presentation = substrate["presentation"]
    lines = [f'# {presentation["title"]} — Presentation Review', ""]
    for slide in presentation["slides"]:
        slide_label = f'S{slide["number"]:02d}'
        projected = slide["projected_copy"]
        projected_text = " ".join(
            str(value).strip()
            for value in (
                projected.get("eyebrow"),
                projected.get("headline"),
                projected.get("support"),
            )
            if value
        )
        lines.extend(
            [
                f'## {slide_label} · {slide["id"]}',
                "",
                review_paragraph(f"{slide_label} · projected_copy", projected_text),
                "",
                review_paragraph(f"{slide_label} · spoken_copy", str(slide["spoken_copy"])),
                "",
                review_paragraph(f"{slide_label} · speaker_notes", str(slide["speaker_notes"])),
                "",
            ]
        )
        if slide.get("interaction_prompt"):
            lines.extend(
                [
                    review_paragraph(
                        f"{slide_label} · interaction_prompt",
                        str(slide["interaction_prompt"]),
                    ),
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--review-markdown", type=Path, default=DEFAULT_REVIEW)
    args = parser.parse_args()

    substrate = load_substrate(args.schema)
    html_text = render_html(substrate, args.schema)
    html_text = "\n".join(line.rstrip() for line in html_text.splitlines()) + "\n"
    args.html.write_text(html_text, encoding="utf-8")
    args.review_markdown.write_text(render_review_markdown(substrate), encoding="utf-8")
    print(f"WROTE {args.html}")
    print(f"WROTE {args.review_markdown}")
    print(f"SLIDES {len(substrate['presentation']['slides'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
