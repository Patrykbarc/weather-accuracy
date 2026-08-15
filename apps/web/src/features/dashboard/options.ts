import type { operations } from "@/types/api";

type AnalyticsQuery =
  operations["read_accuracy_api_analytics_get"]["parameters"]["query"];

export type Metric = AnalyticsQuery["metric"];
export type LocationSlug = NonNullable<AnalyticsQuery["slug"]>;

export const ALL_LOCATIONS = "all";
export type LocationValue = typeof ALL_LOCATIONS | LocationSlug;

type Option<TValue extends string> = { value: TValue; label: string };

function toOptions<TValue extends string>(
  labels: Record<TValue, string>,
): Option<TValue>[] {
  return (Object.entries(labels) as [TValue, string][]).map(
    ([value, label]) => ({ value, label }),
  );
}

const LOCATION_LABELS: Record<LocationSlug, string> = {
  rzeszow: "Rzeszów",
  zakopane: "Zakopane",
  sopot: "Sopot",
  suwalki: "Suwałki",
};

const METRIC_LABELS: Record<Metric, string> = {
  temp_max: "Max temperature",
  temp_min: "Min temperature",
  precipitation: "Precipitation",
  wind_gusts: "Wind gusts",
};

export const LOCATIONS: readonly Option<LocationValue>[] = [
  { value: ALL_LOCATIONS, label: "All locations" },
  ...toOptions(LOCATION_LABELS),
];

export const METRICS: readonly Option<Metric>[] = toOptions(METRIC_LABELS);

export const DEFAULT_LOCATION: LocationValue = ALL_LOCATIONS;
export const DEFAULT_METRIC: Metric = "temp_max";
