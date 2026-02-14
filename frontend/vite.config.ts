import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { visualizer } from "rollup-plugin-visualizer";

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    visualizer({
      open: false, // Don't open browser automatically in this env
      gzipSize: true,
      brotliSize: true,
      filename: "stats.html", // Save file to check if needed
    }),
  ],
})
