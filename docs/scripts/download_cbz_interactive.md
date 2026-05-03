# download_cbz_interactive.py

这是一个用于下载 cloudme.one 漫画章节并打包为 CBZ 文件的 Python 脚本，支持 Windows / macOS / Linux，当前版本为<Badge type="tip" text="v1.1" />。

## 功能说明

`download_cbz_interactive.py` 是一个 cloudme.one 漫画章节下载工具。它通过 API 获取漫画信息，下载章节图片，并自动打包为 CBZ 格式文件，方便在各类漫画阅读器中使用。

## 功能特点

- 交互式或命令行模式选择要下载的章节范围
- 自动通过 API 获取漫画和章节信息
- 通过 img.cloudme.one 代理下载高质量图片（需提供 cf_clearance）
- CDN 直连回退下载（无需 Cookie，但图片质量较低）
- 多线程下载图片，多任务并行下载章节
- 自动打包为 CBZ 文件（ZIP 格式，漫画阅读器通用）
- 支持 HTTP/SOCKS5 代理
- 可配置图片下载线程数（1-32）和并行章节数（1-5）
- 支持命令行传入 cf_clearance，无需交互输入
- 支持跳过确认直接开始下载（`-y`/`--yes`）
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

GitHub：
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/download_cbz_interactive.py
```

### 交互式模式

直接运行脚本进入交互模式，按提示逐步操作：

```bash
python download_cbz_interactive.py
```

### 非交互模式

通过命令行参数提供所有必要信息后，脚本直接开始下载，无需交互输入：

```bash
# 下载第 101-120 章，使用代理，8 线程，3 个章节并行
python download_cbz_interactive.py \
  -o D:\Comics \
  -m 10 \
  -c 101-120 \
  --cf xxxxxxxx \
  -p http://127.0.0.1:7890 \
  -t 16 \
  -j 3 \
  --strip-prefix \
  -y
```

> `-m`、`-c` 和 `-o` 均提供后，脚本自动进入非交互模式。
> 未提供的参数仍会在交互模式中提示输入。

### 指定下载目录

通过命令行参数指定 CBZ 文件的保存目录：

```bash
# Windows
python download_cbz_interactive.py -o D:\Comics

# macOS / Linux
python download_cbz_interactive.py -o ~/Comics

# 也可以和其他参数组合使用
python download_cbz_interactive.py -o ~/Comics -m 10 -c all -y
```

默认下载目录为脚本所在目录。

## 命令行参数

| 参数 | 缩写 | 说明 |
|------|------|------|
| `--output DIR` | `-o` | 指定 CBZ 文件的保存目录（默认：脚本所在目录） |
| `--mid ID` | `-m` | 漫画 ID（如 cloudme.one/refs/10 中的 10） |
| `--chapters RANGE` | `-c` | 章节范围，支持 `101-120`、`101,103,105`、`all` |
| `--cf TOKEN` | | cf_clearance cookie 值（用于下载高质量图片） |
| `--proxy URL` | `-p` | HTTP/SOCKS5 代理地址（如 `http://127.0.0.1:7890`） |
| `--threads N` | `-t` | 图片下载线程数（1-32，默认 8） |
| `--jobs N` | `-j` | 并行下载章节数（1-5，默认 5） |
| `--strip-prefix` | | 去掉标题中 `_` 前的前缀（如 `某漫画_第101话` → `第101话`） |
| `--yes` | `-y` | 跳过确认提示，直接开始下载 |

## 运行流程

### 交互模式流程

1. **确认下载目录**：显示当前下载目录，可直接输入新路径修改，回车确认
2. **（可选）设置代理**：输入 HTTP/SOCKS5 代理地址，直接回车跳过
3. **（可选）设置线程数**：设置图片下载线程数（1-32），回车使用默认 8
4. **（可选）设置并行任务数**：设置同时下载的章节数（1-5），回车使用默认 5
5. **输入漫画 ID**：输入 cloudme.one 网站上的漫画 ID（URL 中的数字，例如 `cloudme.one/refs/10` 中的 `10`）
6. **获取漫画信息**：自动通过 API 获取漫画标题和全部章节列表
7. **前缀处理（可选）**：如果检测到章节标题含有 `_` 分隔符，会提示是否去掉前缀部分
8. **配置 Cloudflare Cookie（可选）**：提供 `cf_clearance` cookie 可下载高质量图片，跳过则使用 CDN 直连下载低质量版本
9. **选择章节**：输入要下载的章节范围，支持以下格式：
   - 单章：`101`
   - 范围：`101-120`
   - 多个：`101,103,105`
   - 混合：`101-105,108,110-112`
   - 全部：`all`
10. **确认并下载**：确认信息后开始下载，显示下载进度和结果汇总

### 非交互模式

当 `-o`、`-m`、`-c` 三个参数均提供时，脚本跳过所有交互提示，直接开始下载。其余参数（`-p`、`-t`、`-j`、`--cf`、`--strip-prefix`、`-y`）可按需选填。

## 如何获取 cf_clearance

高质量图片需要通过 Cloudflare 保护的代理下载，需要提供 `cf_clearance` cookie：

1. 在浏览器中打开 `cloudme.one`
2. 按 `F12` 打开开发者工具
3. 切换到 `Application`（应用）选项卡
4. 在左侧找到 `Cookies` → `https://cloudme.one`
5. 找到 `cf_clearance` 字段，复制其值

::: tip
如果不提供 `cf_clearance`，脚本仍然可以工作，但会通过 CDN 直连下载较低质量的图片。
也可以通过 `--cf` 参数在命令行中直接传入，无需在交互模式中手动粘贴。
:::

## 注意事项

- 脚本需要 Python 3.6 或更高版本
- `curl_cffi` 用于绕过 Cloudflare 保护，是核心依赖
- 下载大量章节时，脚本会自动在章节间添加间隔，避免请求过快
- 已存在的 CBZ 文件会自动跳过，不会重复下载
- Windows 用户如果终端显示乱码，脚本会自动尝试启用 UTF-8 支持
- 建议图片下载线程数（`-t`）不超过 32，并行章节数（`-j`）不超过 5，避免被限制

## 项目仓库

CNB：https://cnb.cool/SDCOM/shit/-/blob/main/script/download_cbz_interactive.py

GitHub：https://github.com/SDCOM-0415/shit/blob/main/script/download_cbz_interactive.py

## © 作者

SDCOM
