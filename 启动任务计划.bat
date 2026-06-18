@echo off
chcp 65001 >nul
title 任务计划

echo 正在启动桌面悬浮任务计划...
python app.py

if errorlevel 1 (
    echo.
    echo 启动失败，请确认已安装 Python 和依赖：
    echo   pip install -r requirements.txt
    echo.
    pause
)
