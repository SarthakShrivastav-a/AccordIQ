export function PageHeader({ eyebrow, title, description, actions }: { eyebrow: string; title: string; description: string; actions?: React.ReactNode }) {
  return (
    <header className="mb-6 flex flex-col gap-4 border-b-2 border-ink pb-6 lg:flex-row lg:items-end lg:justify-between">
      <div>
        <p className="font-mono text-xs font-bold uppercase">{eyebrow}</p>
        <h1 className="mt-2 font-display text-4xl font-black leading-none lg:text-6xl">{title}</h1>
        <p className="mt-3 max-w-3xl text-base font-semibold">{description}</p>
      </div>
      {actions ? <div className="flex flex-wrap gap-3">{actions}</div> : null}
    </header>
  );
}
