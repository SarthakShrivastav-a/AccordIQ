"use client";

import { AppShell } from "@/components/layout/AppShell";
import { Badge } from "@/components/ui/Badge";
import { BrutalCard } from "@/components/ui/BrutalCard";
import { EmptyState } from "@/components/ui/EmptyState";
import { PageHeader } from "@/components/ui/PageHeader";
import { useMe, useWorkspaces } from "@/hooks/useAdminData";

export default function SettingsPage() {
  const me = useMe();
  const workspaces = useWorkspaces();
  return (
    <AppShell>
      <PageHeader eyebrow="Trust controls" title="Capture only what teams expect." description="Configure retention, redaction, channel policy, and integration readiness." />
      <div className="grid gap-4 lg:grid-cols-2">
        {me.data ? <BrutalCard><p className="font-display text-2xl font-black">Signed in</p><p className="font-bold">{me.data.email}</p></BrutalCard> : null}
        <BrutalCard><p className="font-display text-2xl font-black">Workspace access</p><Badge tone={(workspaces.data?.items.length ?? 0) > 0 ? "good" : "warn"}>{workspaces.data?.items.length ?? 0} workspaces</Badge></BrutalCard>
        {(workspaces.data?.items.length ?? 0) === 0 ? <EmptyState title="No workspace settings" detail="No authorized workspace is available for this account." /> : workspaces.data?.items.map((workspace) => <BrutalCard key={workspace.workspace_id}><p className="font-display text-2xl font-black">{workspace.name}</p><p className="font-semibold">{workspace.channel_mode} - {workspace.retention_days} day retention</p></BrutalCard>)}
      </div>
    </AppShell>
  );
}
