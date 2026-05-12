"use client";

import { AppShell } from "@/components/layout/AppShell";
import { MetricCard } from "@/components/ui/MetricCard";
import { EmptyState } from "@/components/ui/EmptyState";
import { PageHeader } from "@/components/ui/PageHeader";
import { useOrganizations, useUsage } from "@/hooks/useAdminData";

export default function UsagePage() {
  const orgs = useOrganizations();
  const organization = orgs.data?.[0];
  const usage = useUsage(organization?.id);
  return (
    <AppShell>
      <PageHeader eyebrow="Metering" title="Usage without billing lock-in." description="Track product activity and AI workload before adding a billing provider." />
      {!organization ? <EmptyState title="No organization" detail="Create an organization before usage is available." /> : (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <MetricCard label="Captured messages" value={`${usage.data?.captured_messages ?? 0}`} detail="Slack messages persisted" tone="info" />
          <MetricCard label="Extracted entities" value={`${usage.data?.extracted_entities ?? 0}`} detail="Tasks, decisions, questions" tone="good" />
          <MetricCard label="Grounded queries" value={`${usage.data?.grounded_queries ?? 0}`} detail="Answers with citations" tone="warn" />
          <MetricCard label="Notion syncs" value={`${usage.data?.notion_syncs ?? 0}`} detail="Records pushed downstream" tone="info" />
        </div>
      )}
    </AppShell>
  );
}
