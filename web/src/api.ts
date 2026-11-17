export interface Owner {
  id: number;
  name: string;
}

export interface Task {
  id: number;
  title: string;
  is_complete: boolean;
  owner_id: number | null;
  created_at: string;
}

async function request<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export const listOwners = () => request<Owner[]>("/owners");
export const listTasks = () => request<Task[]>("/tasks");
export const addTask = (title: string, owner_id: number | null) =>
  request<Task>("/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, owner_id }),
  });
