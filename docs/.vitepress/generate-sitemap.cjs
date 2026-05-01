const fs = require('fs');
const path = require('path');

// 网站基础 URL
const baseUrl = 'https://shit.sdcom.top'
;

// 获取所有 HTML 文件
function getHtmlFiles(dir, base = '') {
  let results = [];
  const list = fs.readdirSync(dir);
  
  list.forEach((file) => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat && stat.isDirectory()) {
      // 排除特殊目录
      if (!['.vitepress', 'node_modules', '.git'].includes(file)) {
        results = results.concat(getHtmlFiles(filePath, path.join(base, file)));
      }
    } else if (file.endsWith('.html')) {
      // 转换为 URL 路径
      let urlPath = path.join(base, file.replace(/\.html$/, ''));
      // 处理 index.html
      if (urlPath.endsWith(path.sep + 'index') || urlPath === 'index') {
        urlPath = urlPath.replace(new RegExp(path.sep + 'index$'), path.sep).replace(/^index$/, '/');
      }
      // 确保以 / 开头
      if (!urlPath.startsWith('/')) {
        urlPath = '/' + urlPath;
      }
      // 统一使用正斜杠（URL 标准）
      urlPath = urlPath.replace(/\\/g, '/');
      results.push(urlPath);
    }
  });
  
  return results;
}

// 生成 sitemap.xml
function generateSitemap(outDir) {
  const pages = getHtmlFiles(outDir);
  
  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
  xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n';
  
  pages.forEach((url) => {
    const fullUrl = baseUrl + url;
    const priority = url === '/' ? '1.0' : '0.8';
    const changefreq = 'weekly';
    
    xml += '  <url>\n';
    xml += `    <loc>${fullUrl}</loc>\n`;
    xml += `    <changefreq>${changefreq}</changefreq>\n`;
    xml += `    <priority>${priority}</priority>\n`;
    
    // 添加多语言链接
    if (url.startsWith('/en/') || url.startsWith('/ja/')) {
      // 这是多语言页面，添加链接到根页面
      const rootUrl = url.replace(/^\/en\/|^\/ja\//, '/');
      xml += `    <xhtml:link rel="alternate" hreflang="zh-CN" href="${baseUrl}${rootUrl}"/>\n`;
      xml += `    <xhtml:link rel="alternate" hreflang="en" href="${baseUrl}/en${url.replace(/^\/en/, '')}"/>\n`;
      xml += `    <xhtml:link rel="alternate" hreflang="ja" href="${baseUrl}/ja${url.replace(/^\/ja/, '')}"/>\n`;
    } else {
      // 这是根页面，添加链接到多语言版本
      xml += `    <xhtml:link rel="alternate" hreflang="zh-CN" href="${fullUrl}"/>\n`;
      xml += `    <xhtml:link rel="alternate" hreflang="en" href="${baseUrl}/en${url}"/>\n`;
      xml += `    <xhtml:link rel="alternate" hreflang="ja" href="${baseUrl}/ja${url}"/>\n`;
    }
    
    xml += '  </url>\n';
  });
  
  xml += '</urlset>';
  
  const sitemapPath = path.join(outDir, 'sitemap.xml');
  fs.writeFileSync(sitemapPath, xml, 'utf8');
  console.log(`✓ Sitemap generated: ${sitemapPath}`);
}

// 主函数
if (require.main === module) {
  const outDir = process.argv[2] || path.join(__dirname, '../../docs/.vitepress/dist');
  generateSitemap(outDir);
}

module.exports = { generateSitemap };
