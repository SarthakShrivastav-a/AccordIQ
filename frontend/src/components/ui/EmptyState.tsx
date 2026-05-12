import { Button } from "./Button";

export function EmptyState({ title, detail, action }: { title: string; detail: string; action?: string }) {
  return (
    <div className="border-2 border-dashed border-ink bg-cream p-6 text-center">
      <h3 className="font-display text-xl font-black">{title}</h3>
      <p className="mx-auto mt-2 max-w-xl text-sm font-semibold">{detail}</p>
      {action ? <Button className="mt-4">{action}</Button> : null}
    </div>
  );
}
