"use client";

import { useParams } from "next/navigation";
import { AppShell } from "@/components/layout/AppShell";
import { Badge } from "@/components/ui/Badge";
import { BrutalCard } from "@/components/ui/BrutalCard";
import { PageHeader } from "@/components/ui/PageHeader";
import { useEntities, useJobs, useWorkspace } from "@/hooks/useAdminData";

export default function WorkspaceDetailPage() {
  const params = useParams<{ workspaceId: string }>();
  const workspace = useWorkspace(params.workspaceId);
  const entities = useEntities(params.workspaceId);
  const jobs = useJobs(params.workspaceId);
  return (
    <AppShell>
      <PageHeader eyebrow="Workspace detail" title={workspace.data?.name ?? params.workspaceId} description="Review extraction quality, job health, and capture settings for this workspace." />
      <div className="grid gap-4 lg:grid-cols-3">
        <BrutalCard><p className="font-mono text-xs font-bold uppercase">Capture</p><Badge tone={workspace.data?.capture_enabled ? "good" : "warn"}>{workspace.data?.capture_enabled ? "enabled" : "paused"}</Badge></BrutalCard>
        <BrutalCard><p className="font-mono text-xs font-bold uppercase">Entities</p><p className="font-display text-4xl font-black">{entities.data?.items.length ?? 0}</p></BrutalCard>
        <BrutalCard><p className="font-mono text-xs font-bold uppercase">Jobs</p><p className="font-display text-4xl font-black">{jobs.data?.items.length ?? 0}</p></BrutalCard>
      </div>
    </AppShell>
  );
}
