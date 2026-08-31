import { LoaderCircle, Plus, Save } from 'lucide-react';
import type { ChangeEvent, FormEvent } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { FormDescription, FormField, FormLabel } from '@/components/ui/form';
import { Input } from '@/components/ui/input';

type ItemFormProps = {
  name: string;
  description: string;
  editing: boolean;
  pending: boolean;
  onNameChange: (event: ChangeEvent<HTMLInputElement>) => void;
  onDescriptionChange: (event: ChangeEvent<HTMLInputElement>) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  onCancel: () => void;
};

function ItemForm({ name, description, editing, pending, onNameChange, onDescriptionChange, onSubmit, onCancel }: ItemFormProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{editing ? 'Edit item' : 'Add an item'}</CardTitle>
        <CardDescription>{editing ? 'Update the selected record.' : 'Create a record in the shared inventory.'}</CardDescription>
      </CardHeader>
      <CardContent>
        <form className="grid gap-4" onSubmit={onSubmit} aria-busy={pending}>
          <FormField>
            <FormLabel htmlFor="item-name">Name</FormLabel>
            <Input id="item-name" value={name} onChange={onNameChange} required maxLength={120} autoComplete="off" />
          </FormField>
          <FormField>
            <FormLabel htmlFor="item-description">Description</FormLabel>
            <Input id="item-description" value={description} onChange={onDescriptionChange} maxLength={500} autoComplete="off" />
            <FormDescription>Optional context for this item.</FormDescription>
          </FormField>
          <div className="flex flex-wrap gap-2 pt-1">
            <Button type="submit" disabled={pending || !name.trim()}>
              {pending ? <LoaderCircle className="animate-spin" /> : editing ? <Save /> : <Plus />}
              {pending ? 'Saving' : editing ? 'Save changes' : 'Add item'}
            </Button>
            {editing && <Button type="button" variant="outline" onClick={onCancel} disabled={pending}>Cancel</Button>}
          </div>
        </form>
      </CardContent>
    </Card>
  );
}

export { ItemForm };