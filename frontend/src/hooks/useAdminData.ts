"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/apiClient";

export const useHealth = () => useQuery({ queryKey: ["health"], queryFn: apiClient.health, retry: false });
export const useVersion = () => useQuery({ queryKey: ["version"], queryFn: apiClient.version, retry: false });
export const useMe = () => useQuery({ queryKey: ["me"], queryFn: apiClient.me, retry: false });
export const useWorkspaces = () => useQuery({ queryKey: ["workspaces"], queryFn: apiClient.workspaces, retry: false });
export const useWorkspace = (id: string) => useQuery({ queryKey: ["workspace", id], queryFn: () => apiClient.workspace(id), enabled: Boolean(id), retry: false });
export const useEntities = (workspaceId?: string) => useQuery({ queryKey: ["entities", workspaceId], queryFn: () => apiClient.entities(workspaceId!), enabled: Boolean(workspaceId), retry: false });
export const useJobs = (workspaceId?: string) => useQuery({ queryKey: ["jobs", workspaceId], queryFn: () => apiClient.jobs(workspaceId!), enabled: Boolean(workspaceId), retry: false });
export const useAudit = (workspaceId?: string) => useQuery({ queryKey: ["audit", workspaceId], queryFn: () => apiClient.audit(workspaceId!), enabled: Boolean(workspaceId), retry: false });
export const useMetrics = (workspaceId?: string) => useQuery({ queryKey: ["metrics", workspaceId], queryFn: () => apiClient.metrics(workspaceId!), enabled: Boolean(workspaceId), retry: false });
export const useQueryMutation = () => useMutation({ mutationFn: apiClient.query });
