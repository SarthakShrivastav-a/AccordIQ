from __future__ import annotations

from accordiq.services.query_classifier import classify_query

def plan_node(state: dict) -> dict:
    return {"intent": classify_query(state.get("text", ""))}

def retrieve_node(state: dict) -> dict:
    return {"retrieved": state.get("retrieved", [])}

def respond_node(state: dict) -> dict:
    sources = state.get("retrieved", [])
    if not sources:
        return {"answer": "I do not have enough in memory to answer that.", "citations": [], "grounded": False}
    return {"answer": "Based on the captured Slack context, here is the grounded answer.", "citations": sources, "grounded": True}

def judge_node(state: dict) -> dict:
    return {"grounded": bool(state.get("citations"))}
