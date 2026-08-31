import { MoreHorizontal, Pencil, Trash2 } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { Item } from "@/types";

type ItemTableProps = {
  items: Item[];
  onEdit: (item: Item) => void;
  onDelete: (id: number) => Promise<boolean>;
};

function ItemTable({ items, onEdit, onDelete }: ItemTableProps) {
  const [deleteItem, setDeleteItem] = useState<Item | null>(null);
  const [deleting, setDeleting] = useState(false);

  async function confirmDelete() {
    if (!deleteItem) return;
    setDeleting(true);
    try {
      const deleted = await onDelete(deleteItem.id);
      if (deleted) setDeleteItem(null);
    } finally {
      setDeleting(false);
    }
  }

  return (
    <Card className="overflow-hidden">
      <div className="flex items-center justify-between border-b px-5 py-4">
        <div>
          <h2 className="m-0 text-base font-semibold">Inventory</h2>
          <p className="mt-1 mb-0 text-sm text-muted-foreground">
            {items.length} {items.length === 1 ? "item" : "items"}
          </p>
        </div>
      </div>
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead className="hidden sm:table-cell">
                Description
              </TableHead>
              <TableHead className="w-16">
                <span className="sr-only">Actions</span>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {items.map((item) => (
              <TableRow key={item.id}>
                <TableCell className="min-w-40 font-semibold">
                  {item.name}
                </TableCell>
                <TableCell className="hidden max-w-xl text-muted-foreground sm:table-cell">
                  {item.description || (
                    <span className="italic">No description</span>
                  )}
                </TableCell>
                <TableCell className="text-right">
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button
                        variant="ghost"
                        size="icon"
                        aria-label={`Actions for ${item.name}`}
                        title={`Actions for ${item.name}`}
                      >
                        <MoreHorizontal />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem onSelect={() => onEdit(item)}>
                        <Pencil />
                        Edit
                      </DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem
                        className="text-destructive focus:text-destructive"
                        onSelect={() => setDeleteItem(item)}
                      >
                        <Trash2 />
                        Delete
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <Dialog
        open={deleteItem !== null}
        onOpenChange={(open) => !open && !deleting && setDeleteItem(null)}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete {deleteItem?.name}?</DialogTitle>
            <DialogDescription>
              This removes the item permanently. This action cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <DialogClose asChild>
              <Button variant="outline" disabled={deleting}>
                Cancel
              </Button>
            </DialogClose>
            <Button
              variant="destructive"
              onClick={confirmDelete}
              disabled={deleting}
            >
              {deleting ? "Deleting" : "Delete item"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </Card>
  );
}

export { ItemTable };
