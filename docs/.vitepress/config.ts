import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Shell脚本文档",
  description: "Shell脚本集合的详细文档",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: '首页', link: '/' },
      { text: '脚本文档', link: '/scripts/'}
    ],

    sidebar: [
      {
        text: '脚本文档',
        items: [
          { text: '脚本概览', link: '/scripts/' },
          { text: 'kill_app.sh', link: '/scripts/kill_app' },
          { text: 'linux_limit.sh', link: '/scripts/linux_limit' },
          { text: 'get_ip.sh', link: '/scripts/get_ip' },
          { text: 'uninstall_docker.sh', link: '/scripts/uninstall_docker' }
        ]
      }
    ],

    socialLinks: [
      { icon: '<?xml version="1.0" encoding="UTF-8" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="128px" height="128px" viewBox="0 0 128 128" enable-background="new 0 0 128 128" xml:space="preserve">  <image id="image0" width="128" height="128" x="0" y="0"xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAABYmlDQ1BpY2MAACiRdZC9S8NQFMVP', link: 'https://cnb.cool/SDCOM/shit' },
      { icon: 'github', link: 'https://github.com/SDCOM-0415/shit' }
    ]
  },
  
  // 修改开发服务器配置
  vite: {
    server: {
      host: '0.0.0.0',
      port: 5173,
      strictPort: true,
      // 添加允许的主机
      allowedHosts: ['9vv957uxa1ok-5173.cnb.run', 'localhost', 'shit.sdcom.asia', 'shit-sdcom.netlify.app']
    }
  }
})