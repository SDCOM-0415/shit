"""
cloudme.one 漫画章节下载工具

用法:
  # 交互模式
  python download_cbz_interactive.py

  # 非交互模式 (提供所有必要参数后直接开始下载)
  python download_cbz_interactive.py -o D:\\Comics -m 10 -c 101-120 --cf xxx
  python download_cbz_interactive.py -o ~/Comics -m 10 -c all -p http://127.0.0.1:7890 -t 16 -j 3 --strip-prefix

支持系统: Windows / macOS / Linux

功能:
  - 交互式或命令行模式选择要下载的章节范围
  - 自动通过API获取章节信息
  - 通过img.cloudme.one代理下载高质量图片
  - 多线程下载图片，多任务并行下载章节
  - 打包为CBZ文件
  - 自动检测并安装缺失依赖
  - 跨平台兼容 (Windows/macOS/Linux)

命令行参数:
  -o, --output DIR         下载目录
  -m, --mid ID             漫画ID
  -c, --chapters RANGE     章节范围 (如 101-120 或 all)
  --cf TOKEN               cf_clearance cookie
  -p, --proxy URL          HTTP代理 (如 http://127.0.0.1:7890)
  -t, --threads N          图片下载线程数 (1-32, 默认8)
  -j, --jobs N             并行下载章节数 (1-5, 默认5)
  --strip-prefix           去掉标题中 '_' 前的前缀
  -y, --yes                跳过确认直接开始

依赖:
  pip install curl_cffi
"""

import re
import os
import sys
import time
import zipfile
import json
import subprocess
import argparse
import platform
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


# ============================================================
# 跨平台适配
# ============================================================
IS_WINDOWS = platform.system() == "Windows"


def setup_windows_console():
    """Windows 终端 UTF-8 支持"""
    if not IS_WINDOWS:
        return
    try:
        # 启用 Windows 终端 UTF-8 输出
        os.system("")  # 激活 ANSI 转义支持
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def get_user_agent():
    """根据当前系统生成合理的 User-Agent"""
    sys_name = platform.system()
    if sys_name == "Windows":
        return ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36")
    elif sys_name == "Darwin":
        return ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36")
    else:
        return ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36")


def safe_filename(title):
    """将标题转换为当前系统安全的文件名"""
    if IS_WINDOWS:
        # Windows 不允许: \ / : * ? " < > |
        return re.sub(r'[\\/:*?"<>|]', '_', title)
    else:
        # macOS 不允许 : , Linux 仅不允许 / 和 \0
        return re.sub(r'[:/]', '_', title)


def supports_unicode():
    """检测终端是否支持 Unicode 字符"""
    try:
        # 静默检测：尝试编码测试字符串，不实际输出
        "✓✗⚠⊙▼█░".encode(sys.stdout.encoding or "utf-8")
        return True
    except (UnicodeEncodeError, UnicodeDecodeError, LookupError):
        return False


# 初始化终端
setup_windows_console()
HAS_UNICODE = supports_unicode()

# 根据 Unicode 支持情况选择符号
if HAS_UNICODE:
    SYM_OK = "✓"
    SYM_FAIL = "✗"
    SYM_WARN = "⚠"
    SYM_SKIP = "⊙"
    SYM_DOWN = "▼"
    BAR_FILL = "█"
    BAR_EMPTY = "░"
else:
    SYM_OK = "[OK]"
    SYM_FAIL = "[X]"
    SYM_WARN = "[!]"
    SYM_SKIP = "[=]"
    SYM_DOWN = ">>"
    BAR_FILL = "#"
    BAR_EMPTY = "-"


