from __future__ import annotations

import base64
import hashlib
import hmac
import time


def verify_slack_signature(body: bytes, timestamp: str | None, signature: str | None, signing_secret: str, tolerance_seconds: int) -> bool:
    if not timestamp or not signature or not signing_secret:
        return False
    try:
        ts = int(timestamp)
    except ValueError:
        return False
    if abs(int(time.time()) - ts) > tolerance_seconds:
        return False
    base = b"v0:" + timestamp.encode() + b":" + body
    digest = "v0=" + hmac.new(signing_secret.encode(), base, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature)


def deterministic_id(*parts: str, prefix: str = "acc") -> str:
    digest = hashlib.sha1(":".join(parts).encode("utf-8")).hexdigest()[:24]
    return f"{prefix}_{digest}"


def mask_token(token: str) -> str:
    if len(token) <= 8:
        return "*" * len(token)
    return token[:4] + "*" * (len(token) - 8) + token[-4:]


def encode_dev_secret(value: str, key: str) -> str:
    material = hashlib.sha256(key.encode()).digest()
    data = bytes(ch ^ material[i % len(material)] for i, ch in enumerate(value.encode()))
    return base64.urlsafe_b64encode(data).decode()


def decode_dev_secret(value: str, key: str) -> str:
    material = hashlib.sha256(key.encode()).digest()
    data = base64.urlsafe_b64decode(value.encode())
    return bytes(ch ^ material[i % len(material)] for i, ch in enumerate(data)).decode()
