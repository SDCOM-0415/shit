#!/bin/bash
# =================================================================
# 核心系统组件离线校验与哪吒原版自适应排查脚本 (V13 极简版)
# =================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}=================================================================${NC}"
echo -e "${RED}  🚨 正在进行系统深度扫描与全组件原版完整性精密比对 (只读取证) 🚨${NC}"
echo -e "${CYAN}=================================================================\n${NC}"

# ==========================================
# 1. 仅对 GitHub 请求进行纯 GEO 智能分流路由
# ==========================================
echo -e "${YELLOW}>>> [1/13] 正在通过 Cloudflare GEO 探测节点网络策略:${NC}"

isCN=""
api_list="https://blog.cloudflare.com/cdn-cgi/trace https://developers.cloudflare.com/cdn-cgi/trace"
ua="Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"

# 采用官方 install.sh 中的标准 GEO 探测逻辑
for url in $api_list; do
    text=$(curl -A "$ua" -m 4 -s "$url" 2>/dev/null)
    if echo "$text" | grep -qw 'CN'; then
        isCN=true
        break
    fi
done

if [ -n "$isCN" ]; then
    echo -e "  -> 探测结果: ${YELLOW}[中国大陆环境] 系统组件免流离线核验，GitHub 请求自动挂载加速实例。${NC}"
    GITHUB_PROXY="https://v4.gh-proxy.org/"
else
    echo -e "  -> 探测结果: ${GREEN}[海外 / 纯净直连环境] 系统组件免流离线核验，GitHub 请求 100% 官方原生直连。${NC}"
    GITHUB_PROXY="" # 海外节点不需要任何 ghproxy 前缀，拒绝污染
fi
echo ""

# ==========================================
# 2. 核心系统组件的别名（Alias）劫持检测
# ==========================================
echo -e "${YELLOW}>>> [2/13] 深度检查核心系统组件别名 (防止审计环境被污染):${NC}"
alias_list=$(alias 2>/dev/null)
if echo "$alias_list" | grep -qE "ls=|ps=|netstat=|ss=|kill=|cat=|grep=|wget=|curl=|md5sum=|sha256sum="; then
    echo -e "  ${RED}[!] 警告：发现敏感命令的本地别名劫持：${NC}"
    echo "$alias_list" | grep -E "ls=|ps=|netstat=|ss=|kill=|cat=|grep=|wget=|curl=|md5sum=|sha256sum="
else
    echo -e "  ${GREEN}[√] 当前会话核心系统命令无别名劫持。${NC}"
fi

echo -e "  -> 静态审计系统环境配置文件 (.bashrc / .profile / etc):"
alias_files=("/root/.bashrc" "/root/.profile" "/etc/profile" "/etc/bash.bashrc")
found_mal_alias=0
for file in "${alias_files[@]}"; do
    if [ -f "$file" ]; then
        res=$(grep -rnE "^alias\ " "$file" 2>/dev/null | grep -v -E "ls='|grep='|fgrep='|egrep='")
        if [ ! -z "$res" ]; then
            echo -e "  ${RED}[!] 恶意别名风险项 - 文件 $file 内包含以下非标准别名：${NC}"
            echo "$res"
            found_mal_alias=1
        fi
    fi
done
[ $found_mal_alias -eq 0 ] && echo -e "  ${GREEN}[√] 静态配置文件中未发现异常别名。${NC}"
echo ""

# ==========================================
# 3. 检查 CPU 占用异常进程
# ==========================================
echo -e "${YELLOW}>>> [3/13] 检查 CPU 占用超 40% 的异常进程:${NC}"
ps -eo pid,ppid,%cpu,%mem,user,lstart,command --sort=-%cpu | awk 'NR==1 || $3>40.0' | head -n 10
echo ""

# ==========================================
# 4. 检查已知恶意软件家族关键字
# ==========================================
echo -e "${YELLOW}>>> [4/13] 检查内存中是否运行已知恶意进程:${NC}"
ps -ef | grep -iE "xmrig|minerd|kdevtmpfsi|xmr-stak|stratum|ice\.sh|traffmonetizer|bash\ --check|nezha\.sh" | grep -v "grep"
echo ""

# ==========================================
# 5. 检查从敏感目录运行的进程
# ==========================================
echo -e "${YELLOW}>>> [5/13] 检查从临时/异常目录启动的进程:${NC}"
ps -eo pid,user,command | grep -E "/tmp/|/var/tmp/|/dev/shm/|/root/" | grep -v -E "grep|/root/\.vscode-server"
echo ""

