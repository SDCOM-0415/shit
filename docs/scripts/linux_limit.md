# linux_limit.sh

这是一个用于限制Linux目录大小的脚本，当前版本为0.2。

## 功能特点

- 支持交互式和命令行参数两种使用方式
- 使用fallocate方法创建固定大小的镜像文件
- 自动备份原始目录数据
- 支持多种大小单位（B/KB/MB/GB/TB）

## 使用方法

### 交互式模式

```bash
chmod +x linux_limit.sh
./linux_limit.sh
```

运行脚本后，按照提示依次输入：
1. 需要限制的原始目录路径
2. 限制大小（支持B/KB/MB/GB/TB等单位）
3. 镜像存储路径（默认为./limit.img）

### 命令行参数模式

```bash
./linux_limit.sh <原始目录路径> <限制大小> [镜像存储路径]
```

例如：
```bash
./linux_limit.sh /path/to/directory 10GB /path/to/limit.img
```

## 参数说明

- `原始目录路径`：要限制大小的目录的完整路径
- `限制大小`：支持的单位包括：
  - B（字节）
  - KB（千字节）
  - MB（兆字节）
  - GB（吉字节）
  - TB（太字节）
- `镜像存储路径`：可选参数，默认为当前目录下的limit.img

## 工作原理

1. 创建指定大小的镜像文件（使用fallocate）
2. 将镜像文件格式化为ext4文件系统
3. 备份原始目录（自动添加时间戳）
4. 创建新目录并挂载镜像文件
5. 恢复原始数据到新的受限目录

## 注意事项

- 需要root权限执行（因为涉及mount操作）
- 原始数据会被自动备份，备份目录名格式为：`原始目录名_backup_时间戳`
- 确保系统有足够的空间存储镜像文件
- 建议在操作前备份重要数据

## 项目地址

- CNB项目地址：[https://cnb.cool/SDCOM/shit/-/blob/main/linux_limit.sh](https://cnb.cool/SDCOM/shit/-/blob/main/linux_limit.sh)
- GitHub项目地址：[https://github.com/SDCOM-0415/shit/blob/main/linux_limit.sh](https://github.com/SDCOM-0415/shit/blob/main/linux_limit.sh)

## 作者

SDCOM