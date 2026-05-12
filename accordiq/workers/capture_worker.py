from __future__ import annotations

from accordiq.graphs.extraction.graph import run_extraction_graph
from accordiq.services.slack_normalizer import normalize_slack_text

async def process_capture_job(payload: dict) -> dict:
    text = normalize_slack_text(payload.get("text", ""))
    return run_extraction_graph({**payload, "text": text})
