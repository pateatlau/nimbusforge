import { useEffect, useState } from 'react';
import type { SubmitEvent } from 'react';
import { itemsApi } from './api/items';
import type { Item } from './types';
import './App.css';

function App() {
  const [items, setItems] = useState<Item[]>([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [editingId, setEditingId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    itemsApi
      .list()
      .then(setItems)
      .catch((err: Error) => setError(err.message));
  }, []);

  function resetForm() {
    setName('');
    setDescription('');
    setEditingId(null);
  }

  async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!name.trim()) return;

    setLoading(true);
    setError(null);
    const input = {
      name: name.trim(),
      description: description.trim() || null,
    };

    try {
      if (editingId === null) {
        const created = await itemsApi.create(input);
        setItems((prev) => [...prev, created]);
      } else {
        const updated = await itemsApi.update(editingId, input);
        setItems((prev) =>
          prev.map((it) => (it.id === updated.id ? updated : it)),
        );
      }
      resetForm();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Request failed');
    } finally {
      setLoading(false);
    }
  }

  function startEdit(item: Item) {
    setEditingId(item.id);
    setName(item.name);
    setDescription(item.description ?? '');
  }

  async function handleDelete(id: number) {
    setError(null);
    try {
      await itemsApi.remove(id);
      setItems((prev) => prev.filter((it) => it.id !== id));
      if (editingId === id) resetForm();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Delete failed');
    }
  }

  return (
    <div className="app">
      <h1>Items</h1>

      <form
        className="item-form"
        onSubmit={handleSubmit}
      >
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Name"
          required
        />
        <input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Description (optional)"
        />
        <div className="form-actions">
          <button
            type="submit"
            disabled={loading}
            className="primary"
          >
            {editingId === null ? 'Add item' : 'Save changes'}
          </button>
          {editingId !== null && (
            <button
              type="button"
              onClick={resetForm}
              disabled={loading}
            >
              Cancel
            </button>
          )}
        </div>
      </form>

      {error && <p className="error">{error}</p>}

      {items.length === 0 ? (
        <p className="empty">No items yet. Add one above.</p>
      ) : (
        <ul className="item-list">
          {items.map((item) => (
            <li
              key={item.id}
              className="item-row"
            >
              <div>
                <strong>{item.name}</strong>
                {item.description && (
                  <span className="item-desc">— {item.description}</span>
                )}
              </div>
              <div className="row-actions">
                <button
                  type="button"
                  onClick={() => startEdit(item)}
                >
                  Edit
                </button>
                <button
                  type="button"
                  onClick={() => handleDelete(item.id)}
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
