from __future__ import annotations

from fastapi import APIRouter
from accordiq.graphs.extraction.graph import run_extraction_graph
from accordiq.graphs.query.graph import run_query_graph
from accordiq.schemas.query import QueryRequest

router = APIRouter(prefix="/api", tags=["internal"])

@router.post("/query")
async def query(payload: QueryRequest):
    return run_query_graph(payload.model_dump())

@router.post("/capture/replay")
async def replay(payload: dict):
    return {"queued": True, "payload": payload}

@router.post("/extraction/reprocess/{message_id}")
async def reprocess(message_id: str):
    return run_extraction_graph({"message_id": message_id, "text": "reprocess requested", "source": {"message_ts": message_id}})
