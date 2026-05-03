# download_cbz_interactive.py

This is a Python script for downloading manga chapters from cloudme.one and packaging them as CBZ files. Supports Windows / macOS / Linux. Current version <Badge type="tip" text="v1.1" />.

## Features

`download_cbz_interactive.py` is a manga chapter download tool for cloudme.one. It fetches manga information via API, downloads chapter images, and automatically packages them into CBZ format files for use with various comic readers.

## Characteristics

- Interactive or command-line mode for selecting chapter ranges to download
- Automatically fetches manga and chapter information via API
- Downloads high-quality images through img.cloudme.one proxy (requires cf_clearance)
- CDN direct fallback download (no Cookie required, but lower image quality)
- Multi-threaded image downloads, multi-task parallel chapter downloads
- Automatically packages into CBZ files (ZIP format, compatible with comic readers)
- Supports HTTP/SOCKS5 proxy
- Configurable image download threads (1-32) and parallel chapter count (1-5)
- Supports passing cf_clearance via command line, no interactive input needed
- Supports skipping confirmation to start download directly (`-y`/`--yes`)
- Auto-detects and installs missing dependencies
- Cross-platform compatible (Windows / macOS / Linux)
- Terminal Unicode auto-adaptation (falls back to ASCII symbols on unsupported terminals)
- Download progress bar display
- Automatically skips existing CBZ files

## Dependencies

- Python 3.6+
- curl_cffi

```bash
pip install curl_cffi
```

The script automatically detects dependencies on first run and prompts to install if missing.

## Usage

### Download Script

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/download_cbz_interactive.py
```

GitHub:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/download_cbz_interactive.py
```

### Interactive Mode

Run the script directly to enter interactive mode and follow the prompts:

```bash
python download_cbz_interactive.py
```

### Non-interactive Mode

Provide all necessary information via command-line arguments, and the script starts downloading directly without interactive input:

```bash
# Download chapters 101-120, use proxy, 16 threads, 3 parallel chapters
python download_cbz_interactive.py \
  -o ~/Comics \
  -m 10 \
  -c 101-120 \
  --cf xxxxxxxx \
  -p http://127.0.0.1:7890 \
  -t 16 \
  -j 3 \
  --strip-prefix \
  -y
```

> When `-m`, `-c`, and `-o` are all provided, the script automatically enters non-interactive mode.
> Parameters not provided will still be prompted in interactive mode.

### Specify Download Directory

Specify the save directory for CBZ files via command line arguments:

```bash
# Windows
python download_cbz_interactive.py -o D:\Comics

# macOS / Linux
python download_cbz_interactive.py -o ~/Comics

# Can also be combined with other parameters
python download_cbz_interactive.py -o ~/Comics -m 10 -c all -y
```

The default download directory is the directory where the script is located.

## Command Line Arguments

| Parameter | Short | Description |
|-----------|-------|-------------|
| `--output DIR` | `-o` | Specify the save directory for CBZ files (default: script directory) |
| `--mid ID` | `-m` | Manga ID (e.g., `10` in cloudme.one/refs/10) |
| `--chapters RANGE` | `-c` | Chapter range, supports `101-120`, `101,103,105`, `all` |
| `--cf TOKEN` | | cf_clearance cookie value (for downloading high-quality images) |
| `--proxy URL` | `-p` | HTTP/SOCKS5 proxy address (e.g., `http://127.0.0.1:7890`) |
| `--threads N` | `-t` | Number of image download threads (1-32, default 8) |
| `--jobs N` | `-j` | Number of parallel chapter downloads (1-5, default 5) |
| `--strip-prefix` | | Remove prefix before `_` in title (e.g., `SomeManga_Chapter101` → `Chapter101`) |
| `--yes` | `-y` | Skip confirmation prompt and start download directly |

## Execution Flow

### Interactive Mode Flow

1. **Confirm download directory**: Displays the current download directory, enter a new path to change it, or press Enter to confirm
2. **(Optional) Set proxy**: Enter HTTP/SOCKS5 proxy address, or press Enter to skip
3. **(Optional) Set thread count**: Set the number of image download threads (1-32), or press Enter to use default 8
4. **(Optional) Set parallel tasks**: Set the number of chapters to download in parallel (1-5), or press Enter to use default 5
5. **Enter manga ID**: Enter the manga ID from the cloudme.one website (the number in the URL, e.g., `10` in `cloudme.one/refs/10`)
6. **Fetch manga information**: Automatically fetches manga title and full chapter list via API
7. **Prefix handling (optional)**: If chapter titles contain `_` separators, you'll be prompted whether to remove the prefix
8. **Configure Cloudflare Cookie (optional)**: Provide `cf_clearance` cookie to download high-quality images; skip to use CDN direct download for lower quality
9. **Select chapters**: Enter the chapter range to download, supporting the following formats:
   - Single chapter: `101`
   - Range: `101-120`
   - Multiple: `101,103,105`
   - Mixed: `101-105,108,110-112`
   - All: `all`
10. **Confirm and download**: Confirm the information and start downloading, with progress and result summary displayed

### Non-interactive Mode

When `-o`, `-m`, and `-c` are all provided, the script skips all interactive prompts and starts downloading directly. Other parameters (`-p`, `-t`, `-j`, `--cf`, `--strip-prefix`, `-y`) can be optionally provided as needed.

## How to Get cf_clearance

High-quality images require downloading through a Cloudflare-protected proxy, which needs a `cf_clearance` cookie:

1. Open `cloudme.one` in your browser
2. Press `F12` to open Developer Tools
3. Switch to the `Application` tab
4. Find `Cookies` → `https://cloudme.one` on the left
5. Find the `cf_clearance` field and copy its value

::: tip
If you don't provide `cf_clearance`, the script will still work, but will download lower quality images via CDN direct connection.
You can also pass it via the `--cf` parameter on the command line, without manually pasting it in interactive mode.
:::

## Notes

- The script requires Python 3.6 or higher
- `curl_cffi` is used to bypass Cloudflare protection and is a core dependency
- When downloading a large number of chapters, the script automatically adds intervals between chapters to avoid too many requests
- Existing CBZ files will be automatically skipped and will not be re-downloaded
- Windows users experiencing garbled text in the terminal will have UTF-8 support automatically enabled by the script
- It is recommended that the image download thread count (`-t`) does not exceed 32, and the parallel chapter count (`-j`) does not exceed 5, to avoid being rate-limited

## Project Repository

CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/download_cbz_interactive.py

GitHub: https://github.com/SDCOM-0415/shit/blob/main/script/download_cbz_interactive.py

## © Author

SDCOM
