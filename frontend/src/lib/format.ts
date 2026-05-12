export function percent(value: number) {
  return `${Math.round(value * 100)}%`;
}

export function compactNumber(value: number) {
  return new Intl.NumberFormat("en", { notation: "compact" }).format(value);
}
