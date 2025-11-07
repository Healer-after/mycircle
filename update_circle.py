# -*- coding: utf-8 -*-
"""
自动提交朋友圈项目到 GitHub
支持中文路径与 UTF-8 提交信息
"""

import os
import subprocess
from datetime import datetime

# 项目路径
project_dir = r"C:\Users\Arrebol\Desktop\mycircle"

def run_cmd(cmd):
    """执行命令并实时打印输出"""
    result = subprocess.run(cmd, shell=True, cwd=project_dir, text=True, encoding='utf-8')
    return result.returncode

def main():
    print("🚀 正在生成最新动态数据...")

    # 运行生成脚本
    run_cmd("python generate_posts.py")

    print("✅ 数据已生成，准备提交到 GitHub...")

    # Git 配置修正，确保中文不会乱码
    subprocess.run("git config --global core.quotepath false", shell=True)
    subprocess.run("git config --global i18n.commitencoding utf-8", shell=True)
    subprocess.run("git config --global i18n.logoutputencoding utf-8", shell=True)
    subprocess.run("git config --global gui.encoding utf-8", shell=True)

    # 添加所有更改
    run_cmd("git add .")

    # 提交信息
    commit_msg = f"自动更新朋友圈动态 {datetime.now():%Y-%m-%d %H:%M:%S}"
    run_cmd(f'git commit -m "{commit_msg}"')

    # 推送
    print("🌍 正在推送到 GitHub...")
    run_cmd("git push")

    print("✅ 已成功更新到 GitHub！")
    print("🌐 可刷新你的 GitHub Pages 查看最新朋友圈动态。")

if __name__ == "__main__":
    main()
