#!/bin/bash

echo "limit Version: v0.1"
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
