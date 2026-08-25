export interface Item {
  id: number;
  name: string;
  description: string | null;
}

export interface ItemInput {
  name: string;
  description: string | null;
}
