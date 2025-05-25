import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Shell脚本文档",
  description: "Shell脚本集合的详细文档",
  head: [
    ['link', { rel: 'icon', href: '/image/favicon.ico' }]
  ],
  themeConfig: {
    logo: '/image/logo.svg',
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
      { icon: 'github', link: 'https://cnb.cool/SDCOM/shit/' },
      { icon: 'telegram', link: 'https://t.me/SDCOM_Message_BOT/'}
    ],
    
    // 编辑链接配置
    editLink: {
      pattern: 'https://cnb.cool/SDCOM/shit/-/edit/main/docs/:path',
      text: '在CNB编辑'
    },
    
    // 上下页导航配置
    docFooter: {
      prev: '上一页',
      next: '下一页'
    }
  },
  
  // 修改开发服务器配置
  vite: {
    server: {
      host: '0.0.0.0',
      port: 5173,
      strictPort: true,
      // 添加允许的主机
      allowedHosts: ['kqwywd0dn186-5173.cnb.run', 'localhost', 'shit.sdcom.asia', 'shit-sdcom.netlify.app']
    }
  }
})