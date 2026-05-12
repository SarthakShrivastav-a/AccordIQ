export type Column<T> = { key: string; label: string; render: (row: T) => React.ReactNode };

export function DataTable<T>({ columns, rows }: { columns: Column<T>[]; rows: T[] }) {
  return (
    <div className="overflow-hidden border-2 border-ink bg-white">
      <div className="hidden grid-cols-12 border-b-2 border-ink bg-ink text-paper md:grid">
        {columns.map((column) => (
          <div className="col-span-3 px-3 py-2 font-mono text-xs font-bold uppercase" key={column.key}>{column.label}</div>
        ))}
      </div>
      <div>
        {rows.map((row, index) => (
          <div className="grid gap-2 border-b-2 border-ink p-3 last:border-b-0 md:grid-cols-12 md:gap-0 md:p-0" key={index}>
            {columns.map((column) => (
              <div className="md:col-span-3 md:px-3 md:py-3" key={column.key}>
                <span className="mb-1 block font-mono text-[10px] font-bold uppercase md:hidden">{column.label}</span>
                {column.render(row)}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
