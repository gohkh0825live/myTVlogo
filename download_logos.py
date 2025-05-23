import os
import requests
import re

M3U_URL = "https://iptv-emw.pages.dev/tvmalaysia.live.m3u"
IMG_DIR = "img"

os.makedirs(IMG_DIR, exist_ok=True)

response = requests.get(M3U_URL)
lines = response.text.splitlines()

for line in lines:
    if line.startswith("#EXTINF"):
        match = re.search(r'tvg-logo="([^"]+)"', line)
        name_match = re.search(r",(.+)", line)

        if match and name_match:
            logo_url = match.group(1)
            channel_name = name_match.group(1).strip().replace("/", "_")

            # 安全获取文件扩展名
            ext = os.path.splitext(logo_url)[-1]
            if not ext or not ext.startswith("."):
                ext = ".png"

            file_path = os.path.join(IMG_DIR, f"{channel_name}{ext}")

            try:
                img_data = requests.get(logo_url, timeout=10).content
                with open(file_path, "wb") as f:
                    f.write(img_data)
                print(f"Downloaded: {channel_name}")
            except Exception as e:
                print(f"Failed to download logo for {channel_name}: {e}")
