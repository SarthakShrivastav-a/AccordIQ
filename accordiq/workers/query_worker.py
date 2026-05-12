from __future__ import annotations

from accordiq.graphs.query.graph import run_query_graph

async def process_query_job(payload: dict) -> dict:
    return run_query_graph(payload)
