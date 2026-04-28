# port_forward.sh

这是一个 VPN 端口转发管理工具（Pro 全能版），用于在 Linux 系统上管理 iptables 端口转发规则，测试支持 `Debian 12` `Ubuntu 22.04`，当前版本为<Badge type="tip" text="v1.0" />。

## 功能

- 自动检测云服务器公网网卡
- 支持 TCP、UDP 协议及全部协议转发
- 支持单端口、多端口和端口范围转发
- 智能处理端口映射（1:1映射或自定义目标端口）
- 自动配置 VPN 网段流量回环（MASQUERADE）
- 可视化查看和删除已生效的转发规则
- 友好的菜单界面操作

## 使用方法

CNB：
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/port_forward.sh && sudo chmod +x ./port_forward.sh && sudo ./port_forward.sh
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/port_forward.sh && sudo chmod +x ./port_forward.sh && sudo ./port_forward.sh
```

运行脚本后，按照菜单提示进行操作：
- 选择 `1` 添加新的端口转发规则
- 选择 `2` 查看并删除现有转发规则
- 选择 `3` 退出脚本

## 脚本内容

```bash
#!/bin/bash

# 自动获取默认公网网卡名称
WAN_IF=$(ip route get 8.8.8.8 | grep -Po 'dev \K\w+' | head -n 1)

echo "========================================"
echo "    VPN 端口转发管理工具 (Pro 全能版)"
echo "========================================"
echo "检测到云服务器公网网卡: $WAN_IF"
echo ""

# 开启 Linux 内核路由转发
echo 1 > /proc/sys/net/ipv4/ip_forward

# --- 函数：添加转发规则 ---
add_rule() {
    echo ""
    echo ">>> [添加规则]"
    read -p "1. 转发协议 (tcp / udp / all): " PROTOCOL
    
    echo "   (支持单端口: 8080)"
    echo "   (支持多端口: 80,443,3389)"
    echo "   (支持范围段: 10000:50000)"
    read -p "2. 公网访问端口: " PUBLIC_PORT
    
    # 容错处理：将用户可能习惯性输入的横杠 "-" 替换为 iptables 识别的冒号 ":"
    PUBLIC_PORT=$(echo "$PUBLIC_PORT" | tr '-' ':')
    
    read -p "3. 本地电脑的 VPN IP (如 192.168.42.10): " TARGET_IP

    # 智能判断：是否包含逗号或冒号
    if [[ "$PUBLIC_PORT" == *","* ]] || [[ "$PUBLIC_PORT" == *":"* ]]; then
        echo "   -> [检测到多端口/段] 本地接收端口将与公网端口 1:1 保持一致。"
        TARGET_PORT_ARGS=""
        MATCH_ARGS="-m multiport --dports $PUBLIC_PORT"
        DISPLAY_PORT="$PUBLIC_PORT (1:1映射)"
    else
        read -p "4. 本地电脑的接收端口 (回车默认与公网 $PUBLIC_PORT 一致): " TARGET_PORT
        TARGET_PORT=${TARGET_PORT:-$PUBLIC_PORT}
        TARGET_PORT_ARGS=":$TARGET_PORT"
        MATCH_ARGS="--dport $PUBLIC_PORT"
        DISPLAY_PORT="$PUBLIC_PORT -> $TARGET_PORT"
    fi

    execute_add() {
        local proto=$1
        # DNAT 映射: 当 TARGET_PORT_ARGS 为空时，iptables 默认保持原始端口号
        iptables -t nat -A PREROUTING -i $WAN_IF -p $proto $MATCH_ARGS -j DNAT --to-destination $TARGET_IP$TARGET_PORT_ARGS
        
        # 放行 FORWARD 链
        iptables -A FORWARD -i $WAN_IF -p $proto -d $TARGET_IP $MATCH_ARGS -j ACCEPT
        
        echo "✅ 已生效: [$proto] 公网 $DISPLAY_PORT  (目标IP: $TARGET_IP)"
    }

    if [ "$PROTOCOL" == "all" ]; then
        execute_add "tcp"
        execute_add "udp"
    elif [ "$PROTOCOL" == "tcp" ] || [ "$PROTOCOL" == "udp" ]; then
        execute_add "$PROTOCOL"
    else
        echo "❌ 错误: 协议只能输入 tcp, udp 或 all。"
        return
    fi

    # 检查并配置回环
    iptables -t nat -C POSTROUTING -s 192.168.42.0/24 -o $WAN_IF -j MASQUERADE 2>/dev/null || {
        iptables -t nat -A POSTROUTING -s 192.168.42.0/24 -o $WAN_IF -j MASQUERADE
        echo "✅ (系统) 已补充配置 VPN 网段全局流量回环。"
    }
}

