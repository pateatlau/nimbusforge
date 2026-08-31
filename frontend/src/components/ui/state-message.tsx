import { CircleCheck, Inbox, LoaderCircle, TriangleAlert } from "lucide-react";
import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

type StateMessageProps = {
  state: "loading" | "empty" | "error" | "success";
  title: string;
  description?: string;
  action?: ReactNode;
  className?: string;
};

const icons = {
  loading: LoaderCircle,
  empty: Inbox,
  error: TriangleAlert,
  success: CircleCheck,
};

function StateMessage({
  state,
  title,
  description,
  action,
  className,
}: StateMessageProps) {
  const Icon = icons[state];
  return (
    <div
      className={cn(
        "flex min-h-48 flex-col items-center justify-center gap-3 px-5 py-10 text-center",
        className,
      )}
      role={state === "error" ? "alert" : "status"}
      aria-live="polite"
    >
      <Icon
        className={cn(
          "size-7 text-muted-foreground",
          state === "loading" && "animate-spin",
          state === "error" && "text-destructive",
          state === "success" && "text-success",
        )}
        aria-hidden="true"
      />
      <div>
        <p className="m-0 font-semibold">{title}</p>
        {description && (
          <p className="mt-1 mb-0 text-sm text-muted-foreground">
            {description}
          </p>
        )}
      </div>
      {action}
    </div>
  );
}

export { StateMessage };
