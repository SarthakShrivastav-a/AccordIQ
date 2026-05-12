"use client";

import { AppShell } from "@/components/layout/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { DataTable } from "@/components/ui/DataTable";
import { EmptyState } from "@/components/ui/EmptyState";
import { PageHeader } from "@/components/ui/PageHeader";
import { useEntities, useWorkspaces } from "@/hooks/useAdminData";
import { Entity } from "@/lib/types";

export default function EntitiesPage() {
  const workspaces = useWorkspaces();
  const workspaceId = workspaces.data?.items[0]?.workspace_id;
  const entities = useEntities(workspaceId);
  const rows = entities.data?.items ?? [];
  return (
    <AppShell>
      <PageHeader eyebrow="Review queue" title="Keep memory clean." description="Approve strong extractions, ignore noise, and inspect source-linked AccordIQ entities." />
      {!workspaceId ? <EmptyState title="No workspace selected" detail="Workspace access is required before entities can be reviewed." /> : rows.length === 0 ? <EmptyState title="No entities found" detail="Captured Slack messages have not produced reviewable entities yet." /> : <DataTable<Entity> rows={rows} columns={[
        { key: "title", label: "Entity", render: (row) => <span className="font-display font-black">{row.title}</span> },
        { key: "type", label: "Type", render: (row) => <Badge tone="info">{row.entity_type}</Badge> },
        { key: "confidence", label: "Confidence", render: (row) => <span className="font-mono font-bold">{Math.round(row.confidence * 100)}%</span> },
        { key: "action", label: "Action", render: () => <Button className="bg-amber">Review</Button> }
      ]} />}
    </AppShell>
  );
}
