import { AppShell } from "@/components/layout/AppShell";
import { QueryBox } from "@/components/QueryBox";
import { PageHeader } from "@/components/ui/PageHeader";

export default function QueryPage() {
  return (
    <AppShell>
      <PageHeader eyebrow="Grounded recall" title="Ask the memory." description="Test query behavior and inspect whether answers include citations." />
      <QueryBox />
    </AppShell>
  );
}
