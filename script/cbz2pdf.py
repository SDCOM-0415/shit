"""
CBZ 转 PDF 转换工具

将 CBZ (漫画档案) 文件转换为 PDF 格式，支持单文件或批量转换。

用法:
  # 交互模式
  python cbz2pdf.py

  # 非交互模式 (提供所有必要参数后直接开始转换)
  python cbz2pdf.py -i "D:\\Comics\\第101话.cbz" -o "D:\\PDF"
  python cbz2pdf.py -i "D:\\Comics" -o "D:\\PDF" --keep-name
  python cbz2pdf.py -i "D:\\Comics" -o "D:\\PDF" --name-format "{index:03d}_{name}"
  python cbz2pdf.py -i "D:\\Comics" -o "D:\\PDF" -y

支持系统: Windows / macOS / Linux

功能:
  - CBZ 文件转 PDF (单文件或整个文件夹)
  - 自动检测并安装缺失依赖
  - 保留原文件名或自定义命名格式
  - 指定输出目录
  - 多线程并行转换
  - 跨平台兼容 (Windows/macOS/Linux)

命令行参数:
  -i, --input PATH         输入: CBZ文件或包含CBZ的文件夹
  -o, --output DIR         输出目录
  --keep-name              保留原文件名 (默认行为)
  --name-format FMT        自定义文件名格式 (可用: {name}, {index}, {date})
  -j, --jobs N             并行转换数 (1-8, 默认4)
  -y, --yes                跳过确认直接开始

依赖:
  pip install Pillow
"""

import re
import os
import sys
import zipfile
import argparse
import platform
import subprocess
import threading
import importlib
from io import BytesIO
from datetime import datetime
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
        os.system("")  # 激活 ANSI 转义支持
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def safe_filename(title):
    """将标题转换为当前系统安全的文件名"""
    if IS_WINDOWS:
        return re.sub(r'[\\/:*?"<>|]', '_', title)
    else:
        return re.sub(r'[:/]', '_', title)


def supports_unicode():
    """检测终端是否支持 Unicode 字符"""
    try:
        "✓✗⚠⊙▼█░".encode(sys.stdout.encoding or "utf-8")
        return True
    except (UnicodeEncodeError, UnicodeDecodeError, LookupError):
        return False


# 初始化终端
setup_windows_console()
HAS_UNICODE = supports_unicode()

if HAS_UNICODE:
    SYM_OK = "✓"
    SYM_FAIL = "✗"
    SYM_WARN = "⚠"
    SYM_SKIP = "⊙"
    BAR_FILL = "█"
    BAR_EMPTY = "░"
else:
    SYM_OK = "[OK]"
    SYM_FAIL = "[X]"
    SYM_WARN = "[!]"
    SYM_SKIP = "[=]"
    BAR_FILL = "#"
    BAR_EMPTY = "-"


