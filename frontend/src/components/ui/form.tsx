import type { HTMLAttributes, LabelHTMLAttributes, ReactNode } from "react";
import { cn } from "@/lib/utils";

function FormField({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("grid gap-1.5", className)} {...props} />;
}

function FormLabel({
  className,
  ...props
}: LabelHTMLAttributes<HTMLLabelElement>) {
  return (
    <label className={cn("text-sm font-semibold", className)} {...props} />
  );
}

function FormDescription({
  className,
  ...props
}: HTMLAttributes<HTMLParagraphElement>) {
  return (
    <p
      className={cn("m-0 text-xs text-muted-foreground", className)}
      {...props}
    />
  );
}

function FormMessage({
  children,
  className,
  ...props
}: HTMLAttributes<HTMLParagraphElement>) {
  if (!children) return null;
  return (
    <p
      className={cn("m-0 text-xs font-medium text-destructive", className)}
      {...props}
    >
      {children as ReactNode}
    </p>
  );
}

export { FormDescription, FormField, FormLabel, FormMessage };
