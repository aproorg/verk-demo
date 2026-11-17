import { type FormEvent, useEffect, useState } from "react";
import { addTask, listOwners, listTasks, type Owner, type Task } from "./api";

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [owners, setOwners] = useState<Owner[]>([]);
  const [title, setTitle] = useState("");
  const [ownerId, setOwnerId] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([listTasks(), listOwners()])
      .then(([t, o]) => {
        setTasks(t);
        setOwners(o);
      })
      .catch((e) => setError(String(e)));
  }, []);

  const ownerName = (id: number | null) => owners.find((o) => o.id === id)?.name ?? "Enginn eigandi";

  async function submit(e: FormEvent) {
    e.preventDefault();
    try {
      const task = await addTask(title, ownerId ? Number(ownerId) : null);
      setTasks([...tasks, task]);
      setTitle("");
      setError("");
    } catch (err) {
      setError(String(err));
    }
  }

  return (
    <main>
      <h1>Verk</h1>
      {error && <p role="alert">{error}</p>}
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            <span>{task.title}</span>
            <small>{ownerName(task.owner_id)}</small>
          </li>
        ))}
      </ul>
      <form onSubmit={submit}>
        <input
          aria-label="Titill"
          placeholder="Nýtt verk"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <select aria-label="Eigandi" value={ownerId} onChange={(e) => setOwnerId(e.target.value)}>
          <option value="">Enginn eigandi</option>
          {owners.map((o) => (
            <option key={o.id} value={o.id}>
              {o.name}
            </option>
          ))}
        </select>
        <button type="submit">Bæta við</button>
      </form>
    </main>
  );
}
