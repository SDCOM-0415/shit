# get_ip.sh

This is a script for quickly obtaining local IP addresses in termux. Tested on `termux`. Current version <Badge type="tip" text="v0.1" />.

## Features

- Get IPv4 addresses of all network interfaces
- Display network interface names and corresponding IP addresses in a clear format
- Automatically check if ifconfig command is available

## Usage

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/get_ip.sh && sudo chmod +x ./get_ip.sh && sudo ./get_ip.sh
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/get_ip.sh && sudo chmod +x ./get_ip.sh && sudo ./get_ip.sh
```

After running, the script will display all network interfaces with IPv4 addresses in the format: `interface_name: IP_address`

## Script Content

```bash
#!/bin/bash

echo "Get IP Version: v0.1"
echo "Author: SDCOM"
echo "CNB Project URL: https://cnb.cool/SDCOM/shit/-/blob/main/script/get_ip.sh"
echo "GitHub Project URL: https://github.com/SDCOM-0415/shit/blob/main/script/get_ip.sh"

# Script function: Get IP addresses of all network interfaces and output in specified format
# Output format: interface_name: IP_address

# Check if ifconfig command is available
if ! command -v ifconfig &> /dev/null; then
    echo "Error: ifconfig command is not available, please install net-tools package"
    exit 1
fi

# Get all network interface names
interfaces=$(ifconfig | grep -E '^[a-zA-Z0-9]+:' | awk -F: '{print $1}')

# Iterate through each interface and get its IP address
for interface in $interfaces; do
    # Get IPv4 address
    ip_addr=$(ifconfig $interface | grep -oP 'inet \K\d+\.\d+\.\d+\.\d+')
    
    # If the interface has an IP address, output it
    if [ ! -z "$ip_addr" ]; then
        echo "$interface: $ip_addr"
    fi
done

exit 0
```

## Working Principle

1. Check if `ifconfig` command is installed on the system
2. Use `ifconfig` to get all network interface names
3. Iterate through each interface and extract its IPv4 address
4. Output interface names and IP addresses in the specified format

## Dependencies

- `net-tools` package (provides `ifconfig` command)

## Notes

- If `ifconfig` command is not installed, the script will prompt to install the `net-tools` package
- The script only displays interfaces with IPv4 addresses; interfaces without IP addresses will not be shown
- This script is mainly designed for termux environment but can also be used on other Linux systems

## Project Repository
CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/get_ip.sh

Github: https://github.com/SDCOM-0415/shit/blob/main/script/get_ip.sh

## © Author
SDCOM