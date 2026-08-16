import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

import { STATUS_LABEL } from "../lib/accuracy";
import { buildTiles } from "../lib/tiles";
import type { AccuracyRow, Metric } from "../types";

type StatTilesProps = {
  rows: readonly AccuracyRow[];
  metric: Metric;
};

function StatTilesGrid({ children }: { children: React.ReactNode }) {
  return <div className="grid gap-4 sm:grid-cols-3">{children}</div>;
}

export function StatTilesSkeleton() {
  return (
    <StatTilesGrid>
      <Skeleton className="h-32" />
      <Skeleton className="h-32" />
      <Skeleton className="h-32" />
    </StatTilesGrid>
  );
}

export function StatTiles({ rows, metric }: StatTilesProps) {
  return (
    <StatTilesGrid>
      {buildTiles(rows, metric).map((tile) => (
        <Card key={tile.key} size="sm">
          <CardContent>
            <p className="flex items-baseline gap-1.5 font-mono">
              <span className="text-3xl tabular-nums">{tile.value}</span>
              <span className="text-muted-foreground text-sm">{tile.unit}</span>
            </p>
          </CardContent>
          <CardHeader>
            <CardDescription>{tile.caption}</CardDescription>
          </CardHeader>
          {STATUS_LABEL[tile.status] && (
            <CardFooter>
              <Badge variant="secondary">{STATUS_LABEL[tile.status]}</Badge>
            </CardFooter>
          )}
        </Card>
      ))}
    </StatTilesGrid>
  );
}
