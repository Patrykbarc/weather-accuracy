import type { SegmentedOption } from "@/components/views/segmented-control";

import {
  ALL_LOCATIONS,
  type LocationSlug,
  type LocationValue,
  type Metric,
} from "./types";

type MetricMeta = {
  label: string;
  unit: string;
  leansHigh: string;
  leansLow: string;
};

export const METRIC_META: Record<Metric, MetricMeta> = {
  temp_max: {
    label: "Max temperature",
    unit: "°C",
    leansHigh: "runs warm",
    leansLow: "runs cold",
  },
  temp_min: {
    label: "Min temperature",
    unit: "°C",
    leansHigh: "runs warm",
    leansLow: "runs cold",
  },
  precipitation: {
    label: "Precipitation",
    unit: "mm",
    leansHigh: "runs wet",
    leansLow: "runs dry",
  },
  wind_gusts: {
    label: "Wind gusts",
    unit: "km/h",
    leansHigh: "runs high",
    leansLow: "runs low",
  },
};

const LOCATION_LABELS: Record<LocationSlug, string> = {
  rzeszow: "Rzeszów",
  zakopane: "Zakopane",
  sopot: "Sopot",
  suwalki: "Suwałki",
};

export const LOCATIONS: readonly SegmentedOption<LocationValue>[] = [
  { value: ALL_LOCATIONS, label: "All locations" },
  ...(Object.entries(LOCATION_LABELS) as [LocationSlug, string][]).map(
    ([value, label]) => ({ value, label }),
  ),
];

export const METRICS: readonly SegmentedOption<Metric>[] = (
  Object.entries(METRIC_META) as [Metric, MetricMeta][]
).map(([value, meta]) => ({ value, label: meta.label }));

export const DEFAULT_LOCATION: LocationValue = ALL_LOCATIONS;
export const DEFAULT_METRIC: Metric = "temp_max";

export const TILE_LEAD_TIMES = { tomorrow: 1, week: 7 } as const;