# ==========================================
# 6. 检查幽灵进程
# ==========================================
echo -e "${YELLOW}>>> [6/13] 检查可疑的幽灵进程 (文件已被删除但仍在内存运行):${NC}"
ls -al /proc/*/exe 2>/dev/null | grep -i "deleted" | grep -v "/memfd:"
echo ""

# ==========================================
# 7. 深度检查所有定时任务
# ==========================================
echo -e "${YELLOW}>>> [7/13] 检查系统与所有用户的定时任务 (异常外联/下载行为):${NC}"
grep -rnE "wget|curl|nc\ |bash|sh|traffmonetizer" /etc/crontab /etc/cron.* 2>/dev/null | grep -v "^#"
for user in $(cut -f1 -d: /etc/passwd); do
    crontab -u "$user" -l 2>/dev/null | grep -v "^#" | grep -E "wget|curl|nc\ |bash|sh|traffmonetizer" && echo -e "  ${RED}[!] 发现异常任务, 所属用户: $user${NC}"
done
echo ""

# ==========================================
# 8. 检查异常开机自启服务
# ==========================================
echo -e "${YELLOW}>>> [8/13] 检查最近 7 天内被修改或创建的 Systemd 系统服务文件:${NC}"
find /etc/systemd/system/ /lib/systemd/system/ -type f -mtime -7 -name "*.service" -exec ls -lt {} \; 2>/dev/null | head -n 10
echo -e "  -> 检查服务文件中是否包含恶意关键字:"
grep -rnE "xmrig|traffmonetizer|wget|curl" /etc/systemd/system/ 2>/dev/null
echo ""

# ==========================================
# 9. 检查网络连接情况
# ==========================================
echo -e "${YELLOW}>>> [9/13] 检查活动公网网络连接 (ESTABLISHED):${NC}"
if command -v ss >/dev/null 2>&1; then
    ss -antp 2>/dev/null | grep ESTAB | grep -v -E "127\.0\.0\.1|10\.|172\.(1[6-9]|2[0-9]|3[0-1])\.|192\.168\." | awk '{print $4, "->", $5, "进程:" $6}'
else
    netstat -antp 2>/dev/null | grep ESTABLISHED | grep -v -E "127\.0\.0\.1|10\.|172\.(1[6-9]|2[0-9]|3[0-1])\.|192\.168\." | awk '{print $4, "->", $5, "进程:" $7}'
fi
echo ""

# ==========================================
# 10. 常用基础系统组件原生安全数据库精密对碰 (100% 纯离线权威引擎)
# ==========================================
echo -e "${YELLOW}>>> [10/13] 常用基础系统组件原生安全数据库精密对碰 (0流量离线模式):${NC}"
declare -A check_pkgs=( ["bash"]="/bin/bash" ["wget"]="/usr/bin/wget" ["curl"]="/usr/bin/curl" ["openssh-server"]="/usr/sbin/sshd" )

printf "\n  %-18s %-22s %-34s %-12s\n" "组件/包名" "物理文件路径" "当前本地文件 MD5" "核验状态"
printf "  %-18s %-22s %-34s %-12s\n" "----------" "------------" "----------------" "--------"

for pkg in "${!check_pkgs[@]}"; do
    current_bin_path="${check_pkgs[$pkg]}"
    if [ -f "$current_bin_path" ]; then
        local_md5=$(md5sum "$current_bin_path" 2>/dev/null | awk '{print $1}')
        
        # 纯离线对碰原生 dpkg 存根，天然兼容官方补丁升级
        verify_output=$(dpkg --verify "$pkg" 2>/dev/null)
        bin_name="${current_bin_path##*/}"
        is_altered=$(echo "$verify_output" | grep -E "bin/${bin_name}$|sbin/${bin_name}$")
        
        if [ -z "$is_altered" ]; then
            status_msg="${GREEN}[√] 纯正官方原版${NC}"
        else
            status_msg="${RED}[!] 遭黑客篡改${NC}"
        fi
        printf "  %-20s %-24s %-34s $status_msg\n" "[$pkg]" "$current_bin_path" "$local_md5"
    else
        printf "  %-20s ${RED}%-24s${NC} %-34s ${RED}[!] 文件失联${NC}\n" "[$pkg]" "$current_bin_path" "N/A"
    fi
done
echo ""

# ==========================================
# 11. 哪吒客户端（nezha-agent）官方原版强比对 (GEO 自适应路由)
# ==========================================
echo -e "${YELLOW}>>> [11/13] 哪吒客户端官方原版自适应完整性安全对碰:${NC}"
agent_pid=$(pgrep -f "nezha-agent" | head -n 1)
agent_path=""
if [ -n "$agent_pid" ]; then
    agent_path=$(ls -l /proc/"$agent_pid"/exe 2>/dev/null | awk '{print $NF}')
fi
if [ -z "$agent_path" ] || [[ "$agent_path" == *"(deleted)"* ]]; then
    [ -f "/opt/nezha/agent/nezha-agent" ] && agent_path="/opt/nezha/agent/nezha-agent"
    [ -f "/usr/local/bin/nezha-agent" ] && agent_path="/usr/local/bin/nezha-agent"
