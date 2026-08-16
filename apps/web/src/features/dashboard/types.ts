import type { components, operations } from "@/types/api";

type AnalyticsQuery =
  operations["read_accuracy_api_analytics_get"]["parameters"]["query"];

export const ALL_LOCATIONS = "all";

export type Metric = AnalyticsQuery["metric"];
export type LocationSlug = NonNullable<AnalyticsQuery["slug"]>;
export type LocationValue = LocationSlug | typeof ALL_LOCATIONS;

export type AccuracyRow = components["schemas"]["AccuracyByLeadTime"];
