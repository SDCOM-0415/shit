import { defineConfig } from 'vite'
import { VitePWA } from '@vite-pwa/vitepress'

export default defineConfig({
  plugins: [
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['image/favicon.ico', 'image/apple-touch-icon-180x180.png', 'image/logo.svg'],
      manifest: {
        name: 'Shell Script Docs',
        short_name: 'Shell Docs',
        description: 'Shell脚本集合的详细文档',
        theme_color: '#3E4E5D',
        background_color: '#ffffff',
        display: 'standalone',
        scope: '/',
        start_url: '/',
        icons: [
          {
            src: 'image/pwa-64x64.png',
            sizes: '64x64',
            type: 'image/png'
          },
          {
            src: 'image/pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'image/pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          },
          {
            src: 'image/maskable-icon-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable'
          }
        ],
        lang: 'zh-CN',
        dir: 'ltr'
      },
      workbox: {
        globPatterns: ['**/*.{md,html,js,css,svg,png,jpg,gif}']
      }
    })
  ]
})
