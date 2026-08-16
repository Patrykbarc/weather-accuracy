import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { fetchLastUpdatedAt } from "../services/last-updated.at";

export function useLastUpdatedAt() {
  return useQuery({
    queryKey: ["last_updated_at"],
    queryFn: ({ signal }) => fetchLastUpdatedAt(signal),
    placeholderData: keepPreviousData,
  });
}
