"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Activity, Briefcase, ClipboardCheck, Gauge, Home, MessageSquare, Plug, Settings, ShieldCheck, SlidersHorizontal, Users } from "lucide-react";
import { clsx } from "clsx";

const nav = [
  { href: "/", label: "Overview", icon: Home },
  { href: "/organization", label: "Organization", icon: Users },
  { href: "/workspaces", label: "Workspaces", icon: Briefcase },
  { href: "/integrations", label: "Integrations", icon: Plug },
  { href: "/usage", label: "Usage", icon: Gauge },
  { href: "/capture-policy", label: "Capture Policy", icon: SlidersHorizontal },
  { href: "/entities", label: "Review", icon: ClipboardCheck },
  { href: "/jobs", label: "Jobs", icon: Activity },
  { href: "/audit", label: "Audit", icon: Activity },
  { href: "/settings", label: "Settings", icon: Settings },
  { href: "/query", label: "Query", icon: MessageSquare }
];

export function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="border-b-2 border-ink bg-cream p-4 lg:min-h-screen lg:w-72 lg:border-b-0 lg:border-r-2">
      <div className="flex items-center gap-3">
        <div className="grid size-12 place-items-center border-2 border-ink bg-amber font-display text-xl font-black shadow-brutalSm">AIQ</div>
        <div>
          <p className="font-display text-2xl font-black">AccordIQ</p>
          <p className="font-mono text-xs font-bold uppercase">Admin console</p>
        </div>
      </div>
      <nav className="mt-6 grid gap-2">
        {nav.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;
          return (
            <Link className={clsx("flex items-center gap-3 border-2 border-ink px-3 py-2 font-display font-bold shadow-brutalSm", active ? "bg-ink text-paper" : "bg-white hover:bg-amber")} href={item.href} key={item.href}>
              <Icon size={18} />
              {item.label}
            </Link>
          );
        })}
      </nav>
      <div className="mt-6 border-2 border-ink bg-white p-3 text-sm font-bold">
        <ShieldCheck className="mb-2" />
        Redacted by default. Every answer needs citations.
      </div>
    </aside>
  );
}
