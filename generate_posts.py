import os
import json
import time

# === 配置部分 ===
POSTS_DIR = "posts"
OUTPUT_FILE = "data/posts.json"

def get_post_entries():
    posts = {}

    # 遍历 posts 文件夹下所有文件
    for file in os.listdir(POSTS_DIR):
        path = os.path.join(POSTS_DIR, file)
        name, ext = os.path.splitext(file)

        # 跳过隐藏文件
        if file.startswith("."):
            continue

        # 只处理图片与文本
        if ext.lower() in [".jpg", ".png", ".jpeg", ".gif", ".mp4", ".mov"]:
            key = "-".join(name.split("-")[:3])  # 日期部分 例: 2025-11-06
            title = "-".join(name.split("-")[3:]) or "未命名动态"

            if key not in posts:
                posts[key] = {
                    "date": key,
                    "title": title,
                    "files": [],
                    "text": "",
                    "timestamp": os.path.getmtime(path)
                }
            posts[key]["files"].append(file)

        elif ext.lower() == ".txt":
            key = "-".join(name.split("-")[:3])
            title = "-".join(name.split("-")[3:]) or "未命名动态"

            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()

            if key not in posts:
                posts[key] = {
                    "date": key,
                    "title": title,
                    "files": [],
                    "text": "",
                    "timestamp": os.path.getmtime(path)
                }

            posts[key]["text"] = text

    # 按文件时间倒序排序
    post_list = sorted(posts.values(), key=lambda x: x["timestamp"], reverse=True)
    return post_list


def main():
    print("正在生成新的动态数据...")
    posts = get_post_entries()

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print(f"✅ 已生成 {len(posts)} 条动态 → {os.path.abspath(OUTPUT_FILE)}")


if __name__ == "__main__":
    main()
