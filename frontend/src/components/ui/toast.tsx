import { Toaster as Sonner } from "sonner";

function Toaster() {
  return (
    <Sonner
      closeButton
      position="bottom-right"
      toastOptions={{
        classNames: {
          toast: "border-border bg-card text-card-foreground shadow-panel",
          description: "text-muted-foreground",
        },
      }}
    />
  );
}

export { Toaster };
