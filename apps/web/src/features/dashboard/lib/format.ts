const EMPTY = "-";

export function formatNumber(value: number | null, digits = 2): string {
  if (value === null || Number.isNaN(value)) return EMPTY;
  return value.toFixed(digits);
}

export function formatSigned(value: number | null, digits = 2): string {
  const text = formatNumber(value, digits);
  return value !== null && value > 0 ? `+${text}` : text;
}

export function formatWithUnit(value: number | null, unit: string): string {
  const text = formatNumber(value);
  return value === null ? text : `${text} ${unit}`;
}

export function formatLeadTime(leadTime: number): string {
  return `${leadTime} ${leadTime === 1 ? "day" : "days"}`;
}

export function formatComparisons(samples: number): string {
  return `${samples} ${samples === 1 ? "comparison" : "comparisons"}`;
}
