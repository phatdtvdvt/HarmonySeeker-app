import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import path from 'path'

export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    host: process.env.HOST || 'localhost',
    port: process.env.PORT || 3000,
    strictPort: true,
    watch: {
      usePolling: true,
    },
    hmr: {
      host: 'localhost'
    }
  }
})
