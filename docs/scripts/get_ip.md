# get_ip.sh

这是一个用于在termux中获取本机IP地址的脚本，当前版本为0.1。

## 功能

- 获取所有网络接口的IPv4地址
- 以清晰的格式显示网络接口名称和对应的IP地址
- 自动检查ifconfig命令是否可用

## 使用方法

```bash
chmod +x get_ip.sh
./get_ip.sh
```

运行后，脚本会显示所有具有IPv4地址的网络接口及其IP地址，格式为：`接口名称：IP地址`

## 输出示例

```
Get IP Version: 0.1
作者: SDCOM
CNB项目地址：https://cnb.cool/SDCOM/shit/-/blob/main/get_ip.sh
GitHub项目地址：https://github.com/SDCOM-0415/shit/blob/main/get_ip.sh

wlan0：192.168.1.100
eth0：10.0.0.15
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

## 项目地址

- CNB项目地址：[https://cnb.cool/SDCOM/shit/-/blob/main/get_ip.sh](https://cnb.cool/SDCOM/shit/-/blob/main/get_ip.sh)
- GitHub项目地址：[https://github.com/SDCOM-0415/shit/blob/main/get_ip.sh](https://github.com/SDCOM-0415/shit/blob/main/get_ip.sh)

## 作者

SDCOM