# get_ip.sh

这是一个用于在termux中快速获取本机IP地址的脚本，测试支持`termux`，当前版本为<Badge type="tip" text="v0.1" />。

## 功能

- 获取所有网络接口的IPv4地址
- 以清晰的格式显示网络接口名称和对应的IP地址
- 自动检查ifconfig命令是否可用

## 使用方法

CNB：
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/get_ip.sh && sudo chmod +x ./get_ip.sh && sudo ./get_ip.sh
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/get_ip.sh && sudo chmod +x ./get_ip.sh && sudo ./get_ip.sh
```

运行后，脚本会显示所有具有IPv4地址的网络接口及其IP地址，格式为：`接口名称：IP地址`

## 脚本内容

```bash
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
```

## 工作原理

1. 检查系统中是否安装了`ifconfig`命令
2. 使用`ifconfig`获取所有网络接口名称
3. 遍历每个接口，提取其IPv4地址
4. 以指定格式输出接口名称和IP地址

## 依赖项

- `net-tools`包（提供`ifconfig`命令）

## 注意事项

- 如果系统中没有安装`ifconfig`命令，脚本会提示安装`net-tools`包
- 脚本只显示具有IPv4地址的接口，没有IP地址的接口不会显示
- 此脚本主要设计用于termux环境，但也可以在其他Linux系统中使用
