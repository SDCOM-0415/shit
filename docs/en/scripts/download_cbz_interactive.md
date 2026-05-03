# download_cbz_interactive.py

This is a Python script for downloading manga chapters from cloudme.one and packaging them as CBZ files. Supports Windows / macOS / Linux. Current version <Badge type="tip" text="v1.0" />.

## Features

`download_cbz_interactive.py` is a manga chapter download tool for cloudme.one. It fetches manga information via API, downloads chapter images, and automatically packages them into CBZ format files for use with various comic readers.

## Characteristics

- Interactive selection of chapter ranges to download
- Automatically fetches manga and chapter information via API
- Downloads high-quality images through img.cloudme.one proxy (requires cf_clearance)
- CDN direct fallback download (no Cookie required, but lower image quality)
- Automatically packages into CBZ files (ZIP format, compatible with comic readers)
- Supports specifying download directory via command line
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

Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/download_cbz_interactive.py
```

### Interactive Mode

Run the script directly to enter interactive mode:

```bash
python download_cbz_interactive.py
```

### Specify Download Directory

Specify the save directory for CBZ files via command line arguments:

```bash
# Windows
python download_cbz_interactive.py -o D:\Comics

# macOS / Linux
python download_cbz_interactive.py -o ~/Comics

# You can also use the long option
python download_cbz_interactive.py --output ./comics
```

The default download directory is the directory where the script is located.

## Command Line Arguments

| Parameter | Short | Description |
|-----------|-------|-------------|
| `--output` | `-o` | Specify the save directory for CBZ files (default: script directory) |

## Execution Flow

1. **Confirm download directory**: Displays the current download directory, enter a new path to change it, or press Enter to confirm
2. **Enter manga ID**: Enter the manga ID from the cloudme.one website (the number in the URL, e.g., `10` in `cloudme.one/refs/10`)
3. **Fetch manga information**: Automatically fetches manga title and full chapter list via API
4. **Prefix handling (optional)**: If chapter titles contain `_` separators, you'll be prompted whether to remove the prefix
5. **Configure Cloudflare Cookie (optional)**: Provide `cf_clearance` cookie to download high-quality images; skip to use CDN direct download for lower quality
6. **Select chapters**: Enter the chapter range to download, supporting the following formats:
   - Single chapter: `101`
   - Range: `101-120`
   - Multiple: `101,103,105`
   - Mixed: `101-105,108,110-112`
   - All: `all`
7. **Confirm and download**: Confirm the information and start downloading, with progress and result summary displayed

## How to Get cf_clearance

High-quality images require downloading through a Cloudflare-protected proxy, which needs a `cf_clearance` cookie:

1. Open `cloudme.one` in your browser
2. Press `F12` to open Developer Tools
3. Switch to the `Application` tab
4. Find `Cookies` → `https://cloudme.one` on the left
5. Find the `cf_clearance` field and copy its value

::: tip
If you don't provide `cf_clearance`, the script will still work, but will download lower quality images via CDN direct connection.
:::

## Notes

- The script requires Python 3.6 or higher
- `curl_cffi` is used to bypass Cloudflare protection and is a core dependency
- When downloading a large number of chapters, the script automatically adds intervals between chapters to avoid too many requests
- Existing CBZ files will be automatically skipped and will not be re-downloaded
- Windows users experiencing garbled text in the terminal will have UTF-8 support automatically enabled by the script

## Project Repository

CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/download_cbz_interactive.py

Github: https://github.com/SDCOM-0415/shit/blob/main/script/download_cbz_interactive.py

## © Author

SDCOM
