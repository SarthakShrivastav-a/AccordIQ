import { clsx } from "clsx";

const toneClass = {
  neutral: "bg-paper",
  good: "bg-signal text-white",
  warn: "bg-amber",
  danger: "bg-danger text-white",
  info: "bg-electric text-white"
};

export function Badge({ children, tone = "neutral" }: { children: React.ReactNode; tone?: keyof typeof toneClass }) {
  return <span className={clsx("inline-flex border-2 border-ink px-2 py-1 font-mono text-xs font-bold uppercase", toneClass[tone])}>{children}</span>;
}
