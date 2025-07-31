import ctypes
import requests
import os

# GitHub 原始图片地址
IMAGE_URL = 'https://raw.githubusercontent.com/xxfttkx/image-composite/main/result.png'

# 下载到本地的路径（可自行修改）
LOCAL_PATH = os.path.expanduser('F:/Code/python/download-and-set-wallpaper/result.png')

def download_image(url: str, path: str):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as f:
        f.write(response.content)

def set_wallpaper(image_path: str):
    # 设置桌面壁纸（Windows）
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)

if __name__ == '__main__':
    try:
        download_image(IMAGE_URL, LOCAL_PATH)
        set_wallpaper(LOCAL_PATH)
        print("壁纸设置成功！")
    except Exception as e:
        print(f"发生错误: {e}")
