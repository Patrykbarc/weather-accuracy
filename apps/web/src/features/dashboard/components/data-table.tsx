import { ChevronDownIcon } from "lucide-react";
import { useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import { cn } from "@/lib/utils";

import { METRIC_META } from "../constants";
import { isLowConfidence } from "../lib/accuracy";
import { formatLeadTime, formatNumber, formatSigned } from "../lib/format";
import type { AccuracyRow, Metric } from "../types";

const NUMERIC = "text-right tabular-nums";
const NUMERIC_CELL = `${NUMERIC} font-mono`;
const CONFIDENCE = "pl-6 text-muted-foreground";

type DataTableProps = {
  rows: readonly AccuracyRow[];
  metric: Metric;
};

export function DataTable({ rows, metric }: DataTableProps) {
  const [open, setOpen] = useState(true);
  const { unit } = METRIC_META[metric];

  return (
    <Card size="sm">
      <Collapsible open={open} onOpenChange={setOpen}>
        <CardHeader>
          <CollapsibleTrigger
            render={
              <Button variant="ghost" className="flex w-full justify-between">
                {open ? "Hide data" : "Show data"}
                <ChevronDownIcon
                  className={cn(
                    "transition-transform duration-300",
                    open ? "-rotate-180" : "rotate-0",
                  )}
                  data-icon="inline-end"
                />
              </Button>
            }
          />
        </CardHeader>
        <CollapsibleContent>
          <CardContent>
            <Table>
              <TableHeader className="text-xs tracking-wide uppercase">
                <TableRow>
                  <TableHead>Lead time</TableHead>
                  <TableHead className={NUMERIC}>Samples</TableHead>
                  <TableHead className={NUMERIC}>Bias ({unit})</TableHead>
                  <TableHead className={NUMERIC}>MAE ({unit})</TableHead>
                  <TableHead className={CONFIDENCE}>Confidence</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {rows.map((row) => (
                  <TableRow key={row.lead_time}>
                    <TableCell>{formatLeadTime(row.lead_time)}</TableCell>
                    <TableCell className={NUMERIC_CELL}>
                      {row.samples}
                    </TableCell>
                    <TableCell className={NUMERIC_CELL}>
                      {formatSigned(row.bias)}
                    </TableCell>
                    <TableCell className={NUMERIC_CELL}>
                      {formatNumber(row.mae)}
                    </TableCell>
                    <TableCell className={CONFIDENCE}>
                      {isLowConfidence(row) ? (
                        <Badge variant="secondary">Low</Badge>
                      ) : (
                        <Badge variant="ghost">OK</Badge>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </CollapsibleContent>
      </Collapsible>
    </Card>
  );
}
