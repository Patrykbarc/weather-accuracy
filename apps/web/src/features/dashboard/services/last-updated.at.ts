import { apiClient } from "@/lib/api-client";

import type { components } from "@/types/api";

type LastUpdatedAt = components["schemas"]["LastUpdatedAt"];

export async function fetchLastUpdatedAt(
  signal: AbortSignal,
): Promise<LastUpdatedAt> {
  const { data } = await apiClient.get<LastUpdatedAt>("/last-updated", {
    signal,
  });

  return data;
}
