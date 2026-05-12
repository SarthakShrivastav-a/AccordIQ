"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/apiClient";

export const useHealth = () => useQuery({ queryKey: ["health"], queryFn: apiClient.health });
export const useVersion = () => useQuery({ queryKey: ["version"], queryFn: apiClient.version });
export const useWorkspaces = () => useQuery({ queryKey: ["workspaces"], queryFn: apiClient.workspaces });
export const useWorkspace = (id: string) => useQuery({ queryKey: ["workspace", id], queryFn: () => apiClient.workspace(id) });
export const useEntities = (workspaceId?: string) => useQuery({ queryKey: ["entities", workspaceId], queryFn: () => apiClient.entities(workspaceId) });
export const useJobs = (workspaceId?: string) => useQuery({ queryKey: ["jobs", workspaceId], queryFn: () => apiClient.jobs(workspaceId) });
export const useMetrics = (workspaceId?: string) => useQuery({ queryKey: ["metrics", workspaceId], queryFn: () => apiClient.metrics(workspaceId) });
export const useQueryMutation = () => useMutation({ mutationFn: apiClient.query });
