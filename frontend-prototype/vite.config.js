import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/reading-vs-screens/',
  server: {
    port: 4173,
    host: true,
  },
});
