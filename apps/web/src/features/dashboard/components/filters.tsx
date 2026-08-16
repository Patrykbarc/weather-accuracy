import { SegmentedControl } from "@/components/views/segmented-control";

import { LOCATIONS, METRICS } from "../constants";
import type { LocationValue, Metric } from "../types";

type FiltersProps = {
  location: LocationValue;
  metric: Metric;
  onLocationChange: (location: LocationValue) => void;
  onMetricChange: (metric: Metric) => void;
};

export function Filters({
  location,
  metric,
  onLocationChange,
  onMetricChange,
}: FiltersProps) {
  return (
    <div className="flex flex-wrap gap-x-8 gap-y-4">
      <SegmentedControl
        label="Location"
        options={LOCATIONS}
        value={location}
        onValueChange={onLocationChange}
      />
      <SegmentedControl
        label="Metric"
        options={METRICS}
        value={metric}
        onValueChange={onMetricChange}
      />
    </div>
  );
}
