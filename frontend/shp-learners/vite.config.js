import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Enables access via LAN IP (e.g., 192.168.x.x)
    port: 5173,       // Optional: change port if needed
  },
})