# ============================================================
# 依赖检查与自动安装
# ============================================================
def check_and_install_dependencies():
    """检查所需依赖，缺失时提示并自动安装"""
    # 依赖列表: (导入名, pip包名, 说明)
    dependencies = [
        ("curl_cffi", "curl_cffi", "绕过Cloudflare的HTTP客户端"),
    ]

    missing = []
    for import_name, pip_name, desc in dependencies:
        try:
            __import__(import_name)
        except ImportError:
            missing.append((import_name, pip_name, desc))

    if not missing:
        return True

    print("检测到缺少以下依赖:\n")
    for import_name, pip_name, desc in missing:
        print(f"  - {pip_name}  -- {desc}")
    print()

    choice = input("是否自动安装? (Y/n): ").strip().lower()
    if choice == 'n':
        print(f"  {SYM_FAIL} 缺少依赖，无法继续。请手动安装:")
        for _, pip_name, _ in missing:
            print(f"  pip install {pip_name}")
        return False

    # 逐个安装
    all_ok = True
    for import_name, pip_name, desc in missing:
        print(f"\n正在安装 {pip_name} ...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", pip_name],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0:
                print(f"  {SYM_OK} {pip_name} 安装成功")
            else:
                print(f"  {SYM_FAIL} {pip_name} 安装失败:")
                print(result.stderr.strip()[-300:] if len(result.stderr) > 300 else result.stderr.strip())
                all_ok = False
        except subprocess.TimeoutExpired:
            print(f"  {SYM_FAIL} {pip_name} 安装超时")
            all_ok = False
        except Exception as e:
            print(f"  {SYM_FAIL} {pip_name} 安装出错: {e}")
            all_ok = False

    if all_ok:
        print(f"\n  {SYM_OK} 所有依赖安装完成")
        return True
    else:
        print(f"\n  {SYM_FAIL} 部分依赖安装失败，请手动安装后重试")
        return False


# 在导入第三方库之前先检查依赖
if not check_and_install_dependencies():
    sys.exit(1)

from curl_cffi import requests

# ============================================================
# 配置
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

API_BASE = "https://api-get-v3.mgsearcher.com/api/chapter/getinfo"
MANGA_API = "https://api-get-v3.mgsearcher.com/api/manga/get"
PROXY_BASE = "https://img.cloudme.one/images?url="
CDN_BASE = "https://t40-1-4.g-mh.online"

IMPERSONATE = "chrome136"

USER_AGENT = get_user_agent()

API_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
    "Referer": "https://cloudme.one/",
}

IMG_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Referer": "https://cloudme.one/",
}

COOKIES = {
    "i18n_redirected": "zh",
    # cf_clearance 需要从浏览器获取，详见下方说明
    "cf_clearance": "",
}


# ============================================================
# 工具函数
# ============================================================
def parse_chapter_range(text):
    """
    解析章节范围输入，支持以下格式:
      - 单个章节: 101
      - 范围: 101-120
      - 逗号分隔: 101,103,105
      - 混合: 101-105,108,110-112
    返回排序后的章节号列表
    """
    chapters = set()
    parts = text.replace(' ', '').split(',')
    for part in parts:
        if not part:
            continue
        if '-' in part:
            bounds = part.split('-', 1)
            try:
                start, end = int(bounds[0]), int(bounds[1])
                if start > end:
                    start, end = end, start
                chapters.update(range(start, end + 1))
            except ValueError:
                print(f"  {SYM_WARN} 无法解析范围: {part}")
        else:
            try:
                chapters.add(int(part))
            except ValueError:
                print(f"  {SYM_WARN} 无法解析章节号: {part}")
    return sorted(chapters)


def get_manga_info(mid, session):
    """从API获取漫画全部章节列表"""
    url = f"{MANGA_API}?mid={mid}&mode=all"
    try:
        resp = session.get(url, headers=API_HEADERS, timeout=30, impersonate=IMPERSONATE)
        if resp.status_code != 200:
            return None
        data = resp.json()
        if data.get("code") != 200:
            return None
        return data.get("data", {})
    except Exception as e:
        print(f"  获取漫画信息失败: {e}")
        return None