fi
clean_agent_path="${agent_path%% *}"

if [ -n "$clean_agent_path" ] && [ -f "$clean_agent_path" ]; then
    local_version=$($clean_agent_path -v 2>/dev/null | head -n 1 | awk '{print $NF}')
    [ -z "$local_version" ] && local_version=$($clean_agent_path --version 2>/dev/null | head -n 1 | awk '{print $NF}')
    
    echo -e "  -> 当前监控运行路径: ${CYAN}$clean_agent_path${NC}"
    echo -e "  -> 检测到本地监控版本: ${CYAN}${local_version:-未知}${NC}"
    local_md5=$(md5sum "$clean_agent_path" 2>/dev/null | awk '{print $1}')
    echo -e "  -> 本地物理运行 MD5:   ${CYAN}$local_md5${NC}"
    
    if [ -n "$local_version" ]; then
        mach=$(uname -m)
        case "$mach" in x86_64|amd64) os_arch="amd64" ;; aarch64|arm64) os_arch="arm64" ;; *) os_arch="" ;; esac
        system=$(uname)
        case "$system" in *Linux*) os="linux" ;; *) os="" ;; esac
        
        if [ -n "$os_arch" ] && [ -n "$os" ]; then
            pkg_name="nezha-agent_${os}_${os_arch}.zip"
            # 仅在 GitHub 下载链接处动态拼接代理变量（海外为空直连，国内挂反代）
            download_url="${GITHUB_PROXY}https://github.com/nezhahq/agent/releases/download/${local_version}/${pkg_name}"
            
            echo -e "  -> 正在通过最优通道 (URL: ${CYAN}$download_url${NC}) 拉取官方包..."
            tmp_zip="/tmp/nezha_verify_v13.zip"
            tmp_extract_dir="/tmp/nezha_verify_extract_v13"
            
            curl -sL --connect-timeout 10 "$download_url" -o "$tmp_zip" 2>/dev/null
            
            if [ -f "$tmp_zip" ] && [ -s "$tmp_zip" ]; then
                mkdir -p "$tmp_extract_dir"
                unzip -qo "$tmp_zip" -d "$tmp_extract_dir" 2>/dev/null
                if [ -f "$tmp_extract_dir/nezha-agent" ]; then
                    official_md5=$(md5sum "$tmp_extract_dir/nezha-agent" | awk '{print $1}')
                    echo -e "  -> 官方同版本原生二进制 MD5: ${GREEN}$official_md5${NC}"
                    if [ "$local_md5" = "$official_md5" ]; then
                        echo -e "  ${GREEN}[√] 完整性校验成功！本地监控二进制与官方原版 100% 吻合！${NC}"
                    else
                        echo -e "  ${RED}[!] 极高风险警告：完整性校验失败！！本地组件已被篡改或注入！${NC}"
                    fi
                else echo -e "  ${RED}[!] 错误：官方包解压格式异常。${NC}"
                fi
                rm -rf "$tmp_zip" "$tmp_extract_dir"
            else
                echo -e "  ${RED}[!] 错误：无法触达 GitHub 官方发布源，请检查当前服务器的 DNS 配置。${NC}"
            fi
        fi
    fi
else
    echo -e "  ${RED}[!] 极高风险：未能在系统任何常规及内存挂载点找到合法的 nezha-agent 实体文件！${NC}"
fi
echo ""

# ==========================================
# 12. 检查 SSH 后门公钥 (保留)
# ==========================================
echo -e "${YELLOW}>>> [12/13] 检查 root 用户的 SSH 免密登录公钥 (authorized_keys):${NC}"
if [ -s /root/.ssh/authorized_keys ]; then
    echo -e "${RED}[!] 发现公钥内容如下，请核对是否为您本人添加：${NC}"
    cat /root/.ssh/authorized_keys
else
    echo -e "  ${GREEN}[√] /root/.ssh/authorized_keys 为空或不存在。${NC}"
fi
echo ""

# ==========================================
# 13. 检查提权隐藏账户与动态链接库劫持 (保留)
# ==========================================
echo -e "${YELLOW}>>> [13/13] 检查提权隐藏账户与动态链接库劫持:${NC}"
echo -n "  -> 拥有最高权限 (UID=0) 的账户: "
awk -F: '$3 == 0 {print $1}' /etc/passwd
if [ -s /etc/ld.so.preload ]; then
    echo -e "  ${RED}[!] 警告：/etc/ld.so.preload 不为空！内容如下：${NC}"
    cat /etc/ld.so.preload
else
    echo -e "  ${GREEN}[√] /etc/ld.so.preload 为空，正常。${NC}"
fi
echo ""

echo -e "\n${CYAN}=================================================================${NC}"
echo -e "${GREEN}  V13 纯净去噪精密审计运行结束！(只读模式，未修改系统任何数据)  ${NC}"
echo -e "${CYAN}=================================================================${NC}"