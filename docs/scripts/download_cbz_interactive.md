# download_cbz_interactive.py

这是一个用于下载 cloudme.one 漫画章节并打包为 CBZ 文件的 Python 脚本，支持 Windows / macOS / Linux，当前版本为<Badge type="tip" text="v1.0" />。

## 功能说明

`download_cbz_interactive.py` 是一个 cloudme.one 漫画章节下载工具。它通过 API 获取漫画信息，下载章节图片，并自动打包为 CBZ 格式文件，方便在各类漫画阅读器中使用。

## 功能特点

- 交互式选择要下载的章节范围
- 自动通过 API 获取漫画和章节信息
- 通过 img.cloudme.one 代理下载高质量图片（需提供 cf_clearance）
- CDN 直连回退下载（无需 Cookie，但图片质量较低）
- 自动打包为 CBZ 文件（ZIP 格式，漫画阅读器通用）
- 支持命令行指定下载目录
- 自动检测并安装缺失依赖
- 跨平台兼容（Windows / macOS / Linux）
- 终端 Unicode 自适应（无 Unicode 支持时自动降级为 ASCII 符号）
- 下载进度条显示
- 已存在的 CBZ 文件自动跳过

## 依赖

- Python 3.6+
- curl_cffi

```bash
pip install curl_cffi
```

脚本首次运行时会自动检测依赖，缺失时提示自动安装。

## 使用方法

### 下载脚本

CNB：
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/download_cbz_interactive.py
```

Github：
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/download_cbz_interactive.py
```

### 交互式模式

直接运行脚本进入交互模式：

```bash
python download_cbz_interactive.py
```

### 指定下载目录

通过命令行参数指定 CBZ 文件的保存目录：

```bash
# Windows
python download_cbz_interactive.py -o D:\Comics

# macOS / Linux
python download_cbz_interactive.py -o ~/Comics

# 也可以使用长参数
python download_cbz_interactive.py --output ./comics
```

默认下载目录为脚本所在目录。

## 命令行参数

| 参数 | 缩写 | 说明 |
|------|------|------|
| `--output` | `-o` | 指定 CBZ 文件的保存目录（默认: 脚本所在目录） |

## 运行流程

1. **确认下载目录**：显示当前下载目录，可直接输入新路径修改，回车确认
2. **输入漫画 ID**：输入 cloudme.one 网站上的漫画 ID（URL 中的数字，例如 `cloudme.one/refs/10` 中的 `10`）
3. **获取漫画信息**：自动通过 API 获取漫画标题和全部章节列表
4. **前缀处理（可选）**：如果检测到章节标题含有 `_` 分隔符，会提示是否去掉前缀部分
5. **配置 Cloudflare Cookie（可选）**：提供 `cf_clearance` cookie 可下载高质量图片，跳过则使用 CDN 直连下载低质量版本
6. **选择章节**：输入要下载的章节范围，支持以下格式：
   - 单章：`101`
   - 范围：`101-120`
   - 多个：`101,103,105`
   - 混合：`101-105,108,110-112`
   - 全部：`all`
7. **确认并下载**：确认信息后开始下载，显示下载进度和结果汇总

## 如何获取 cf_clearance

高质量图片需要通过 Cloudflare 保护的代理下载，需要提供 `cf_clearance` cookie：

1. 在浏览器中打开 `cloudme.one`
2. 按 `F12` 打开开发者工具
3. 切换到 `Application`（应用）选项卡
4. 在左侧找到 `Cookies` → `https://cloudme.one`
5. 找到 `cf_clearance` 字段，复制其值

::: tip
如果不提供 `cf_clearance`，脚本仍然可以工作，但会通过 CDN 直连下载较低质量的图片。
:::

## 注意事项

- 脚本需要 Python 3.6 或更高版本
- `curl_cffi` 用于绕过 Cloudflare 保护，是核心依赖
- 下载大量章节时，脚本会自动在章节间添加间隔，避免请求过快
- 已存在的 CBZ 文件会自动跳过，不会重复下载
- Windows 用户如果终端显示乱码，脚本会自动尝试启用 UTF-8 支持

## 项目仓库

CNB：https://cnb.cool/SDCOM/shit/-/blob/main/script/download_cbz_interactive.py

Github：https://github.com/SDCOM-0415/shit/blob/main/script/download_cbz_interactive.py

## © 作者

SDCOM
