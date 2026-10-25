import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    proxy: {
      '/v1': process.env.BACKEND_URL || 'http://localhost:8000',
    },
  },
})
