---
layout: home

hero:
  name: Shell Scripts Collection
  text: 实用Shell脚本集合
  tagline: 其实就是我写过的💩
  actions:
    - theme: brand
      text: 查看脚本文档
      link: /scripts/
    - theme: alt
      text: CNB
      link: https://cnb.cool/SDCOM/shit
    - theme: alt
      text: GitHub
      link: https://github.com/SDCOM-0415/shit
---

# Shell Scripts Collection

这是一个我写的💩的集合，但是带有一点点实用性。

## Web 构建状态
[![Netlify Status](https://api.netlify.com/api/v1/badges/237be5bf-d8e3-4c5f-afcc-ff571562bc52/deploy-status)](https://app.netlify.com/projects/shit-sdcom/deploys)

## 项目介绍

本项目是一个基于 **VitePress** 构建的静态文档站点，用于展示和管理各种实用的 Shell 脚本。站点支持多语言切换（中文、英文、日语），提供清晰的文档结构和友好的用户界面。

### 技术特性

- **响应式设计**: 完美适配桌面端和移动端
- **多语言支持**: 支持中文、英文、日语三种语言
- **代码高亮**: 支持 Shell 脚本语法高亮显示
- **语言切换**: 切换语言时自动保留当前页面位置
- **网站地图**: 自动生成 sitemap.xml 便于搜索引擎收录

### 文档结构

站点采用清晰的目录结构：

```
docs/
├── index.md                    # 首页
├── scripts/                    # 脚本文档
│   ├── index.md                # 脚本概览
│   └── *.md                    # 各脚本详细文档
├── en/                         # 英文文档
│   ├── index.md
│   └── scripts/
└── ja/                         # 日语文档
    ├── index.md
    └── scripts/
```

### 访问方式

本站点提供多个访问地址：

- **主域名**: https://shit.sdcom.top/
- **备用域名**: https://shit.sdcom.asia/
- **Netlify**: https://shit-sdcom.netlify.app/

## 使用方法

### 浏览文档

1. 使用顶部导航栏在首页和脚本文档之间切换
2. 使用左侧侧边栏快速跳转到特定脚本的文档
3. 使用顶部语言选择器切换显示语言
4. 点击文档中的代码块可以查看脚本的完整内容

### 获取脚本

每个脚本文档页面都提供了从 CNB 和 GitHub 获取脚本的方法：

```bash
# 从 CNB 获取
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/script_name.sh

# 从 GitHub 获取
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/script_name.sh
```

## 主要脚本

- **kill_app.sh**: 快速结束Linux系统程序的脚本
- **linux_limit.sh**: 目录大小限制相关的脚本，有交互模式和非交互模式
- **get_ip.sh**: 在termux中获取本机IP地址的脚本
- **uninstall_docker.sh**: Docker卸载脚本
- **disable_docker.sh**: 彻底禁用Docker并防止重新安装
- **enable_docker.sh**: 重新启用Docker
- **fix_env.sh**: 将环境变量永久固定到shell配置文件
- **upload_to_box.sh**: 上传文件到文件快递柜的脚本
- **port_forward.sh**: IPsec VPN端口转发管理工具

## 项目仓库

- **CNB**: https://cnb.cool/SDCOM/shit/
- **GitHub**: https://github.com/SDCOM-0415/shit/

## © 作者

SDCOM