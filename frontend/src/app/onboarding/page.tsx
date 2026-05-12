"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { BrutalCard } from "@/components/ui/BrutalCard";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { PageHeader } from "@/components/ui/PageHeader";
import { useCreateOrganization, useOrganizations } from "@/hooks/useAdminData";

export default function OnboardingPage() {
  const router = useRouter();
  const orgs = useOrganizations();
  const createOrg = useCreateOrganization();
  const [name, setName] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    const organization = await createOrg.mutateAsync({ name });
    router.push(`/organization?org=${organization.id}`);
  }

  return (
    <AppShell>
      <PageHeader eyebrow="SaaS setup" title="Create your team memory workspace." description="Start with an organization, then connect Slack, connect Notion, and tune capture policy." />
      {(orgs.data?.length ?? 0) > 0 ? <EmptyState title="Organization already exists" detail="Use the organization console to manage members, integrations, and usage." action="Open organization" /> : (
        <BrutalCard>
          <form className="grid gap-4" onSubmit={submit}>
            <label className="grid gap-2 font-display text-lg font-black">
              Organization name
              <input className="border-2 border-ink bg-paper p-3 font-sans text-base font-semibold outline-none" value={name} onChange={(event) => setName(event.target.value)} placeholder="Acme Product Team" required minLength={2} />
            </label>
            <Button className="w-fit bg-amber" disabled={createOrg.isPending}>Create organization</Button>
          </form>
        </BrutalCard>
      )}
    </AppShell>
  );
}
