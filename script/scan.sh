#!/bin/bash
# =================================================================
# 核心系统组件与哪吒客户端完整性安全校验脚本 (V4 实例优化版)
# =================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}=================================================================${NC}"
echo -e "${GREEN}    🛡️ 核心系统组件与哪吒客户端完整性智能审计系统 (只读) 🛡️${NC}"
echo -e "${CYAN}=================================================================\n${NC}"

# ==========================================
# 维度一：核心系统组件的别名（Alias）劫持检测
# ==========================================
echo -e "${YELLOW}>>> [1/5] 深度检查核心系统组件别名 (防止审计环境被污染):${NC}"
alias_list=$(alias 2>/dev/null)
if echo "$alias_list" | grep -qE "ls=|ps=|netstat=|ss=|kill=|cat=|grep=|wget=|curl=|md5sum=|sha256sum="; then
    echo -e "  ${RED}[!] 警告：发现敏感命令的本地别名劫持：${NC}"
    echo "$alias_list" | grep -E "ls=|ps=|netstat=|ss=|kill=|cat=|grep=|wget=|curl=|md5sum=|sha256sum="
else
    echo -e "  ${GREEN}[√] 当前会话核心系统命令无别名劫持。${NC}"
fi
echo ""

# ==========================================
# 维度二：国内外网络地理位置智能探测 (联动官方安装脚本逻辑)
# ==========================================
echo -e "${YELLOW}>>> [2/5] 智能探测网络环境与官方源联通性:${NC}"
isCN=""
api_list="https://blog.cloudflare.com/cdn-cgi/trace https://developers.cloudflare.com/cdn-cgi/trace"
ua="Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"

for url in $api_list; do
    text=$(curl -A "$ua" -m 5 -s "$url" 2>/dev/null)
    if echo "$text" | grep -qw 'CN'; then
        isCN=true
        break
    fi
done

if [ -n "$isCN" ]; then
    echo -e "  -> 探测结果: ${YELLOW}中国大陆网络环境 (启用指定国内 Ghproxy 加速实例)${NC}"
    # 按照您提供的专属实例进行前缀拼接定义
    MIRROR_PROXY="https://v4.gh-proxy.org/" 
else
    echo -e "  -> 探测结果: ${GREEN}国际网络环境 (直连 GitHub 官方仓库)${NC}"
    MIRROR_PROXY=""
fi
echo ""

# ==========================================
# 维度三：常用基础系统组件的完整性校验 (bash, wget, curl, sshd)
# ==========================================
echo -e "${YELLOW}>>> [3/5] 常用基础系统组件路径及哈希提取 (排查是否被黑客偷梁换柱):${NC}"
core_deps=("bash" "wget" "curl" "sshd")

printf "  %-10s %-25s %-32s\n" "组件名" "绝对物理路径" "本地文件 MD5 摘要"
printf "  %-10s %-25s %-32s\n" "------" "------------" "----------------"

for dep in "${core_deps[@]}"; do
    dep_path=$(command -v "$dep" 2>/dev/null)
    if [ -z "$dep_path" ] && [ "$dep" = "sshd" ]; then
        [ -f "/usr/sbin/sshd" ] && dep_path="/usr/sbin/sshd"
        [ -f "/usr/bin/sshd" ] && dep_path="/usr/bin/sshd"
    fi
    
    if [ -n "$dep_path" ] && [ -f "$dep_path" ]; then
        dep_md5=$(md5sum "$dep_path" 2>/dev/null | awk '{print $1}')
        printf "  %-12s %-27s ${CYAN}%-32s${NC}\n" "[$dep]" "$dep_path" "$dep_md5"
    else
        printf "  %-12s ${RED}%-27s${NC} %-32s\n" "[$dep]" "未找到或已被物理删除" "N/A"
    fi
done
echo -e "  ${YELLOW}[💡 集群比对提示]：相同系统版本的不同服务器，正常组件 MD5 应全等。若某一节点发生偏离，说明被恶意篡改。${NC}"
echo ""

