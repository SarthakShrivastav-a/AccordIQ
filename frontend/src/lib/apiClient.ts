import { demoEntities, demoJobs, demoWorkspaces } from "./demoData";
import { Entity, Job, QueryResponse, Workspace } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_ACCORDIQ_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit, fallback?: T): Promise<T> {
  try {
    const response = await fetch(`${API_BASE}${path}`, { ...init, headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) } });
    if (!response.ok) throw new Error(`Request failed: ${response.status}`);
    const data = await response.json();
    if (Array.isArray((data as { items?: unknown[] }).items) && (data as { items: unknown[] }).items.length === 0 && fallback) return fallback;
    return data as T;
  } catch {
    if (fallback) return fallback;
    throw new Error(`Unable to reach AccordIQ API at ${API_BASE}`);
  }
}

export const apiClient = {
  health: () => request<{ status: string }>("/health", undefined, { status: "offline-demo" }),
  version: () => request<{ version: string }>("/version", undefined, { version: "0.1.1" }),
  workspaces: () => request<{ items: Workspace[] }>("/api/admin/workspaces", undefined, { items: demoWorkspaces }),
  workspace: (id: string) => request<Workspace>(`/api/admin/workspaces/${id}`, undefined, demoWorkspaces.find((workspace) => workspace.workspace_id === id) ?? demoWorkspaces[0]),
  entities: (workspaceId = "demo-workspace") => request<{ items: Entity[] }>(`/api/admin/workspaces/${workspaceId}/entities`, undefined, { items: demoEntities }),
  jobs: (workspaceId = "demo-workspace") => request<{ items: Job[] }>(`/api/admin/workspaces/${workspaceId}/jobs`, undefined, { items: demoJobs }),
  metrics: (workspaceId = "demo-workspace") => request<Record<string, number | string>>(`/api/admin/workspaces/${workspaceId}/metrics`, undefined, { workspace_id: workspaceId, captured_messages: 128, entities: 42, queries: 19 }),
  query: (payload: { workspace_id: string; user_id: string; text: string }) => request<QueryResponse>("/api/query", { method: "POST", body: JSON.stringify(payload) }, { answer: "Based on captured Slack context, the team agreed to keep Notion as the durable task system.", intent: "recall", grounded: true, citations: [{ title: "Source message", url: "https://slack.example/source", preview: payload.text }] })
};
