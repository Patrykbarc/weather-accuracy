import { METRIC_META, TILE_LEAD_TIMES } from "../constants";
import type { AccuracyRow, Metric } from "../types";
import {
  describeLean,
  overallBias,
  rowStatus,
  type RowStatus,
} from "./accuracy";
import { formatLeadTime, formatNumber, formatSigned } from "./format";

export type Tile = {
  key: string;
  value: string;
  unit: string;
  caption: string;
  status: RowStatus;
};

const HORIZONS = [
  { key: "tomorrow", when: "tomorrow", leadTime: TILE_LEAD_TIMES.tomorrow },
  { key: "week", when: "in a week", leadTime: TILE_LEAD_TIMES.week },
] as const;

export function buildTiles(
  rows: readonly AccuracyRow[],
  metric: Metric,
): Tile[] {
  const bias = overallBias(rows);
  const unit = METRIC_META[metric].unit;

  const horizons = HORIZONS.map(({ key, when, leadTime }) => {
    const row = rows.find((candidate) => candidate.lead_time === leadTime);
    return {
      key,
      value: formatNumber(row?.mae ?? null),
      unit,
      caption: `Typical error ${when} (${formatLeadTime(leadTime)} ahead)`,
      status: rowStatus(row),
    };
  });

  return [
    ...horizons,
    {
      key: "bias",
      value: formatSigned(bias),
      unit,
      caption: `Overall bias, the forecast ${describeLean(bias, metric)}`,
      status: bias === null ? "missing" : "ok",
    },
  ];
}
