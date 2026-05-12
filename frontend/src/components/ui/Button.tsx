import { ButtonHTMLAttributes } from "react";
import { clsx } from "clsx";

export function Button({ className, ...props }: ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      className={clsx("inline-flex min-h-10 items-center justify-center gap-2 border-2 border-ink bg-paper px-4 py-2 font-display text-sm font-bold shadow-brutalSm transition hover:-translate-y-0.5 hover:shadow-brutal disabled:cursor-not-allowed disabled:opacity-50", className)}
      {...props}
    />
  );
}
