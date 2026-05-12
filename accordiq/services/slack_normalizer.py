from __future__ import annotations

import re

USER_RE = re.compile(r"<@([A-Z0-9]+)>")
CHANNEL_RE = re.compile(r"<#([A-Z0-9]+)\|([^>]+)>")

def normalize_slack_text(text: str) -> str:
    text = USER_RE.sub(lambda m: "@" + m.group(1), text)
    text = CHANNEL_RE.sub(lambda m: "#" + m.group(2), text)
    return text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").strip()

def chunk_text(text: str, chunk_tokens: int, overlap_tokens: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    chunks = []
    step = max(1, chunk_tokens - overlap_tokens)
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + chunk_tokens]))
        if start + chunk_tokens >= len(words):
            break
    return chunks
