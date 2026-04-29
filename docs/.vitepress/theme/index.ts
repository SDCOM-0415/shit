import { h } from 'vue'
import Theme from 'vitepress/theme'
import type { Theme as ThemeType } from 'vitepress'

export default {
  ...Theme,
  Layout() {
    return h(Theme.Layout, null, {
      'footer-after': () => {
        if (typeof window !== 'undefined') {
          const hostname = window.location.hostname
          const isBeianDomain = hostname.endsWith('.sdcom.top') || hostname.endsWith('.cnb.run')
          if (isBeianDomain) {
            return h('div', { class: 'icp-beian' }, [
              h('a', { 
                href: 'https://beian.miit.gov.cn/',
                target: '_blank',
                rel: 'noopener noreferrer'
              }, '赣ICP备2023009313号-3')
            ])
          }
        }
        return null
      }
    })
  }
} satisfies ThemeType
