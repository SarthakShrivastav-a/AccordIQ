import { AppShell } from "@/components/layout/AppShell";
import { Badge } from "@/components/ui/Badge";
import { BrutalCard } from "@/components/ui/BrutalCard";
import { Button } from "@/components/ui/Button";
import { PageHeader } from "@/components/ui/PageHeader";

export default function SettingsPage() {
  return (
    <AppShell>
      <PageHeader eyebrow="Trust controls" title="Capture only what teams expect." description="Configure retention, redaction, channel policy, and integration readiness." />
      <div className="grid gap-4 lg:grid-cols-2">
        <BrutalCard><p className="font-display text-2xl font-black">Slack install</p><Badge tone="good">connected</Badge></BrutalCard>
        <BrutalCard><p className="font-display text-2xl font-black">Notion data source</p><Badge tone="warn">needs review</Badge></BrutalCard>
        <BrutalCard className="lg:col-span-2"><p className="font-display text-2xl font-black">Danger zone</p><p className="my-3 font-semibold">Export or wipe workspace data with explicit confirmation.</p><Button className="bg-danger text-white">Queue wipe</Button></BrutalCard>
      </div>
    </AppShell>
  );
}
