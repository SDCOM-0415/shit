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
      { icon: '/icons/cnb.svg', link: 'https://cnb.cool/SDCOM/shit' },
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