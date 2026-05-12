"use client";

import { AppShell } from "@/components/layout/AppShell";
import { BrutalCard } from "@/components/ui/BrutalCard";
import { EmptyState } from "@/components/ui/EmptyState";
import { PageHeader } from "@/components/ui/PageHeader";
import { useAudit, useWorkspaces } from "@/hooks/useAdminData";

export default function AuditPage() {
  const workspaces = useWorkspaces();
  const workspaceId = workspaces.data?.items[0]?.workspace_id;
  const audit = useAudit(workspaceId);
  const rows = audit.data?.items ?? [];
  return (
    <AppShell>
      <PageHeader eyebrow="Audit trail" title="Every decision leaves a mark." description="A timeline-ready view for admin changes, retries, reviews, exports, and wipe requests." />
      <div className="grid gap-4">
        {!workspaceId ? <EmptyState title="No workspace selected" detail="Workspace access is required before audit events can be inspected." /> : rows.length === 0 ? <EmptyState title="No audit events" detail="Admin actions will appear here after real changes occur." /> : rows.map((item) => <BrutalCard key={item.id}><p className="font-display text-xl font-black">{item.action}</p><p className="font-mono text-xs font-bold uppercase">{item.target_type} - {item.created_at ?? "unknown time"}</p></BrutalCard>)}
      </div>
    </AppShell>
  );
}
