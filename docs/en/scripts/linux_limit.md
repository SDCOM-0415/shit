# linux_limit.sh

This is a script for limiting directory size on Linux systems. Tested on `Debian 12`. Current version <Badge type="tip" text="v1.0" />.

## Features

- Supports both interactive and command-line argument modes
- Uses fallocate method to create fixed-size image files
- Automatically backs up original directory data
- Supports multiple size units (B/KB/MB/GB/TB)

## Usage

### Interactive Mode

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/linux_limit.sh && sudo chmod +x ./linux_limit.sh && sudo ./linux_limit.sh
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/linux_limit.sh && sudo chmod +x ./linux_limit.sh && sudo ./linux_limit.sh
```

After running the script, follow the prompts to enter:
1. Original directory path to be limited
2. Size limit (supports units like B/KB/MB/GB/TB)
3. Image storage path (default: ./limit.img)

### Command Line Mode

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/linux_limit.sh && sudo chmod +x ./linux_limit.sh && sudo ./linux_limit.sh <original_dir> <size> <image_path>
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/linux_limit.sh && sudo chmod +x ./linux_limit.sh && sudo ./linux_limit.sh <original_dir> <size> <image_path>
```

Example:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/linux_limit.sh && sudo chmod +x ./linux_limit.sh && sudo ./linux_limit.sh /path/to/directory 10GB /path/to/limit.img
```

## Parameters

- `Original Directory Path`: Full path of the directory to be limited
- `Size Limit`: Supported units include:
  - B (bytes)
  - KB (kilobytes)
  - MB (megabytes)
  - GB (gigabytes)
  - TB (terabytes)
- `Image Storage Path`: Optional parameter, defaults to ./limit.img in current directory

## Script Content
```bash
#!/bin/bash

echo "limit Version: v1.0"
echo "Author: SDCOM"
echo "CNB Project URL: https://cnb.cool/SDCOM/shit/-/blob/main/script/linux_limit.sh"
echo "GitHub Project URL: https://github.com/SDCOM-0415/shit/blob/main/script/linux_limit.sh"

# Method selection
METHOD=2  # Default to fallocate method

# Interactive input
interactive_input() {
    read -p "Please enter the original directory path to limit: " ORIGINAL_DIR
    read -p "Please enter the size limit (supports B/KB/MB/GB/TB): " SIZE_STR
    read -p "Please enter the image storage path (default ./limit.img): " IMG_PATH
    IMG_PATH=${IMG_PATH:-"./limit.img"}
}

# Parameter parsing
if [ $# -eq 0 ]; then
    interactive_input
else
    ORIGINAL_DIR=$1
    SIZE_STR=$2
    IMG_PATH=${3:-"./limit.img"}
fi

# Validate original directory
[ ! -d "$ORIGINAL_DIR" ] && echo "Error: Original directory does not exist" && exit 1

# Create limited space
if [ $METHOD -eq 2 ]; then
    # 1. Create image file
    fallocate -l $SIZE_STR "$IMG_PATH"
    mkfs.ext4 "$IMG_PATH"
    
    # 2. Backup original directory
    BACKUP_DIR="${ORIGINAL_DIR}_backup_$(date +%s)"
    mv "$ORIGINAL_DIR" "$BACKUP_DIR"
    
    # 3. Create new directory and mount
    mkdir -p "$ORIGINAL_DIR"
    mount -o loop "$IMG_PATH" "$ORIGINAL_DIR"
    
    # 4. Restore original data (optional)
    echo "Restoring original data (may take time)..."
    cp -a "$BACKUP_DIR"/. "$ORIGINAL_DIR"/
    
    echo "Successfully limited directory $ORIGINAL_DIR to size $SIZE_STR"
    echo "Original data backed up at: $BACKUP_DIR"
fi

```

## Working Principle

1. Create an image file of specified size (using fallocate)
2. Format the image file as ext4 filesystem
3. Backup the original directory (automatically adds timestamp)
4. Create new directory and mount the image file
5. Restore original data to the new limited directory

## Notes

- Requires root privileges (due to mount operation)
- Original data is automatically backed up, backup directory format: `original_dir_backup_timestamp`
- Ensure the system has enough space to store the image file
- It is recommended to backup important data before operation

## Project Repository

CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/linux_limit.sh

Github: https://github.com/SDCOM-0415/shit/blob/main/script/linux_limit.sh

## © Author

SDCOM