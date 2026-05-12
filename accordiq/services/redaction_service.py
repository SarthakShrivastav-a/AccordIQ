from __future__ import annotations

import yaml
from pathlib import Path
from accordiq.core.config import get_settings
from accordiq.core.redaction import redact_text

def redact_customer_text(text: str) -> str:
    settings = get_settings()
    config = yaml.safe_load(Path("config/redaction.yaml").read_text(encoding="utf-8"))
    result = redact_text(text, config["patterns"], settings.security.redaction_patterns, config["replacement"])
    return result.text
