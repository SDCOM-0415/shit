#!/bin/bash

# ================= 配置区域 =================
TOKEN="eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpc19hZG1pbiI6IHRydWUsICJleHAiOiAxNzc4NTAzMTkyfQ==.oawg/OR7Ch6ZoAojxrZSZbK8u9DaJsQfPtffdGHQY0M="
BASE_URL="http://bj-tx1.sdcom.top:12345"
# ===========================================

FILE_PATH=$1

if [ -z "$FILE_PATH" ]; then
    echo "使用方法: sh upload_to_box.sh <文件路径>"
    exit 1
fi

FILE_NAME=$(basename "$FILE_PATH")
FILE_SIZE=$(stat -c%s "$FILE_PATH")

echo "正在准备上传: $FILE_NAME ($FILE_SIZE bytes)..."

# 1. 初始化上传任务
INIT_RES=$(curl -s -X POST "$BASE_URL/presign/upload/init" \
  -H "authorization: Bearer $TOKEN" \
  -H "content-type: application/json" \
  --data "{\"file_name\":\"$FILE_NAME\",\"file_size\":$FILE_SIZE,\"expire_value\":1,\"expire_style\":\"day\"}")

UPLOAD_PATH=$(echo $INIT_RES | grep -oP '(?<="upload_url":")[^"]+')

if [ -z "$UPLOAD_PATH" ]; then
    echo "❌ 初始化失败！服务器返回:"
    echo "$INIT_RES"
    exit 1
fi

if [[ $UPLOAD_PATH == /api/* ]]; then
    FULL_UPLOAD_URL="${BASE_URL}${UPLOAD_PATH#/api}"
else
    FULL_UPLOAD_URL="${BASE_URL}${UPLOAD_PATH}"
fi

echo "✅ 初始化成功，正在上传..."

# 3. 正式上传文件内容
UPLOAD_RES=$(curl -s -X PUT "$FULL_UPLOAD_URL" \
  -H "authorization: Bearer $TOKEN" \
  -F "file=@$FILE_PATH")

echo "------------------------------------------"
# 4. 提取取件码 (排除HTTP状态码200，精确提取字符串类型的code)
PICKUP_CODE=$(echo "$UPLOAD_RES" | grep -oP '(?<="code":")[^"]+')

if [ -n "$PICKUP_CODE" ]; then
    echo "🎉 上传成功！"
    echo "🔑 取件码: $PICKUP_CODE"
    echo "🌐 下载地址: $BASE_URL"
elif [[ $UPLOAD_RES == *"200"* ]]; then
    echo "✅ 上传已成功！但未能自动解析出取件码。"
    echo "📦 服务器原始返回数据: $UPLOAD_RES"
    echo "请在上面的数据中寻找或者直接访问网页版查看。"
else
    echo "❌ 上传可能失败，服务器返回:"
    echo "$UPLOAD_RES"
fi
echo "------------------------------------------"