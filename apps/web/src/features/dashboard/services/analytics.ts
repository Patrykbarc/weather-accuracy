import { apiClient } from "@/lib/api-client";

import {
  ALL_LOCATIONS,
  type AccuracyRow,
  type LocationValue,
  type Metric,
} from "../types";

export async function fetchAccuracy(
  location: LocationValue,
  metric: Metric,
  signal: AbortSignal,
): Promise<AccuracyRow[]> {
  const { data } = await apiClient.get<AccuracyRow[]>("/analytics", {
    params: {
      metric,
      slug: location === ALL_LOCATIONS ? undefined : location,
    },
    signal,
  });

  return data;
}
