#!/bin/bash

read -p "请输入要终止的进程名称: " PROCESS_NAME

if [ -z "$PROCESS_NAME" ]; then
    echo "错误：进程名称不能为空！"
    exit 1
fi

PIDS=$(pgrep -x "$PROCESS_NAME")

if [ -z "$PIDS" ]; then
    echo "错误：未找到进程 '$PROCESS_NAME'"
    exit 1
fi

# 将空格分隔的PID转换为逗号分隔（修复ps参数问题）
PIDS_COMMA=$(echo $PIDS | tr ' ' ',')

echo "找到以下进程PID："
ps -p $PIDS_COMMA -o pid,cmd  # 使用逗号分隔的PID列表

for PID in $PIDS; do
    echo "正在终止进程 (PID: $PID)..."
    kill -15 "$PID"
done

echo "操作完成"
