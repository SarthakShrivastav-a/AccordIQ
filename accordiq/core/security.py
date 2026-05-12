from __future__ import annotations

import base64
import hashlib
import hmac
import time
from datetime import timedelta
from typing import Any

import jwt

from accordiq.core.config import JwtSettings
from accordiq.core.time import utc_now


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


def hash_oauth_state(state: str) -> str:
    return hashlib.sha256(state.encode("utf-8")).hexdigest()


def create_access_token(user_id: str, email: str, jwt_settings: JwtSettings) -> str:
    if not jwt_settings.secret:
        raise ValueError(f"missing JWT secret env var: {jwt_settings.secret_env}")
    issued_at = utc_now()
    expires_at = issued_at + timedelta(minutes=jwt_settings.access_token_ttl_minutes)
    payload: dict[str, Any] = {
        "sub": user_id,
        "email": email,
        "iss": jwt_settings.issuer,
        "aud": jwt_settings.audience,
        "iat": int(issued_at.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    return jwt.encode(payload, jwt_settings.secret, algorithm=jwt_settings.algorithm)


def decode_access_token(token: str, jwt_settings: JwtSettings) -> dict[str, Any]:
    if not jwt_settings.secret:
        raise ValueError(f"missing JWT secret env var: {jwt_settings.secret_env}")
    return jwt.decode(
        token,
        jwt_settings.secret,
        algorithms=[jwt_settings.algorithm],
        issuer=jwt_settings.issuer,
        audience=jwt_settings.audience,
    )
