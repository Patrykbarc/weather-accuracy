import {
  Bar,
  BarChart,
  CartesianGrid,
  LabelList,
  Line,
  LineChart,
  ReferenceLine,
  XAxis,
  YAxis,
} from "recharts";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ChartContainer,
  ChartTooltip,
  type ChartConfig,
} from "@/components/ui/chart";

import { METRIC_META } from "../constants";
import {
  formatComparisons,
  formatLeadTime,
  formatNumber,
  formatWithUnit,
} from "../lib/format";
import type { AccuracyRow, Metric } from "../types";

const AXIS_WIDTH = 44;
const CHART_MARGIN = { top: 8, right: 16, bottom: 0, left: 0 };
const STRIP_MARGIN = { top: 4, right: 16, bottom: 20, left: AXIS_WIDTH };

const chartConfig = {
  mae: { label: "MAE", color: "var(--chart-3)" },
  bias: { label: "Bias", color: "var(--chart-6)" },
} satisfies ChartConfig;

const samplesConfig = {
  samples: { label: "Comparisons", color: "var(--muted-foreground)" },
} satisfies ChartConfig;

type Series = keyof typeof chartConfig;

type AccuracyChartProps = {
  rows: readonly AccuracyRow[];
  metric: Metric;
};

function LegendItem({ series, hint }: { series: Series; hint: string }) {
  return (
    <span className="flex items-center gap-2 text-sm">
      <span
        className="h-0.5 w-5 rounded-full"
        style={{ backgroundColor: chartConfig[series].color }}
      />
      <span className="font-medium">{chartConfig[series].label}</span>
      <span className="text-muted-foreground text-xs">{hint}</span>
    </span>
  );
}

function TooltipRow({
  series,
  value,
  unit,
}: {
  series: Series;
  value: number | null;
  unit: string;
}) {
  return (
    <div className="flex items-center justify-between gap-4">
      <span className="text-muted-foreground flex items-center gap-1.5">
        <span
          className="size-2 rounded-xs"
          style={{ backgroundColor: chartConfig[series].color }}
        />
        {chartConfig[series].label}
      </span>
      <span className="font-medium tabular-nums">
        {formatWithUnit(value, unit)}
      </span>
    </div>
  );
}

function AccuracyTooltip({
  active,
  payload,
  unit,
}: {
  active?: boolean;
  payload?: { payload?: AccuracyRow }[];
  unit: string;
}) {
  const point = payload?.[0]?.payload;
  if (!active || !point) return null;

  return (
    <div className="bg-popover text-popover-foreground ring-foreground/5 dark:ring-foreground/10 grid min-w-44 gap-1.5 rounded-xl px-2.5 py-1.5 text-xs shadow-lg ring-1">
      <div className="font-medium">
        {formatLeadTime(point.lead_time)} ahead ·{" "}
        {formatComparisons(point.samples)}
      </div>
      <TooltipRow series="mae" value={point.mae} unit={unit} />
      <TooltipRow series="bias" value={point.bias} unit={unit} />
    </div>
  );
}

export function AccuracyChart({ rows, metric }: AccuracyChartProps) {
  const meta = METRIC_META[metric];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Error by lead time</CardTitle>
        <CardDescription>
          MAE and bias in {meta.unit}, measured against what actually happened.
        </CardDescription>
      </CardHeader>

      <CardContent className="flex flex-col gap-4">
        <div className="flex flex-wrap items-center gap-x-6 gap-y-2">
          <LegendItem series="mae" hint="how far off, either way" />
          <LegendItem series="bias" hint="signed lean" />
        </div>

        <ChartContainer config={chartConfig} className="h-75 w-full">
          <LineChart data={rows} margin={CHART_MARGIN}>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="lead_time"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
            />
            <YAxis
              width={AXIS_WIDTH}
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              tickFormatter={(value: number) => formatNumber(value, 1)}
            />
            <ReferenceLine
              y={0}
              strokeDasharray="2 3"
              label={{
                value: "0 (perfect)",
                position: "insideTopRight",
                fontSize: 10,
                className: "fill-muted-foreground",
              }}
            />
            <ChartTooltip content={<AccuracyTooltip unit={meta.unit} />} />
            <Line
              dataKey="bias"
              stroke="var(--color-bias)"
              strokeWidth={2}
              dot={{ r: 2.5, fill: "var(--color-bias)", strokeWidth: 0 }}
              activeDot={{ r: 4 }}
            />
            <Line
              dataKey="mae"
              stroke="var(--color-mae)"
              strokeWidth={2}
              dot={{ r: 2.5, fill: "var(--color-mae)", strokeWidth: 0 }}
              activeDot={{ r: 4 }}
            />
          </LineChart>
        </ChartContainer>

        <p className="text-muted-foreground text-center text-xs">
          days ahead (lead time)
        </p>

        <div className="flex flex-col gap-1.5">
          <p className="text-muted-foreground text-xs font-medium tracking-wide uppercase">
            Comparisons per lead time
          </p>
          <ChartContainer config={samplesConfig} className="h-20 w-full">
            <BarChart data={rows} margin={STRIP_MARGIN}>
              <XAxis dataKey="lead_time" scale="point" hide />
              <YAxis hide />
              <Bar
                dataKey="samples"
                fill="var(--color-samples)"
                fillOpacity={0.45}
                radius={2}
                barSize={14}
              >
                <LabelList
                  dataKey="samples"
                  position="bottom"
                  offset={6}
                  fontSize={10}
                  className="fill-muted-foreground"
                />
              </Bar>
            </BarChart>
          </ChartContainer>
        </div>
      </CardContent>
    </Card>
  );
}
