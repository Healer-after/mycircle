@echo off
chcp 65001 >nul
title 一键更新朋友圈

echo.
echo ==========================================
echo 一键更新朋友圈脚本
echo 项目目录：%cd%
echo ==========================================
echo.

:: 1. 检查 Python 是否存在
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 未检测到 Python，请先安装 Python 并加入系统 PATH。
    pause
    exit /b
)

:: 2. 生成动态数据
echo 正在生成最新动态数据...
python generate_posts.py
if %errorlevel% neq 0 (
    echo 生成动态数据失败，请检查 generate_posts.py。
    pause
    exit /b
)
echo 已生成 data/posts.json
echo.

:: 3. Git 配置
git config --global core.quotepath false
git config --global i18n.commitencoding utf-8
git config --global i18n.logoutputencoding utf-8

:: 4. 添加文件
git add -A

:: 5. 获取当前时间
for /f "tokens=1-3 delims=/ " %%a in ("%date%") do (
    set today=%%a-%%b-%%c
)
set timestr=%time:~0,2%:%time:~3,2%

:: 6. 提交
git commit -m "自动更新朋友圈动态 %today% %timestr%" --no-verify
if %errorlevel% neq 0 (
    echo 没有新的改动需要提交。
) else (
    echo 已提交最新动态。
)

:: 7. 推送到 GitHub
echo 正在推送到 GitHub...
git push origin master
if %errorlevel% neq 0 (
    echo 推送失败，请检查网络或 GitHub 连接。
    pause
    exit /b
)
echo 推送成功。
echo.

:: 8. 打开网页
start https://healer-after.github.io/mycircle/

echo 操作完成，请刷新网页查看最新朋友圈。
pause
exit /b
