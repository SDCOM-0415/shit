# disable_docker.sh

## 功能说明

彻底禁用 Docker 并防止重新安装。该脚本会：

1. 停止并禁用所有 Docker 相关服务
2. 终止 Docker 相关进程
3. 卸载 Docker 软件包
4. 清理 Docker 文件和目录
5. 锁定 Docker 相关软件包
6. 创建 APT 阻止策略
7. 禁用相关内核模块
8. 创建监控脚本防止重新安装
9. 创建审计规则

## 使用方法

```bash
# 必须使用 sudo 或以 root 用户运行
sudo ./disable_docker.sh
```

## 执行步骤

1. **停止服务**：停止 docker、docker.socket、containerd 服务
2. **终止进程**：杀死 dockerd、containerd、docker-proxy 进程
3. **备份配置**：将当前 Docker 配置备份到 `/root/docker-backup-{timestamp}/`
4. **卸载软件包**：移除所有 Docker 相关包
5. **清理目录**：删除 Docker 数据目录并创建只读空目录
6. **锁定软件包**：使用 apt-mark hold 锁定 Docker 包
7. **创建阻止策略**：在 APT 配置中添加 Docker 阻止规则
8. **禁用内核模块**：黑名单 overlay 和 br_netfilter 模块
9. **安装监控脚本**：定时检查并终止任何 Docker 进程
10. **清理用户目录**：删除用户目录下的 .docker 配置
11. **创建审计规则**：监控 Docker 相关文件访问

## 注意事项

- 该脚本需要 root 权限运行
- 操作不可逆，请确保备份重要数据
- 监控脚本每10分钟运行一次，防止 Docker 重新安装
- 日志保存在 `/var/log/docker-disable.log` 和 `/var/log/docker-monitor.log`

## 作者

SDCOM

## 项目地址

- CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/disable_docker.sh
- GitHub: https://github.com/SDCOM-0415/shit/blob/main/script/disable_docker.sh