# ============================================================
# 依赖检查与自动安装
# ============================================================
def check_and_install_dependencies():
    """检查所需依赖，缺失时提示并自动安装"""
    dependencies = [
        ("PIL", "Pillow", "图片处理与PDF生成"),
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
                stderr = result.stderr.strip()
                print(stderr[-300:] if len(stderr) > 300 else stderr)
                all_ok = False
        except subprocess.TimeoutExpired:
            print(f"  {SYM_FAIL} {pip_name} 安装超时")
            all_ok = False
        except Exception as e:
            print(f"  {SYM_FAIL} {pip_name} 安装出错: {e}")
            all_ok = False

    if all_ok:
        print(f"\n  {SYM_OK} 所有依赖安装完成")
        # 安装后验证能否实际导入
        for import_name, pip_name, _ in missing:
            try:
                importlib.import_module(import_name)
            except ImportError:
                print(f"  {SYM_WARN} {pip_name} 已安装但无法导入，可能需要重启脚本")
                print(f"  请尝试: {sys.executable} {os.path.abspath(sys.argv[0])}")
                all_ok = False
                break
    else:
        print(f"\n  {SYM_FAIL} 部分依赖安装失败，请手动安装后重试")

    return all_ok


# 在导入第三方库之前先检查依赖
if not check_and_install_dependencies():
    sys.exit(1)

# 动态导入: 安装后 importlib 可立即加载，无需重启脚本
Image = importlib.import_module("PIL.Image")


# ============================================================
# 核心转换逻辑
# ============================================================
def collect_cbz_files(path):
    """
    收集 CBZ 文件列表
    - 如果 path 是文件: 返回 [path]
    - 如果 path 是目录: 返回目录下所有 .cbz 文件 (递归)
    """
    path = os.path.abspath(path)

    if os.path.isfile(path):
        if path.lower().endswith('.cbz'):
            return [path]
        else:
            print(f"  {SYM_FAIL} 不是 CBZ 文件: {path}")
            return []

    if os.path.isdir(path):
        cbz_files = []
        for root, dirs, files in os.walk(path):
            for f in sorted(files):
                if f.lower().endswith('.cbz'):
                    cbz_files.append(os.path.join(root, f))
        return cbz_files

    print(f"  {SYM_FAIL} 路径不存在: {path}")
    return []


def clean_path(path_str):
    """清理用户输入的路径字符串
    - 去除首尾引号
    - 展开波浪号 (~)
    - 去除 shell 转义反斜杠 (如 'folder\\ name' → 'folder name')
    """
    path_str = path_str.strip()
    path_str = path_str.strip('"').strip("'")
    path_str = os.path.expanduser(path_str)
    # 去除 shell 转义: \空格 → 空格, \换行 → 忽略
    path_str = path_str.replace('\\ ', ' ')
    return path_str



    """
    将单个 CBZ 文件转换为 PDF (无页边距，图片尺寸即页面尺寸)
    直接构建 PDF 二进制流，每页 MediaBox 精确等于图片尺寸，零边距
    返回 (True, output_path) 或 (False, error_message)
    """
    try:
        with zipfile.ZipFile(cbz_path, 'r') as zf:
            # 获取所有图片文件并按名称排序
            image_names = sorted([
                n for n in zf.namelist()
                if not n.endswith('/') and
                n.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'))
            ])

            if not image_names:
                return False, "CBZ 中未找到图片文件"

            # 解码所有图片
            # 对于原始 JPEG + RGB 图片，直接透传原始数据避免重复编码伪影
            pages = []  # [(width, height, jpeg_bytes), ...]
            for name in image_names:
                try:
                    data = zf.read(name)
                    img = Image.open(BytesIO(data))
                    w, h = img.size

                    is_jpeg = name.lower().endswith(('.jpg', '.jpeg'))
                    needs_reencode = False

                    # 非 RGB 模式必须转换
                    if img.mode != 'RGB':
                        needs_reencode = True
                        img = img.convert('RGB')

                    # 检查 EXIF 方向标签，非默认方向需要重新编码
                    if not needs_reencode and is_jpeg:
                        try:
                            from PIL.ExifTags import Base as ExifBase
                            exif = img.getexif()
                            if exif and exif.get(ExifBase.Orientation, 1) != 1:
                                needs_reencode = True
                        except Exception:
                            pass

                    if is_jpeg and not needs_reencode:
                        # 原始 JPEG + RGB + 无方向修正 → 直接透传，零质量损失
                        jpeg_data = data
                    else:
                        # 非 JPEG 或需转换 → 编码为 JPEG
                        buf = BytesIO()
                        img.save(buf, format='JPEG', quality=95)
                        jpeg_data = buf.getvalue()

                    img.close()
                    pages.append((w, h, jpeg_data))
                except Exception:
                    continue

            if not pages:
                return False, "所有图片均无法读取"

            # 直接构建 PDF 二进制 (零边距 + 出血防白边)
            pdf_bytes = _build_pdf(pages)
            with open(output_path, 'wb') as f:
                f.write(pdf_bytes)

            return True, output_path

    except zipfile.BadZipFile:
        return False, "无效的 ZIP/CBZ 文件"
    except Exception as e:
        return False, str(e)


def _build_pdf(pages):
    """
    直接构建 PDF 二进制流，零边距
    pages: [(width_px, height_px, jpeg_bytes), ...]
    每页 MediaBox 精确等于图片像素尺寸 (72 DPI)，无任何页边距
    使用出血(bleed)技术：图片向外扩展 1pt，CropBox 裁切，消除抗锯齿白边
    """
    DPI = 72.0
    BLEED = 1  # 出血量（点），图片向外扩展，确保边缘无白边
    total_pages = len(pages)

    # 预计算对象编号，避免使用占位符
    # 对象顺序: N个图片 + N个内容流 + N个页面对象 + Pages + Catalog
    pages_id = 3 * total_pages + 1   # Pages 节点对象编号
    catalog_id = pages_id + 1        # Catalog 对象编号

    pdf_parts = []
    offsets = []
    obj_num = 0

    # PDF 文件头 (必须，阅读器靠此识别文件格式)
    pdf_parts.append(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")

    def write_obj(content_bytes):
        """写入一个 PDF 对象，返回对象编号"""
        nonlocal obj_num
        obj_num += 1
        offset = sum(len(p) for p in pdf_parts)
        offsets.append(offset)
        header = f"{obj_num} 0 obj\n".encode('latin-1')
        tail = b"\nendobj\n"
        pdf_parts.append(header + content_bytes + tail)
        return obj_num

    img_ids = []
    stream_ids = []
    page_ids = []

    # 1. 写入图片 XObject
    for w_px, h_px, jpeg_data in pages:
        header = (
            f"<< /Type /XObject /Subtype /Image "
            f"/Width {w_px} /Height {h_px} "
            f"/ColorSpace /DeviceRGB /BitsPerComponent 8 "
            f"/Filter /DCTDecode /Length {len(jpeg_data)} >>"
            f"\nstream\n"
        ).encode('latin-1')
        img_id = write_obj(header + jpeg_data + b"\nendstream")
        img_ids.append(img_id)

    # 2. 写入每页的 Content Stream (绘制图片指令)
    #    使用出血技术：图片从 (-BLEED, -BLEED) 绘制到 (w_pt+BLEED, h_pt+BLEED)
    #    CropBox 裁切为 [0 0 w_pt h_pt]，确保边缘无白边
    for i in range(total_pages):
        w_px, h_px, _ = pages[i]
        w_pt = int(w_px / DPI * 72)  # DPI=72 时 w_pt == w_px
        h_pt = int(h_px / DPI * 72)
        stream = (
            f"q\n"
            f"{w_pt + 2 * BLEED} 0 0 {h_pt + 2 * BLEED} {-BLEED} {-BLEED} cm\n"
            f"/Im0 Do\nQ\n"
        ).encode('latin-1')
        stream_header = f"<< /Length {len(stream)} >>\nstream\n".encode('latin-1')
        s_id = write_obj(stream_header + stream + b"\nendstream")
        stream_ids.append(s_id)

    # 3. 写入 Page 对象 (直接使用预计算的 pages_id，无需占位符)
    #    添加 CropBox = MediaBox，确保阅读器裁切区域精确
    for i in range(total_pages):
        w_px, h_px, _ = pages[i]
        w_pt = int(w_px / DPI * 72)
        h_pt = int(h_px / DPI * 72)
        page = (
            f"<< /Type /Page "
            f"/Parent {pages_id} 0 R "
            f"/MediaBox [0 0 {w_pt} {h_pt}] "
            f"/CropBox [0 0 {w_pt} {h_pt}] "
            f"/Contents {stream_ids[i]} 0 R "
            f"/Resources << /XObject << /Im0 {img_ids[i]} 0 R >> >> >>"
        ).encode('latin-1')
        p_id = write_obj(page)
        page_ids.append(p_id)

    # 4. Pages 对象
    kids = " ".join(f"{pid} 0 R" for pid in page_ids)
    pages_obj = f"<< /Type /Pages /Kids [{kids}] /Count {total_pages} >>".encode('latin-1')
    pages_offset = sum(len(p) for p in pdf_parts)
    offsets.append(pages_offset)
    pdf_parts.append(f"{pages_id} 0 obj\n".encode('latin-1') + pages_obj + b"\nendobj\n")

    # 5. Catalog 对象
    catalog_offset = sum(len(p) for p in pdf_parts)
    offsets.append(catalog_offset)
    catalog_obj = f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode('latin-1')
    pdf_parts.append(f"{catalog_id} 0 obj\n".encode('latin-1') + catalog_obj + b"\nendobj\n")

    # 6. Cross-reference table
    xref_offset = sum(len(p) for p in pdf_parts)
    xref = b"xref\n"
    xref += f"0 {catalog_id + 1}\n".encode('latin-1')
    xref += b"0000000000 65535 f \n"
    for off in offsets:
        xref += f"{off:010d} 00000 n \n".encode('latin-1')
    pdf_parts.append(xref)

    # 7. Trailer
    trailer = (
        f"trailer\n<< /Size {catalog_id + 1} /Root {catalog_id} 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n"
    ).encode('latin-1')
    pdf_parts.append(trailer)

    return b"".join(pdf_parts)


def format_output_name(cbz_path, name_format, index, output_dir):
    """
    根据命名格式生成输出文件名
    可用变量: {name} 原文件名(无扩展名), {index} 序号, {date} 日期
    """
    base_name = os.path.splitext(os.path.basename(cbz_path))[0]
    today = datetime.now().strftime("%Y%m%d")

    result = name_format.format(
        name=base_name,
        index=index,
        date=today,
    )
    result = safe_filename(result)
    return os.path.join(output_dir, f"{result}.pdf")


# ============================================================
# 交互流程
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="CBZ 转 PDF 转换工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-i", "--input", default=None,
                        help="输入: CBZ文件或包含CBZ的文件夹")
    parser.add_argument("-o", "--output", default=None,
                        help="输出目录")
    parser.add_argument("--keep-name", action="store_true", default=False,
                        help="保留原文件名 (默认行为)")
    parser.add_argument("--name-format", default=None,
                        help="自定义文件名格式 (可用: {name}, {index}, {date})")
    parser.add_argument("-j", "--jobs", type=int, default=None,
                        help="并行转换数 (1-8, 默认4)")
    parser.add_argument("-y", "--yes", action="store_true", default=False,
                        help="跳过确认直接开始")
    args = parser.parse_args()

    # 判断是否为非交互模式
    non_interactive = all([
        args.input is not None,
        args.output is not None,
    ])

    print("=" * 56)
    print("   CBZ 转 PDF 转换工具")
    print("=" * 56)
    print()

    # ==================== 输入路径 ====================
    if args.input:
        input_path = args.input
        if non_interactive:
            print(f"  {SYM_OK} 输入: {os.path.abspath(input_path)}")
        else:
            print(f"【输入路径】命令行指定: {os.path.abspath(input_path)}")
            new_input = input("  输入新路径可修改，回车确认: ").strip()
            if new_input:
                input_path = clean_path(new_input)
    else:
        print("【输入路径】")
        print("  请输入 CBZ 文件路径或包含 CBZ 文件的文件夹路径")
        input_path = input("  输入路径: ").strip()
        if not input_path:
            print(f"  {SYM_FAIL} 未输入路径")
            return
        input_path = clean_path(input_path)

    input_path = os.path.abspath(input_path)
    if not os.path.exists(input_path):
        print(f"  {SYM_FAIL} 路径不存在: {input_path}")
        return

    # 收集 CBZ 文件
    cbz_files = collect_cbz_files(input_path)
    if not cbz_files:
        print(f"  {SYM_FAIL} 未找到 CBZ 文件")
        return

    is_folder = os.path.isdir(input_path)
    print(f"  找到 {len(cbz_files)} 个 CBZ 文件" + (" (含子目录)" if is_folder else ""))

    # ==================== 输出目录 ====================
    if args.output:
        output_dir = args.output
        if non_interactive:
            print(f"  {SYM_OK} 输出到: {os.path.abspath(output_dir)}")
        else:
            print(f"\n【输出目录】命令行指定: {os.path.abspath(output_dir)}")
            new_output = input("  输入新路径可修改，回车确认: ").strip()
            if new_output:
                output_dir = clean_path(new_output)
    else:
        print(f"\n【输出目录】")
        print("  请输入 PDF 文件的保存目录")
        output_input = input("  输出目录: ").strip()
        if not output_input:
            print(f"  {SYM_FAIL} 未指定输出目录")
            return
        output_dir = clean_path(output_input)

    try:
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        print(f"  {SYM_FAIL} 输出目录无效: {e}")
        return
    if not args.output or not non_interactive:
        print(f"  {SYM_OK} 输出目录: {output_dir}")

    # ==================== 文件名格式 ====================
    keep_name = True
    name_format = "{name}"

    if args.name_format:
        keep_name = False
        name_format = args.name_format
        if non_interactive:
            print(f"  {SYM_OK} 命名格式: {name_format}")
        else:
            print(f"\n【文件命名】命令行指定格式: {name_format}")
            fmt_input = input("  输入新格式可修改，回车确认: ").strip()
            if fmt_input:
                name_format = fmt_input
            print(f"  {SYM_OK} 命名格式: {name_format}")
    elif args.keep_name:
        if non_interactive:
            pass
        else:
            print(f"\n【文件命名】命令行指定: 保留原文件名")
            name_choice = input("  是否更改为自定义格式? (y/N): ").strip().lower()
            if name_choice == 'y':
                keep_name = False
                print("  可用变量: {name}=原文件名, {index}=序号, {date}=日期")
                print("  示例: {index:03d}_{name}  →  001_第101话.pdf")
                fmt_input = input("  输入命名格式: ").strip()
                if fmt_input:
                    name_format = fmt_input
                    print(f"  {SYM_OK} 命名格式: {name_format}")
                else:
                    keep_name = True
                    print(f"  {SYM_SKIP} 保留原文件名")
    elif not non_interactive:
        print(f"\n【文件命名】")
        print("  默认保留原文件名 (如 第101话.cbz → 第101话.pdf)")
        name_choice = input("  是否使用自定义命名格式? (y/N): ").strip().lower()
        if name_choice == 'y':
            keep_name = False
            print("  可用变量: {name}=原文件名, {index}=序号, {date}=日期")
            print("  示例: {index:03d}_{name}  →  001_第101话.pdf")
            fmt_input = input("  输入命名格式: ").strip()
            if fmt_input:
                name_format = fmt_input
                print(f"  {SYM_OK} 命名格式: {name_format}")
            else:
                keep_name = True
                print(f"  {SYM_SKIP} 保留原文件名")
        else:
            print(f"  {SYM_OK} 保留原文件名")

    if keep_name and not non_interactive:
        print(f"  {SYM_OK} 保留原文件名")

    # ==================== 并行任务数 ====================
    max_jobs = 4
    if args.jobs is not None:
        if 1 <= args.jobs <= 8:
            max_jobs = args.jobs
        else:
            print(f"  {SYM_WARN} 并行数需在 1-8 之间，使用默认 4")
    elif not non_interactive:
        print(f"\n【并行转换】")
        print(f"  当前: {max_jobs} 个文件同时转换")
        jobs_input = input("  设置并行数 (1-8, 回车保持默认): ").strip()
        if jobs_input:
            try:
                j = int(jobs_input)
                if 1 <= j <= 8:
                    max_jobs = j
                    print(f"  {SYM_OK} 设置为 {max_jobs} 个并行转换")
                else:
                    print(f"  {SYM_WARN} 并行数需在 1-8 之间，使用默认 {max_jobs}")
            except ValueError:
                print(f"  {SYM_WARN} 无效输入，使用默认 {max_jobs}")
    if non_interactive:
        print(f"  {SYM_OK} 并行转换: {max_jobs}")

    # ==================== 确认 ====================
    print(f"\n{'=' * 56}")
    print(f"  输入: {input_path}")
    print(f"  文件数: {len(cbz_files)} 个 CBZ")
    print(f"  输出到: {output_dir}")
    print(f"  命名: {name_format if not keep_name else '保留原文件名'}")
    print(f"  并行: {max_jobs}")

    if not args.yes or not non_interactive:
        confirm = input("\n  开始转换? (Y/n): ").strip().lower()
        if confirm == 'n':
            print("  已取消")
            return

    # ==================== 转换 ====================
    print(f"\n{'=' * 56}")
    print(f"  开始转换... (并行: {max_jobs})")
    print(f"{'=' * 56}")

    success = 0
    fail = 0
    skipped = 0
    result_lock = threading.Lock()

    def _convert_one(index, cbz_path):
        """转换单个 CBZ 文件"""
        # 确定输出文件名
        if keep_name:
            base = os.path.splitext(os.path.basename(cbz_path))[0]
            pdf_path = os.path.join(output_dir, f"{safe_filename(base)}.pdf")
        else:
            pdf_path = format_output_name(cbz_path, name_format, index, output_dir)

        # 跳过已存在的文件
        if os.path.exists(pdf_path):
            return index, True, "skipped"

        ok, result = cbz_to_pdf(cbz_path, pdf_path)
        return index, ok, result

    def _on_done(future):
        nonlocal success, fail, skipped
        index, ok, result = future.result()
        with result_lock:
            if ok:
                if result == "skipped":
                    skipped += 1
                    basename = os.path.basename(cbz_files[index - 1])
                    print(f"  {SYM_SKIP} 已存在，跳过: {basename}")
                else:
                    success += 1
                    size = os.path.getsize(result) if os.path.exists(result) else 0
                    size_str = f"{size / 1024:.0f} KB" if size < 1024 * 1024 else f"{size / 1024 / 1024:.1f} MB"
                    basename = os.path.basename(result)
                    print(f"  {SYM_OK} {basename} ({size_str})")
            else:
                fail += 1
                basename = os.path.basename(cbz_files[index - 1])
                print(f"  {SYM_FAIL} {basename} - 转换失败: {result}")

    with ThreadPoolExecutor(max_workers=max_jobs) as executor:
        futures = []
        for idx, cbz_path in enumerate(cbz_files, 1):
            f = executor.submit(_convert_one, idx, cbz_path)
            f.add_done_callback(_on_done)
            futures.append(f)

        for f in as_completed(futures):
            try:
                f.result()
            except Exception as e:
                with result_lock:
                    fail += 1
                print(f"  {SYM_FAIL} 任务异常: {e}")

    # ==================== 结果 ====================
    print(f"\n{'=' * 56}")
    print(f"  转换完成!")
    print(f"  成功: {success}  跳过: {skipped}  失败: {fail}")
    print(f"  文件保存在: {output_dir}")
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
