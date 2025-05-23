import os
import requests
import re

M3U_URL = "https://iptv-emw.pages.dev/live/m3u/tvmalaysia.live.m3u"
LOGO_DIR = "img"  # 保存到 img 文件夹

# 创建 img 目录（如果不存在）
os.makedirs(LOGO_DIR, exist_ok=True)

# 获取 M3U 内容
response = requests.get(M3U_URL)
lines = response.text.splitlines()

for line in lines:
    if line.startswith("#EXTINF"):
        match = re.search(r'tvg-logo="([^"]+)"', line)
        name_match = re.search(r",(.+)", line)

        if match and name_match:
            logo_url = match.group(1)
            if not logo_url.startswith("http"):
                continue  # 跳过无效 URL

            # 清理频道名作为文件名，防止非法字符
            channel_name = name_match.group(1).strip().replace("/", "_")
            ext = os.path.splitext(logo_url)[-1] or ".jpg"
            file_path = os.path.join(LOGO_DIR, f"{channel_name}{ext}")

            # 跳过已存在的文件，避免重复下载
            if os.path.exists(file_path):
                print(f"Already exists: {channel_name}")
                continue

            try:
                img_data = requests.get(logo_url, timeout=10).content
                with open(file_path, "wb") as f:
                    f.write(img_data)
                print(f"Downloaded: {channel_name}")
            except Exception as e:
                print(f"Failed to download logo for {channel_name}: {e}")
