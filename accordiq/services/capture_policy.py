from __future__ import annotations

def should_capture_event(event: dict, paused_users: set[str], ignored_channels: set[str], ignore_bot_messages: bool = True) -> tuple[bool, str]:
    if ignore_bot_messages and (event.get("bot_id") or event.get("subtype") == "bot_message"):
        return False, "bot_message"
    if event.get("user") in paused_users:
        return False, "user_paused"
    if event.get("channel") in ignored_channels:
        return False, "channel_ignored"
    if event.get("subtype") in {"channel_join", "channel_leave"}:
        return False, "noise_subtype"
    if not (event.get("text") or "").strip():
        return False, "empty_text"
    return True, "capturable"
