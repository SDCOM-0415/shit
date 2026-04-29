# port_forward.sh

This is a VPN port forwarding management tool (Pro version) for managing iptables port forwarding rules on Linux systems. Tested on `Debian 12` and `Ubuntu 22.04`. Current version <Badge type="tip" text="v1.0" />.

## Features

- Automatically detects cloud server public network interface
- Supports TCP, UDP protocols and all-protocol forwarding
- Supports single port, multiple ports and port range forwarding
- Intelligent port mapping (1:1 mapping or custom target port)
- Automatically configures VPN subnet traffic loopback (MASQUERADE)
- Visual viewing and deletion of active forwarding rules
- User-friendly menu interface

## Usage

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/port_forward.sh && sudo chmod +x ./port_forward.sh && sudo ./port_forward.sh
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/port_forward.sh && sudo chmod +x ./port_forward.sh && sudo ./port_forward.sh
```

After running the script, follow the menu prompts:
- Select `1` to add a new port forwarding rule
- Select `2` to view and delete existing forwarding rules
- Select `3` to exit the script

## Script Content

```bash
#!/bin/bash

# Auto-detect default public network interface
WAN_IF=$(ip route get 8.8.8.8 | grep -Po 'dev \K\w+' | head -n 1)

echo "========================================"
echo "    VPN Port Forwarding Manager (Pro)"
echo "========================================"
echo "Detected cloud server public interface: $WAN_IF"
echo ""

# Enable Linux kernel IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# --- Function: Add forwarding rule ---
add_rule() {
    echo ""
    echo ">>> [Add Rule]"
    read -p "1. Protocol (tcp / udp / all): " PROTOCOL
    
    echo "   (Single port: 8080)"
    echo "   (Multiple ports: 80,443,3389)"
    echo "   (Port range: 10000:50000)"
    read -p "2. Public access port: " PUBLIC_PORT
    
    # Error tolerance: replace hyphen "-" with colon ":" for iptables compatibility
    PUBLIC_PORT=$(echo "$PUBLIC_PORT" | tr '-' ':')
    
    read -p "3. Local VPN IP (e.g., 192.168.42.10): " TARGET_IP

    # Smart detection: check for comma or colon
    if [[ "$PUBLIC_PORT" == *","* ]] || [[ "$PUBLIC_PORT" == *":"* ]]; then
        echo "   -> [Multiple ports/range detected] Local port will match public port 1:1."
        TARGET_PORT_ARGS=""
        MATCH_ARGS="-m multiport --dports $PUBLIC_PORT"
        DISPLAY_PORT="$PUBLIC_PORT (1:1 mapping)"
    else
        read -p "4. Local receive port (Enter to match public $PUBLIC_PORT): " TARGET_PORT
        TARGET_PORT=${TARGET_PORT:-$PUBLIC_PORT}
        TARGET_PORT_ARGS=":$TARGET_PORT"
        MATCH_ARGS="--dport $PUBLIC_PORT"
        DISPLAY_PORT="$PUBLIC_PORT -> $TARGET_PORT"
    fi

    execute_add() {
        local proto=$1
        # DNAT mapping: when TARGET_PORT_ARGS is empty, iptables keeps original port
        iptables -t nat -A PREROUTING -i $WAN_IF -p $proto $MATCH_ARGS -j DNAT --to-destination $TARGET_IP$TARGET_PORT_ARGS
        
        # Allow through FORWARD chain
        iptables -A FORWARD -i $WAN_IF -p $proto -d $TARGET_IP $MATCH_ARGS -j ACCEPT
        
        echo "✅ Active: [$proto] Public $DISPLAY_PORT  (Target IP: $TARGET_IP)"
    }

    if [ "$PROTOCOL" == "all" ]; then
        execute_add "tcp"
        execute_add "udp"
    elif [ "$PROTOCOL" == "tcp" ] || [ "$PROTOCOL" == "udp" ]; then
        execute_add "$PROTOCOL"
    else
        echo "❌ Error: Protocol must be tcp, udp, or all."
        return
    fi

    # Check and configure loopback
    iptables -t nat -C POSTROUTING -s 192.168.42.0/24 -o $WAN_IF -j MASQUERADE 2>/dev/null || {
        iptables -t nat -A POSTROUTING -s 192.168.42.0/24 -o $WAN_IF -j MASQUERADE
        echo "✅ (System) Configured VPN subnet traffic loopback."
    }
}

# --- Function: Delete forwarding rule ---
delete_rule() {
    echo ""
    echo ">>> [Currently Active Port Forwarding Rules]"
    echo "------------------------------------------------------------"
    iptables -t nat -nL PREROUTING --line-numbers
    echo "------------------------------------------------------------"
    
    read -p "Enter rule number to delete (first column) [Enter 0 to cancel]: " RULE_NUM
    
    if [[ "$RULE_NUM" =~ ^[0-9]+$ ]]; then
        if [ "$RULE_NUM" -eq 0 ]; then
            echo "Deletion cancelled."
            return
        fi
        iptables -t nat -D PREROUTING $RULE_NUM 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "✅ Successfully deleted rule #$RULE_NUM! (Note: After deleting NAT rule, FORWARD chain entries remain but don't affect usage. They will be cleaned on reboot.)"
        else
            echo "❌ Deletion failed, please check if the number exists."
        fi
    else
        echo "❌ Error: Please enter a valid number."
    fi
}

# --- Main Program: Menu Loop ---
while true; do
    echo ""
    echo "========== Operation Menu =========="
    echo "  1) ➕ Add new port forwarding"
    echo "  2) ➖ View and delete existing rules"
    echo "  3) 🚪 Exit"
    echo "===================================="
    read -p "Select operation [1-3]: " CHOICE

    case $CHOICE in
        1) add_rule ;;
        2) delete_rule ;;
        3) echo "👋 Done, goodbye!"; exit 0 ;;
        *) echo "❌ Invalid option, please try again." ;;
    esac
done
```

## Working Principle

1. **Auto-detect public interface**: Get default route interface via `ip route get 8.8.8.8`
2. **Enable IP forwarding**: Set `/proc/sys/net/ipv4/ip_forward` to 1
3. **Add forwarding rules**:
   - Add DNAT rule in PREROUTING chain to map public ports to VPN client
   - Add ACCEPT rule in FORWARD chain to allow traffic
   - Configure MASQUERADE for VPN subnet traffic loopback
4. **Delete rules**: Remove specified rule by number via `iptables -t nat -D PREROUTING`

## Supported Port Formats

| Format Type | Example | Description |
|-------------|---------|-------------|
| Single Port | `8080` | Forward single port |
| Multiple Ports | `80,443,3389` | Forward multiple ports (comma separated) |
| Port Range | `10000:50000` | Forward port range (colon separated) |
| Hyphen Range | `10000-50000` | Support hyphen-separated ranges (auto-converted) |

## Notes

- Script requires root privileges
- Forwarding rules will be lost after system reboot. Use iptables-save for persistence
- After deleting NAT rules, FORWARD chain entries remain but don't affect usage
- Default VPN subnet is `192.168.42.0/24`, modify subnet configuration in script if needed
- Ensure target VPN client can access the server properly

## Project Repository

CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/port_forward.sh

Github: https://github.com/SDCOM-0415/shit/blob/main/script/port_forward.sh

## © Author

SDCOM