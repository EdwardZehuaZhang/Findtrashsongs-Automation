import os
import time
from instagram_upload import main as instagram_upload
from snapchat_upload import main as snapchat_upload
from tiktok_upload import main as tiktok_upload
from youtube_upload import main as youtube_upload
from x_upload import main as x_upload
from linkedin_upload import main as linkedin_upload
from config import Config

def upload_with_retry(upload_func, *args, max_retries=3):
    for attempt in range(max_retries):
        try:
            upload_func(*args)
            print(f"{upload_func.__name__} succeeded on attempt {attempt + 1}")
            return True
        except Exception as e:
            print(f"{upload_func.__name__} failed on attempt {attempt + 1}: {e}")
            time.sleep(5)
    print(f"{upload_func.__name__} failed after {max_retries} attempts")
    return False

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)

    video_path = Config.get_video_path()
    description_file_path = Config.description_file_path

    platforms = [
        ("Snapchat", snapchat_upload, None),
        ("TikTok", tiktok_upload, Config.tiktok_cookies_file),
        ("Instagram", instagram_upload, Config.instagram_cookies_file),
        ("YouTube", youtube_upload, Config.youtube_cookies_file),
        ("X", x_upload, Config.x_cookies_file),
        ("Linkedin", linkedin_upload, Config.linkedin_cookies_file)
    ]

    failed_uploads = []

    for platform_name, upload_func, cookies_file in platforms:
        if not upload_with_retry(upload_func, video_path, description_file_path, cookies_file):
            failed_uploads.append((platform_name, upload_func, video_path, description_file_path, cookies_file))

    while failed_uploads:
        platform_name, func, *args = failed_uploads.pop(0)
        print(f"Retrying {platform_name} upload...")
        if not upload_with_retry(func, *args):
            failed_uploads.append((platform_name, func, *args))

if __name__ == "__main__":
    main()
