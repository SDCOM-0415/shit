import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Shell脚本文档",
  description: "Shell脚本集合的详细文档",
  head: [
    ['link', { rel: 'icon', href: '/image/favicon.ico' }]
  ],
  locales: {
    root: {
      label: '中文',
      lang: 'zh-CN'
    },
    en: {
      label: 'English',
      lang: 'en',
      title: "Shell Script Documentation",
      description: "Detailed documentation for Shell script collection"
    }
  },
  themeConfig: {
    logo: '/image/logo.svg',
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: '首页', link: '/' },
      { text: '脚本文档', link: '/scripts/' },
      {
        text: '语言',
        items: [
          { text: '中文', link: '/', activeMatch: '^/$|^/scripts/' },
          { text: 'English', link: '/en/', activeMatch: '^/en/' }
        ]
      }
    ],

    sidebar: {
      '/': [
        {
          text: '脚本文档',
          items: [
            { text: '脚本概览', link: '/scripts/' },
            { text: 'kill_app.sh', link: '/scripts/kill_app' },
            { text: 'linux_limit.sh', link: '/scripts/linux_limit' },
            { text: 'get_ip.sh', link: '/scripts/get_ip' },
            { text: 'uninstall_docker.sh', link: '/scripts/uninstall_docker' },
            { text: 'disable_docker.sh', link: '/scripts/disable_docker' },
            { text: 'enable_docker.sh', link: '/scripts/enable_docker' },
            { text: 'fix_env.sh', link: '/scripts/fix_env' },
            { text: 'upload_to_box.sh', link: '/scripts/upload_to_box' },
            { text: 'port_forward.sh', link: '/scripts/port_forward' }
          ]
        }
      ],
      '/en/': [
        {
          text: 'Script Documentation',
          items: [
            { text: 'Overview', link: '/en/scripts/' },
            { text: 'kill_app.sh', link: '/en/scripts/kill_app' },
            { text: 'linux_limit.sh', link: '/en/scripts/linux_limit' },
            { text: 'get_ip.sh', link: '/en/scripts/get_ip' },
            { text: 'uninstall_docker.sh', link: '/en/scripts/uninstall_docker' },
            { text: 'disable_docker.sh', link: '/en/scripts/disable_docker' },
            { text: 'enable_docker.sh', link: '/en/scripts/enable_docker' },
            { text: 'fix_env.sh', link: '/en/scripts/fix_env' },
            { text: 'upload_to_box.sh', link: '/en/scripts/upload_to_box' },
            { text: 'port_forward.sh', link: '/en/scripts/port_forward' }
          ]
        }
      ]
    },

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
    },
    
    // 页脚配置
    footer: {
      message: '文档支持多语言',
      copyright: 'Copyright 2024 SDCOM'
    }
  },
  // 修改开发服务器配置
  vite: {
    server: {
      host: '0.0.0.0',
      port: 5173,
      strictPort: true,
      // 添加允许的主机
      allowedHosts: ['6xa7hc8o04-5173.cnb.run', 'mctbxvdgcs-5173.cnb.run', 'localhost', 'shit.sdcom.asia', 'shit-sdcom.netlify.app', 'shit.sdcom.top', 'shit.cdn.sdcom.top']
    }
  }
})