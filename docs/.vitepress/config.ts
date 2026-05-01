import { defineConfig } from 'vitepress'
import { withPwa } from '@vite-pwa/vitepress'

// 网站基础 URL - 根据需要修改
const baseUrl = 'https://shit.sdcom.top'

export default withPwa(defineConfig({
  title: "Shell脚本文档",
  description: "Shell脚本集合的详细文档 - 提供 kill_app, linux_limit, get_ip 等常用 Shell 脚本的使用说明和示例",
  head: [
    ['link', { rel: 'icon', href: '/image/favicon.ico', sizes: 'any' }],
    ['link', { rel: 'icon', href: '/image/logo.svg', type: 'image/svg+xml' }],
    ['link', { rel: 'apple-touch-icon', href: '/image/apple-touch-icon-180x180.png' }],
    ['link', { rel: 'manifest', href: '/manifest.webmanifest' }],
    ['meta', { name: 'theme-color', content: '#3E4E5D' }],
    // SEO 基础标签
    ['meta', { name: 'author', content: 'SDCOM' }],
    ['meta', { name: 'keywords', content: 'Shell脚本,Linux脚本,Shell文档,脚本教程,kill_app,linux_limit,get_ip,docker管理' }],
    ['meta', { name: 'robots', content: 'index, follow' }],
    ['meta', { name: 'googlebot', content: 'index, follow' }],
    ['meta', { name: 'revisit-after', content: '7 days' }],
    ['meta', { name: 'copyright', content: 'Copyright 2026 SDCOM' }],
    ['meta', { name: 'language', content: 'zh-CN' }],
    // Open Graph 基础标签
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:site_name', content: 'Shell脚本文档' }],
    ['meta', { property: 'og:image', content: `${baseUrl}/image/logo.svg` }],
    ['meta', { property: 'og:image:width', content: '512' }],
    ['meta', { property: 'og:image:height', content: '512' }],
    ['meta', { property: 'og:image:type', content: 'image/svg+xml' }],
    // Twitter Card 基础标签
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
    ['meta', { name: 'twitter:image', content: `${baseUrl}/image/logo.svg` }]
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
  
  // 动态生成每个页面的 SEO 标签
  transformHead: ({ pageData, title, description }) => {
    const canonicalUrl = `${baseUrl}${pageData.relativePath.replace(/((^|\/)index)?\.md$/, '$2')}`
    const pageTitle = title || pageData.title || "Shell脚本文档"
    const pageDescription = description || pageData.description || "Shell脚本集合的详细文档"
    const pageLang = pageData.lang || 'zh-CN'
    
    // 判断页面类型
    const isHomePage = pageData.relativePath === 'index.md' || pageData.relativePath === ''
    const schemaType = isHomePage ? 'WebSite' : 'TechArticle'
    
    // 创建 JSON-LD 结构化数据
    const jsonLd = {
      '@context': 'https://schema.org',
      '@type': schemaType,
      name: pageTitle,
      description: pageDescription,
      url: canonicalUrl,
      inLanguage: pageLang,
      author: {
        '@type': 'Organization',
        name: 'SDCOM',
        url: baseUrl
      },
      publisher: {
        '@type': 'Organization',
        name: 'SDCOM',
        logo: {
          '@type': 'ImageObject',
          url: `${baseUrl}/image/logo.svg`
        }
      }
    }
    
    // 如果是文章类型，添加更多字段
    if (!isHomePage) {
      jsonLd.datePublished = pageData.frontmatter?.date || new Date().toISOString().split('T')[0]
      jsonLd.dateModified = pageData.lastUpdated || new Date().toISOString().split('T')[0]
      jsonLd.headline = pageTitle
    }
    
    return [
      // Canonical URL
      ['link', { rel: 'canonical', href: canonicalUrl }],
      // Open Graph 动态标签
      ['meta', { property: 'og:title', content: pageTitle }],
      ['meta', { property: 'og:description', content: pageDescription }],
      ['meta', { property: 'og:url', content: canonicalUrl }],
      ['meta', { property: 'og:locale', content: pageLang === 'zh-CN' ? 'zh_CN' : pageLang }],
      // Twitter Card 动态标签
      ['meta', { name: 'twitter:title', content: pageTitle }],
      ['meta', { name: 'twitter:description', content: pageDescription }],
      // JSON-LD 结构化数据
      ['script', { type: 'application/ld+json' }, JSON.stringify(jsonLd, null, 2)]
    ]
  },
  
  vite: {
    server: {
      host: '0.0.0.0',
      port: 5173,
      strictPort: true,
      allowedHosts: ['6xa7hc8o04-5173.cnb.run', 'mctbxvdgcs-5173.cnb.run', 'localhost', 'shit.sdcom.asia', 'shit-sdcom.netlify.app', 'shit.sdcom.top', 'shit.cdn.sdcom.top']
    }
  }
}))
