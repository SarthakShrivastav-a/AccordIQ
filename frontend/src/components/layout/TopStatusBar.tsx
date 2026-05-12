"use client";

import { useRouter } from "next/navigation";
import { clearAccessToken } from "@/lib/apiClient";
import { useHealth, useMe, useVersion } from "@/hooks/useAdminData";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

export function TopStatusBar() {
  const router = useRouter();
  const health = useHealth();
  const version = useVersion();
  const me = useMe();
  return (
    <div className="flex flex-wrap items-center justify-between gap-3 border-b-2 border-ink bg-white px-4 py-3">
      <div className="font-mono text-xs font-bold uppercase">Operational memory console</div>
      <div className="flex flex-wrap gap-2">
        {me.data ? <Badge tone="info">{me.data.email}</Badge> : null}
        <Badge tone={health.data?.status === "ok" ? "good" : "warn"}>API {health.data?.status ?? "checking"}</Badge>
        <Badge tone="info">v{version.data?.version ?? "0.1.x"}</Badge>
        <Button onClick={() => { clearAccessToken(); router.replace("/login"); }}>Logout</Button>
      </div>
    </div>
  );
}