# --- 函数：删除转发规则 ---
delete_rule() {
    echo ""
    echo ">>> [当前生效的端口转发规则]"
    echo "------------------------------------------------------------"
    iptables -t nat -nL PREROUTING --line-numbers
    echo "------------------------------------------------------------"
    
    read -p "请输入要删除的规则序号 (第一列的 num) [输入 0 取消]: " RULE_NUM
    
    if [[ "$RULE_NUM" =~ ^[0-9]+$ ]]; then
        if [ "$RULE_NUM" -eq 0 ]; then
            echo "已取消删除。"
            return
        fi
        iptables -t nat -D PREROUTING $RULE_NUM 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "✅ 成功删除序号为 $RULE_NUM 的规则！(注: 删除 NAT 后，FORWARD 链的放行记录依然存在但不影响使用，重启后会自动清理纯净)"
        else
            echo "❌ 删除失败，请检查输入的序号是否存在。"
        fi
    else
        echo "❌ 错误: 请输入有效的数字序号。"
    fi
}

# --- 主程序：菜单循环 ---
while true; do
    echo ""
    echo "========== 操作菜单 =========="
    echo "  1) ➕ 添加新的端口转发"
    echo "  2) ➖ 查看并删除现有转发"
    echo "  3) 🚪 退出脚本"
    echo "=============================="
    read -p "请选择操作 [1-3]: " CHOICE

    case $CHOICE in
        1) add_rule ;;
        2) delete_rule ;;
        3) echo "👋 运行结束，再见！"; exit 0 ;;
        *) echo "❌ 无效的选项，请重新输入。" ;;
    esac
done
```

## 工作原理

1. **自动检测公网网卡**：通过 `ip route get 8.8.8.8` 获取默认路由使用的网卡
2. **开启路由转发**：设置 `/proc/sys/net/ipv4/ip_forward` 为 1
3. **添加转发规则**：
   - 在 PREROUTING 链添加 DNAT 规则，将公网端口映射到 VPN 客户端
   - 在 FORWARD 链添加放行规则，允许流量通过
   - 配置 MASQUERADE 实现 VPN 网段流量回环
4. **删除规则**：通过 `iptables -t nat -D PREROUTING` 删除指定序号的规则

## 端口格式支持

| 格式类型 | 示例 | 说明 |
|---------|------|------|
| 单端口 | `8080` | 转发单个端口 |
| 多端口 | `80,443,3389` | 同时转发多个端口（逗号分隔） |
| 端口范围 | `10000:50000` | 转发端口范围（冒号分隔） |
| 横杠范围 | `10000-50000` | 支持横杠分隔的端口范围（自动转换） |

## 注意事项

- 脚本需要 root 权限运行
- 转发规则在系统重启后会失效，如需持久化请配置 iptables-save
- 删除 NAT 规则后，FORWARD 链的放行记录依然存在但不影响使用
- 默认 VPN 网段为 `192.168.42.0/24`，如需修改请调整脚本中的子网配置
- 确保目标 VPN 客户端能正常访问服务器

## 项目仓库

CNB：https://cnb.cool/SDCOM/shit/-/blob/main/script/port_forward.sh

Github：https://github.com/SDCOM-0415/shit/blob/main/script/port_forward.sh

## © 作者

SDCOM