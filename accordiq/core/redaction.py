from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RedactionResult:
    text: str
    count: int


def redact_text(text: str, patterns: dict[str, str], enabled: list[str], replacement: str = "[REDACTED]") -> RedactionResult:
    count = 0
    redacted = text
    for name in enabled:
        pattern = patterns.get(name)
        if not pattern:
            continue
        redacted, changed = re.subn(pattern, replacement, redacted)
        count += changed
    return RedactionResult(text=redacted, count=count)
