# fix_env.sh

## 功能说明

将环境变量永久固定到用户的 shell 配置文件中，防止环境变量在会话结束后丢失。支持自动检测并写入 .bashrc、.zshrc 或 .profile。

## 使用方法

```bash
# 运行脚本
./fix_env.sh

# 按提示输入环境变量名称和内容
```

## 交互流程

1. 输入环境变量名称（如 `API_KEY`、`PATH` 等）
2. 输入环境变量的内容（如 `/usr/local/bin` 或 `abc123`）
3. 脚本自动检测当前使用的 shell（bash/zsh）
4. 将环境变量写入对应的配置文件

## 环境变量名称规则

- 只允许字母、数字和下划线
- 不能以数字开头
- 首字符必须是字母或下划线

## 支持的 Shell 配置文件

- **Bash**: `~/.bashrc`
- **Zsh**: `~/.zshrc`
- **其他**: `~/.profile`

## 使配置生效

执行脚本后，运行以下命令使配置生效：

```bash
# Bash
source ~/.bashrc

# Zsh
source ~/.zshrc

# 或者重新打开终端窗口
```

## 使用示例

```bash
$ ./fix_env.sh
================================
  固定环境变量工具
================================

请输入环境变量名称: NODE_ENV
请输入环境变量内容: production

================================
成功! 环境变量已添加到 /home/user/.bashrc
================================
环境变量名称: NODE_ENV
环境变量内容: production

请运行以下命令使配置生效:
  source /home/user/.bashrc

或者重新打开终端窗口
```

## 注意事项

- 如果环境变量已存在，脚本会更新其值
- 配置文件不存在时会自动创建
- 需要重新加载配置文件或重启终端才能生效

## 作者

SDCOM

## 项目地址

- CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/fix_env.sh
- GitHub: https://github.com/SDCOM-0415/shit/blob/main/script/fix_env.sh
