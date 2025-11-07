@echo off
title 🌀 一键更新朋友圈到 GitHub 并预览
color 0a

:: === 1. 进入项目目录 ===
cd /d "C:\Users\Arrebol\Desktop\mycircle"

echo 🚀 正在生成新的动态数据...
python generate_posts.py
if %errorlevel% neq 0 (
    echo ❌ Python 脚本执行失败，请检查 generate_posts.py！
    pause
    exit /b
)

echo ✅ 已生成最新 posts.json 文件
echo.

:: === 2. 提交并推送到 GitHub ===
echo 📤 正在推送到 GitHub...
git add .
git commit -m "自动更新朋友圈动态"
git push

if %errorlevel% neq 0 (
    echo ❌ 推送失败，请检查网络或 GitHub 设置。
    pause
    exit /b
)

echo ✅ 成功更新到 GitHub！
echo.

:: === 3. 等待 GitHub Pages 更新（可选 5 秒延迟）===
echo ⏳ 正在等待 GitHub Pages 同步更新...
timeout /t 5 >nul

:: === 4. 自动打开网页预览 ===
set "url=https://healer-after.github.io/mycircle/"
echo 🌐 正在打开网页：%url%
start "" "%url%"

echo ✅ 全部完成！请在浏览器中查看最新朋友圈！
pause
