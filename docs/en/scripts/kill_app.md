# kill_app.sh
This script is used to quickly terminate running programs on Linux and macOS systems. Tested on `FydeOS Linux Subsystem`, `macOS 10.15.7`, and `Debian 12`. Current version <Badge type="tip" text="v1.0" />

## Features

- Allows users to input a process name and attempts to find and terminate that process
- If no exact match is found, displays potentially related processes
- Supports terminating processes directly by PID

## Usage
CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/kill_app.sh && sudo chmod +x ./kill_app.sh && sudo ./kill_app.sh
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/kill_app.sh && sudo chmod +x ./kill_app.sh && sudo ./kill_app.sh
```

After running the script, follow the prompts to enter the process name to terminate. If no exact match is found, the script will list potentially related processes and allow you to enter a PID to terminate a specific process.

## Script Content

```bash
#!/bin/bash

echo "Kill_app Version: v1.0"
echo "Author: SDCOM"
echo "CNB Project URL: https://cnb.cool/SDCOM/shit/-/blob/main/script/kill_app.sh"
echo "GitHub Project URL: https://github.com/SDCOM-0415/shit/blob/main/script/kill_app.sh"


read -p "Please enter the process name to terminate: " PROCESS_NAME

if [ -z "$PROCESS_NAME" ]; then
    echo "Error: Process name cannot be empty!"
    exit 1
fi

PIDS=$(pgrep -x "$PROCESS_NAME")

if [ -z "$PIDS" ]; then
    echo "Error: No exact match found for process '$PROCESS_NAME'. Executing command: pgrep -x '$PROCESS_NAME'"
    echo "The following may be related processes:"
    ps aux | grep -i "$PROCESS_NAME" | grep -v -e grep -e $0
    read -p "Please enter the PID(s) to terminate (separate multiple PIDs with spaces): " USER_PIDS
    
    # Validate input is not empty
    if [ -z "$USER_PIDS" ]; then
        echo "Error: PID cannot be empty."
        exit 1
    fi
    
    # Validate each PID
    for PID in $USER_PIDS; do
        if ! [[ "$PID" =~ ^[0-9]+$ ]]; then
            echo "Error: PID must be a number."
            exit 1
        fi
        if ! ps -p "$PID" > /dev/null 2>&1; then
            echo "Error: PID $PID does not exist."
            exit 1
        fi
    done
    
    # Terminate processes
    for PID in $USER_PIDS; do
        echo "Terminating process (PID: $PID)..."
        kill -15 "$PID"
    done
    echo "Operation completed."
    exit 0
fi

# Convert PIDs to comma-separated
PIDS_COMMA=$(echo $PIDS | tr ' ' ',')

echo "Found the following process PIDs:"
ps -p $PIDS_COMMA -o pid,cmd

for PID in $PIDS; do
    echo "Terminating process (PID: $PID)..."
    kill -15 "$PID"
done

echo "Operation completed"

```

## Notes

- This script uses the `kill -9` command to force terminate processes, which may cause data loss or other issues
- Before terminating important processes, ensure all work has been saved
- When using this script on Linux systems, root privileges may be required to terminate certain system processes

## Project Repository

CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/kill_app.sh

Github: https://github.com/SDCOM-0415/shit/blob/main/script/kill_app.sh

## © Author

SDCOM