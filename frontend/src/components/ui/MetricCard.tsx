import { Badge } from "./Badge";
import { BrutalCard } from "./BrutalCard";

export function MetricCard({ label, value, detail, tone = "neutral" }: { label: string; value: string; detail: string; tone?: "neutral" | "good" | "warn" | "danger" | "info" }) {
  return (
    <BrutalCard>
      <div className="flex items-start justify-between gap-3">
        <p className="font-mono text-xs font-bold uppercase">{label}</p>
        <Badge tone={tone}>{tone}</Badge>
      </div>
      <p className="mt-4 font-display text-4xl font-black leading-none">{value}</p>
      <p className="mt-2 text-sm font-semibold">{detail}</p>
    </BrutalCard>
  );
}
