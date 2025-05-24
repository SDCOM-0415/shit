#!/bin/bash

echo "启动VitePress文档服务器..."
echo "服务器将监听所有网络接口 (0.0.0.0:5173)"
echo "在Code Server环境中，请使用提供的URL访问文档"
echo "--------------------------------------------"

# 启动VitePress开发服务器
npm run docs:dev