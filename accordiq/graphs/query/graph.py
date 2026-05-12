from __future__ import annotations

from accordiq.graphs.query.nodes import judge_node, plan_node, respond_node, retrieve_node

def run_query_graph(initial_state: dict) -> dict:
    state = dict(initial_state)
    for node in [plan_node, retrieve_node, respond_node, judge_node]:
        state.update(node(state))
    return state
