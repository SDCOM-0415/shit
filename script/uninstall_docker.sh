#!/bin/bash
# 完全卸载 Docker 的脚本
# 适用于 Debian 12 系统 (其他系统未测试)

echo "Docker Uninstall Script Version: v1.0"
echo "作者: SDCOM"
echo "CNB项目地址：https://cnb.cool/SDCOM/shit/-/blob/main/script/uninstall_docker.sh"
echo "GitHub项目地址：https://github.com/SDCOM-0415/shit/blob/main/script/uninstall_docker.sh"

echo "🛑 正在停止 Docker 服务..."
sudo systemctl stop docker || true

echo "❌ 正在卸载 Docker 相关软件包..."
sudo apt purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin || true
sudo apt autoremove -y --purge

echo "🧹 正在删除 Docker 数据目录..."
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd

echo "🗑️ 正在删除配置文件和服务配置..."
sudo rm -rf /etc/docker
sudo rm -rf /etc/systemd/system/docker.service.d
sudo rm -f  /etc/apt/sources.list.d/docker.list
sudo rm -f  /etc/apt/keyrings/docker.gpg
sudo rm -f  /etc/apt/keyrings/docker.asc

echo "🔄 更新 apt 缓存..."
sudo apt update

echo "✅ Docker 已彻底卸载完毕，你可以重新安装。"
