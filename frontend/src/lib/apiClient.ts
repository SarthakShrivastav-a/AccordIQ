import { AuditEvent, CapturePolicy, Entity, Integration, Job, Organization, OrganizationMember, QueryResponse, Usage, User, Workspace } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_ACCORDIQ_API_BASE_URL ?? "http://localhost:8000";
const TOKEN_KEY = "accordiq_access_token";

export function getAccessToken() {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(TOKEN_KEY);
}

export function setAccessToken(token: string) {
  window.localStorage.setItem(TOKEN_KEY, token);
}

export function clearAccessToken() {
  if (typeof window !== "undefined") window.localStorage.removeItem(TOKEN_KEY);
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getAccessToken();
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(init?.headers ?? {})
    }
  });
  if (response.status === 401) {
    clearAccessToken();
    if (typeof window !== "undefined") window.location.assign("/login");
    throw new Error("Authentication required");
  }
  if (!response.ok) throw new Error(`Request failed: ${response.status}`);
  return response.json() as Promise<T>;
}

export const authStartUrl = `${API_BASE}/api/auth/google/start`;

export const apiClient = {
  health: () => request<{ status: string }>("/health"),
  version: () => request<{ version: string }>("/version"),
  me: () => request<User>("/api/auth/me"),
  organizations: () => request<Organization[]>("/api/orgs"),
  createOrganization: (payload: { name: string }) => request<Organization>("/api/orgs", { method: "POST", body: JSON.stringify(payload) }),
  organization: (id: string) => request<Organization>(`/api/orgs/${id}`),
  organizationMembers: (id: string) => request<OrganizationMember[]>(`/api/orgs/${id}/members`),
  inviteMember: (id: string, payload: { email: string; role: string }) => request(`/api/orgs/${id}/invites`, { method: "POST", body: JSON.stringify(payload) }),
  integrations: (id: string) => request<Integration[]>(`/api/orgs/${id}/integrations`),
  startSlackIntegration: (id: string) => request(`/api/orgs/${id}/integrations/slack/start`, { method: "POST" }),
  startNotionIntegration: (id: string) => request(`/api/orgs/${id}/integrations/notion/start`, { method: "POST" }),
  usage: (id: string) => request<Usage>(`/api/orgs/${id}/usage`),
  capturePolicy: (id: string) => request<CapturePolicy>(`/api/orgs/${id}/capture-policy`),
  updateCapturePolicy: (id: string, payload: Partial<CapturePolicy>) => request<CapturePolicy>(`/api/orgs/${id}/capture-policy`, { method: "PATCH", body: JSON.stringify(payload) }),
  workspaces: () => request<{ items: Workspace[] }>("/api/admin/workspaces"),
  workspace: (id: string) => request<Workspace>(`/api/admin/workspaces/${id}`),
  entities: (workspaceId: string) => request<{ items: Entity[] }>(`/api/admin/workspaces/${workspaceId}/entities`),
  jobs: (workspaceId: string) => request<{ items: Job[] }>(`/api/admin/workspaces/${workspaceId}/jobs`),
  audit: (workspaceId: string) => request<{ items: AuditEvent[] }>(`/api/admin/workspaces/${workspaceId}/audit-log`),
  metrics: (workspaceId: string) => request<Record<string, number | string>>(`/api/admin/workspaces/${workspaceId}/metrics`),
  query: (payload: { workspace_id: string; user_id: string; text: string }) => request<QueryResponse>("/api/query", { method: "POST", body: JSON.stringify(payload) })
};
