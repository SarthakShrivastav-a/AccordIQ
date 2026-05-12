import { AppShell } from "@/components/layout/AppShell";
import { BrutalCard } from "@/components/ui/BrutalCard";
import { PageHeader } from "@/components/ui/PageHeader";

export default function AuditPage() {
  return (
    <AppShell>
      <PageHeader eyebrow="Audit trail" title="Every decision leaves a mark." description="A timeline-ready view for admin changes, retries, reviews, exports, and wipe requests." />
      <div className="grid gap-4">
        {["Workspace settings updated", "Entity approved", "Query refused without citations"].map((item) => <BrutalCard key={item}><p className="font-display text-xl font-black">{item}</p><p className="font-mono text-xs font-bold uppercase">demo-workspace - just now</p></BrutalCard>)}
      </div>
    </AppShell>
  );
}
