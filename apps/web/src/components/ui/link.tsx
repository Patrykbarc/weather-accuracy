export function Link({ children, ...props }: React.ComponentProps<"a">) {
  return (
    <a
      target={
        props.target === "_blank"
          ? (props.rel = "noreferrer noopener")
          : undefined
      }
      {...props}
    >
      {children}
    </a>
  );
}
