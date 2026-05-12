import { clsx } from "clsx";

export function BrutalCard({ children, className }: { children: React.ReactNode; className?: string }) {
  return <section className={clsx("brutal-border bg-white p-5", className)}>{children}</section>;
}
