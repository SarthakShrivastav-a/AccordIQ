# Backend Scope

The backend owns the SaaS tenancy model, auth enforcement, Slack capture,
entity extraction, grounded query answers, Notion sync boundaries, audit
events, worker queues, and usage metering.

The API is organization-aware by default. Workspace data is available only to
users with organization or workspace membership.
