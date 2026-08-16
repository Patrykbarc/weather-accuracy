import { useId, type ReactNode } from "react";

import { FieldLegend, FieldSet } from "@/components/ui/field";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";

export type SegmentedOption<TValue extends string> = {
  value: TValue;
  label: ReactNode;
};

type SegmentedControlProps<TValue extends string> = {
  label: ReactNode;
  options: readonly SegmentedOption<TValue>[];
  value: TValue;
  onValueChange: (value: TValue) => void;
  className?: string;
};

export function SegmentedControl<TValue extends string>({
  label,
  options,
  value,
  onValueChange,
  className,
}: SegmentedControlProps<TValue>) {
  const labelId = useId();

  function handleValueChange([next]: string[]) {
    const selected = options.find((option) => option.value === next);
    if (selected) onValueChange(selected.value);
  }

  return (
    <FieldSet className={className}>
      <FieldLegend id={labelId} variant="label">
        {label}
      </FieldLegend>
      <ToggleGroup
        aria-labelledby={labelId}
        variant="outline"
        spacing={1}
        className="flex-wrap"
        value={[value]}
        onValueChange={handleValueChange}
      >
        {options.map((option) => (
          <ToggleGroupItem key={option.value} value={option.value}>
            {option.label}
          </ToggleGroupItem>
        ))}
      </ToggleGroup>
    </FieldSet>
  );
}
