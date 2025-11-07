@echo off
chcp 65001 >nul
title 一键更新朋友圈动态

echo ==========================================
echo 一键更新朋友圈动态脚本
echo ==========================================
echo.

REM 切换到项目目录
pushd "C:\Users\Arrebol\Desktop\mycircle" || (
    echo ❌ 无法进入项目目录，请检查路径是否正确。
    pause
    exit /b
)

echo 正在生成最新动态数据...
python generate_posts.py

echo.
echo 数据生成完成，准备提交到 GitHub...
python update_circle.py

echo.
echo 操作完成，请刷新网页查看最新朋友圈。
pause
popd
