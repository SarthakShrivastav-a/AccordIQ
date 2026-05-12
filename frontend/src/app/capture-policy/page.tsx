"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { BrutalCard } from "@/components/ui/BrutalCard";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { PageHeader } from "@/components/ui/PageHeader";
import { useCapturePolicy, useOrganizations, useUpdateCapturePolicy } from "@/hooks/useAdminData";

export default function CapturePolicyPage() {
  const orgs = useOrganizations();
  const organization = orgs.data?.[0];
  const policy = useCapturePolicy(organization?.id);
  const update = useUpdateCapturePolicy(organization?.id ?? "");
  const [channelMode, setChannelMode] = useState("invited_channels");
  const [retentionDays, setRetentionDays] = useState(365);

  useEffect(() => {
    if (policy.data) {
      setChannelMode(policy.data.channel_mode);
      setRetentionDays(policy.data.retention_days);
    }
  }, [policy.data]);

  async function submit(event: FormEvent) {
    event.preventDefault();
    await update.mutateAsync({ channel_mode: channelMode, retention_days: retentionDays });
  }

  return (
    <AppShell>
      <PageHeader eyebrow="Governance" title="Capture policy." description="Control what AccordIQ listens to and how long team memory is retained." />
      {!organization ? <EmptyState title="No organization" detail="Create an organization before editing capture policy." /> : (
        <BrutalCard>
          <form className="grid gap-4" onSubmit={submit}>
            <label className="grid gap-2 font-display text-lg font-black">
              Channel mode
              <select className="border-2 border-ink bg-paper p-3 font-sans text-base font-bold" value={channelMode} onChange={(event) => setChannelMode(event.target.value)}>
                <option value="invited_channels">invited_channels</option>
                <option value="allowlist">allowlist</option>
              </select>
            </label>
            <label className="grid gap-2 font-display text-lg font-black">
              Retention days
              <input className="border-2 border-ink bg-paper p-3 font-sans text-base font-semibold outline-none" type="number" min={30} value={retentionDays} onChange={(event) => setRetentionDays(Number(event.target.value))} />
            </label>
            <Button className="w-fit bg-amber" disabled={update.isPending}>Save policy</Button>
          </form>
        </BrutalCard>
      )}
    </AppShell>
  );
}
