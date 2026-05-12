"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { BarMetricChart } from "@/components/charts/BarMetricChart";
import { EmptyState } from "@/components/ui/EmptyState";
import { MetricCard } from "@/components/ui/MetricCard";
import { PageHeader } from "@/components/ui/PageHeader";
import { useEntities, useJobs, useMetrics, useOrganizations, useUsage, useWorkspaces } from "@/hooks/useAdminData";

export default function OverviewPage() {
  const router = useRouter();
  const organizations = useOrganizations();
  const workspaces = useWorkspaces();
  const activeOrgId = organizations.data?.[0]?.id;
  const activeWorkspaceId = workspaces.data?.items[0]?.workspace_id;
  const entities = useEntities(activeWorkspaceId);
  const jobs = useJobs(activeWorkspaceId);
  const metrics = useMetrics(activeWorkspaceId);
  const usage = useUsage(activeOrgId);
  const failedJobs = jobs.data?.items.filter((job) => job.status === "failed").length ?? 0;
  const metricData = [
    { name: "Capture", value: Number(metrics.data?.captured_messages ?? 0) },
    { name: "Entities", value: Number(metrics.data?.entities ?? 0) },
    { name: "Queries", value: Number(metrics.data?.queries ?? 0) }
  ];
  useEffect(() => {
    if (organizations.data && organizations.data.length === 0) router.replace("/onboarding");
  }, [organizations.data, router]);
  return (
    <AppShell>
      <PageHeader eyebrow="AccordIQ control plane" title="Team memory, under control." description="Monitor capture, review extracted agreements, and keep every answer grounded in cited Slack context." />
      {!activeWorkspaceId ? <EmptyState title="No workspaces available" detail="Your invited Google account is authenticated, but no workspace membership exists yet." /> : (
        <>
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <MetricCard label="Workspaces" value={`${workspaces.data?.items.length ?? 0}`} detail="Authorized admin surfaces" tone="info" />
            <MetricCard label="Entities" value={`${entities.data?.items.length ?? 0}`} detail="Tasks, decisions, questions" tone="good" />
            <MetricCard label="Failed jobs" value={`${failedJobs}`} detail="Needs operator attention" tone={failedJobs ? "danger" : "good"} />
            <MetricCard label="Usage events" value={`${usage.data?.grounded_queries ?? metrics.data?.queries ?? 0}`} detail="Grounded recall checks" tone="warn" />
          </div>
          <div className="mt-6">
            <BarMetricChart data={metricData} />
          </div>
        </>
      )}
    </AppShell>
  );
}
