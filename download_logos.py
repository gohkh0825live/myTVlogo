import os
import requests
import re
from io import BytesIO
from PIL import Image  # Pillow 库

M3U_URL = "https://iptv-emw.pages.dev/live/m3u/tvmalaysia.live.m3u"
LOGO_DIR = "img"

os.makedirs(LOGO_DIR, exist_ok=True)

response = requests.get(M3U_URL)
lines = response.text.splitlines()

for line in lines:
    if line.startswith("#EXTINF"):
        match = re.search(r'tvg-logo="([^"]+)"', line)
        name_match = re.search(r",(.+)", line)

        if match and name_match:
            logo_url = match.group(1)
            if not logo_url.startswith("http"):
                continue

            channel_name = name_match.group(1).strip().replace("/", "_")
            file_path = os.path.join(LOGO_DIR, f"{channel_name}.png")

            if os.path.exists(file_path):
                print(f"Already exists: {channel_name}")
                continue

            try:
                img_response = requests.get(logo_url, timeout=10)
                img = Image.open(BytesIO(img_response.content)).convert("RGBA")  # 转为透明背景 PNG
                img.save(file_path, "PNG")
                print(f"Downloaded: {channel_name}")
            except Exception as e:
                print(f"Failed to download logo for {channel_name}: {e}")
