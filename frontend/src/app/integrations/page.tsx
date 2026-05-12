"use client";

import { AppShell } from "@/components/layout/AppShell";
import { Badge } from "@/components/ui/Badge";
import { BrutalCard } from "@/components/ui/BrutalCard";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { PageHeader } from "@/components/ui/PageHeader";
import { useIntegrations, useOrganizations, useStartNotionIntegration, useStartSlackIntegration } from "@/hooks/useAdminData";

export default function IntegrationsPage() {
  const orgs = useOrganizations();
  const organization = orgs.data?.[0];
  const integrations = useIntegrations(organization?.id);
  const slack = useStartSlackIntegration(organization?.id ?? "");
  const notion = useStartNotionIntegration(organization?.id ?? "");
  return (
    <AppShell>
      <PageHeader eyebrow="Connectors" title="Wire the operating system." description="Slack is the capture source. Notion is the durable system of record." />
      {!organization ? <EmptyState title="No organization" detail="Create an organization before connecting integrations." /> : (
        <div className="grid gap-4 lg:grid-cols-2">
          {(integrations.data ?? []).map((integration) => (
            <BrutalCard key={integration.provider}>
              <p className="font-display text-3xl font-black capitalize">{integration.provider}</p>
              <Badge tone={integration.status === "connected" ? "good" : integration.status === "error" ? "danger" : "warn"}>{integration.status}</Badge>
              <Button className="mt-5 bg-amber" onClick={() => integration.provider === "slack" ? slack.mutate() : notion.mutate()} disabled={slack.isPending || notion.isPending}>{integration.status === "connected" ? "Reconnect" : "Start setup"}</Button>
            </BrutalCard>
          ))}
        </div>
      )}
    </AppShell>
  );
}
