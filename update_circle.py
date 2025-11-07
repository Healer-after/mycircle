import os
import subprocess
import time
import json
from pathlib import Path

# === 基础路径设置 ===
ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "posts.json"
POSTS_DIR = ROOT / "posts"

# === 第一步：运行 generate_posts.py ===
print("🌀 正在生成最新动态数据...")
subprocess.run("python generate_posts.py", shell=True)

# === 第二步：检测是否有更新 ===
print("🔍 检查是否有新动态...")

# 获取 git 状态
result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
changed_files = result.stdout.strip().split("\n")

# 筛选出变化文件
changed_files = [f for f in changed_files if f.strip() != ""]

if not changed_files:
    print("🟢 没有检测到新的动态或文件更改，跳过推送。")
else:
    print("📝 检测到变动的文件：")
    for f in changed_files:
        print("  •", f)

    # === 第三步：执行 Git 提交 ===
    commit_message = f"自动更新朋友圈动态 {time.strftime('%Y-%m-%d %H:%M:%S')}"
    commands = [
        "git add data/posts.json",
        "git add posts/",
        f'git commit -m "{commit_message}"',
        "git push"
    ]

    print("\n🚀 开始上传到 GitHub...\n")
    for cmd in commands:
        print(f"👉 {cmd}")
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            print(f"⚠️ 命令执行失败: {cmd}")
            break

    print("\n✅ 已成功推送到 GitHub！")
    print("🌐 可访问最新动态页面： https://healer-after.github.io/mycircle/")

print("\n🎉 任务完成！")
