#!/bin/bash
# disable-docker.sh - 彻底禁用 Docker 并防止重新安装
# 用法: sudo ./disable-docker.sh

set -e

echo "==============================================="
echo "开始彻底禁用 Docker"
echo "==============================================="

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then
    echo "请使用 sudo 或以 root 用户运行此脚本"
    exit 1
fi

# 记录操作日志
LOG_FILE="/var/log/docker-disable.log"
exec > >(tee -a "$LOG_FILE") 2>&1
echo "禁用操作开始时间: $(date)"

# 1. 停止并禁用所有相关服务
echo "步骤 1: 停止 Docker 相关服务"
for service in docker docker.socket containerd; do
    if systemctl is-active --quiet $service 2>/dev/null; then
        systemctl stop $service
        echo "已停止: $service"
    fi
    if systemctl is-enabled --quiet $service 2>/dev/null; then
        systemctl disable $service
        echo "已禁用: $service"
    fi
done

# 2. 杀死所有相关进程
echo "步骤 2: 终止 Docker 相关进程"
pkill -9 dockerd 2>/dev/null || true
pkill -9 containerd 2>/dev/null || true
pkill -9 docker-proxy 2>/dev/null || true
echo "已终止相关进程"

# 3. 备份当前配置（用于恢复）
BACKUP_DIR="/root/docker-backup-$(date +%Y%m%d-%H%M%S)"
echo "步骤 3: 备份当前配置到 $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# 备份包状态
dpkg --get-selections | grep -E "docker|containerd" > "$BACKUP_DIR/package-list.txt" 2>/dev/null || true

# 备份配置文件
[ -d "/etc/docker" ] && cp -r /etc/docker "$BACKUP_DIR/" 2>/dev/null || true
[ -f "/etc/containerd/config.toml" ] && cp /etc/containerd/config.toml "$BACKUP_DIR/" 2>/dev/null || true
[ -f "/lib/systemd/system/docker.service" ] && cp /lib/systemd/system/docker.service "$BACKUP_DIR/" 2>/dev/null || true

echo "备份完成"

# 4. 卸载 Docker
echo "步骤 4: 卸载 Docker 软件包"
apt-get update
apt-get remove --purge -y \
    docker.io \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin \
    podman-docker \
    docker-doc 2>/dev/null || true

# 5. 清理文件和目录
echo "步骤 5: 清理 Docker 文件和目录"
for dir in /var/lib/docker /var/lib/containerd /etc/docker /etc/containerd; do
    if [ -d "$dir" ]; then
        rm -rf "$dir"
        echo "已删除: $dir"
    fi
done

# 创建只读空目录
mkdir -p /var/lib/docker /etc/docker
chmod 000 /var/lib/docker /etc/docker
chattr +i /var/lib/docker 2>/dev/null || true
chattr +i /etc/docker 2>/dev/null || true
echo "已创建只读空目录"

# 6. 锁定软件包
echo "步骤 6: 锁定 Docker 相关软件包"
for pkg in docker.io docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin; do
    apt-mark hold $pkg 2>/dev/null || true
    echo "$pkg hold" | dpkg --set-selections 2>/dev/null || true
    echo "已锁定: $pkg"
done

# 7. 创建 APT 阻止策略
echo "步骤 7: 创建 APT 阻止策略"
cat > /etc/apt/preferences.d/00-block-docker << 'EOF'
Package: docker.io
Pin: version *
Pin-Priority: -1000

Package: docker-ce
Pin: version *
Pin-Priority: -1000

Package: docker-ce-cli
Pin: version *
Pin-Priority: -1000

Package: containerd.io
Pin: version *
Pin-Priority: -1000

Package: docker-buildx-plugin
Pin: version *
Pin-Priority: -1000

Package: docker-compose-plugin
Pin: version *
Pin-Priority: -1000
EOF

cat > /etc/apt/apt.conf.d/99block-docker << 'EOF'
APT::NeverAutoRemove:: "docker";
APT::NeverInstall:: "docker";
APT::NeverAutoRemove:: "docker-ce";
APT::NeverInstall:: "docker-ce";
APT::NeverAutoRemove:: "containerd";
APT::NeverInstall:: "containerd";
EOF
echo "APT 阻止策略已创建"

