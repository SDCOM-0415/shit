# cbz2pdf.py

CBZ comic archive to PDF conversion tool, supporting single file or batch conversion, cross-platform compatible. Current version <Badge type="tip" text="v1.0" />

## Features

- **CBZ to PDF** — Convert CBZ (ZIP-compressed image archives) to PDF files
- **Single/Batch Conversion** — Supports single CBZ file or entire folder (including subdirectories) batch processing
- **Interactive/Non-interactive Dual Mode** — Interactive mode with guided configuration, non-interactive mode with direct parameter passing
- **Automatic Dependency Installation** — Detects missing Pillow dependency and prompts to auto-install
- **Custom Naming Format** — Supports `{name}` `{index}` `{date}` variable combinations
- **Parallel Conversion** — Multi-threaded parallel processing of multiple CBZ files for faster batch conversion
- **Skip Existing** — Automatically skips conversion when output PDF already exists
- **Cross-platform Compatible** — Works on Windows / macOS / Linux, with Windows terminal UTF-8 auto-detection

## Dependencies

| Dependency | Purpose | Install |
|-----------|---------|---------|
| Python 3.6+ | Runtime environment | — |
| [Pillow](https://pypi.org/project/Pillow) | Image reading and PDF generation | `pip install Pillow` |

> The script auto-detects on startup. If missing, it will prompt and guide installation — no manual intervention required.

## Usage

### Download Script

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/cbz2pdf.py
```

GitHub:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/cbz2pdf.py
```

### Interactive Mode

Run the script directly, then follow the prompts:

```bash
python cbz2pdf.py
```

Workflow:
1. Enter the CBZ file path or folder path containing CBZ files
2. Enter the PDF output directory
3. Choose whether to use a custom naming format (default: keep original filename)
4. Set the number of parallel conversions (1-8, default 4)
5. Confirm and start conversion

### Non-interactive Mode

Provide `-i` and `-o` parameters to skip all interactive prompts and start conversion immediately:

```bash
# Convert a single CBZ file
python cbz2pdf.py -i "/path/to/Chapter101.cbz" -o "/path/to/PDF"

# Batch convert an entire folder
python cbz2pdf.py -i "/path/to/Comics" -o "/path/to/PDF"

# Keep original filename (default behavior, can be omitted)
python cbz2pdf.py -i "/path/to/Comics" -o "/path/to/PDF" --keep-name

# Custom naming format
python cbz2pdf.py -i "/path/to/Comics" -o "/path/to/PDF" --name-format "{index:03d}_{name}"

# Skip confirmation and start immediately
python cbz2pdf.py -i "/path/to/Comics" -o "/path/to/PDF" -y
```

## Command-line Parameters

| Parameter | Short | Description |
|-----------|-------|-------------|
| `--input PATH` | `-i` | Input: CBZ file or folder containing CBZ files (required for non-interactive mode) |
| `--output DIR` | `-o` | Output directory (required for non-interactive mode) |
| `--keep-name` | | Keep original filename (default behavior) |
| `--name-format FMT` | | Custom filename format. Available variables: `{name}` `{index}` `{date}` |
| `--jobs N` | `-j` | Number of parallel conversions, range 1-8, default 4 |
| `--yes` | `-y` | Skip confirmation, start conversion immediately |

### Naming Format Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{name}` | Original filename (without extension) | `Chapter101` |
| `{index}` | File index (starting from 1) | `1` `2` ... |
| `{date}` | Current date | `20260504` |

Format examples:

```
{name}.pdf              →  Chapter101.pdf
{index:03d}_{name}.pdf  →  001_Chapter101.pdf
{date}_{name}.pdf       →  20260504_Chapter101.pdf
```

## Workflow

### Interactive Mode

```
========================================================
   CBZ to PDF Conversion Tool
========================================================

[Input Path]
  Please enter the CBZ file path or folder path containing CBZ files
  Input path: /path/to/Comics
  Found 5 CBZ files (including subdirectories)

[Output Directory]
  Please enter the PDF output directory
  Output directory: /path/to/PDF
  ✓ Output directory: /path/to/PDF

[File Naming]
  Default: keep original filename (e.g. Chapter101.cbz → Chapter101.pdf)
  Use custom naming format? (y/N): n
  ✓ Keep original filename

[Parallel Conversion]
  Current: 4 files converting simultaneously
  Set parallel count (1-8, Enter to keep default): 4
  ✓ Set to 4 parallel conversions

========================================================
  Input: /path/to/Comics
  Files: 5 CBZ files
  Output to: /path/to/PDF
  Naming: Keep original filename
  Parallel: 4

  Start conversion? (Y/n): Y

========================================================
  Starting conversion... (parallel: 4)
========================================================
  ✓ Chapter101.pdf (2.3 MB)
  ✓ Chapter102.pdf (1.8 MB)
  ⊙ Chapter103.pdf already exists, skipped
  ✗ Chapter104.cbz - conversion failed: No images found in CBZ

========================================================
  Conversion complete!
  Success: 2  Skipped: 1  Failed: 1
  Files saved to: /path/to/PDF
========================================================
```

### Non-interactive Mode

```bash
python cbz2pdf.py -i "/path/to/Comics" -o "/path/to/PDF" -j 4 -y
```

```
========================================================
   CBZ to PDF Conversion Tool
========================================================

  ✓ Input: /path/to/Comics
  ✓ Output to: /path/to/PDF
  ✓ Naming format: {name}
  ✓ Parallel conversion: 4

========================================================
  Starting conversion... (parallel: 4)
========================================================
  ✓ Chapter101.pdf (2.3 MB)
  ✓ Chapter102.pdf (1.8 MB)
  Conversion complete!
```

## Notes

- **Image Format Support**: JPG, PNG, WebP, GIF, BMP inside CBZ are all recognized and convertible
- **PDF Compatibility**: All images are converted to RGB mode for maximum compatibility
- **PDF Resolution**: Default 150 DPI, balancing clarity and file size
- **Parallel Safety**: Parallel conversion count should not exceed 8; higher values may cause memory issues
- **Skip Mechanism**: Automatically skips when output PDF already exists; re-running will not cause duplicate conversions
- **Windows Terminal**: Script auto-detects and sets UTF-8 encoding; Chinese filenames display correctly

## Project Repository

CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/cbz2pdf.py

GitHub: https://github.com/SDCOM-0415/shit/blob/main/script/cbz2pdf.py

## © Author

SDCOM
