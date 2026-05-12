import os
import uuid
from datetime import timedelta

import pytest
from sqlalchemy import select

from accordiq.core.config import get_settings
from accordiq.core.security import create_access_token, decode_access_token, hash_oauth_state
from accordiq.core.time import utc_now
from accordiq.db.session import AsyncSessionLocal, init_models
from accordiq.models.auth import OAuthState, User, WorkspaceMembership
from accordiq.services.auth_service import AuthError, AuthService


@pytest.mark.asyncio
async def test_jwt_round_trip():
    os.environ["ACCORDIQ_JWT_SECRET"] = "test-jwt-secret-for-accordiq-auth-tests"
    token = create_access_token("user-1", "person@example.com", get_settings().auth.jwt)
    claims = decode_access_token(token, get_settings().auth.jwt)
    assert claims["sub"] == "user-1"
    assert claims["email"] == "person@example.com"


@pytest.mark.asyncio
async def test_google_callback_rejects_uninvited_email(monkeypatch):
    await init_models()
    os.environ["GOOGLE_CLIENT_ID"] = "google-client"
    os.environ["GOOGLE_CLIENT_SECRET"] = "google-secret"
    os.environ["ACCORDIQ_JWT_SECRET"] = "test-jwt-secret-for-accordiq-auth-tests"
    auth = get_settings().auth.model_copy(deep=True)
    auth.invites.allowed_emails = ["allowed@example.com"]
    service = AuthService(auth)

    async def exchange(_: str) -> dict:
        return {"id_token": "id-token"}

    monkeypatch.setattr(service, "_exchange_code", exchange)
    monkeypatch.setattr(service, "_verify_id_token", lambda _: {"email": "blocked@example.com", "sub": "google-1", "name": "Blocked"})
    async with AsyncSessionLocal() as session:
        state = f"state-{uuid.uuid4().hex}"
        session.add(OAuthState(state_hash=hash_oauth_state(state), expires_at=utc_now() + timedelta(minutes=5)))
        await session.commit()
        with pytest.raises(AuthError, match="email_not_invited"):
            await service.handle_google_callback(session, "code", state)


@pytest.mark.asyncio
async def test_google_callback_creates_user_and_membership(monkeypatch):
    await init_models()
    os.environ["GOOGLE_CLIENT_ID"] = "google-client"
    os.environ["GOOGLE_CLIENT_SECRET"] = "google-secret"
    os.environ["ACCORDIQ_JWT_SECRET"] = "test-jwt-secret-for-accordiq-auth-tests"
    email = f"person-{uuid.uuid4().hex[:8]}@example.com"
    auth = get_settings().auth.model_copy(deep=True)
    auth.invites.allowed_emails = [email]
    auth.workspace_domain_map = {"example.com": "Example Workspace"}
    service = AuthService(auth)

    async def exchange(_: str) -> dict:
        return {"id_token": "id-token"}

    monkeypatch.setattr(service, "_exchange_code", exchange)
    monkeypatch.setattr(service, "_verify_id_token", lambda _: {"email": email, "sub": f"google-{uuid.uuid4().hex}", "name": "Person"})
    async with AsyncSessionLocal() as session:
        url = await service.build_google_start_url(session)
        state = url.split("state=", 1)[1].split("&", 1)[0]
        token = await service.handle_google_callback(session, "code", state)
        assert decode_access_token(token, auth.jwt)["email"] == email
        user = (await session.execute(select(User).where(User.email == email))).scalar_one()
        membership = (await session.execute(select(WorkspaceMembership).where(WorkspaceMembership.user_id == user.id))).scalar_one()
        assert membership.role == "admin"
