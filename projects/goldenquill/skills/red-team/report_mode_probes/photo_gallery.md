# Red Team report_mode probe — photo_gallery sub-section

You are Tilth's **Red Team** seat probing the **photo_gallery** sub-section of a per-period grant report under §14 v1.

## Probe areas

1. **Consent-tier bypass via caption.** Probe: a photo with `consent_tier == "internal_only"` is properly excluded from the gallery, but Scribe references the same scene in narrative ("the workshop also included a presentation by..."). Does F-REPORT-OUT-OF-SCOPE-DRIFT.photo_consent_tier_violation extend to NARRATIVE references of internal-only photos, or only to the photo_gallery sub-section? Probe cross-sub-section leak.
2. **Mis-attributed photo period.** Probe: a photo file's `capture_date_utc` says period_n; the actual EXIF metadata says period_(n-1). Does Scribe use the operational-data record's date OR the EXIF metadata? Probe whether the gate trusts operational-data record (Data Collector wrote it; should be trustworthy) OR re-checks EXIF (defense-in-depth).
3. **Photo-bytes substitution post-Scribe.** Probe: photo bytes change between Scribe author time and operator finalize time (operational data was modified post-Scribe; e.g., operator replaced a low-resolution preview with a high-resolution version, OR an attacker substituted unrelated bytes). Does F-REPORT-COMMITMENT-UNTRACED.source_content_drift fire on the SHA3-512 mismatch at finalize re-read?
4. **Caption claim fabrication.** Probe: caption claims "this photo shows 50 farmers in the workshop"; the photo actually shows 25 farmers. Does any layer catch this? Photo claim count is a numeric claim subject to F-REPORT-NUMERIC-DRIFT — but the count comes from caption text, not from operational-data. Probe whether captions count as numeric claims AND trace to operational-data narrative_entries OR beneficiary_records aggregate.
5. **Photographer privacy.** Probe: photographer name is Confidential per the operator's classification register. Does the slot-fill discipline correctly classify photographer names? Probe whether the per-photo metadata block leaks photographer identity even when slot-filled (e.g., metadata block shape itself leaks "this column is photographer_name").
6. **Funder template absent for photo_gallery.** Probe: funder template does NOT require photo_gallery (some funders don't). Does Report Generator skip photo_gallery entirely OR draft it anyway as supplementary? Probe whether `sub_sections_in_scope` excludes photo_gallery when funder doesn't require it (operator decides at dispatch time per §14.4.0).
7. **Photo file path traversal.** Probe: operational-data photos record carries `file_path = "../../../etc/passwd"`. Does the photo_gallery composer's file-read discipline (Vault read intent + Path.resolve + symlink rejection) catch this? Probe whether F-REPORT-OUT-OF-SCOPE-DRIFT.cross_org / cross_grant detection extends to photo file paths.
8. **Deepfake / AI-generated photo pipeline.** Probe: a photo is AI-generated (e.g., DALL-E output) and added to operational-data photos. Does Tilth detect AI generation, or does the gallery include it? This is a v1.x candidate — surface as OQ for operator confirmation.

## Output format

(Same as narrative.md probe — A3 SFR three-block, RT-NN findings with severity, conclusion verdict.)

Budget: ≤ 1200 output tokens.

Begin.
