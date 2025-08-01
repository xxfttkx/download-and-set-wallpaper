import ctypes
import requests
import os
import sys
import winreg
from datetime import datetime
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

DEFAULT_IMAGE_URL = 'https://raw.githubusercontent.com/xxfttkx/image-composite/main/result.png'
LOCAL_PATH = os.path.expanduser('F:/Code/python/download-and-set-wallpaper/result.png')

def log(msg: str):
    now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{now} {msg}")

def download_image(url: str, path: str):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as f:
        f.write(response.content)
    log("图片下载成功")

def is_16_9(image_path: str, tolerance: float = 0.02) -> bool:
    with Image.open(image_path) as img:
        width, height = img.size
    ratio = width / height
    return abs(ratio - (16 / 9)) < tolerance

def set_wallpaper_style(fit: bool):
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r'Control Panel\Desktop',
            0, winreg.KEY_SET_VALUE
        )
        if fit:
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "6")   # Fit
            log("设置显示方式为 适应（Fit）")
        else:
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "10")  # Fill
            log("设置显示方式为 填充（Fill）")
        winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
        winreg.CloseKey(key)
    except Exception as e:
        log(f"注册表设置失败: {e}")

def set_wallpaper(image_path: str):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    log("壁纸设置成功")

if __name__ == '__main__':
    try:
        image_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_IMAGE_URL
        download_image(image_url, LOCAL_PATH)
        fit_mode = is_16_9(LOCAL_PATH)
        set_wallpaper_style(fit_mode)
        set_wallpaper(LOCAL_PATH)
    except Exception as e:
        log(f"发生错误: {e}")
