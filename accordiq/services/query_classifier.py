from __future__ import annotations

def classify_query(text: str) -> str:
    lowered = text.lower()
    if any(term in lowered for term in ["open task", "working on", "status"]):
        return "status"
    if any(term in lowered for term in ["decide", "decided", "landed on"]):
        return "recall"
    if any(term in lowered for term in ["who owns", "who is on", "owner"]):
        return "people"
    if any(term in lowered for term in ["this week", "timeline", "happened"]):
        return "timeline"
    if "open question" in lowered or "unknown" in lowered:
        return "unknowns"
    return "recall"
