from __future__ import annotations

from accordiq.graphs.extraction.nodes import classify_node, extract_node, score_node, validate_node

def run_extraction_graph(initial_state: dict) -> dict:
    state = dict(initial_state)
    for node in [classify_node, extract_node, validate_node, score_node]:
        state.update(node(state))
    return state
