"use client";

import { useHealth, useVersion } from "@/hooks/useAdminData";
import { Badge } from "@/components/ui/Badge";

export function TopStatusBar() {
  const health = useHealth();
  const version = useVersion();
  return (
    <div className="flex flex-wrap items-center justify-between gap-3 border-b-2 border-ink bg-white px-4 py-3">
      <div className="font-mono text-xs font-bold uppercase">Operational memory console</div>
      <div className="flex flex-wrap gap-2">
        <Badge tone={health.data?.status === "ok" ? "good" : "warn"}>API {health.data?.status ?? "checking"}</Badge>
        <Badge tone="info">v{version.data?.version ?? "0.1.x"}</Badge>
      </div>
    </div>
  );
}
