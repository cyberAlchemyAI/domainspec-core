"""Local-only Channel G intake adapter.

This module is a deterministic in-memory boundary around the Channel G parser.
It performs no file I/O, live fetch, network access, automation,
model invocations, database mutations, API behavior, UI behavior,
generation, or external transmission.
"""

from pipeline.scout._channel_g_parser import (
    ChannelGParseResult,
    parse_channel_g_csv_text,
)


def ingest_local_channel_g_csv(
    csv_text: str,
    *,
    applied_as_entity_id: str,
    source_filename: str,
    imported_at_utc: str,
) -> ChannelGParseResult:
    """Parse raw Channel G CSV text through the local deterministic parser."""
    if not isinstance(csv_text, str):
        raise TypeError("csv_text must be a string")
    if not isinstance(applied_as_entity_id, str) or not applied_as_entity_id.strip():
        raise ValueError("applied_as_entity_id must be a non-empty string")
    if not isinstance(source_filename, str) or not source_filename.strip():
        raise ValueError("source_filename must be a non-empty string")
    if not isinstance(imported_at_utc, str) or not imported_at_utc.strip():
        raise ValueError("imported_at_utc must be a non-empty string")

    return parse_channel_g_csv_text(
        csv_text,
        applied_as_entity_id=applied_as_entity_id.strip(),
        source_filename=source_filename.strip(),
        imported_at_utc=imported_at_utc.strip(),
    )
