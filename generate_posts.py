import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR = os.path.join(BASE_DIR, "posts")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "posts.json")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

IMAGE_EXTS = [".jpg", ".jpeg", ".png"]
VIDEO_EXTS = [".mp4", ".webm"]
TEXT_EXT = ".txt"

def get_file_time(filepath):
    return datetime.fromtimestamp(os.path.getmtime(filepath))

def collect_posts():
    posts = {}
    for filename in os.listdir(POSTS_DIR):
        filepath = os.path.join(POSTS_DIR, filename)
        if not os.path.isfile(filepath):
            continue
        name, ext = os.path.splitext(filename)
        prefix = "-".join(name.split("-")[:3])
        if prefix not in posts:
            posts[prefix] = {
                "text": "",
                "images": [],
                "video": None,
                "time": get_file_time(filepath).strftime("%Y-%m-%d %H:%M")
            }
        if ext.lower() == TEXT_EXT:
            with open(filepath, "r", encoding="utf-8") as f:
                posts[prefix]["text"] = f.read().strip()
        elif ext.lower() in IMAGE_EXTS:
            posts[prefix]["images"].append(f"posts/{filename}")
        elif ext.lower() in VIDEO_EXTS:
            posts[prefix]["video"] = f"posts/{filename}")
    return sorted(
        posts.values(),
        key=lambda x: datetime.strptime(x["time"], "%Y-%m-%d %H:%M"),
        reverse=True
    )

def main():
    posts_data = collect_posts()
    output = {
        "author": "舜禹工作室",
        "signature": "微信: GPT2888",
        "posts": posts_data
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"✅ 已生成 {len(posts_data)} 条动态 -> {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
