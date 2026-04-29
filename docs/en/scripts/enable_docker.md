# enable_docker.sh

This is a script for re-enabling Docker. Tested on `Debian 12` and `Ubuntu 22.04`. Current version <Badge type="tip" text="v1.0" />.

## Features

Re-enable Docker by removing all restrictions set by `disable_docker.sh` and install Docker.

## Usage

```bash
# Must be run with sudo or as root user
sudo ./enable_docker.sh
```

## Execution Steps

1. **Remove Monitoring Script**: Delete the scheduled Docker monitoring script
2. **Unlock Packages**: Remove locks from Docker-related packages
3. **Remove Blocking Policy**: Delete Docker blocking rules from APT configuration
4. **Restore Kernel Modules**: Remove kernel module blacklist
5. **Remove Audit Rules**: Delete Docker-related audit rules
6. **Restore Directory Permissions**: Restore normal permissions for /var/lib/docker and /etc/docker
7. **Install Docker**: Install docker.io or available version
8. **Install Related Tools**: Install docker-compose and containerd
9. **Start Services**: Enable and start Docker service
10. **Verify Installation**: Test if Docker is running properly

## Notes

- This script requires root privileges
- Previous backup files (in `/root/docker-backup-*`) may need to be manually restored
- Logs are saved in `/var/log/docker-enable.log`

## Author

SDCOM

## Project URL

- CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/enable_docker.sh
- GitHub: https://github.com/SDCOM-0415/shit/blob/main/script/enable_docker.sh