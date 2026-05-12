"use client";

import { AppShell } from "@/components/layout/AppShell";
import { BarMetricChart } from "@/components/charts/BarMetricChart";
import { MetricCard } from "@/components/ui/MetricCard";
import { PageHeader } from "@/components/ui/PageHeader";
import { useEntities, useJobs, useMetrics, useWorkspaces } from "@/hooks/useAdminData";

export default function OverviewPage() {
  const workspaces = useWorkspaces();
  const entities = useEntities();
  const jobs = useJobs();
  const metrics = useMetrics();
  const failedJobs = jobs.data?.items.filter((job) => job.status === "failed").length ?? 0;
  return (
    <AppShell>
      <PageHeader eyebrow="AccordIQ control plane" title="Team memory, under control." description="Monitor capture, review extracted agreements, and keep every answer grounded in cited Slack context." />
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Workspaces" value={`${workspaces.data?.items.length ?? 0}`} detail="Connected admin surfaces" tone="info" />
        <MetricCard label="Entities" value={`${entities.data?.items.length ?? 0}`} detail="Tasks, decisions, questions" tone="good" />
        <MetricCard label="Failed jobs" value={`${failedJobs}`} detail="Needs operator attention" tone={failedJobs ? "danger" : "good"} />
        <MetricCard label="Queries" value={`${metrics.data?.queries ?? 0}`} detail="Grounded recall checks" tone="warn" />
      </div>
      <div className="mt-6">
        <BarMetricChart data={[{ name: "Capture", value: 128 }, { name: "Entities", value: 42 }, { name: "Queries", value: 19 }]} />
      </div>
    </AppShell>
  );
}
