import { useState } from "react";

import { SegmentedControl } from "@/components/views/segmented-control";
import {
  DEFAULT_LOCATION,
  DEFAULT_METRIC,
  LOCATIONS,
  METRICS,
  type LocationValue,
  type Metric,
} from "./options";

export function Dashboard() {
  const [location, setLocation] = useState<LocationValue>(DEFAULT_LOCATION);
  const [metric, setMetric] = useState<Metric>(DEFAULT_METRIC);

  return (
    <section className="flex flex-col gap-4">
      <SegmentedControl
        label="Location"
        options={LOCATIONS}
        value={location}
        onValueChange={setLocation}
      />
      <SegmentedControl
        label="Metric"
        options={METRICS}
        value={metric}
        onValueChange={setMetric}
      />
    </section>
  );
}
