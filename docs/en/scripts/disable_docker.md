# disable_docker.sh

This is a script for completely disabling Docker and preventing reinstallation. Tested on `Debian 12` and `Ubuntu 22.04`. Current version <Badge type="tip" text="v1.0" />.

## Features

Completely disable Docker and prevent reinstallation. The script will:

1. Stop and disable all Docker-related services
2. Terminate Docker-related processes
3. Uninstall Docker packages
4. Clean up Docker files and directories
5. Lock Docker-related packages
6. Create APT blocking policy
7. Disable related kernel modules
8. Create monitoring script to prevent reinstallation
9. Create audit rules

## Usage

```bash
# Must be run with sudo or as root user
sudo ./disable_docker.sh
```

## Execution Steps

1. **Stop Services**: Stop docker, docker.socket, containerd services
2. **Terminate Processes**: Kill dockerd, containerd, docker-proxy processes
3. **Backup Configuration**: Backup current Docker configuration to `/root/docker-backup-{timestamp}/`
4. **Uninstall Packages**: Remove all Docker-related packages
5. **Clean Directories**: Delete Docker data directories and create read-only empty directories
6. **Lock Packages**: Use apt-mark hold to lock Docker packages
7. **Create Blocking Policy**: Add Docker blocking rules to APT configuration
8. **Disable Kernel Modules**: Blacklist overlay and br_netfilter modules
9. **Install Monitoring Script**: Periodically check and terminate any Docker processes
10. **Clean User Directories**: Remove .docker configuration from user directories
11. **Create Audit Rules**: Monitor Docker-related file access

## Notes

- This script requires root privileges
- Operations are irreversible, please ensure important data is backed up
- Monitoring script runs every 10 minutes to prevent Docker reinstallation
- Logs are saved in `/var/log/docker-disable.log` and `/var/log/docker-monitor.log`

## Author

SDCOM

## Project URL

- CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/disable_docker.sh
- GitHub: https://github.com/SDCOM-0415/shit/blob/main/script/disable_docker.sh