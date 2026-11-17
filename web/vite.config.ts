import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

const api = "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: { port: 3000, strictPort: true, proxy: { "/tasks": api, "/owners": api } },
});
