#!/bin/bash

# 固定环境变量脚本
# 运行脚本后会提示输入环境变量名称和内容，然后将其固定到用户的 shell 配置文件中

# 获取当前用户
USER_HOME="$HOME"

# 检测使用的 shell
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$USER_HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$USER_HOME/.bashrc"
else
    SHELL_CONFIG="$USER_HOME/.profile"
fi

# 提示用户输入环境变量名称
echo "================================"
echo "  固定环境变量工具"
echo "================================"
echo
read -p "请输入环境变量名称: " ENV_NAME

# 检查环境变量名称是否为空
if [ -z "$ENV_NAME" ]; then
    echo "错误: 环境变量名称不能为空"
    exit 1
fi

# 验证环境变量名称格式（只允许字母、数字和下划线）
if ! [[ "$ENV_NAME" =~ ^[a-zA-Z_][a-zA-Z0-9_]*$ ]]; then
    echo "错误: 环境变量名称格式无效，只允许字母、数字和下划线，且不能以数字开头"
    exit 1
fi

# 提示用户输入环境变量内容
read -p "请输入环境变量内容: " ENV_VALUE

# 检查配置文件是否存在
if [ ! -f "$SHELL_CONFIG" ]; then
    echo "警告: 配置文件 $SHELL_CONFIG 不存在，将创建新文件"
    touch "$SHELL_CONFIG"
fi

# 检查环境变量是否已存在
if grep -q "^export $ENV_NAME=" "$SHELL_CONFIG" 2>/dev/null; then
    echo "提示: 环境变量 $ENV_NAME 已存在于 $SHELL_CONFIG 中，将更新其值"
    # 只删除匹配的环境变量行
    sed -i "/^export $ENV_NAME=/d" "$SHELL_CONFIG"
fi

# 将环境变量添加到配置文件
echo "export $ENV_NAME=\"$ENV_VALUE\"" >> "$SHELL_CONFIG"

echo
echo "================================"
echo "成功! 环境变量已添加到 $SHELL_CONFIG"
echo "================================"
echo "环境变量名称: $ENV_NAME"
echo "环境变量内容: $ENV_VALUE"
echo
echo "请运行以下命令使配置生效:"
echo "  source $SHELL_CONFIG"
echo
echo "或者重新打开终端窗口"
