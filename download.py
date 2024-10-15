import pandas as pd
import os
import subprocess
import re
import json

def load_song_info(file_path='song_info.json'):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)
    
def download_and_convert(video_url):
    if not video_url:
        print(f"No valid video URL found for video. Skipping...")
        return

    intermediate_output = f"D:\\Coding Files\\GitHub\\Findtrashsongs Automation\\video.mp4" 
    final_output = f"D:\\Coding Files\\GitHub\\Findtrashsongs Automation\\video_premiere.mp4"
    
    yt_dlp_command = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio",
        "-o", intermediate_output,
        video_url
    ]
    
    try:
        result = subprocess.run(yt_dlp_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
        print(result.stderr.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error downloading video: {e}")
        return

    ffmpeg_command = f'ffmpeg -y -i "{intermediate_output}" -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k "{final_output}"'
    try:
        result = subprocess.run(ffmpeg_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
        print(result.stderr.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error converting video: {e}")
        return

    if os.path.exists(intermediate_output):
        os.remove(intermediate_output)
        print(f"Deleted intermediate file: {intermediate_output}")



def clean_song_name(song_name):
    clean_name = re.sub(r'\(.*?\)|feat\.|[^A-Za-z0-9 ]+', '', song_name).strip()
    return clean_name

def clean_artist_name(artist_name):
    clean_name = artist_name.split(',')[0].split('&')[0].strip()
    return clean_name

    
def search_youtube(song_name, artist_name):
    cleaned_song_name = clean_song_name(song_name)
    cleaned_artist_name = clean_artist_name(artist_name)

    live_keywords = ["live", "concert", "performance", "session", "live show"]

    for keyword in live_keywords:
        query = f"{cleaned_song_name} {cleaned_artist_name} {keyword}"
        
        yt_dlp_command = [
            "yt-dlp",
            f"ytsearch20:{query}",  
            "--get-title", "--get-id"
        ]

        try:
            result = subprocess.run(yt_dlp_command, shell=True, capture_output=True, text=True)
            output = result.stdout.strip().split("\n")
            
            if output and len(output) > 1:
                print(f"Found results for {song_name} by {artist_name} using '{keyword}' keyword.")
                for i in range(0, len(output), 2):
                    video_title = output[i]
                    video_id = output[i + 1]
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    print(f"Title: {video_title}\nURL: {video_url}")

                return f"https://www.youtube.com/watch?v={output[1]}"
        except subprocess.CalledProcessError as e:
            print(f"Error searching YouTube for {song_name} by {artist_name} using '{keyword}': {e}")

    print(f"No live video found for {song_name} by {artist_name} using any keyword.")
    return None


def run_download_pipeline():
    print(f"Processing {song_name} by {artist_name}...")

    video_url = search_youtube(song_name, artist_name)

    download_and_convert(video_url)

    print(f"Processed {song_name} by {artist_name}. Exiting.")


if __name__ == "__main__":
    song_info = load_song_info()
    day = song_info['day']
    song_name = song_info['song_name']
    artist_name = song_info['artist_name']
    
    run_download_pipeline()
