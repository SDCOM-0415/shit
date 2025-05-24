#!/bin/bash

echo "Get IP Version: v0.1"
echo "作者: SDCOM"
echo "CNB项目地址：https://cnb.cool/SDCOM/shit/-/blob/main/script/get_ip.sh"
echo "GitHub项目地址：https://github.com/SDCOM-0415/shit/blob/main/script/get_ip.sh"

# 脚本功能：获取所有网络接口的IP地址并以指定格式输出
# 输出格式：网络接口：IP地址

# 检查ifconfig命令是否可用
if ! command -v ifconfig &> /dev/null; then
    echo "错误：ifconfig命令不可用，请安装net-tools包"
    exit 1
fi

# 获取所有网络接口名称
interfaces=$(ifconfig | grep -E '^[a-zA-Z0-9]+:' | awk -F: '{print $1}')

# 遍历每个接口并获取其IP地址
for interface in $interfaces; do
    # 获取IPv4地址
    ip_addr=$(ifconfig $interface | grep -oP 'inet \K\d+\.\d+\.\d+\.\d+')
    
    # 如果接口有IP地址，则输出
    if [ ! -z "$ip_addr" ]; then
        echo "$interface：$ip_addr"
    fi
done

exit 0