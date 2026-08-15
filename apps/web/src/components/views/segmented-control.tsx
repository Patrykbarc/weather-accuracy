import { Radio } from "@base-ui/react/radio";
import { RadioGroup } from "@base-ui/react/radio-group";
import { useId, type ReactNode } from "react";

import { cn } from "@/lib/utils";

export type SegmentedOption<TValue extends string> = {
  value: TValue;
  label: ReactNode;
};

export type SegmentedControlProps<TValue extends string> = {
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

  return (
    <div className={cn("flex flex-col gap-2", className)}>
      <span
        id={labelId}
        className="text-muted-foreground text-xs font-medium tracking-wide uppercase"
      >
        {label}
      </span>
      <RadioGroup
        aria-labelledby={labelId}
        value={value}
        onValueChange={onValueChange}
        className="bg-muted inline-flex h-8 w-fit items-center justify-center rounded-2xl p-[3px]"
      >
        {options.map((option) => (
          <Radio.Root
            key={option.value}
            value={option.value}
            className="text-foreground/60 hover:text-foreground focus-visible:ring-ring/50 data-checked:bg-background data-checked:text-foreground dark:text-muted-foreground dark:hover:text-foreground dark:data-checked:bg-input/30 inline-flex h-full cursor-default items-center justify-center rounded-2xl px-3 text-sm font-medium whitespace-nowrap transition-all focus-visible:ring-[3px] focus-visible:outline-none"
          >
            {option.label}
          </Radio.Root>
        ))}
      </RadioGroup>
    </div>
  );
}
