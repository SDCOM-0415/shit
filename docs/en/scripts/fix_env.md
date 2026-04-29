# fix_env.sh

This is a script for permanently fixing environment variables to shell configuration files. Tested on `Bash` and `Zsh`. Current version <Badge type="tip" text="v1.0" />.

## Features

Permanently fix environment variables to the user's shell configuration file, preventing environment variables from being lost after the session ends. Supports automatic detection and writing to .bashrc, .zshrc, or .profile.

## Usage

### Download Script

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/fix_env.sh && sudo chmod +x ./fix_env.sh
```

Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/fix_env.sh && sudo chmod +x ./fix_env.sh
```

### Run Script

```bash
# Run the script
./fix_env.sh

# Follow prompts to enter environment variable name and content
```

## Interactive Flow

1. Enter environment variable name (e.g., `API_KEY`, `PATH`, etc.)
2. Enter environment variable content (e.g., `/usr/local/bin` or `abc123`)
3. Script automatically detects current shell (bash/zsh)
4. Write environment variable to corresponding configuration file

## Environment Variable Name Rules

- Only letters, numbers, and underscores are allowed
- Cannot start with a number
- First character must be a letter or underscore

## Supported Shell Configuration Files

- **Bash**: `~/.bashrc`
- **Zsh**: `~/.zshrc`
- **Other**: `~/.profile`

## Apply Configuration

After running the script, execute the following command to apply the configuration:

```bash
# Bash
source ~/.bashrc

# Zsh
source ~/.zshrc

# Or reopen the terminal window
```

## Usage Example

```bash
$ ./fix_env.sh
================================
  Environment Variable Fix Tool
================================

Please enter the environment variable name: NODE_ENV
Please enter the environment variable content: production

================================
Success! Environment variable added to /home/user/.bashrc
================================
Environment variable name: NODE_ENV
Environment variable content: production

Please run the following command to apply changes:
  source /home/user/.bashrc

Or reopen the terminal window
```

## Notes

- If the environment variable already exists, the script will update its value
- Configuration file will be created automatically if it doesn't exist
- Configuration file needs to be reloaded or terminal restarted to take effect

## Author

SDCOM

## Project URL

- CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/fix_env.sh
- GitHub: https://github.com/SDCOM-0415/shit/blob/main/script/fix_env.sh