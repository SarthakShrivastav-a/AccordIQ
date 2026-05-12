from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from accordiq.api.deps import get_current_user, require_workspace_member
from accordiq.db.session import get_db_session
from accordiq.graphs.extraction.graph import run_extraction_graph
from accordiq.models.auth import User
from accordiq.schemas.query import QueryRequest
from accordiq.services.query_service import QueryService

router = APIRouter(prefix="/api", tags=["internal"])
query_service = QueryService()


@router.post("/query")
async def query(payload: QueryRequest, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    await require_workspace_member(payload.workspace_id, user, session)
    return await query_service.answer(session, payload.workspace_id, user.id, payload.text, payload.channel_id)


@router.post("/capture/replay")
async def replay(payload: dict, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    workspace_id = payload.get("workspace_id")
    if workspace_id:
        await require_workspace_member(workspace_id, user, session)
    return {"queued": True, "payload": payload}


@router.post("/extraction/reprocess/{message_id}")
async def reprocess(message_id: str, user: User = Depends(get_current_user)):
    return run_extraction_graph({"message_id": message_id, "text": "reprocess requested", "source": {"message_ts": message_id}, "requested_by": user.id})
