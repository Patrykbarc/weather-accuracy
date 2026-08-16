import { keepPreviousData, useQuery } from "@tanstack/react-query";

import { fetchAccuracy } from "../services/analytics";
import type { LocationValue, Metric } from "../types";

export function useAccuracy(location: LocationValue, metric: Metric) {
  return useQuery({
    queryKey: ["accuracy", location, metric],
    queryFn: ({ signal }) => fetchAccuracy(location, metric, signal),
    placeholderData: keepPreviousData,
  });
}
