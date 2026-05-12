from __future__ import annotations

def dead_letter_payload(job_type: str, payload: dict, error: str) -> dict:
    return {"job_type": job_type, "payload": payload, "error": error, "status": "dead_letter"}
