# upload_to_box.sh

This is a script for uploading files to a file courier service. Current version <Badge type="tip" text="v1.0" />.

## Features

`upload_to_box.sh` is a script for uploading files to a file courier service. It allows users to quickly upload files via command line and obtain a pickup code and download URL.

## Characteristics

- Supports custom server addresses
- Token is optional, can be skipped if not needed
- Prompts user for configuration information each time it runs, no persistent storage required
- Automatically handles the upload process, including initializing upload tasks and uploading file content
- Displays pickup code and download URL after successful upload

## Usage

### Download Script

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/upload_to_box.sh && sudo chmod +x ./upload_to_box.sh
```

Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/upload_to_box.sh && sudo chmod +x ./upload_to_box.sh
```

### Run Script

```bash
# Run the script and upload a file
./upload_to_box.sh <file_path>
```

### Examples

```bash
# Upload test.txt from current directory
./upload_to_box.sh test.txt

# Upload file from specified path
./upload_to_box.sh /path/to/file.zip
```

## Execution Flow

1. When running the script, the user will be prompted to enter the following information:
   - Token (optional, press Enter to skip)
   - Server Base URL (required)

2. The script will perform the following operations:
   - Initialize upload task and get upload URL
   - Upload file content
   - Extract and display pickup code and download URL

## Notes

- Ensure the server Base URL is correct, in format like `https://filebox.example.com`
- Token is optional, required only if server authentication is enabled
- Uploaded file size should comply with server limits
- If upload fails, the script will display error information returned by the server

## Project Repository

CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/upload_to_box.sh

Github: https://github.com/SDCOM-0415/shit/blob/main/script/upload_to_box.sh

## © Author

SDCOM