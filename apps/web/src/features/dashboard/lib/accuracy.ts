import { METRIC_META } from "../constants";
import type { AccuracyRow, Metric } from "../types";

const LOW_CONFIDENCE_THRESHOLD = 5;
const NEUTRAL_BIAS = 0.05;

export type RowStatus = "ok" | "low" | "missing";

export const STATUS_LABEL: Record<RowStatus, string | null> = {
  ok: null,
  low: "Few comparisons",
  missing: "Not enough history yet",
};

export function isLowConfidence(row: AccuracyRow): boolean {
  return row.samples < LOW_CONFIDENCE_THRESHOLD;
}

export function rowStatus(row: AccuracyRow | undefined): RowStatus {
  if (row === undefined) return "missing";
  return isLowConfidence(row) ? "low" : "ok";
}

export function overallBias(rows: readonly AccuracyRow[]): number | null {
  let weighted = 0;
  let weight = 0;

  for (const row of rows) {
    if (row.bias === null) continue;
    weighted += row.bias * row.samples;
    weight += row.samples;
  }

  return weight > 0 ? weighted / weight : null;
}

export function describeLean(bias: number | null, metric: Metric): string {
  if (bias === null) return "shows no clear lean";
  if (bias > NEUTRAL_BIAS) return METRIC_META[metric].leansHigh;
  if (bias < -NEUTRAL_BIAS) return METRIC_META[metric].leansLow;
  return "is well centered";
}
