# uninstall_docker.sh

This is a script for completely uninstalling Docker. Tested on `Debian 12`. Current version <Badge type="tip" text="v1.0" />.

## Features

- Stop all Docker services
- Uninstall all Docker-related packages
- Remove Docker data directories and configuration files
- Clean up Docker residual files in the system
- Update apt cache

## Usage

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/uninstall_docker.sh && sudo chmod +x ./uninstall_docker.sh && sudo ./uninstall_docker.sh
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/uninstall_docker.sh && sudo chmod +x ./uninstall_docker.sh && sudo ./uninstall_docker.sh
```

Note: This script requires sudo privileges as it performs system-level operations.

## Execution Process

The script displays progress for the following steps:

1. Stop Docker services
2. Uninstall Docker-related packages
3. Remove Docker data directories
4. Remove configuration files and service configurations
5. Update apt cache

Upon completion, a confirmation message will be displayed: "✅ Docker has been completely uninstalled. You can reinstall it now."

## Script Content

```bash
#!/bin/bash
# Script to completely uninstall Docker
# For Debian 12 systems (not tested on other systems)

echo "Docker Uninstall Script Version: v1.0"
echo "© Author: SDCOM"
echo "CNB Project URL: https://cnb.cool/SDCOM/shit/-/blob/main/script/uninstall_docker.sh"
echo "GitHub Project URL: https://github.com/SDCOM-0415/shit/blob/main/script/uninstall_docker.sh"

echo "🛑 Stopping Docker services..."
sudo systemctl stop docker || true

echo "❌ Uninstalling Docker-related packages..."
sudo apt purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin || true
sudo apt autoremove -y --purge

echo "🧹 Removing Docker data directories..."
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd

echo "🗑️ Removing configuration files and service configurations..."
sudo rm -rf /etc/docker
sudo rm -rf /etc/systemd/system/docker.service.d
sudo rm -f  /etc/apt/sources.list.d/docker.list
sudo rm -f  /etc/apt/keyrings/docker.gpg
sudo rm -f  /etc/apt/keyrings/docker.asc

echo "🔄 Updating apt cache..."
sudo apt update

echo "✅ Docker has been completely uninstalled. You can reinstall it now."

```

## Notes

- This script will **completely remove** all Docker-related data and configurations, including:
  - All Docker containers
  - All Docker images
  - All Docker volumes
  - All Docker networks
  - All Docker configurations
- Before executing this script, ensure you have backed up any important Docker data
- The script uses `|| true` syntax to ensure the entire script continues even if some commands fail
- This script is mainly designed for Docker installed via official methods. If installed using other methods, additional cleanup steps may be required

## Project Repository

CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/uninstall_docker.sh

Github: https://github.com/SDCOM-0415/shit/blob/main/script/uninstall_docker.sh
## © Author

SDCOM