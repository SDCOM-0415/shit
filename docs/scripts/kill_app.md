# kill_app.sh
这个脚本用于快速结束Linux、macOS系统运行中程序，测试支持`FydeOS Linux子系统` `macOS 10.15.7` `Debian 12`，当前版本<Badge type="tip" text="v1.0" />

## 功能

- 允许用户输入进程名称，然后尝试找到并终止该进程
- 如果找不到精确匹配的进程，会显示可能相关的进程
- 支持通过PID直接终止进程

## 使用方法
CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/kill_app.sh && sudo chmod +x ./kill_app.sh && sudo ./kill_app.sh
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/kill_app.sh && sudo chmod +x ./kill_app.sh && sudo ./kill_app.sh
```

运行脚本后，按照提示输入要终止的进程名称。如果找不到精确匹配的进程，脚本会列出可能相关的进程，并允许你输入PID来终止特定进程。

## 脚本内容

```bash
#!/bin/bash

echo "Kill_app Version: v1.0"
echo "作者: SDCOM"
echo "CNB项目地址：https://cnb.cool/SDCOM/shit/-/blob/main/script/kill_app.sh"
echo "GitHub项目地址：https://github.com/SDCOM-0415/shit/blob/main/script/kill_app.sh"


read -p "请输入要终止的进程名称: " PROCESS_NAME

if [ -z "$PROCESS_NAME" ]; then
    echo "错误：进程名称不能为空！"
    exit 1
fi

PIDS=$(pgrep -x "$PROCESS_NAME")

if [ -z "$PIDS" ]; then
    echo "错误：未找到精确匹配进程 '$PROCESS_NAME'。执行命令：pgrep -x '$PROCESS_NAME'"
    echo "以下可能是相关的进程："
    ps aux | grep -i "$PROCESS_NAME" | grep -v -e grep -e $0
    read -p "请输入要终止的PID（多个请用空格分隔）: " USER_PIDS
    
    # 验证输入是否为空
    if [ -z "$USER_PIDS" ]; then
        echo "错误：PID 不能为空。"
        exit 1
    fi
    
    # 验证每个 PID
    for PID in $USER_PIDS; do
        if ! [[ "$PID" =~ ^[0-9]+$ ]]; then
            echo "错误：PID 必须是数字。"
            exit 1
        fi
        if ! ps -p "$PID" > /dev/null 2>&1; then
            echo "错误：PID $PID 不存在。"
            exit 1
        fi
    done
    
    # 终止进程
    for PID in $USER_PIDS; do
        echo "正在终止进程 (PID: $PID)..."
        kill -15 "$PID"
    done
    echo "操作完成。"
    exit 0
fi

# 转换 PID 为逗号分隔
PIDS_COMMA=$(echo $PIDS | tr ' ' ',')

echo "找到以下进程PID："
ps -p $PIDS_COMMA -o pid,cmd

for PID in $PIDS; do
    echo "正在终止进程 (PID: $PID)..."
    kill -15 "$PID"
done

echo "操作完成"

```

## 注意事项

- 此脚本使用`kill -9`命令强制终止进程，这可能会导致数据丢失或其他问题
- 在终止重要进程前，请确保已保存所有工作
- 在Linux系统中使用此脚本时，可能需要root权限来终止某些系统进程

## 项目仓库

CNB：https://cnb.cool/SDCOM/shit/-/blob/main/script/kill_app.sh

Github：https://github.com/SDCOM-0415/shit/blob/main/script/kill_app.sh

## © 作者

SDCOM