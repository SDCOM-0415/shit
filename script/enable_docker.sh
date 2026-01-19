#!/bin/bash
# enable-docker.sh - 重新启用 Docker
# 用法: sudo ./enable-docker.sh

set -e

echo "==============================================="
echo "开始重新启用 Docker"
echo "==============================================="

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then
    echo "请使用 sudo 或以 root 用户运行此脚本"
    exit 1
fi

# 记录操作日志
LOG_FILE="/var/log/docker-enable.log"
exec > >(tee -a "$LOG_FILE") 2>&1
echo "启用操作开始时间: $(date)"

# 1. 移除监控脚本
echo "步骤 1: 移除监控脚本"
if [ -f "/usr/local/bin/monitor-docker.sh" ]; then
    rm -f /usr/local/bin/monitor-docker.sh
    echo "已移除监控脚本"
fi

# 从 crontab 移除监控任务
sed -i '/monitor-docker\.sh/d' /etc/crontab
echo "已移除定时监控任务"

# 2. 解锁软件包
echo "步骤 2: 解锁 Docker 软件包"
for pkg in docker.io docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin; do
    apt-mark unhold $pkg 2>/dev/null || true
    echo "$pkg install" | dpkg --set-selections 2>/dev/null || true
    echo "已解锁: $pkg"
done

# 3. 移除阻止策略
echo "步骤 3: 移除阻止策略"
rm -f /etc/apt/preferences.d/00-block-docker
rm -f /etc/apt/apt.conf.d/99block-docker
echo "已移除 APT 阻止策略"

# 4. 移除内核模块黑名单
echo "步骤 4: 恢复内核模块"
rm -f /etc/modprobe.d/blacklist-docker.conf
echo "已移除内核模块限制"

# 5. 移除审计规则
echo "步骤 5: 移除审计规则"
rm -f /etc/audit/rules.d/30-docker.rules
if command -v augenrules &>/dev/null; then
    augenrules --load
    systemctl restart auditd 2>/dev/null || true
fi
echo "已移除审计规则"

# 6. 恢复文件目录权限
echo "步骤 6: 恢复文件目录权限"
for dir in /var/lib/docker /etc/docker; do
    if [ -d "$dir" ]; then
        chattr -i "$dir" 2>/dev/null || true
        chmod 755 "$dir"
        echo "已恢复权限: $dir"
    fi
done

# 7. 检查并安装 Docker
echo "步骤 7: 安装 Docker"
apt-get update

# 检查可用的 Docker 包
AVAILABLE_PKG=$(apt-cache search ^docker.io$ | head -1 | awk '{print $1}')
if [ -n "$AVAILABLE_PKG" ]; then
    echo "正在安装 Docker: $AVAILABLE_PKG"
    apt-get install -y $AVAILABLE_PKG
else
    echo "正在安装 Docker.io"
    apt-get install -y docker.io
fi

# 8. 安装相关工具
echo "步骤 8: 安装相关工具"
apt-get install -y docker-compose containerd 2>/dev/null || true

# 9. 启动并启用服务
echo "步骤 9: 启动 Docker 服务"
systemctl daemon-reload
systemctl enable docker
systemctl start docker
systemctl status docker --no-pager

# 10. 验证安装
echo ""
echo "==============================================="
echo "验证 Docker 安装"
echo "==============================================="

echo "1. Docker 版本:"
docker --version 2>/dev/null && echo "   通过" || echo "   失败"

echo "2. Docker 服务状态:"
if systemctl is-active --quiet docker; then
    echo "   通过: Docker 服务正在运行"
else
    echo "   警告: Docker 服务未运行"
fi

echo "3. 测试 Docker 运行:"
if docker run --rm hello-world 2>&1 | grep -q "Hello from Docker"; then
    echo "   通过: Docker 可以正常运行容器"
else
    echo "   警告: Docker 运行测试失败"
fi

echo ""
echo "==============================================="
echo "Docker 已重新启用！"
echo "==============================================="
echo "Docker 版本: $(docker --version 2>/dev/null || echo '未知')"
echo "服务状态: $(systemctl is-active docker)"
echo "操作日志: $LOG_FILE"
echo ""
echo "警告: 之前的备份文件可能需要手动恢复"
echo "备份文件可能在: /root/docker-backup-*"
echo "==============================================="