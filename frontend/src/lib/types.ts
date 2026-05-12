export type Workspace = {
  workspace_id: string;
  name: string;
  capture_enabled: boolean;
  retention_days: number;
  channel_mode: string;
  last_activity: string | null;
  role?: string | null;
};

export type Entity = {
  id: string;
  title: string;
  entity_type: "task" | "decision" | "question" | "fyi";
  confidence: number;
  status: "active" | "review" | "ignored" | "done";
  source: string;
};

export type Job = {
  id: string;
  job_type: string;
  status: "queued" | "running" | "failed" | "done";
  error?: string;
};

export type QueryResponse = {
  answer: string;
  intent: string;
  grounded: boolean;
  citations: { title: string; url: string; preview: string }[];
};

export type Membership = {
  workspace_id: string;
  role: string;
};

export type User = {
  id: string;
  email: string;
  name?: string | null;
  picture?: string | null;
  memberships: Membership[];
};

export type AuditEvent = {
  id: string;
  workspace_id: string;
  actor_id?: string | null;
  action: string;
  target_type: string;
  target_id?: string | null;
  payload: Record<string, unknown>;
  created_at?: string | null;
};
