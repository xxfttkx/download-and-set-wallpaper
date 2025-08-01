import ctypes
import requests
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import winreg

# 原始图片地址
DEFAULT_IMAGE_URL = 'https://raw.githubusercontent.com/xxfttkx/image-composite/main/result.png'

# 下载到本地的路径
LOCAL_PATH = os.path.expanduser('F:/Code/python/download-and-set-wallpaper/result.png')

def download_image(url: str, path: str):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as f:
        f.write(response.content)

def set_wallpaper(image_path: str):
    # 设置壁纸显示样式为“适应”（Fit）：宽度占满，过长不裁剪
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r'Control Panel\Desktop',
            0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "10")  # 10 = Fill
        winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
        winreg.CloseKey(key)
    except Exception as e:
        print(f"注册表设置失败: {e}")

    # 设置壁纸
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)

if __name__ == '__main__':
    try:
        image_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_IMAGE_URL
        download_image(image_url, LOCAL_PATH)
        set_wallpaper(LOCAL_PATH)
        print("壁纸设置成功！")
    except Exception as e:
        print(f"发生错误: {e}")
