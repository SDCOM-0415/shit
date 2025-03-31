#!/bin/bash

echo "Kill_app Version: 0.2"
echo "作者: SDCOM"
echo "项目地址：https://cnb.cool/SDCOM/shit/-/blob/main/kill_app.sh"

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
