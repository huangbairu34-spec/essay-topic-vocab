@echo off
chcp 65001 >nul
title 考研英语作文主题词 - 手机背诵服务
cd /d "%~dp0"
echo 正在启动考研英语作文主题词本地服务...
python start_server.py
pause
