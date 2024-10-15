import json
import os

class Config:
    description_file_path = ""
    instagram_cookies_file = ""
    tiktok_cookies_file = ""
    youtube_cookies_file = ""
    x_cookies_file = ""
    snapchat_cookies_file = ""
    linkedin_cookies_file = ""
    douyin_cookies_file = ""
    bilibili_cookies_file = ""
    snapchat_username = ""
    snapchat_password = ""
    instagram_username = ""
    instagram_password = ""
    tiktok_username = ""
    tiktok_password = ""
    youtube_email = ""
    youtube_password ="" 
    x_email = ""
    x_password ="" 
    linkedin_email = ""
    linkedin_password = "" 
    douyin_email = ""
    douyin_password = "" 
    bilibili_email = ""
    bilibili_password = ""

    @staticmethod
    def load_song_info(file_path='D:\\Coding Files\\GitHub\\Findtrashsongs Automation\\song_info.json'):
        with open(file_path, 'r') as json_file:
            return json.load(json_file)

    @staticmethod
    def get_video_path():
        song_info = Config.load_song_info()
        day = song_info['day']
        song_name = song_info['song_name']
        artist_name = song_info['artist_name']
        video_name = f"Day {day} {song_name} - {artist_name}.mp4"
        return os.path.join("D:\\Coding Files\\GitHub\\Findtrashsongs Automation", video_name)