def get_chapter_images(chapter_id, mid, session):
    """从API获取章节图片URL列表"""
    url = f"{API_BASE}?m={mid}&c={chapter_id}"
    try:
        resp = session.get(url, headers=API_HEADERS, timeout=30, impersonate=IMPERSONATE)
        if resp.status_code != 200:
            print(f"  {SYM_WARN} API返回状态码 {resp.status_code}")
            return None
        data = resp.json()
        if data.get("code") != 200:
            print(f"  {SYM_WARN} API返回错误码 {data.get('code')}")
            return None
        info = data["data"]["info"]
        images = sorted(info["images"]["images"], key=lambda x: x["order"])
        return {
            "title": info.get("title", ""),
            "slug": info.get("slug", ""),
            "order": info.get("order", 0),
            "images": images,
        }
    except Exception as e:
        print(f"  {SYM_WARN} 获取章节信息失败: {e}")
        return None


def download_image(rel_url, session, use_proxy=True, retries=3):
    """下载单张图片，优先通过代理获取高质量版本"""
    cdn_url = f"{CDN_BASE}{rel_url}"

    if use_proxy and COOKIES.get("cf_clearance"):
        proxy_url = f"{PROXY_BASE}{cdn_url}"
        for attempt in range(retries):
            try:
                resp = session.get(
                    proxy_url, headers=IMG_HEADERS, cookies=COOKIES,
                    timeout=30, impersonate=IMPERSONATE
                )
                if resp.status_code == 200 and len(resp.content) > 1000:
                    return resp.content
                elif resp.status_code == 403:
                    break  # Cloudflare拦截，回退到CDN
                if attempt < retries - 1:
                    time.sleep(1)
            except Exception:
                if attempt < retries - 1:
                    time.sleep(1)

    # CDN直连（低质量但无需Cloudflare）
    for attempt in range(retries):
        try:
            resp = session.get(
                cdn_url, headers=IMG_HEADERS, timeout=30, impersonate=IMPERSONATE
            )
            if resp.status_code == 200:
                return resp.content
            if attempt < retries - 1:
                time.sleep(1)
        except Exception:
            if attempt < retries - 1:
                time.sleep(1)

    return None


def strip_title_prefix(title):
    """去掉标题中 '_' 前的前缀部分，例如 '某漫画_第101话' → '第101话'"""
    _, _, suffix = title.partition('_')
    return suffix if suffix else title


def create_cbz(title, images, session, output_dir, strip_prefix=False, max_workers=8):
    """下载图片并创建CBZ文件，返回(True, 文件路径) 或 (False, 错误信息)"""
    display_title = strip_title_prefix(title) if strip_prefix else title
    safe_title = safe_filename(display_title)
    cbz_filename = f"{safe_title}.cbz"
    cbz_path = os.path.join(output_dir, cbz_filename)

    if os.path.exists(cbz_path):
        print(f"  {SYM_SKIP} 已存在，跳过: {cbz_filename}")
        return True, cbz_path

    total = len(images)
    print(f"  {SYM_DOWN} 下载中: {cbz_filename} ({total} 张图片, {max_workers} 线程)")

    # 多线程下载
    downloaded = {}
    failed = 0
    completed = 0
    lock = threading.Lock()

    def _download_one(idx, img_url):
        nonlocal failed, completed
        data = download_image(img_url, session)
        with lock:
            if data:
                downloaded[idx] = data
            else:
                failed += 1
            completed += 1
            # 进度显示
            bar_len = 30
            filled = int(bar_len * completed / total)
            bar = BAR_FILL * filled + BAR_EMPTY * (bar_len - filled)
            pct = completed * 100 / total
            sys.stdout.write(f"\r  [{bar}] {pct:.0f}% ({completed}/{total})")
            sys.stdout.flush()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i, img in enumerate(images):
            futures.append(executor.submit(_download_one, i, img["url"]))
        for f in as_completed(futures):
            pass  # 结果已在 _download_one 中处理

    print()  # 换行

    if not downloaded:
        return False, "未能下载任何图片"

    # 按序号排序后创建CBZ
    sorted_items = sorted(downloaded.items(), key=lambda x: x[0])
    with zipfile.ZipFile(cbz_path, 'w', zipfile.ZIP_STORED) as zf:
        for idx, data in sorted_items:
            ext = ".webp"
            if data[:4] == b'\x89PNG':
                ext = ".png"
            elif data[:2] == b'\xff\xd8':
                ext = ".jpg"
            elif data[:4] == b'RIFF':
                ext = ".webp"
            zf.writestr(f"{idx + 1:03d}{ext}", data)

    file_size = os.path.getsize(cbz_path)
    size_str = f"{file_size / 1024:.0f} KB" if file_size < 1024 * 1024 else f"{file_size / 1024 / 1024:.1f} MB"
    print(f"  {SYM_OK} 完成: {cbz_filename} ({size_str}, {len(downloaded)}/{total} 张)")
    if failed:
        print(f"  {SYM_WARN} {failed} 张图片下载失败")
    return True, cbz_path


