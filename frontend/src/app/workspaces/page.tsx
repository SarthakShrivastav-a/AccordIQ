"use client";

import Link from "next/link";
import { AppShell } from "@/components/layout/AppShell";
import { Badge } from "@/components/ui/Badge";
import { DataTable } from "@/components/ui/DataTable";
import { EmptyState } from "@/components/ui/EmptyState";
import { PageHeader } from "@/components/ui/PageHeader";
import { useWorkspaces } from "@/hooks/useAdminData";
import { Workspace } from "@/lib/types";

export default function WorkspacesPage() {
  const workspaces = useWorkspaces();
  return (
    <AppShell>
      <PageHeader eyebrow="Workspace registry" title="Capture boundaries." description="Control which teams AccordIQ listens to, how long memory lasts, and where review work is happening." />
      {(workspaces.data?.items.length ?? 0) === 0 ? <EmptyState title="No workspaces" detail="You are signed in but do not have workspace access." /> : <DataTable<Workspace> rows={workspaces.data?.items ?? []} columns={[
        { key: "name", label: "Workspace", render: (row) => <Link className="font-display font-black underline" href={`/workspaces/${row.workspace_id}`}>{row.name}</Link> },
        { key: "capture", label: "Capture", render: (row) => <Badge tone={row.capture_enabled ? "good" : "warn"}>{row.capture_enabled ? "on" : "paused"}</Badge> },
        { key: "retention", label: "Retention", render: (row) => <span className="font-mono font-bold">{row.retention_days}d</span> },
        { key: "activity", label: "Last activity", render: (row) => <span className="font-bold">{row.last_activity ?? "none"}</span> }
      ]} />}
    </AppShell>
  );
}
