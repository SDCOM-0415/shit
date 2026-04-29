# Shit
Shell 脚本集合文档站点

## 项目简介
本项目是一个基于 VitePress 构建的 Shell 脚本文档站点，提供多语言支持（中文、英文、日语），用于展示和管理各种实用的 Shell 脚本。

## 访问地址
https://shit.sdcom.top/

https://shit.sdcom.asia/

https://shit-sdcom.netlify.app/

## 部署状态
[![Netlify Status](https://api.netlify.com/api/v1/badges/237be5bf-d8e3-4c5f-afcc-ff571562bc52/deploy-status)](https://app.netlify.com/projects/shit-sdcom/deploys)

## 技术栈
- **框架**: VitePress 1.6.x
- **语言**: Markdown + Vue 3
- **多语言支持**: 中文、英文、日语
- **构建工具**: Vite 6.x
- **部署平台**: Netlify

## 功能特性
- ✅ 多语言文档支持（中文/英文/日语）
- ✅ 语言切换保留当前页面
- ✅ 响应式设计
- ✅ 代码语法高亮
- ✅ 网站地图（sitemap.xml）
- ✅ 自定义导航和侧边栏

## 文件结构

```
/workspace/
├── .cnb.yml                    # CNB 平台配置文件
├── .dockerignore               # Docker 忽略文件
├── package.json                # 项目依赖配置
├── README.md                   # 项目说明文档
├── docs/                       # 文档目录（VitePress 站点）
│   ├── .vitepress/             # VitePress 配置目录
│   │   └── config.ts           # VitePress 主配置文件
│   │       # - 多语言配置（中文/英文/日语）
│   │       # - 导航栏和侧边栏配置
│   │       # - 主题配置（logo、社交链接、页脚）
│   │       # - 开发服务器配置
│   ├── public/                 # 静态资源目录
│   │   ├── image/              # 图片资源
│   │   │   ├── cnb-favicon.svg
│   │   │   ├── favicon.ico
│   │   │   ├── github-favicon.png
│   │   │   └── logo.svg
│   │   └── sitemap.xml         # 网站地图
│   ├── scripts/                # 中文脚本文档目录
│   │   ├── index.md            # 脚本概览页面
│   │   ├── kill_app.md
│   │   ├── linux_limit.md
│   │   ├── get_ip.md
│   │   ├── uninstall_docker.md
│   │   ├── disable_docker.md
│   │   ├── enable_docker.md
│   │   ├── fix_env.md
│   │   ├── upload_to_box.md
│   │   └── port_forward.md
│   ├── en/                     # 英文文档目录
│   │   ├── index.md            # 英文首页
│   │   └── scripts/            # 英文脚本文档
│   │       ├── index.md
│   │       └── ... (各脚本英文文档)
│   ├── ja/                     # 日语文档目录
│   │   ├── index.md            # 日语首页
│   │   └── scripts/            # 日语脚本文档
│   │       ├── index.md
│   │       └── ... (各脚本日语文档)
│   └── index.md                # 中文首页
└── script/                     # Shell 脚本源码目录
    ├── none/                   # 额外资源文件
    │   ├── pan_newuser.html
    │   └── pan_restart_password.html
    ├── disable_docker.sh
    ├── enable_docker.sh
    ├── fix_env.sh
    ├── get_ip.sh
    ├── kill_app.sh
    ├── linux_limit.sh
    ├── port_forward.sh
    ├── uninstall_docker.sh
    └── upload_to_box.sh
```

## 目录说明

### docs/
VitePress 静态站点的主目录，包含所有文档内容和配置。

### docs/.vitepress/
VitePress 的配置目录，包含站点配置文件。

### docs/public/
静态资源目录，存放图片、favicon 和网站地图等资源。

### docs/scripts/
中文脚本文档目录，包含各脚本的详细说明文档。

### docs/en/
英文文档目录，包含所有中文页面的英文翻译版本。

### docs/ja/
日语文档目录，包含所有中文页面的日语翻译版本。

### script/
Shell 脚本源码目录，存放所有脚本的原始代码文件。

## 开发命令

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run docs:dev

# 构建生产版本
npm run docs:build

# 预览生产版本
npm run docs:preview
```

## 多语言支持

本项目支持三种语言：

| 语言 | 路径前缀 | 状态 |
|------|----------|------|
| 中文 | `/` | 默认语言 |
| 英文 | `/en/` | 由AI完整翻译 |
| 日语 | `/ja/` | 由AI完整翻译 |

语言切换会自动保留当前页面位置，例如从 `/scripts/kill_app` 切换到英文会跳转到 `/en/scripts/kill_app`。

## 项目仓库

- CNB: https://cnb.cool/SDCOM/shit
- GitHub: https://github.com/SDCOM-0415/shit

## 作者

SDCOM