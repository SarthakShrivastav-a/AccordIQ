"use client";

import { AppShell } from "@/components/layout/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { DataTable } from "@/components/ui/DataTable";
import { EmptyState } from "@/components/ui/EmptyState";
import { PageHeader } from "@/components/ui/PageHeader";
import { useJobs, useWorkspaces } from "@/hooks/useAdminData";
import { Job } from "@/lib/types";

export default function JobsPage() {
  const workspaces = useWorkspaces();
  const workspaceId = workspaces.data?.items[0]?.workspace_id;
  const jobs = useJobs(workspaceId);
  const rows = jobs.data?.items ?? [];
  return (
    <AppShell>
      <PageHeader eyebrow="Worker operations" title="Queues without mystery." description="Inspect capture, extraction, query, Notion sync, and dead-letter jobs." />
      {!workspaceId ? <EmptyState title="No workspace selected" detail="Workspace access is required before jobs can be inspected." /> : rows.length === 0 ? <EmptyState title="No jobs found" detail="No worker jobs exist for this workspace yet." /> : <DataTable<Job> rows={rows} columns={[
        { key: "id", label: "Job", render: (row) => <span className="font-mono font-bold">{row.id}</span> },
        { key: "type", label: "Type", render: (row) => <span className="font-bold">{row.job_type}</span> },
        { key: "status", label: "Status", render: (row) => <Badge tone={row.status === "failed" ? "danger" : row.status === "done" ? "good" : "warn"}>{row.status}</Badge> },
        { key: "action", label: "Action", render: () => <Button>Retry</Button> }
      ]} />}
    </AppShell>
  );
}
