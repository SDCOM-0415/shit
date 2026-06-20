#!/bin/bash
# =================================================================
# 深度系统安全与后门排查脚本 (V2 增强版 - 纯只读模式)
# =================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}=================================================================${NC}"
echo -e "${RED}  🚨 正在进行系统深度扫描 (只读模式，无破坏性操作) 🚨${NC}"
echo -e "${CYAN}=================================================================\n${NC}"

# 1. 检查畸高资源占用进程 (挖矿/空转脚本)
echo -e "${YELLOW}>>> [1/12] 检查 CPU 占用超 40% 的异常进程:${NC}"
ps -eo pid,ppid,%cpu,%mem,user,lstart,command --sort=-%cpu | awk 'NR==1 || $3>40.0' | head -n 10
echo ""

# 2. 检查已知恶意软件家族关键字 (涵盖 XMRig, Traffmonetizer, 常见后门)
echo -e "${YELLOW}>>> [2/12] 检查内存中是否运行已知恶意进程:${NC}"
ps -ef | grep -iE "xmrig|minerd|kdevtmpfsi|xmr-stak|stratum|ice\.sh|traffmonetizer|bash\ --check|nezha\.sh" | grep -v "grep"
echo ""

# 3. 检查敏感目录运行的进程 (木马及伪装系统进程)
echo -e "${YELLOW}>>> [3/12] 检查从临时/异常目录 (/tmp, /dev/shm, /var/tmp, /root/) 启动的进程:${NC}"
ps -eo pid,user,command | grep -E "/tmp/|/var/tmp/|/dev/shm/|/root/" | grep -v -E "grep|/root/\.vscode-server"
echo ""

# 4. 检查幽灵进程 (Fileless 无文件落地攻击)
echo -e "${YELLOW}>>> [4/12] 检查可疑的幽灵进程 (执行文件已被删除但仍在内存中运行):${NC}"
ls -al /proc/*/exe 2>/dev/null | grep -i "deleted" | grep -v "/memfd:"
echo ""

# 5. 深度检查所有定时任务 (用户级 + 系统级)
echo -e "${YELLOW}>>> [5/12] 检查系统与所有用户的定时任务 (异常下载/执行/外联行为):${NC}"
# 系统级
grep -rnE "wget|curl|nc\ |bash|sh|traffmonetizer" /etc/crontab /etc/cron.* 2>/dev/null | grep -v "^#"
# 用户级
for user in $(cut -f1 -d: /etc/passwd); do
    crontab -u $user -l 2>/dev/null | grep -v "^#" | grep -E "wget|curl|nc\ |bash|sh|traffmonetizer" && echo -e "  ${RED}[!] 发现异常任务, 所属用户: $user${NC}"
done
echo ""

# 6. 检查异常开机自启服务 (Systemd 劫持)
echo -e "${YELLOW}>>> [6/12] 检查最近 7 天内被修改或创建的 Systemd 系统服务文件:${NC}"
find /etc/systemd/system/ /lib/systemd/system/ -type f -mtime -7 -name "*.service" -exec ls -lt {} \; 2>/dev/null | head -n 10
echo -e "  -> ${CYAN}检查服务文件中是否包含恶意关键字:${NC}"
grep -rnE "xmrig|traffmonetizer|wget|curl" /etc/systemd/system/ 2>/dev/null
echo ""

# 7. 检查网络连接情况 (外联 C2 与矿池)
echo -e "${YELLOW}>>> [7/12] 检查异常公网网络连接 (ESTABLISHED):${NC}"
if command -v ss >/dev/null 2>&1; then
    ss -antp | grep ESTAB | grep -v -E "127\.0\.0\.1|10\.|172\.(1[6-9]|2[0-9]|3[0-1])\.|192\.168\." | awk '{print $4, "->", $5, "进程:" $6}'
else
    netstat -antp 2>/dev/null | grep ESTABLISHED | grep -v -E "127\.0\.0\.1|10\.|172\.(1[6-9]|2[0-9]|3[0-1])\.|192\.168\." | awk '{print $4, "->", $5, "进程:" $7}'
fi
echo ""

# 8. 检查 SSH 后门公钥 (重点排查)
echo -e "${YELLOW}>>> [8/12] 检查 root 用户的 SSH 免密登录公钥 (authorized_keys):${NC}"
if [ -s /root/.ssh/authorized_keys ]; then
    echo -e "${RED}[!] 发现公钥内容如下，请核对是否为您本人添加：${NC}"
    cat /root/.ssh/authorized_keys
else
    echo -e "${GREEN}[√] /root/.ssh/authorized_keys 为空或不存在。${NC}"
fi
echo ""

# 9. 检查隐藏的提权后门账户 (UID为0的黑客账户)
echo -e "${YELLOW}>>> [9/12] 检查系统中拥有最高权限 (UID=0) 的账户:${NC}"
awk -F: '$3 == 0 {print $1}' /etc/passwd
echo ""

# 10. 检查 Rootkit 动态链接库劫持
echo -e "${YELLOW}>>> [10/12] 检查动态链接库劫持 (/etc/ld.so.preload):${NC}"
if [ -s /etc/ld.so.preload ]; then
    echo -e "${RED}[!] 警告：/etc/ld.so.preload 不为空！极有可能存在底层后门，内容如下：${NC}"
    cat /etc/ld.so.preload
else
    echo -e "${GREEN}[√] /etc/ld.so.preload 为空，正常。${NC}"
fi
echo ""

# 11. 检查环境变量与别名劫持 (防呆木马)
echo -e "${YELLOW}>>> [11/12] 检查 Shell 启动文件是否被恶意植入隐藏代码:${NC}"
grep -iE "alias|curl|wget|bash" /root/.bashrc /root/.profile /etc/profile /etc/bash.bashrc 2>/dev/null | grep -v "^#" | head -n 10
echo ""

# 12. 检查操作记录是否被抹除
echo -e "${YELLOW}>>> [12/12] 检查 Bash 历史记录文件状态:${NC}"
ls -la /root/.bash_history 2>/dev/null
echo ""

echo -e "${CYAN}=================================================================${NC}"
echo -e "${GREEN}排查扫描完毕！(当前脚本为只读模式，未对系统进行任何修改)${NC}"
echo -e "请截图或保存以上输出日志，人工核对后再编写清理脚本。"
echo -e "${CYAN}=================================================================${NC}"
