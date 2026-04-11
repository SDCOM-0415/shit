#!/bin/bash

# 配置上传参数
configure_upload() {
    echo "请配置上传参数："
    echo "（提示：Token为可选项，可直接按回车键跳过）"
    read -p "请输入Token: " TOKEN
    read -p "请输入服务器Base URL: " BASE_URL
    
    if [ -z "$BASE_URL" ]; then
        echo "❌ Base URL不能为空"
        exit 1
    fi
}

# 配置上传参数
configure_upload

FILE_PATH=$1

if [ -z "$FILE_PATH" ]; then
    echo "使用方法: sh upload_to_box.sh <文件路径>"
    exit 1
fi

FILE_NAME=$(basename "$FILE_PATH")
FILE_SIZE=$(stat -c%s "$FILE_PATH")

echo "正在准备上传: $FILE_NAME ($FILE_SIZE bytes)..."

# 1. 初始化上传任务
if [ -n "$TOKEN" ]; then
    INIT_RES=$(curl -s -X POST "$BASE_URL/presign/upload/init" \
      -H "authorization: Bearer $TOKEN" \
      -H "content-type: application/json" \
      --data "{\"file_name\":\"$FILE_NAME\",\"file_size\":$FILE_SIZE,\"expire_value\":1,\"expire_style\":\"day\"}")
else
    INIT_RES=$(curl -s -X POST "$BASE_URL/presign/upload/init" \
      -H "content-type: application/json" \
      --data "{\"file_name\":\"$FILE_NAME\",\"file_size\":$FILE_SIZE,\"expire_value\":1,\"expire_style\":\"day\"}")
fi

UPLOAD_PATH=$(echo $INIT_RES | grep -oP '(?<="upload_url":")[^"]+')

if [ -z "$UPLOAD_PATH" ]; then
    echo "❌ 初始化失败！服务器返回:"
    echo "$INIT_RES"
    exit 1
fi

if [ "$(echo "$UPLOAD_PATH" | cut -c 1-5)" = "/api/" ]; then
    FULL_UPLOAD_URL="${BASE_URL}${UPLOAD_PATH#/api}"
else
    FULL_UPLOAD_URL="${BASE_URL}${UPLOAD_PATH}"
fi

echo "✅ 初始化成功，正在上传..."

# 3. 正式上传文件内容
if [ -n "$TOKEN" ]; then
    UPLOAD_RES=$(curl -s -X PUT "$FULL_UPLOAD_URL" \
      -H "authorization: Bearer $TOKEN" \
      -F "file=@$FILE_PATH")
else
    UPLOAD_RES=$(curl -s -X PUT "$FULL_UPLOAD_URL" \
      -F "file=@$FILE_PATH")
fi

echo "------------------------------------------"
# 4. 提取取件码 (排除HTTP状态码200，精确提取字符串类型的code)
PICKUP_CODE=$(echo "$UPLOAD_RES" | grep -oP '(?<="code":")[^"]+')

if [ -n "$PICKUP_CODE" ]; then
    echo "🎉 上传成功！"
    echo "🔑 取件码: $PICKUP_CODE"
    echo "🌐 下载地址: $BASE_URL"
elif [ "$(echo "$UPLOAD_RES" | grep -o "200")" = "200" ]; then
    echo "✅ 上传已成功！但未能自动解析出取件码。"
    echo "📦 服务器原始返回数据: $UPLOAD_RES"
    echo "请在上面的数据中寻找或者直接访问网页版查看。"
else
    echo "❌ 上传可能失败，服务器返回:"
    echo "$UPLOAD_RES"
fi
echo "------------------------------------------"