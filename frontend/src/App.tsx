import { RefreshCw } from "lucide-react";
import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { toast } from "sonner";
import { itemsApi } from "@/api/items";
import { ThemeMenu } from "@/components/theme-menu";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { StateMessage } from "@/components/ui/state-message";
import { Toaster } from "@/components/ui/toast";
import { ItemForm } from "@/features/items/item-form";
import { ItemTable } from "@/features/items/item-table";
import type { Item } from "@/types";

function App() {
  const [items, setItems] = useState<Item[]>([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [editingId, setEditingId] = useState<number | null>(null);
  const [saving, setSaving] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [requestError, setRequestError] = useState<string | null>(null);

  async function loadItems() {
    setInitialLoading(true);
    setLoadError(null);
    try {
      setItems(await itemsApi.list());
    } catch (err) {
      setLoadError(err instanceof Error ? err.message : "Unable to load items");
    } finally {
      setInitialLoading(false);
    }
  }

  useEffect(() => {
    let active = true;

    itemsApi
      .list()
      .then((result) => {
        if (active) setItems(result);
      })
      .catch((err: unknown) => {
        if (active) {
          setLoadError(
            err instanceof Error ? err.message : "Unable to load items",
          );
        }
      })
      .finally(() => {
        if (active) setInitialLoading(false);
      });

    return () => {
      active = false;
    };
  }, []);

  function resetForm() {
    setName("");
    setDescription("");
    setEditingId(null);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!name.trim()) return;

    setSaving(true);
    setRequestError(null);
    const input = {
      name: name.trim(),
      description: description.trim() || null,
    };

    try {
      if (editingId === null) {
        const created = await itemsApi.create(input);
        setItems((prev) => [...prev, created]);
        toast.success("Item added", { description: created.name });
      } else {
        const updated = await itemsApi.update(editingId, input);
        setItems((prev) =>
          prev.map((it) => (it.id === updated.id ? updated : it)),
        );
        toast.success("Changes saved", { description: updated.name });
      }
      resetForm();
    } catch (err) {
      setRequestError(err instanceof Error ? err.message : "Request failed");
    } finally {
      setSaving(false);
    }
  }

  function startEdit(item: Item) {
    setEditingId(item.id);
    setName(item.name);
    setDescription(item.description ?? "");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function handleDelete(id: number) {
    setRequestError(null);
    try {
      await itemsApi.remove(id);
      const deleted = items.find((item) => item.id === id);
      setItems((prev) => prev.filter((it) => it.id !== id));
      if (editingId === id) resetForm();
      toast.success("Item deleted", { description: deleted?.name });
    } catch (err) {
      setRequestError(err instanceof Error ? err.message : "Delete failed");
    }
  }

  return (
    <div className="min-h-svh">
      <header className="border-b bg-card/90">
        <div className="mx-auto flex min-h-16 max-w-(--size-content) items-center justify-between gap-4 px-4 sm:px-page">
          <div>
            <p className="m-0 text-base font-bold">NimbusForge</p>
            <p className="m-0 hidden text-xs text-muted-foreground sm:block">
              Item operations workspace
            </p>
          </div>
          <ThemeMenu />
        </div>
      </header>

      <main className="mx-auto grid max-w-(--size-content) gap-6 px-4 py-6 sm:px-page sm:py-8 lg:grid-cols-[22rem_minmax(0,1fr)] lg:items-start">
        <ItemForm
          name={name}
          description={description}
          editing={editingId !== null}
          pending={saving}
          onNameChange={(event) => setName(event.target.value)}
          onDescriptionChange={(event) => setDescription(event.target.value)}
          onSubmit={handleSubmit}
          onCancel={resetForm}
        />

        <section className="grid gap-4" aria-label="Inventory">
          {requestError && (
            <Card>
              <StateMessage
                className="min-h-0 items-start py-4 text-left"
                state="error"
                title="Request failed"
                description={requestError}
              />
            </Card>
          )}
          {initialLoading ? (
            <Card>
              <StateMessage
                state="loading"
                title="Loading inventory"
                description="Retrieving the latest items."
              />
            </Card>
          ) : loadError ? (
            <Card>
              <StateMessage
                state="error"
                title="Unable to load inventory"
                description={loadError}
                action={
                  <Button variant="outline" onClick={() => void loadItems()}>
                    <RefreshCw />
                    Try again
                  </Button>
                }
              />
            </Card>
          ) : items.length === 0 ? (
            <Card>
              <StateMessage
                state="empty"
                title="No items yet"
                description="Add the first item using the form."
              />
            </Card>
          ) : (
            <ItemTable
              items={items}
              onEdit={startEdit}
              onDelete={handleDelete}
            />
          )}
        </section>
      </main>
      <Toaster />
    </div>
  );
}

export default App;
