import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "Shell脚本文档",
  description: "Shell脚本集合的详细文档",
  head: [
    ['link', { rel: 'icon', href: '/image/favicon.ico', sizes: 'any' }],
    ['link', { rel: 'icon', href: '/image/logo.svg', type: 'image/svg+xml' }],
    ['link', { rel: 'apple-touch-icon', href: '/image/apple-touch-icon-180x180.png' }],
    ['link', { rel: 'manifest', href: '/manifest.webmanifest' }],
    ['meta', { name: 'theme-color', content: '#3E4E5D' }]
  ],
  ignoreDeadLinks: true,
  
  locales: {
    root: {
      label: '中文',
      lang: 'zh-CN',
      title: "Shell脚本文档",
      description: "Shell脚本集合的详细文档",
      themeConfig: {
        nav: [
          { text: '首页', link: '/' },
          { text: '脚本文档', link: '/scripts/' }
        ],
        sidebar: [
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
        docFooter: {
          prev: '上一页',
          next: '下一页'
        },
        editLink: {
          pattern: 'https://cnb.cool/SDCOM/shit/-/edit/main/docs/:path',
          text: '在CNB编辑'
        }
      }
    },
    en: {
      label: 'English',
      lang: 'en',
      title: "Shell Script Documentation",
      description: "Detailed documentation for Shell script collection",
      themeConfig: {
        nav: [
          { text: 'Home', link: '/en/' },
          { text: 'Script Docs', link: '/en/scripts/' }
        ],
        sidebar: [
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
        ],
        docFooter: {
          prev: 'Previous',
          next: 'Next'
        },
        editLink: {
          pattern: 'https://cnb.cool/SDCOM/shit/-/edit/main/docs/:path',
          text: 'Edit on CNB'
        }
      }
    },
    ja: {
      label: '日本語',
      lang: 'ja',
      title: "Shell スクリプトドキュメンテーション",
      description: "Shellスクリプトコレクションの詳細なドキュメント",
      themeConfig: {
        nav: [
          { text: 'ホーム', link: '/ja/' },
          { text: 'スクリプトドキュメント', link: '/ja/scripts/' }
        ],
        sidebar: [
          {
            text: 'スクリプトドキュメント',
            items: [
              { text: '概要', link: '/ja/scripts/' },
              { text: 'kill_app.sh', link: '/ja/scripts/kill_app' },
              { text: 'linux_limit.sh', link: '/ja/scripts/linux_limit' },
              { text: 'get_ip.sh', link: '/ja/scripts/get_ip' },
              { text: 'uninstall_docker.sh', link: '/ja/scripts/uninstall_docker' },
              { text: 'disable_docker.sh', link: '/ja/scripts/disable_docker' },
              { text: 'enable_docker.sh', link: '/ja/scripts/enable_docker' },
              { text: 'fix_env.sh', link: '/ja/scripts/fix_env' },
              { text: 'upload_to_box.sh', link: '/ja/scripts/upload_to_box' },
              { text: 'port_forward.sh', link: '/ja/scripts/port_forward' }
            ]
          }
        ],
        docFooter: {
          prev: '前のページ',
          next: '次のページ'
        },
        editLink: {
          pattern: 'https://cnb.cool/SDCOM/shit/-/edit/main/docs/:path',
          text: 'CNBで編集'
        }
      }
    }
  },
  
  themeConfig: {
    logo: '/image/logo.svg',
    
    selectLanguageText: '语言',
    selectLanguageAriaLabel: '选择语言',
    
    socialLinks: [
      { icon: 'github', link: 'https://cnb.cool/SDCOM/shit/' },
      { icon: 'telegram', link: 'https://t.me/SDCOM_Message_BOT/' }
    ],
    
    footer: {
      message: '文档支持多语言',
      copyright: 'Copyright 2026 SDCOM'
    }
  },
  
  vite: {
    server: {
      host: '0.0.0.0',
      port: 5173,
      strictPort: true,
      allowedHosts: ['6xa7hc8o04-5173.cnb.run', 'mctbxvdgcs-5173.cnb.run', 'localhost', 'shit.sdcom.asia', 'shit-sdcom.netlify.app', 'shit.sdcom.top', 'shit.cdn.sdcom.top']
    }
  }
})
