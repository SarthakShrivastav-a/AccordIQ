"use client";

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from "recharts";

export function BarMetricChart({ data }: { data: { name: string; value: number }[] }) {
  return (
    <div className="h-52 border-2 border-ink bg-paper p-3">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <XAxis dataKey="name" tickLine={false} axisLine={false} />
          <YAxis tickLine={false} axisLine={false} />
          <Bar dataKey="value" fill="#2f6df6" stroke="#111111" strokeWidth={2} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