def _process_chapter(order, ch, mid, session, output_dir, strip_prefix, max_workers):
    """处理单个章节：获取信息 + 下载图片 + 打包CBZ"""
    chapter_info = get_chapter_images(ch["id"], mid, session)
    if not chapter_info:
        return order, False, "获取章节信息失败"

    title = chapter_info["title"] or ch["title"]
    ok, result = create_cbz(title, chapter_info["images"], session, output_dir, strip_prefix, max_workers)
    if ok:
        if "已存在" in str(result):
            return order, True, "skipped"
        return order, True, result
    return order, False, result


# ============================================================
# 交互流程
# ============================================================
def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="cloudme.one 漫画章节下载工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-o", "--output", default=None, help="下载目录")
    parser.add_argument("-m", "--mid", default=None, help="漫画ID (如 cloudme.one/refs/10 中的 10)")
    parser.add_argument("-c", "--chapters", default=None, help="章节范围 (如 101-120, 101,103,105, all)")
    parser.add_argument("--cf", default=None, help="cf_clearance cookie (用于高质量图片)")
    parser.add_argument("-p", "--proxy", default=None, help="HTTP代理 (如 http://127.0.0.1:7890)")
    parser.add_argument("-t", "--threads", type=int, default=None, help="图片下载线程数 (1-32, 默认8)")
    parser.add_argument("-j", "--jobs", type=int, default=None, help="并行下载章节数 (1-5, 默认5)")
    parser.add_argument("--strip-prefix", action="store_true", default=False, help="去掉标题中 '_' 前的前缀")
    parser.add_argument("-y", "--yes", action="store_true", default=False, help="跳过确认直接开始下载")
    args = parser.parse_args()

    # 判断是否为非交互模式 (所有必要参数都已通过命令行提供)
    non_interactive = all([
        args.output,
        args.mid,
        args.chapters is not None,
    ])

    print("=" * 56)
    print("   cloudme.one 漫画章节下载工具")
    print("=" * 56)
    print()

    session = requests.Session()

    # ==================== 下载目录 ====================
    if args.output:
        output_dir = args.output
        if non_interactive:
            print(f"  {SYM_OK} 下载目录: {os.path.abspath(output_dir)}")
        else:
            print(f"  命令行指定: {os.path.abspath(output_dir)}")
            dir_input = input("  输入新路径可修改，回车确认: ").strip()
            if dir_input:
                dir_input = dir_input.strip('"').strip("'")
                dir_input = os.path.expanduser(dir_input)
                output_dir = dir_input
    else:
        print("【下载目录】")
        print("  请输入下载目录路径 (CBZ文件将保存到此目录)")
        dir_input = input("  下载目录: ").strip()
        if dir_input:
            dir_input = dir_input.strip('"').strip("'")
            dir_input = os.path.expanduser(dir_input)
        output_dir = dir_input

    if not output_dir:
        print(f"  {SYM_FAIL} 未指定下载目录")
        return

    try:
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        print(f"  {SYM_FAIL} 目录无效: {e}")
        return
    if not args.output or not non_interactive:
        print(f"  {SYM_OK} 下载目录: {output_dir}")

    # ==================== 代理设置 ====================
    if args.proxy:
        proxy_url = args.proxy
        if non_interactive:
            print(f"  {SYM_OK} 代理: {proxy_url}")
        else:
            print(f"\n【代理设置】命令行指定: {proxy_url}")
            proxy_input = input("  输入新代理可修改，直接回车确认: ").strip()
            if proxy_input:
                proxy_url = proxy_input
    else:
        if non_interactive:
            proxy_url = None
        else:
            print(f"\n【代理设置】(可选)")
            print("  格式: http://host:port 或 socks5://host:port")
            proxy_input = input("  代理地址 (直接回车跳过): ").strip()
            proxy_url = proxy_input or None

    if proxy_url:
        session.proxies = {"http": proxy_url, "https": proxy_url}
        if not args.proxy or not non_interactive:
            print(f"  {SYM_OK} 已设置代理: {proxy_url}")
    else:
        if not non_interactive:
            print(f"  {SYM_SKIP} 不使用代理")

    # ==================== 线程设置 ====================
    max_workers = 8
    if args.threads is not None:
        if 1 <= args.threads <= 32:
            max_workers = args.threads
        else:
            print(f"  {SYM_WARN} 线程数需在 1-32 之间，使用默认 8")
    elif not non_interactive:
        print(f"\n【下载线程】")
        print(f"  当前: {max_workers} 线程")
        thread_input = input("  是否设置更多线程? (1-32, 回车保持默认): ").strip()
        if thread_input:
            try:
                t = int(thread_input)
                if 1 <= t <= 32:
                    max_workers = t
                    print(f"  {SYM_OK} 设置为 {max_workers} 线程")
                else:
                    print(f"  {SYM_WARN} 线程数需在 1-32 之间，使用默认 {max_workers} 线程")
            except ValueError:
                print(f"  {SYM_WARN} 无效输入，使用默认 {max_workers} 线程")
    if non_interactive:
        print(f"  {SYM_OK} 下载线程: {max_workers}")

    # ==================== 并行任务数 ====================
    max_jobs = 5
    if args.jobs is not None:
        if 1 <= args.jobs <= 5:
            max_jobs = args.jobs
        else:
            print(f"  {SYM_WARN} 并行任务数需在 1-5 之间，使用默认 5")
    elif not non_interactive:
        print(f"\n【并行任务】")
        print(f"  当前: {max_jobs} 个章节同时下载")
        jobs_input = input("  设置并行任务数 (1-5, 回车保持默认): ").strip()
        if jobs_input:
            try:
                j = int(jobs_input)
                if 1 <= j <= 5:
                    max_jobs = j
                    print(f"  {SYM_OK} 设置为 {max_jobs} 个并行任务")
                else:
                    print(f"  {SYM_WARN} 并行任务数需在 1-5 之间，使用默认 {max_jobs}")
            except ValueError:
                print(f"  {SYM_WARN} 无效输入，使用默认 {max_jobs}")
    if non_interactive:
        print(f"  {SYM_OK} 并行任务: {max_jobs}")

    # ==================== 漫画ID ====================
    if args.mid:
        mid = args.mid
        if non_interactive:
            print(f"  {SYM_OK} 漫画ID: {mid}")
        else:
            print(f"\n【漫画ID】命令行指定: {mid}")
            mid_input = input("  输入新ID可修改，回车确认: ").strip()
            if mid_input:
                mid = mid_input
    else:
        print("\n【漫画ID】")
        print("  提示: 漫画ID是网站URL中的数字，例如 cloudme.one/refs/10 中的 10")
        mid = input("  漫画ID: ").strip()
        if not mid:
            print(f"  {SYM_FAIL} 未输入漫画ID")
            return

    # ==================== 获取漫画信息 ====================
    print(f"\n  获取漫画信息 (ID: {mid}) ...")
    manga = get_manga_info(mid, session)
    if not manga:
        print(f"  {SYM_FAIL} 无法获取漫画信息，请检查ID是否正确")
        return

    manga_title = manga.get("title", "未知漫画")
    print(f"  漫画标题: {manga_title}")

    # 提取章节列表
    chapters_raw = manga.get("chapters", [])
    if not chapters_raw:
        print(f"  {SYM_FAIL} 未找到章节列表")
        return

    # 构建章节映射: {序号: {id, title}}
    chapter_map = {}
    for ch in chapters_raw:
        attrs = ch.get("attributes", {})
        ch_id = ch.get("id", "")
        ch_order = attrs.get("order", 0)
        ch_title = attrs.get("title", "")
        if ch_id and ch_order:
            chapter_map[ch_order] = {
                "id": str(ch_id),
                "title": ch_title or f"第{ch_order}话",
            }

    if not chapter_map:
        print(f"  {SYM_FAIL} 章节列表为空")
        return

    sorted_orders = sorted(chapter_map.keys())
    print(f"  共 {len(chapter_map)} 章，范围: {sorted_orders[0]} - {sorted_orders[-1]}")

    # ==================== 前缀处理 ====================
    strip_prefix = args.strip_prefix
    if not non_interactive:
        sample_titles = [chapter_map[o]['title'] for o in sorted_orders[:5]]
        print(f"\n【前缀处理】")
        print("  章节标题示例:")
        for t in sample_titles:
            if '_' in t:
                prefix, _, suffix = t.partition('_')
                print(f"    {t}  (前缀: {prefix})")
            else:
                print(f"    {t}")
        print("  前缀格式: '_' 前的名称，去掉后保留 '_' 后的部分")
        print("  示例: '某漫画_第101话' → '第101话'")
        if strip_prefix:
            print(f"  命令行指定: 去掉前缀")
            prefix_input = input("  是否修改? (输入 n 保留完整标题，回车确认): ").strip().lower()
            if prefix_input == 'n':
                strip_prefix = False
                print(f"  {SYM_SKIP} 保留完整标题")
            else:
                print(f"  {SYM_OK} 将去掉前缀 (保留 '_' 后的部分)")
        else:
            prefix_choice = input("  是否去掉标题中 '_' 前的前缀? (y/N): ").strip().lower()
            if prefix_choice == 'y':
                strip_prefix = True
                print(f"  {SYM_OK} 将去掉前缀 (保留 '_' 后的部分)")
            else:
                print(f"  {SYM_SKIP} 保留完整标题")
    elif strip_prefix:
        print(f"  {SYM_OK} 去掉标题前缀")

    # ==================== Cloudflare Cookie ====================
    if args.cf:
        COOKIES["cf_clearance"] = args.cf
        if non_interactive:
            print(f"  {SYM_OK} cf_clearance: 已设置")
        else:
            print(f"\n【Cloudflare Cookie】命令行已指定")
            cf_input = input("  输入新cookie可修改，直接回车确认: ").strip()
            if cf_input:
                COOKIES["cf_clearance"] = cf_input
                print(f"  {SYM_OK} 已更新 cf_clearance")
    else:
        if non_interactive:
            pass  # 非交互模式未提供则静默跳过
        else:
            print(f"\n【Cloudflare Cookie】(可选)")
            print("  说明: 提供 cf_clearance cookie 可下载高质量图片，否则只能下载低质量版本")
            print("  获取方法: 浏览器打开 cloudme.one -> F12 -> Application -> Cookies -> cf_clearance")
            cf_input = input("  cf_clearance (直接回车跳过): ").strip()
            if cf_input:
                COOKIES["cf_clearance"] = cf_input
                print(f"  {SYM_OK} 已设置 cf_clearance")
            elif COOKIES.get("cf_clearance"):
                print(f"  {SYM_OK} 使用脚本内置的 cf_clearance")
            else:
                print(f"  {SYM_SKIP} 未设置 cf_clearance，将使用CDN直连（低质量）")

    # ==================== 选择章节 ====================
    if args.chapters is not None:
        if args.chapters.lower() == 'all':
            selected_orders = sorted_orders
        else:
            selected_orders = parse_chapter_range(args.chapters)
        if non_interactive:
            pass  # 静默
        else:
            print(f"\n【章节范围】命令行指定: {args.chapters}")
            range_input = input("  输入新范围可修改，回车确认: ").strip()
            if range_input:
                if range_input.lower() == 'all':
                    selected_orders = sorted_orders
                else:
                    selected_orders = parse_chapter_range(range_input)
    else:
        print(f"\n【选择章节】")
        print(f"  可用范围: {sorted_orders[0]} - {sorted_orders[-1]}")
        print("  输入格式: 101 | 101-120 | 101,103,105 | all")
        range_input = input(f"  要下载的章节 (默认 all): ").strip()
        if not range_input or range_input.lower() == 'all':
            selected_orders = sorted_orders
        else:
            selected_orders = parse_chapter_range(range_input)

    # 过滤掉不存在的章节
    valid_orders = [o for o in selected_orders if o in chapter_map]
    invalid_orders = [o for o in selected_orders if o not in chapter_map]
    if invalid_orders:
        print(f"  {SYM_WARN} 以下章节不存在: {', '.join(map(str, invalid_orders))}")
    if not valid_orders:
        print(f"  {SYM_FAIL} 没有有效的章节可下载")
        return

    # ==================== 确认 ====================
    print(f"\n{'=' * 56}")
    print(f"  漫画: {manga_title} (ID: {mid})")
    print(f"  章节: {valid_orders[0]}-{valid_orders[-1]}" if len(valid_orders) > 1 else f"  章节: {valid_orders[0]}")
    print(f"  数量: {len(valid_orders)} 章")
    print(f"  保存到: {os.path.abspath(output_dir)}")
    print(f"  图片质量: {'高质量 (代理)' if COOKIES.get('cf_clearance') else '低质量 (CDN直连)'}")
    print(f"  网络代理: {proxy_url or '无'}")
    print(f"  下载线程: {max_workers}")
    print(f"  并行任务: {max_jobs}")
    print(f"  标题前缀: {'去掉' if strip_prefix else '保留完整标题'}")

    if not args.yes or not non_interactive:
        confirm = input("\n  开始下载? (Y/n): ").strip().lower()
        if confirm == 'n':
            print("  已取消")
            return

    # ==================== 下载 ====================
    print(f"\n{'=' * 56}")
    print(f"  开始下载... (并行任务: {max_jobs})")
    print(f"{'=' * 56}")

    success = 0
    fail = 0
    skipped = 0
    result_lock = threading.Lock()

    def _on_chapter_done(future):
        nonlocal success, fail, skipped
        order, ok, result = future.result()
        with result_lock:
            if ok:
                if result == "skipped":
                    skipped += 1
                else:
                    success += 1
            else:
                fail += 1

    with ThreadPoolExecutor(max_workers=max_jobs) as job_executor:
        futures = []
        for i, order in enumerate(valid_orders):
            ch = chapter_map[order]
            print(f"\n[排队] 第{order}话: {ch['title']} (ID: {ch['id']})")
            f = job_executor.submit(
                _process_chapter, order, ch, mid, session, output_dir,
                strip_prefix, max_workers
            )
            f.add_done_callback(_on_chapter_done)
            futures.append(f)

        # 等待所有任务完成
        for f in as_completed(futures):
            try:
                f.result()  # 触发异常（如果有）
            except Exception as e:
                print(f"  {SYM_FAIL} 任务异常: {e}")

    # ==================== 结果 ====================
    print(f"\n{'=' * 56}")
    print(f"  下载完成!")
    print(f"  成功: {success}  跳过: {skipped}  失败: {fail}")
    print(f"  文件保存在: {os.path.abspath(output_dir)}")
    print(f"{'=' * 56}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  已中断")
    except Exception as e:
        print(f"\n  发生错误: {e}")
        import traceback
        traceback.print_exc()
