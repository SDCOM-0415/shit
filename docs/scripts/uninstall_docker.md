# uninstall_docker.sh

这是一个用于完全卸载Docker的脚本，测试支持`Debian 12`系统，当前版本<Badge type="tip" text="v1.0" />。

## 功能

- 停止所有Docker服务
- 卸载所有Docker相关软件包
- 删除Docker数据目录和配置文件
- 清理系统中的Docker残留文件
- 更新apt缓存

## 使用方法

CNB：
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/uninstall_docker.sh && sudo chmod +x ./uninstall_docker.sh && sudo ./uninstall_docker.sh
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/uninstall_docker.sh && sudo chmod +x ./uninstall_docker.sh && sudo ./uninstall_docker.sh
```

注意：此脚本需要使用sudo权限运行，因为它需要执行系统级操作。

## 执行过程

脚本执行时会显示以下步骤的进度：

1. 停止Docker服务
2. 卸载Docker相关软件包
3. 删除Docker数据目录
4. 删除配置文件和服务配置
5. 更新apt缓存

完成后，会显示确认消息："✅ Docker 已彻底卸载完毕，你可以重新安装。"

## 脚本内容

```bash
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

```

## 注意事项

- 此脚本会**完全删除**所有Docker相关的数据和配置，包括：
  - 所有Docker容器
  - 所有Docker镜像
  - 所有Docker卷
  - 所有Docker网络
  - 所有Docker配置
- 执行此脚本前，请确保已备份任何重要的Docker数据
- 脚本使用`|| true`语法确保即使某些命令失败，整个脚本也会继续执行
- 此脚本主要针对通过官方方法安装的Docker，如果使用其他方式安装，可能需要额外的清理步骤
