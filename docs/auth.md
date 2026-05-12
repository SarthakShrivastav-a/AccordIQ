# AccordIQ Authentication

AccordIQ uses Google OAuth for sign-in and AccordIQ-issued JWT bearer tokens for API access. The browser stores the access token in `localStorage` and sends it as `Authorization: Bearer <token>`.

## Required Environment

Configure these values outside the repo:

```text
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
ACCORDIQ_JWT_SECRET=
```

The names, redirect URI, token issuer/audience, TTL, invite list, CORS origins, and frontend callback URLs are defined in `config/app.yaml`.

## Google OAuth Setup

Create an OAuth client in Google Cloud Console and set the redirect URI to:

```text
http://localhost:8000/api/auth/google/callback
```

For deployed environments, update `auth.google.redirect_uri`, `auth.frontend_success_url`, `auth.frontend_error_url`, and `auth.cors_origins` in the YAML config used by that environment.

## Access Policy

Only emails listed in `auth.invites.allowed_emails` can sign in. After a successful invite-gated login, AccordIQ maps the user's email domain to a workspace. The domain display name can be configured in `auth.workspace_domain_map`.

Protected endpoints require a valid JWT and workspace membership:

```text
GET /api/auth/me
GET /api/admin/**
POST /api/query
POST /api/capture/replay
POST /api/extraction/reprocess/{message_id}
```

Public endpoints remain available for health checks, webhooks, and OAuth bootstrap.
