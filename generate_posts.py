import os
import json
import time
import re
from pathlib import Path

# 配置
ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
OUTPUT_FILE = ROOT / "data" / "posts.json"

date_re = re.compile(r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD

def parse_filename(fn: str):
    """
    解析文件名 (不含扩展名)
    返回 (date_str, title_base, original_name)
    例如: '2025-11-06-新品发布-1' -> ('2025-11-06', '新品发布', '2025-11-06-新品发布-1')
    """
    parts = fn.split("-")
    # 找到第一个符合 YYYY-MM-DD 的片段索引
    date_idx = None
    for i, p in enumerate(parts):
        if date_re.match(p):
            date_idx = i
            break
    if date_idx is None:
        # 没找到日期，则认为整体是标题，使用 file mtime 为时间
        return (None, fn, fn)

    date_token = parts[date_idx]
    title_parts = parts[date_idx+1:]  # 日期后面的所有作为标题部分
    if not title_parts:
        title = "未命名动态"
    else:
        title = "-".join(title_parts)

    # 去掉末尾的数字索引，例如 '新品发布-1' -> '新品发布'
    title_base = re.sub(r"-\d+$", "", title)
    original_name = fn
    return (date_token, title_base, original_name)

def collect_posts():
    posts_map = {}  # key -> post dict

    if not POSTS_DIR.exists():
        print(f"posts 目录不存在: {POSTS_DIR}")
        return []

    for entry in POSTS_DIR.iterdir():
        if entry.name.startswith("."):
            continue
        if entry.is_dir():
            continue
        name = entry.stem  # 文件名不含扩展
        ext = entry.suffix.lower()
        date_token, title_base, original_name = parse_filename(name)
        # use key combining date (or mtime if no date) and title_base
        if date_token:
            key = f"{date_token}||{title_base}"
        else:
            # fallback: use mtime date as key prefix
            mtime = int(entry.stat().st_mtime)
            mdate = time.strftime("%Y-%m-%d", time.localtime(mtime))
            key = f"{mdate}||{title_base}"

        # initialize post if missing
        if key not in posts_map:
            # Use timestamp from the most recent file added; will update later
            mtime = entry.stat().st_mtime
            posts_map[key] = {
                "date": date_token if date_token else time.strftime("%Y-%m-%d", time.localtime(mtime)),
                "title": title_base if title_base else "未命名动态",
                "files": [],
                "text": "",
                "timestamp": mtime
            }

        # add file (images/videos) or text
        if ext in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".mp4", ".mov", ".webm"]:
            posts_map[key]["files"].append(entry.name)
            # update timestamp to latest modified among files
            posts_map[key]["timestamp"] = max(posts_map[key]["timestamp"], entry.stat().st_mtime)
        elif ext == ".txt":
            # read text as UTF-8 (如果是其他编码可能需要手动转换)
            try:
                with open(entry, "r", encoding="utf-8") as f:
                    text = f.read().strip()
            except Exception:
                # 尝试以系统默认编码读取（容错）
                with open(entry, "r", encoding="gbk", errors="ignore") as f:
                    text = f.read().strip()
            posts_map[key]["text"] = text
            posts_map[key]["timestamp"] = max(posts_map[key]["timestamp"], entry.stat().st_mtime)
        else:
            # 未知类型暂时忽略
            pass

    # convert to list and sort by timestamp desc (最新在前)
    posts = sorted(posts_map.values(), key=lambda x: x["timestamp"], reverse=True)
    return posts

def main():
    os.makedirs(OUTPUT_FILE.parent, exist_ok=True)
    posts = collect_posts()
    # normalize files order: keep alphabetical or by timestamp? we keep current order
    # write json (utf-8)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"✅ 已生成 {len(posts)} 条动态 → {OUTPUT_FILE.resolve()}")

if __name__ == "__main__":
    main()
