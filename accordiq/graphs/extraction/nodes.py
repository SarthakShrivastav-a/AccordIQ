from __future__ import annotations

import re
from accordiq.core.config import get_settings
from accordiq.services.entity_service import build_accordiq_id, route_entity_status

TASK_PATTERNS = ["i will", "i'll", "can you", "please handle", "by "]
DECISION_PATTERNS = ["decided", "we choose", "go with", "agreed"]
QUESTION_PATTERNS = ["?", "who owns", "open question"]

def classify_node(state: dict) -> dict:
    text = state.get("text", "").lower()
    kinds = []
    if any(p in text for p in TASK_PATTERNS):
        kinds.append("task")
    if any(p in text for p in DECISION_PATTERNS):
        kinds.append("decision")
    if any(p in text for p in QUESTION_PATTERNS):
        kinds.append("question")
    return {"candidate_types": kinds or ["fyi"]}

def extract_node(state: dict) -> dict:
    settings = get_settings()
    entities = []
    for kind in state.get("candidate_types", ["fyi"]):
        title = re.sub(r"\s+", " ", state.get("text", "").strip())[:90] or "Untitled"
        confidence = 0.82 if kind != "fyi" else 0.45
        status = route_entity_status(confidence, settings.workflow.confidence_threshold)
        entities.append({
            "accordiq_id": build_accordiq_id(state.get("workspace_id", ""), state.get("source", {}).get("message_ts", ""), kind, title),
            "entity_type": kind,
            "title": title,
            "confidence": confidence,
            "status": status,
            "source": state.get("source", {}),
        })
    return {"entities": entities}

def validate_node(state: dict) -> dict:
    errors = []
    for entity in state.get("entities", []):
        if not entity.get("title") or not entity.get("entity_type"):
            errors.append("entity_missing_required_fields")
    return {"errors": errors}

def score_node(state: dict) -> dict:
    entities = state.get("entities", [])
    confidence = max((entity.get("confidence", 0) for entity in entities), default=0)
    return {"confidence": confidence, "status": "failed" if state.get("errors") else "ready"}