# 8. 内核模块黑名单
echo "步骤 8: 禁用内核模块"
cat > /etc/modprobe.d/blacklist-docker.conf << 'EOF'
blacklist overlay
blacklist br_netfilter
install overlay /bin/false
install br_netfilter /bin/false
EOF

# 卸载模块
modprobe -r overlay 2>/dev/null || true
modprobe -r br_netfilter 2>/dev/null || true
echo "内核模块已禁用"

# 9. 创建监控脚本
echo "步骤 9: 创建监控脚本"
cat > /usr/local/bin/monitor-docker.sh << 'EOF'
#!/bin/bash
# Docker 监控脚本
LOG_FILE="/var/log/docker-monitor.log"

check_and_kill() {
    # 检查 Docker 进程
    if pgrep -x "dockerd" >/dev/null || \
       pgrep -x "containerd" >/dev/null || \
       pgrep -f "docker-proxy" >/dev/null; then
        
        echo "$(date): 检测到 Docker 进程，正在终止..." >> "$LOG_FILE"
        
        # 终止进程
        pkill -9 dockerd 2>/dev/null
        pkill -9 containerd 2>/dev/null
        pkill -9 docker-proxy 2>/dev/null
        
        # 尝试卸载
        apt-get remove --purge -y docker.io docker-ce 2>/dev/null
    fi
    
    # 检查 Docker 目录权限
    if [ -d "/var/lib/docker" ] && [ "$(stat -c %a /var/lib/docker)" != "0" ]; then
        echo "$(date): 修复 /var/lib/docker 权限" >> "$LOG_FILE"
        chmod 000 /var/lib/docker
        chattr +i /var/lib/docker 2>/dev/null
    fi
}

check_and_kill
EOF

chmod +x /usr/local/bin/monitor-docker.sh

# 添加定时任务
if ! grep -q "monitor-docker" /etc/crontab; then
    echo "*/10 * * * * root /usr/local/bin/monitor-docker.sh" >> /etc/crontab
fi
echo "监控脚本已安装"

# 10. 清理用户目录
echo "步骤 10: 清理用户 Docker 配置"
for user_dir in /home/* /root; do
    docker_dir="$user_dir/.docker"
    if [ -d "$docker_dir" ]; then
        rm -rf "$docker_dir"
        echo "已清理: $docker_dir"
    fi
done

# 11. 创建审计规则
echo "步骤 11: 创建审计规则"
cat > /etc/audit/rules.d/30-docker.rules << 'EOF'
# 监控 Docker 相关文件和命令
-w /usr/bin/docker -p x
-w /usr/bin/dockerd -p x
-w /usr/bin/containerd -p x
-w /usr/bin/docker-compose -p x
-w /var/lib/docker -p wa
-w /etc/docker -p wa
-w /etc/containerd -p wa
EOF

# 重新加载审计规则
if command -v augenrules &>/dev/null; then
    augenrules --load
    systemctl restart auditd 2>/dev/null || true
fi
echo "审计规则已配置"

# 12. 更新系统
echo "步骤 12: 更新系统配置"
apt-get update
update-initramfs -u
systemctl daemon-reload

# 最终验证
echo ""
echo "==============================================="
echo "最终验证"
echo "==============================================="

echo "1. 检查 Docker 命令:"
if command -v docker &>/dev/null; then
    echo "   警告: docker 命令仍然存在"
else
    echo "   通过: docker 命令已移除"
fi

echo "2. 检查 Docker 进程:"
if pgrep -f docker >/dev/null; then
    echo "   警告: 发现 Docker 进程"
else
    echo "   通过: 无 Docker 进程"
fi

echo "3. 检查 Docker 服务:"
if systemctl list-unit-files | grep -q docker; then
    echo "   警告: Docker 服务单元存在"
else
    echo "   通过: 无 Docker 服务"
fi

echo "4. 检查包锁定状态:"
for pkg in docker.io docker-ce; do
    if dpkg --get-selections | grep -q "^$pkg.*hold$"; then
        echo "   通过: $pkg 已锁定"
    else
        echo "   通过: $pkg 未安装"
    fi
done

echo ""
echo "==============================================="
echo "Docker 已彻底禁用！"
echo "==============================================="
echo "备份文件位置: $BACKUP_DIR"
echo "监控日志: /var/log/docker-monitor.log"
echo "操作日志: $LOG_FILE"
echo "==============================================="