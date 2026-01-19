# enable_docker.sh

## 功能说明

重新启用 Docker，解除 `disable_docker.sh` 设置所有限制并安装 Docker。

## 使用方法

```bash
# 必须使用 sudo 或以 root 用户运行
sudo ./enable_docker.sh
```

## 执行步骤

1. **移除监控脚本**：删除定时监控 Docker 的脚本
2. **解锁软件包**：解除 Docker 相关软件包的锁定
3. **移除阻止策略**：删除 APT 配置中的 Docker 阻止规则
4. **恢复内核模块**：移除内核模块黑名单
5. **移除审计规则**：删除 Docker 相关的审计规则
6. **恢复目录权限**：恢复 /var/lib/docker 和 /etc/docker 的正常权限
7. **安装 Docker**：安装 docker.io 或可用版本
8. **安装相关工具**：安装 docker-compose 和 containerd
9. **启动服务**：启用并启动 Docker 服务
10. **验证安装**：测试 Docker 是否正常运行

## 注意事项

- 该脚本需要 root 权限运行
- 之前的备份文件（在 `/root/docker-backup-*`）可能需要手动恢复
- 日志保存在 `/var/log/docker-enable.log`

## 作者

SDCOM

## 项目地址

- CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/enable_docker.sh
- GitHub: https://github.com/SDCOM-0415/shit/blob/main/script/enable_docker.sh
