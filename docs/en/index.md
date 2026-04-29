---
layout: home

hero:
  name: Shell Scripts Collection
  text: Useful Shell Scripts Collection
  tagline: Actually it's just some 💩 I wrote
  actions:
    - theme: brand
      text: View Script Documentation
      link: /en/scripts/
    - theme: alt
      text: CNB
      link: https://cnb.cool/SDCOM/shit
    - theme: alt
      text: GitHub
      link: https://github.com/SDCOM-0415/shit
---

# Shell Scripts Collection

This is a collection of 💩 I wrote, but with a little practicality.

## Web Build Status
[![Netlify Status](https://api.netlify.com/api/v1/badges/237be5bf-d8e3-4c5f-afcc-ff571562bc52/deploy-status)](https://app.netlify.com/projects/shit-sdcom/deploys)

## About This Project

This project is a static documentation site built with **VitePress**, designed to showcase and manage various useful Shell scripts. The site supports multilingual switching (Chinese, English, Japanese) and provides a clear document structure with a user-friendly interface.

### Technical Features

- **Responsive Design**: Perfectly adapts to desktop and mobile devices
- **Multilingual Support**: Supports Chinese, English, and Japanese languages
- **Code Highlighting**: Shell script syntax highlighting
- **Language Switching**: Preserves current page position when switching languages
- **Sitemap**: Automatically generates sitemap.xml for search engine indexing

### Documentation Structure

The site uses a clear directory structure:

```
docs/
├── index.md                    # Home page
├── scripts/                    # Script documentation
│   ├── index.md                # Script overview
│   └── *.md                    # Detailed documentation for each script
├── en/                         # English documentation
│   ├── index.md
│   └── scripts/
└── ja/                         # Japanese documentation
    ├── index.md
    └── scripts/
```

### Access Methods

This site is available at multiple addresses:

- **Main Domain**: https://shit.sdcom.top/
- **Secondary Domain**: https://shit.sdcom.asia/
- **Netlify**: https://shit-sdcom.netlify.app/

## Usage

### Browsing Documentation

1. Use the top navigation bar to switch between home and script documentation
2. Use the left sidebar to quickly jump to specific script documentation
3. Use the top language selector to switch display languages
4. Click on code blocks in the documentation to view the complete script content

### Getting Scripts

Each script documentation page provides methods to obtain scripts from CNB and GitHub:

```bash
# Get from CNB
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/script_name.sh

# Get from GitHub
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/script_name.sh
```

## Main Scripts

- **kill_app.sh**: A script to quickly terminate Linux system programs
- **linux_limit.sh**: Directory size limit related script with interactive and non-interactive modes
- **get_ip.sh**: A script to get local IP address in termux
- **uninstall_docker.sh**: Docker uninstall script
- **disable_docker.sh**: Completely disable Docker and prevent reinstallation
- **enable_docker.sh**: Re-enable Docker
- **fix_env.sh**: Permanently fix environment variables to shell configuration files
- **upload_to_box.sh**: Script to upload files to file courier
- **port_forward.sh**: IPsec VPN port forwarding management tool

## Project Repository

- **CNB**: https://cnb.cool/SDCOM/shit/
- **GitHub**: https://github.com/SDCOM-0415/shit/

## © Author

SDCOM