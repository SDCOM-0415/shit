# kill_app.sh

这个脚本用于在FydeOS中快速结束Linux子系统程序。

## 功能

- 允许用户输入进程名称，然后尝试找到并终止该进程
- 如果找不到精确匹配的进程，会显示可能相关的进程
- 支持通过PID直接终止进程

## 使用方法

```bash
chmod +x kill_app.sh
./kill_app.sh
```

运行脚本后，按照提示输入要终止的进程名称。如果找不到精确匹配的进程，脚本会列出可能相关的进程，并允许你输入PID来终止特定进程。

## 脚本内容

```bash
#!/bin/bash

# 提示用户输入进程名称
echo "请输入要终止的进程名称："
read process_name

# 尝试找到并终止进程
pid=$(ps -ef | grep "$process_name" | grep -v grep | awk '{print $2}')

if [ -z "$pid" ]; then
    echo "未找到进程：$process_name"
    echo "以下是可能相关的进程："
    ps -ef | grep -i "$process_name" | grep -v grep
    
    echo "请输入要终止的进程PID（如果没有要终止的进程，请直接按回车）："
    read pid_to_kill
    
    if [ -n "$pid_to_kill" ]; then
        kill -9 $pid_to_kill
        echo "已终止PID为 $pid_to_kill 的进程"
    else
        echo "未终止任何进程"
    fi
else
    kill -9 $pid
    echo "已终止进程：$process_name (PID: $pid)"
fi
```

## 注意事项

- 此脚本使用`kill -9`命令强制终止进程，这可能会导致数据丢失或其他问题
- 在终止重要进程前，请确保已保存所有工作
- 在FydeOS的Linux子系统中使用此脚本时，可能需要root权限来终止某些系统进程