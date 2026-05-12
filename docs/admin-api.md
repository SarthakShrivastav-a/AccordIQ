# Admin and SaaS APIs

AccordIQ exposes protected SaaS and admin APIs. All protected requests require
`Authorization: Bearer <accordiq_jwt>`.

## SaaS APIs

- `POST /api/orgs` creates an organization for the current user.
- `GET /api/orgs` lists organizations the current user belongs to.
- `GET /api/orgs/{org_id}` returns organization details.
- `GET /api/orgs/{org_id}/members` lists members.
- `POST /api/orgs/{org_id}/invites` creates an invite record.
- `GET /api/orgs/{org_id}/integrations` returns Slack/Notion status.
- `POST /api/orgs/{org_id}/integrations/slack/start` marks Slack setup pending.
- `POST /api/orgs/{org_id}/integrations/notion/start` marks Notion setup pending.
- `GET /api/orgs/{org_id}/usage` returns usage counters.
- `GET /api/orgs/{org_id}/capture-policy` returns capture policy.
- `PATCH /api/orgs/{org_id}/capture-policy` updates capture policy.

## Admin APIs

Workspace, entity, job, audit, metrics, export, query, replay, and reprocess
APIs are membership-protected and must never return data across tenant
boundaries.
