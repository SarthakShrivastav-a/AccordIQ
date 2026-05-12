from __future__ import annotations

import secrets
from datetime import timedelta
from urllib.parse import urlencode

import httpx
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accordiq.core.config import AuthSettings, get_settings
from accordiq.core.security import create_access_token, hash_oauth_state
from accordiq.core.time import utc_now
from accordiq.models.auth import OAuthState, User, WorkspaceMembership
from accordiq.models.workspace import Workspace


class AuthError(Exception):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


class AuthService:
    google_authorization_url = "https://accounts.google.com/o/oauth2/v2/auth"
    google_token_url = "https://oauth2.googleapis.com/token"

    def __init__(self, auth: AuthSettings | None = None) -> None:
        self.auth = auth or get_settings().auth

    async def build_google_start_url(self, session: AsyncSession) -> str:
        if not self.auth.google.client_id:
            raise AuthError("google_client_not_configured")
        state = secrets.token_urlsafe(32)
        session.add(OAuthState(state_hash=hash_oauth_state(state), expires_at=utc_now() + timedelta(minutes=10)))
        await session.commit()
        query = urlencode(
            {
                "client_id": self.auth.google.client_id,
                "redirect_uri": self.auth.google.redirect_uri,
                "response_type": "code",
                "scope": " ".join(self.auth.google.scopes),
                "state": state,
                "access_type": "offline",
                "prompt": "select_account",
            }
        )
        return f"{self.google_authorization_url}?{query}"

    async def handle_google_callback(self, session: AsyncSession, code: str | None, state: str | None) -> str:
        if not code or not state:
            raise AuthError("missing_google_callback_params")
        await self._consume_state(session, state)
        token_payload = await self._exchange_code(code)
        user_info = self._verify_id_token(token_payload.get("id_token"))
        email = str(user_info.get("email", "")).lower()
        if not email or email not in {item.lower() for item in self.auth.invites.allowed_emails}:
            raise AuthError("email_not_invited")
        user = await self._upsert_user(session, user_info)
        await self._ensure_workspace_membership(session, user)
        await session.commit()
        return create_access_token(user.id, user.email, self.auth.jwt)

    async def _consume_state(self, session: AsyncSession, state: str) -> None:
        result = await session.execute(select(OAuthState).where(OAuthState.state_hash == hash_oauth_state(state)))
        oauth_state = result.scalar_one_or_none()
        if not oauth_state or oauth_state.consumed_at is not None or oauth_state.expires_at < utc_now():
            raise AuthError("invalid_oauth_state")
        oauth_state.consumed_at = utc_now()

    async def _exchange_code(self, code: str) -> dict:
        if not self.auth.google.client_secret:
            raise AuthError("google_secret_not_configured")
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                self.google_token_url,
                data={
                    "code": code,
                    "client_id": self.auth.google.client_id,
                    "client_secret": self.auth.google.client_secret,
                    "redirect_uri": self.auth.google.redirect_uri,
                    "grant_type": "authorization_code",
                },
            )
        if response.status_code >= 400:
            raise AuthError("google_token_exchange_failed")
        return response.json()

    def _verify_id_token(self, raw_id_token: str | None) -> dict:
        if not raw_id_token:
            raise AuthError("missing_google_id_token")
        try:
            return id_token.verify_oauth2_token(raw_id_token, google_requests.Request(), self.auth.google.client_id)
        except ValueError as exc:
            raise AuthError("invalid_google_id_token") from exc

    async def _upsert_user(self, session: AsyncSession, user_info: dict) -> User:
        email = str(user_info["email"]).lower()
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user is None:
            user = User(email=email, google_sub=str(user_info["sub"]))
            session.add(user)
        user.name = user_info.get("name")
        user.picture = user_info.get("picture")
        user.google_sub = str(user_info["sub"])
        user.status = "active"
        await session.flush()
        return user

    async def _ensure_workspace_membership(self, session: AsyncSession, user: User) -> None:
        domain = user.email.split("@", 1)[1]
        workspace_name = self.auth.workspace_domain_map.get(domain, domain)
        result = await session.execute(select(Workspace).where(Workspace.slack_team_id == domain))
        workspace = result.scalar_one_or_none()
        if workspace is None:
            workspace = Workspace(slack_team_id=domain, name=workspace_name, capture_enabled=True, settings_json={})
            session.add(workspace)
            await session.flush()
        membership_result = await session.execute(
            select(WorkspaceMembership).where(
                WorkspaceMembership.user_id == user.id,
                WorkspaceMembership.workspace_id == workspace.id,
            )
        )
        if membership_result.scalar_one_or_none() is None:
            session.add(WorkspaceMembership(user_id=user.id, workspace_id=workspace.id, role="admin"))
