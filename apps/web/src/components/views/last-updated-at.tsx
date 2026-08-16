import { QueryClientProvider } from "@tanstack/react-query";

import { Skeleton } from "@/components/ui/skeleton";
import { useLastUpdatedAt } from "@/features/dashboard/hooks/use-last-updated-at";
import { formatDate } from "@/features/dashboard/lib/format";
import { queryClient } from "@/lib/query-client";

export function LastUpdatedAt() {
  return (
    <QueryClientProvider client={queryClient}>
      <LastUpdatedAtView />
    </QueryClientProvider>
  );
}

function LastUpdatedAtView() {
  const { data, isPending, isError } = useLastUpdatedAt();

  if (isPending) return <Skeleton className="h-4 w-40" />;

  if (isError || !data?.last_updated) return null;

  return (
    <p className="text-muted-foreground text-xs">
      Last updated <span>{formatDate(data.last_updated)}</span>
    </p>
  );
}
