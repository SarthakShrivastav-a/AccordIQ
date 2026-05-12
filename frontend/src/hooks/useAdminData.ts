"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/apiClient";

export const useHealth = () => useQuery({ queryKey: ["health"], queryFn: apiClient.health, retry: false });
export const useVersion = () => useQuery({ queryKey: ["version"], queryFn: apiClient.version, retry: false });
export const useMe = () => useQuery({ queryKey: ["me"], queryFn: apiClient.me, retry: false });
export const useOrganizations = () => useQuery({ queryKey: ["organizations"], queryFn: apiClient.organizations, retry: false });
export const useOrganization = (id?: string) => useQuery({ queryKey: ["organization", id], queryFn: () => apiClient.organization(id!), enabled: Boolean(id), retry: false });
export const useOrganizationMembers = (id?: string) => useQuery({ queryKey: ["organizationMembers", id], queryFn: () => apiClient.organizationMembers(id!), enabled: Boolean(id), retry: false });
export const useIntegrations = (id?: string) => useQuery({ queryKey: ["integrations", id], queryFn: () => apiClient.integrations(id!), enabled: Boolean(id), retry: false });
export const useUsage = (id?: string) => useQuery({ queryKey: ["usage", id], queryFn: () => apiClient.usage(id!), enabled: Boolean(id), retry: false });
export const useCapturePolicy = (id?: string) => useQuery({ queryKey: ["capturePolicy", id], queryFn: () => apiClient.capturePolicy(id!), enabled: Boolean(id), retry: false });
export const useWorkspaces = () => useQuery({ queryKey: ["workspaces"], queryFn: apiClient.workspaces, retry: false });
export const useWorkspace = (id: string) => useQuery({ queryKey: ["workspace", id], queryFn: () => apiClient.workspace(id), enabled: Boolean(id), retry: false });
export const useEntities = (workspaceId?: string) => useQuery({ queryKey: ["entities", workspaceId], queryFn: () => apiClient.entities(workspaceId!), enabled: Boolean(workspaceId), retry: false });
export const useJobs = (workspaceId?: string) => useQuery({ queryKey: ["jobs", workspaceId], queryFn: () => apiClient.jobs(workspaceId!), enabled: Boolean(workspaceId), retry: false });
export const useAudit = (workspaceId?: string) => useQuery({ queryKey: ["audit", workspaceId], queryFn: () => apiClient.audit(workspaceId!), enabled: Boolean(workspaceId), retry: false });
export const useMetrics = (workspaceId?: string) => useQuery({ queryKey: ["metrics", workspaceId], queryFn: () => apiClient.metrics(workspaceId!), enabled: Boolean(workspaceId), retry: false });
export const useQueryMutation = () => useMutation({ mutationFn: apiClient.query });
export const useCreateOrganization = () => useMutation({ mutationFn: apiClient.createOrganization });
export const useInviteMember = (id: string) => useMutation({ mutationFn: (payload: { email: string; role: string }) => apiClient.inviteMember(id, payload) });
export const useStartSlackIntegration = (id: string) => useMutation({ mutationFn: () => apiClient.startSlackIntegration(id) });
export const useStartNotionIntegration = (id: string) => useMutation({ mutationFn: () => apiClient.startNotionIntegration(id) });
export const useUpdateCapturePolicy = (id: string) => useMutation({ mutationFn: (payload: { channel_mode?: string; retention_days?: number; ignored_channels?: string[]; allowed_channels?: string[] }) => apiClient.updateCapturePolicy(id, payload) });