# ==========================================
# 维度四：哪吒客户端（nezha-agent）版本与云端官方哈希校验
# ==========================================
echo -e "${YELLOW}>>> [4/5] 哪吒客户端 (nezha-agent) 实体与内存映像双重校验:${NC}"

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
    echo -e "  -> 哪吒组件真实可执行路径: ${CYAN}$clean_agent_path${NC}"
    
    local_version=$($clean_agent_path -v 2>/dev/null | head -n 1 | awk '{print $NF}')
    [ -z "$local_version" ] && local_version=$($clean_agent_path --version 2>/dev/null | head -n 1 | awk '{print $NF}')
    echo -e "  -> 本地二进制检测版本:     ${CYAN}${local_version:-未知}${NC}"
    
    local_md5=$(md5sum "$clean_agent_path" 2>/dev/null | awk '{print $1}')
    local_sha256=$(sha256sum "$clean_agent_path" 2>/dev/null | awk '{print $1}')
    echo -e "  -> 本地可执行实体 MD5:     ${CYAN}$local_md5${NC}"
    echo -e "  -> 本地可执行实体 SHA256:  ${CYAN}$local_sha256${NC}"
    
    if [ -n "$local_version" ]; then
        mach=$(uname -m)
        case "$mach" in
            x86_64|amd64) os_arch="amd64" ;;
            aarch64|arm64) os_arch="arm64" ;;
            *) os_arch="" ;;
        esac
        
        system=$(uname)
        case "$system" in
            *Linux*) os="linux" ;;
            *Darwin*) os="darwin" ;;
            *) os="" ;;
        esac
        
        if [ -n "$os_arch" ] && [ -n "$os" ]; then
            pkg_name="nezha-agent_${os}_${os_arch}.zip"
            # 严格按照完整链接格式拼接：前缀 + 完整的 GitHub 线上 HTTPS 链接
            hash_url="${MIRROR_PROXY}https://github.com/nezhahq/agent/releases/download/${local_version}/sha256sum.txt"
            
            echo -e "  -> 正在通过安全通道拉取官方哈希验证集 (URL: ${CYAN}$hash_url${NC})..."
            remote_hashes=$(curl -sL --connect-timeout 5 "$hash_url" 2>/dev/null)
            
            if [ -n "$remote_hashes" ]; then
                remote_sha256=$(echo "$remote_hashes" | grep "$pkg_name" | awk '{print $1}')
                if [ -n "$remote_sha256" ]; then
                    echo -e "  -> 官方 Release 发布包 (${pkg_name}) 预估 SHA256: ${GREEN}$remote_sha256${NC}"
                else
                    echo -e "  ${YELLOW}[!] 提示：成功连接官方仓库，但该版本校验文件中未找到对应架构的哈希配对。${NC}"
                fi
            else
                echo -e "  ${RED}[!] 警告：云端哈希连接超时。当前网络可能被阻断或控制，建议直接采用集群内多机 MD5 离线交叉取证法。${NC}"
            fi
        fi
    fi
else
    echo -e "  ${RED}[!] 极高风险：未能在系统任何常规及内存挂载点找到合法的 nezha-agent 实体文件！${NC}"
fi
echo ""

# ==========================================
# 维度五：幽灵后门与残留常驻 C2 实时监测
# ==========================================
echo -e "${YELLOW}>>> [5/5] 内存隐藏后门与黑客外联 C2 流定向扫描:${NC}"
ghost_processes=$(ls -al /proc/*/exe 2>/dev/null | grep -i "deleted" | grep -v -E "/memfd:|/dev/shm")
if [ -n "$ghost_processes" ]; then
    echo -e "  ${RED}[!] 警告：发现系统存在隐藏的、即用即删的“无文件落地”幽灵进程：${NC}"
    echo "$ghost_processes"
else
    echo -e "  ${GREEN}[√] 未发现内存无文件幽灵进程。${NC}"
fi

if command -v ss >/dev/null 2>&1; then
    net_connections=$(ss -antp 2>/dev/null | grep ESTAB | grep -E "103\.106\.|45\.196\.|61\.132\.|86\.54\.|supportxmr")
else
    net_connections=$(netstat -antp 2>/dev/null | grep ESTABLISHED | grep -E "103\.106\.|45\.196\.|61\.132\.|86\.54\.|supportxmr")
fi

if [ -n "$net_connections" ]; then
    echo -e "  ${RED}[!] 警告：检测到本机正与黑客的控制端或外部矿池保持活动网络连接：${NC}"
    echo "$net_connections"
else
    echo -e "  ${GREEN}[√] 本机当前未发现任何与已知黑客控制端的网络长连接。${NC}"
fi

echo -e "\n${CYAN}=================================================================${NC}"
echo -e "${GREEN}  智能完整性安全核验运行结束！(只读模式，未对系统数据执行任何修改)  ${NC}"
echo -e "${CYAN}=================================================================${NC}"