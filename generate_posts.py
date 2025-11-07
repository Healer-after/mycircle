import os
import json
from datetime import datetime

# 文件路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR = os.path.join(BASE_DIR, "posts")
DATA_FILE = os.path.join(BASE_DIR, "data", "posts.json")

def get_post_info(filename):
    """解析文件名获取日期与标题"""
    name, ext = os.path.splitext(filename)
    # 支持格式：2025-11-06-新品发布-1.jpg
    parts = name.split("-")
    if len(parts) >= 4 and parts[0].isdigit() and len(parts[0]) == 4:
        date_str = "-".join(parts[0:3])
        title = "-".join(parts[3:])
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")
        title = name
    return date_str, title

def main():
    posts = {}

    # 遍历 posts 文件夹
    for file in os.listdir(POSTS_DIR):
        path = os.path.join(POSTS_DIR, file)
        if os.path.isdir(path):
            continue

        date_str, title = get_post_info(file)

        # 自动分组（同日期+标题的文件归为一组）
        key = f"{date_str}-{title}"
        if key not in posts:
            posts[key] = {
                "date": date_str,
                "title": title,
                "files": [],
                "text": "",
                "timestamp": os.path.getmtime(path)
            }

        # 分类文件
        if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".mp4")):
            posts[key]["files"].append(file)
        elif file.lower().endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                posts[key]["text"] = f.read().strip()

    # 按修改时间排序（新→旧）
    sorted_posts = sorted(posts.values(), key=lambda x: x["timestamp"], reverse=True)

    # 写入 JSON
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted_posts, f, ensure_ascii=False, indent=2)

    print(f"✅ 已生成 {len(sorted_posts)} 条动态 → {DATA_FILE}")

if __name__ == "__main__":
    main()
