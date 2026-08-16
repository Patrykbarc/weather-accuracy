import { QueryClientProvider } from "@tanstack/react-query";
import { lazy, Suspense, useState } from "react";

import {
  Empty,
  EmptyDescription,
  EmptyHeader,
  EmptyTitle,
} from "@/components/ui/empty";
import { Skeleton } from "@/components/ui/skeleton";
import { queryClient } from "@/lib/query-client";

import { DEFAULT_LOCATION, DEFAULT_METRIC } from "../constants";
import { useAccuracy } from "../hooks/use-accuracy";
import type { AccuracyRow, LocationValue, Metric } from "../types";
import { DataTable } from "./data-table";
import { Filters } from "./filters";
import { StatTiles, StatTilesSkeleton } from "./stat-tiles";

const AccuracyChart = lazy(() =>
  import("./accuracy-chart").then((module) => ({
    default: module.AccuracyChart,
  })),
);

export function Dashboard() {
  return (
    <QueryClientProvider client={queryClient}>
      <DashboardView />
    </QueryClientProvider>
  );
}

function DashboardView() {
  const [location, setLocation] = useState<LocationValue>(DEFAULT_LOCATION);
  const [metric, setMetric] = useState<Metric>(DEFAULT_METRIC);
  const { data: rows = [], isPending, isError } = useAccuracy(location, metric);

  return (
    <section className="flex flex-col gap-8">
      <Filters
        location={location}
        metric={metric}
        onLocationChange={setLocation}
        onMetricChange={setMetric}
      />
      <Results
        rows={rows}
        metric={metric}
        isPending={isPending}
        isError={isError}
      />
    </section>
  );
}

type ResultsProps = {
  rows: readonly AccuracyRow[];
  metric: Metric;
  isPending: boolean;
  isError: boolean;
};

function Results({ rows, metric, isPending, isError }: ResultsProps) {
  if (isPending) {
    return (
      <>
        <StatTilesSkeleton />
        <Skeleton className="h-96" />
      </>
    );
  }

  if (rows.length > 0) {
    return (
      <>
        <StatTiles rows={rows} metric={metric} />
        <Suspense fallback={<Skeleton className="h-96" />}>
          <AccuracyChart rows={rows} metric={metric} />
        </Suspense>
        <DataTable rows={rows} metric={metric} />
      </>
    );
  }

  if (isError) {
    return (
      <Empty>
        <EmptyHeader>
          <EmptyTitle>Could not load the numbers</EmptyTitle>
          <EmptyDescription>
            The analytics request failed. Check that the API is running, then
            switch a filter to try again.
          </EmptyDescription>
        </EmptyHeader>
      </Empty>
    );
  }

  return (
    <Empty>
      <EmptyHeader>
        <EmptyTitle>Nothing to compare yet</EmptyTitle>
        <EmptyDescription>
          No forecast has met its measurement for this pick. Come back once the
          collector has a day or two behind it.
        </EmptyDescription>
      </EmptyHeader>
    </Empty>
  );
}
