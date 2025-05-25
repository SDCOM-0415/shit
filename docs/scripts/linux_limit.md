# linux_limit.sh

这是一个用于限制Linux目录大小的脚本，测试支持`Debian 12`，当前版本为<Badge type="tip" text="v1.0" />。

## 功能特点

- 支持交互式和命令行参数两种使用方式
- 使用fallocate方法创建固定大小的镜像文件
- 自动备份原始目录数据
- 支持多种大小单位（B/KB/MB/GB/TB）

## 使用方法

### 交互式模式

CNB：
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/linux_limit.sh && sudo chmod +x ./linux_limit.sh && sudo ./linux_limit.sh
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/linux_limit.sh && sudo chmod +x ./linux_limit.sh && sudo ./linux_limit.sh
```

运行脚本后，按照提示依次输入：
1. 需要限制的原始目录路径
2. 限制大小（支持B/KB/MB/GB/TB等单位）
3. 镜像存储路径（默认为./limit.img）

### 命令行参数模式

CNB：
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/linux_limit.sh && sudo chmod +x ./linux_limit.sh && sudo ./linux_limit.sh <原始目录> <大小> <镜像存储路径> 
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/linux_limit.sh && sudo chmod +x ./linux_limit.sh && sudo ./linux_limit.sh <原始目录> <大小> <镜像存储路径> 
```

例如：
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/linux_limit.sh && sudo chmod +x ./linux_limit.sh && sudo ./linux_limit.sh /path/to/directory 10GB /path/to/limit.img
```

## 参数说明

- `原始目录路径`：要限制大小的目录的完整路径
- `限制大小`：支持的单位包括：
  - B（字节）
  - KB（千字节）
  - MB（兆字节）
  - GB（吉字节）
  - TB（太字节）
- `镜像存储路径`：可选参数，默认为当前目录下的limit.img

## 脚本内容
```bash
#!/bin/bash

echo "limit Version: v1.0"
echo "作者: SDCOM"
echo "CNB项目地址：https://cnb.cool/SDCOM/shit/-/blob/main/script/linux_limit.sh"
echo "GitHub项目地址：https://github.com/SDCOM-0415/shit/blob/main/script/linux_limit.sh"

# 方法选择
METHOD=2  # 默认使用fallocate方法

# 交互式输入
interactive_input() {
    read -p "请输入需要限制的原始目录路径: " ORIGINAL_DIR
    read -p "请输入限制大小(支持B/KB/MB/GB/TB等): " SIZE_STR
    read -p "请输入镜像存储路径(默认./limit.img): " IMG_PATH
    IMG_PATH=${IMG_PATH:-"./limit.img"}
}

# 参数解析
if [ $# -eq 0 ]; then
    interactive_input
else
    ORIGINAL_DIR=$1
    SIZE_STR=$2
    IMG_PATH=${3:-"./limit.img"}
fi

# 验证原始目录
[ ! -d "$ORIGINAL_DIR" ] && echo "错误：原始目录不存在" && exit 1

# 创建限制空间
if [ $METHOD -eq 2 ]; then
    # 1. 创建镜像文件
    fallocate -l $SIZE_STR "$IMG_PATH"
    mkfs.ext4 "$IMG_PATH"
    
    # 2. 备份原始目录
    BACKUP_DIR="${ORIGINAL_DIR}_backup_$(date +%s)"
    mv "$ORIGINAL_DIR" "$BACKUP_DIR"
    
    # 3. 创建新目录并挂载
    mkdir -p "$ORIGINAL_DIR"
    mount -o loop "$IMG_PATH" "$ORIGINAL_DIR"
    
    # 4. 恢复原数据(可选)
    echo "正在恢复原始数据(可能需要时间)..."
    cp -a "$BACKUP_DIR"/. "$ORIGINAL_DIR"/
    
    echo "已成功限制目录 $ORIGINAL_DIR 大小为 $SIZE_STR"
    echo "原始数据备份在: $BACKUP_DIR"
fi

```

## 工作原理

1. 创建指定大小的镜像文件（使用fallocate）
2. 将镜像文件格式化为ext4文件系统
3. 备份原始目录（自动添加时间戳）
4. 创建新目录并挂载镜像文件
5. 恢复原始数据到新的受限目录

## 注意事项

- 需要root权限执行（因为涉及mount操作）
- 原始数据会被自动备份，备份目录名格式为：`原始目录名_backup_时间戳`
- 确保系统有足够的空间存储镜像文件
- 建议在操作前备份重要数据

## 项目仓库

CNB：https://cnb.cool/SDCOM/shit/-/blob/main/script/linux_limit.sh

Github：https://github.com/SDCOM-0415/shit/blob/main/script/linux_limit.sh

## © 作者

SDCOM