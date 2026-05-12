from __future__ import annotations

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from accordiq.models.graph_run import GraphRun
from accordiq.models.message import SlackMessage


class QueryService:
    async def answer(self, session: AsyncSession, workspace_id: str, user_id: str, text: str, channel_id: str | None = None) -> dict:
        terms = [term.strip() for term in text.split() if len(term.strip()) >= 4][:6]
        conditions = [SlackMessage.workspace_id == workspace_id, SlackMessage.deleted.is_(False)]
        if channel_id:
            conditions.append(SlackMessage.channel_id == channel_id)
        if terms:
            conditions.append(or_(*[SlackMessage.redacted_text.ilike(f"%{term}%") for term in terms]))
        result = await session.execute(select(SlackMessage).where(*conditions).order_by(SlackMessage.created_at.desc()).limit(5))
        messages = result.scalars().all()
        citations = [
            {
                "title": f"#{message.channel_id} at {message.message_ts}",
                "url": message.permalink or "",
                "preview": message.redacted_text[:160],
            }
            for message in messages
        ]
        grounded = bool(citations)
        answer = "I found matching captured context. Review the citations before acting on it." if grounded else "I do not have enough captured context to answer that."
        payload = {"workspace_id": workspace_id, "user_id": user_id, "text": text, "answer": answer, "intent": "recall", "citations": citations, "grounded": grounded}
        session.add(GraphRun(workspace_id=workspace_id, graph_name="query", status="completed", state_json=payload))
        await session.commit()
        return payload
