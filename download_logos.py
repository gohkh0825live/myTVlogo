import os
import re
import requests
from io import BytesIO
from PIL import Image

# 配置
M3U_URL = "https://perfecttv.net/PerfecttvFree.m3u"
LOGO_DIR = "img"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 创建 logo 存放目录
os.makedirs(LOGO_DIR, exist_ok=True)

# 获取 M3U 内容
response = requests.get(M3U_URL, headers=HEADERS)
lines = response.text.splitlines()

# 提取所有频道信息行
extinf_lines = [line for line in lines if line.startswith("#EXTINF")]
print(f"共检测到 {len(extinf_lines)} 个频道")

for index, line in enumerate(extinf_lines, start=1):
    # 匹配 logo 和频道名称
    logo_match = re.search(r'tvg-logo="([^"]+)"', line)
    name_match = re.search(r'tvg-name="([^"]+)"', line)
    fallback_match = re.search(r",(.+)", line)

    if not logo_match:
        continue

    logo_url = logo_match.group(1)
    if not logo_url.startswith("http"):
        continue

    # 使用 tvg-name 或备用名称
    if name_match:
        channel_name = name_match.group(1).strip()
    elif fallback_match:
        channel_name = fallback_match.group(1).strip()
    else:
        continue

    # 清理文件名非法字符
    channel_name = re.sub(r'[\\/:*?"<>|]', '_', channel_name)
    file_path = os.path.join(LOGO_DIR, f"{channel_name}.png")

    # 跳过已下载
    if os.path.exists(file_path):
        print(f"[{index}/{len(extinf_lines)}] 已存在: {channel_name}")
        continue

    # 下载并保存 logo
    try:
        img_response = requests.get(logo_url, headers=HEADERS, timeout=10)
        img = Image.open(BytesIO(img_response.content)).convert("RGBA")
        img.save(file_path, "PNG")
        print(f"[{index}/{len(extinf_lines)}] 下载完成: {channel_name}")
    except Exception as e:
        print(f"[{index}/{len(extinf_lines)}] 下载失败: {channel_name} - {e}")
