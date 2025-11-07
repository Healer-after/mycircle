import os
import subprocess
from datetime import datetime

# 第一步：生成 posts.json
print("📦 正在生成 posts.json ...")
subprocess.run(["python", "generate_posts.py"], check=True)

# 第二步：Git 提交
print("📤 正在提交到 GitHub ...")
commit_message = f"自动更新动态 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

commands = [
    ["git", "add", "."],
    ["git", "commit", "-m", commit_message],
    ["git", "push", "origin", "master"]
]

for cmd in commands:
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("❌ 出错：", cmd)
        break
else:
    print("✅ 已成功推送到 GitHub！")

print("\n🎉 更新完成！请稍等几秒后刷新你的 GitHub Pages 网址查看最新朋友圈。")
