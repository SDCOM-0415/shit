# upload_to_box.sh

## 功能说明

`upload_to_box.sh` 是一个用于上传文件到文件快递柜的脚本。它允许用户通过命令行快速上传文件，并获取取件码和下载地址。

## 特点

- 支持自定义服务器地址
- Token 为可选项，可根据需要选择是否输入
- 每次运行时都会提示用户输入配置信息，无需持久化存储
- 自动处理上传过程，包括初始化上传任务和正式上传文件内容
- 上传成功后显示取件码和下载地址

## 使用方法

### 下载脚本

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/upload_to_box.sh && sudo chmod +x ./upload_to_box.sh
```

Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/upload_to_box.sh && sudo chmod +x ./upload_to_box.sh
```

### 运行脚本

```bash
# 运行脚本并上传文件
./upload_to_box.sh <文件路径>
```

### 示例

```bash
# 上传当前目录下的 test.txt 文件
./upload_to_box.sh test.txt

# 上传指定路径的文件
./upload_to_box.sh /path/to/file.zip
```

## 运行流程

1. 运行脚本时，会提示用户输入以下信息：
   - Token（可选项，直接按回车键跳过）
   - 服务器 Base URL（必填项）

2. 脚本会执行以下操作：
   - 初始化上传任务，获取上传 URL
   - 正式上传文件内容
   - 提取并显示取件码和下载地址

## 注意事项

- 确保输入的服务器 Base URL 是正确的，格式如 `https://filebox.example.com`
- Token 为可选项，如果服务器要求认证，则需要输入有效的 Token
- 上传的文件大小应符合服务器的限制
- 如果上传失败，脚本会显示服务器返回的错误信息

## 项目仓库

CNB：https://cnb.cool/SDCOM/shit/-/blob/main/script/upload_to_box.sh

Github：https://github.com/SDCOM-0415/shit/blob/main/script/upload_to_box.sh

## © 作者

SDCOM