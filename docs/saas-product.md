# AccordIQ SaaS Product

AccordIQ is positioned as an AI team-memory SaaS for Slack-first teams that
need decisions, tasks, open questions, and rationale captured into governed,
cited records.

## Wedge

Start with Slack + Notion teams. AccordIQ listens only where configured,
extracts reviewable entities, keeps citations back to source messages, and
syncs durable records into Notion.

## Tenant Model

- Organization: customer account.
- Workspace: Slack workspace or capture boundary under an organization.
- User: Google-authenticated human.
- Organization membership: owner, admin, or viewer.
- Workspace membership: direct workspace-level access where needed.
- Integration connection: Slack/Notion status per organization.
- Usage event: metered product activity per organization.

## Current SaaS Capabilities

- Create organization after Google login.
- Manage members and invite records.
- Track Slack and Notion integration status.
- Edit organization capture policy.
- Track usage for captured messages, extracted entities, grounded queries, and Notion syncs.
- Enforce organization/workspace authorization on protected APIs.

Billing is intentionally not implemented yet.
