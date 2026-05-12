import { Entity, Job, Workspace } from "./types";

export const demoWorkspaces: Workspace[] = [
  { workspace_id: "demo-workspace", name: "Founding Team", capture_enabled: true, retention_days: 365, channel_mode: "invited_channels", last_activity: "2m ago" },
  { workspace_id: "design-lab", name: "Design Lab", capture_enabled: true, retention_days: 180, channel_mode: "allowlist", last_activity: "18m ago" },
  { workspace_id: "ops-room", name: "Ops Room", capture_enabled: false, retention_days: 90, channel_mode: "invited_channels", last_activity: "1h ago" }
];

export const demoEntities: Entity[] = [
  { id: "ent_1", title: "Draft onboarding rollback plan", entity_type: "task", confidence: 0.86, status: "active", source: "#eng" },
  { id: "ent_2", title: "Use Notion as system of record", entity_type: "decision", confidence: 0.91, status: "active", source: "#product" },
  { id: "ent_3", title: "Who owns private channel policy?", entity_type: "question", confidence: 0.49, status: "review", source: "#ops" }
];

export const demoJobs: Job[] = [
  { id: "job_1", job_type: "capture", status: "done" },
  { id: "job_2", job_type: "notion_sync", status: "queued" },
  { id: "job_3", job_type: "query", status: "failed", error: "No citations found" }
];
