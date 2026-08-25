import type { Item, ItemInput } from '../types';

// In dev, Vite proxies /api -> http://localhost:8000 (see vite.config.ts).
// In production, set VITE_API_BASE_URL to the backend origin.
const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });

  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`;
    try {
      const body = await response.json();
      if (body?.detail) {
        detail =
          typeof body.detail === 'string'
            ? body.detail
            : JSON.stringify(body.detail);
      }
    } catch {
      // keep default detail
    }
    throw new Error(detail);
  }

  // 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export const itemsApi = {
  list: () => request<Item[]>('/items'),
  create: (input: ItemInput) =>
    request<Item>('/items', { method: 'POST', body: JSON.stringify(input) }),
  update: (id: number, input: ItemInput) =>
    request<Item>(`/items/${id}`, {
      method: 'PUT',
      body: JSON.stringify(input),
    }),
  remove: (id: number) => request<void>(`/items/${id}`, { method: 'DELETE' }),
};
