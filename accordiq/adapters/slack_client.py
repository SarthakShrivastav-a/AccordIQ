from __future__ import annotations

class SlackClient:
    def __init__(self, token: str | None = None) -> None:
        self.token = token

    async def post_message(self, channel: str, text: str, thread_ts: str | None = None) -> dict:
        return {"ok": True, "channel": channel, "text": text, "thread_ts": thread_ts}

    async def update_message(self, channel: str, ts: str, text: str) -> dict:
        return {"ok": True, "channel": channel, "ts": ts, "text": text}
