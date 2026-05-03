"""
cloudme.one 漫画章节下载工具

用法:
  python download_cbz_interactive.py                    # 交互模式
  python download_cbz_interactive.py -o D:\\Comics       # 指定下载目录 (Windows)
  python download_cbz_interactive.py -o ~/Comics        # 指定下载目录 (macOS/Linux)
  python download_cbz_interactive.py --output ./comics  # 同上

支持系统: Windows / macOS / Linux

功能:
  - 交互式选择要下载的章节范围
  - 自动通过API获取章节信息
  - 通过img.cloudme.one代理下载高质量图片
  - 打包为CBZ文件
  - 支持命令行指定下载目录
  - 自动检测并安装缺失依赖
  - 跨平台兼容 (Windows/macOS/Linux)

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


def create_cbz(title, images, session, output_dir, strip_prefix=False):
    """下载图片并创建CBZ文件，返回(True, 文件路径) 或 (False, 错误信息)"""
    display_title = strip_title_prefix(title) if strip_prefix else title
    safe_title = safe_filename(display_title)
    cbz_filename = f"{safe_title}.cbz"
    cbz_path = os.path.join(output_dir, cbz_filename)

    if os.path.exists(cbz_path):
        print(f"  {SYM_SKIP} 已存在，跳过: {cbz_filename}")
        return True, cbz_path

    print(f"  {SYM_DOWN} 下载中: {cbz_filename} ({len(images)} 张图片)")

    downloaded = []
    failed = 0
    for i, img in enumerate(images):
        data = download_image(img["url"], session)
        if data:
            downloaded.append((i, data))
        else:
            failed += 1

        # 进度显示
        progress = i + 1
        if progress % 10 == 0 or progress == len(images):
            bar_len = 30
            filled = int(bar_len * progress / len(images))
            bar = BAR_FILL * filled + BAR_EMPTY * (bar_len - filled)
            pct = progress * 100 / len(images)
            sys.stdout.write(f"\r  [{bar}] {pct:.0f}% ({progress}/{len(images)})")
            sys.stdout.flush()

        # 每10张图暂停一下，避免过快请求
        if progress % 10 == 0 and progress < len(images):
            time.sleep(0.3)

    print()  # 换行

    if not downloaded:
        return False, "未能下载任何图片"

    # 创建CBZ
    with zipfile.ZipFile(cbz_path, 'w', zipfile.ZIP_STORED) as zf:
        for idx, data in downloaded:
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
    print(f"  {SYM_OK} 完成: {cbz_filename} ({size_str}, {len(downloaded)}/{len(images)} 张)")
    if failed:
        print(f"  {SYM_WARN} {failed} 张图片下载失败")
    return True, cbz_path


# ============================================================
# 交互流程
# ============================================================
def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="cloudme.one 漫画章节下载工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-o", "--output", default=None,
        help="指定下载目录 (交互模式下会要求输入)"
    )
    args = parser.parse_args()

    print("=" * 56)
    print("   cloudme.one 漫画章节下载工具")
    print("=" * 56)
    print()

    session = requests.Session()

    # --- 第0步: 确认下载目录 ---
    print("【下载目录】")
    if args.output:
        output_dir = args.output
        print(f"  命令行指定: {os.path.abspath(output_dir)}")
        dir_input = input(f"  输入新路径可修改，回车确认: ").strip()
    else:
        print("  请输入下载目录路径 (CBZ文件将保存到此目录)")
        dir_input = input("  下载目录: ").strip()

    if dir_input:
        dir_input = dir_input.strip('"').strip("'")
        dir_input = os.path.expanduser(dir_input)
        output_dir = dir_input

    # 校验路径
    if not output_dir:
        print(f"  {SYM_FAIL} 未指定下载目录")
        return

    try:
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        print(f"  {SYM_FAIL} 目录无效: {e}")
        return
    print(f"  {SYM_OK} 下载目录: {output_dir}")

    # --- 第1步: 输入漫画ID ---
    print("【第1步】输入漫画ID")
    print("  提示: 漫画ID是网站URL中的数字，例如 cloudme.one/refs/10 中的 10")
    mid = input("  漫画ID (默认 10): ").strip()
    if not mid:
        mid = "10"

    # --- 第2步: 获取漫画信息 ---
    print(f"\n【第2步】获取漫画信息 (ID: {mid}) ...")
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
    print(f"  最新: {chapter_map[sorted_orders[-1]]['title']}")

    # --- 第2.5步: 是否去掉标题前缀 ---
    strip_prefix = False
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
    prefix_choice = input("  是否去掉标题中 '_' 前的前缀? (y/N): ").strip().lower()
    if prefix_choice == 'y':
        strip_prefix = True
        print(f"  {SYM_OK} 将去掉前缀 (保留 '_' 后的部分)")
    else:
        print(f"  {SYM_SKIP} 保留完整标题")

    # --- 第3步: 配置Cloudflare Cookie ---
    print(f"\n【第3步】Cloudflare Cookie (可选)")
    print("  说明: 提供 cf_clearance cookie 可下载高质量图片，否则只能下载低质量版本")
    print("  获取方法: 在浏览器中打开 cloudme.one -> F12 -> Application -> Cookies -> cf_clearance")
    cf_input = input("  cf_clearance (直接回车跳过): ").strip()
    if cf_input:
        COOKIES["cf_clearance"] = cf_input
        print(f"  {SYM_OK} 已设置 cf_clearance")
    elif COOKIES.get("cf_clearance"):
        print(f"  {SYM_OK} 使用脚本内置的 cf_clearance")
    else:
        print(f"  {SYM_SKIP} 未设置 cf_clearance，将使用CDN直连（低质量）")

    # --- 第4步: 选择章节 ---
    print(f"\n【第4步】选择要下载的章节")
    print(f"  可用范围: {sorted_orders[0]} - {sorted_orders[-1]}")
    print("  输入格式示例:")
    print("    单章: 101")
    print("    范围: 101-120")
    print("    多个: 101,103,105")
    print("    混合: 101-105,108,110-112")
    print("    全部: all")
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

    print(f"  将下载 {len(valid_orders)} 个章节")

    # --- 第5步: 确认 ---
    print(f"\n【确认】")
    print(f"  漫画: {manga_title} (ID: {mid})")
    print(f"  章节: {valid_orders[0]}-{valid_orders[-1]}" if len(valid_orders) > 1 else f"  章节: {valid_orders[0]}")
    print(f"  数量: {len(valid_orders)} 章")
    print(f"  保存到: {os.path.abspath(output_dir)}")
    print(f"  图片质量: {'高质量 (代理)' if COOKIES.get('cf_clearance') else '低质量 (CDN直连)'}")
    print(f"  标题前缀: {'去掉' if strip_prefix else '保留完整标题'}")
    confirm = input("\n  开始下载? (Y/n): ").strip().lower()
    if confirm == 'n':
        print("  已取消")
        return

    # --- 第6步: 下载 ---
    print(f"\n{'=' * 56}")
    print("  开始下载...")
    print(f"{'=' * 56}")

    success = 0
    fail = 0
    skipped = 0

    for i, order in enumerate(valid_orders):
        ch = chapter_map[order]
        print(f"\n[{i+1}/{len(valid_orders)}] 第{order}话: {ch['title']} (ID: {ch['id']})")

        chapter_info = get_chapter_images(ch["id"], mid, session)
        if not chapter_info:
            print(f"  {SYM_FAIL} 获取章节信息失败")
            fail += 1
            continue

        # 用API返回的标题（更准确）
        title = chapter_info["title"] or ch["title"]
        ok, result = create_cbz(title, chapter_info["images"], session, output_dir, strip_prefix)
        if ok:
            if "已存在" in str(result):
                skipped += 1
            else:
                success += 1
        else:
            fail += 1

        # 章节间暂停
        if i < len(valid_orders) - 1:
            time.sleep(1)

    # --- 结果 ---
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
