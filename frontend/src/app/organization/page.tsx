"use client";

import { FormEvent, useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { Badge } from "@/components/ui/Badge";
import { BrutalCard } from "@/components/ui/BrutalCard";
import { Button } from "@/components/ui/Button";
import { DataTable } from "@/components/ui/DataTable";
import { EmptyState } from "@/components/ui/EmptyState";
import { PageHeader } from "@/components/ui/PageHeader";
import { useInviteMember, useOrganizationMembers, useOrganizations } from "@/hooks/useAdminData";
import { OrganizationMember } from "@/lib/types";

export default function OrganizationPage() {
  const orgs = useOrganizations();
  const organization = orgs.data?.[0];
  const members = useOrganizationMembers(organization?.id);
  const invite = useInviteMember(organization?.id ?? "");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("viewer");

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!organization) return;
    await invite.mutateAsync({ email, role });
    setEmail("");
  }

  return (
    <AppShell>
      <PageHeader eyebrow="SaaS control plane" title="Organization." description="Manage the customer account, teammates, and access roles." />
      {!organization ? <EmptyState title="No organization" detail="Create an organization before inviting teammates." /> : (
        <div className="grid gap-5">
          <BrutalCard>
            <p className="font-display text-3xl font-black">{organization.name}</p>
            <div className="mt-3 flex flex-wrap gap-2"><Badge tone="info">{organization.role}</Badge><Badge tone={organization.onboarding_complete ? "good" : "warn"}>{organization.onboarding_complete ? "onboarded" : "setup needed"}</Badge></div>
          </BrutalCard>
          <BrutalCard>
            <form className="flex flex-wrap gap-3" onSubmit={submit}>
              <input className="min-h-11 min-w-64 flex-1 border-2 border-ink bg-paper px-3 font-semibold outline-none" placeholder="teammate@company.com" value={email} onChange={(event) => setEmail(event.target.value)} required />
              <select className="border-2 border-ink bg-paper px-3 font-bold" value={role} onChange={(event) => setRole(event.target.value)}>
                <option value="viewer">viewer</option>
                <option value="admin">admin</option>
                <option value="owner">owner</option>
              </select>
              <Button className="bg-amber" disabled={invite.isPending}>Invite</Button>
            </form>
          </BrutalCard>
          <DataTable<OrganizationMember> rows={members.data ?? []} columns={[
            { key: "email", label: "Email", render: (row) => <span className="font-bold">{row.email}</span> },
            { key: "name", label: "Name", render: (row) => <span>{row.name ?? "Unknown"}</span> },
            { key: "role", label: "Role", render: (row) => <Badge tone={row.role === "owner" ? "good" : "info"}>{row.role}</Badge> }
          ]} />
        </div>
      )}
    </AppShell>
  );
}
