export type Workspace = {
  workspace_id: string;
  name: string;
  capture_enabled: boolean;
  retention_days: number;
  channel_mode: string;
  last_activity: string;
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
