import pandas as pd
import os
import subprocess
import re

def download_and_convert(video_url, counter):
    if not video_url:
        print(f"No valid video URL found for video_{counter}. Skipping...")
        return

    intermediate_output = f"D:\\Coding Files\\GitHub\\Findtrashsongs Automation\\video_{counter}.mp4" 
    final_output = f"D:\\Coding Files\\GitHub\\Findtrashsongs Automation\\video_{counter}_premiere.mp4"
    
    yt_dlp_command = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio",
        "-o", intermediate_output,
        video_url
    ]
    
    try:
        subprocess.run(yt_dlp_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading video: {e}")
        return

    ffmpeg_command = f'ffmpeg -y -i "{intermediate_output}" -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k "{final_output}"'
    try:
        subprocess.run(ffmpeg_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting video: {e}")
        return

    if os.path.exists(intermediate_output):
        os.remove(intermediate_output)
        print(f"Deleted intermediate file: {intermediate_output}")


def clean_track_name(track_name):
    clean_name = re.sub(r'\(.*?\)|feat\.|[^A-Za-z0-9 ]+', '', track_name).strip()
    return clean_name

def clean_artist_name(artist_name):
    clean_name = artist_name.split(',')[0].strip()
    return clean_name

def clean_track_name(track_name):
    clean_name = re.sub(r'\(.*?\)|feat\.|[^A-Za-z0-9 ]+', '', track_name).strip()
    return clean_name

def clean_artist_name(artist_name):
    clean_name = artist_name.split(',')[0].split('&')[0].strip()
    return clean_name
    
def search_youtube(track_name, artist_name):
    cleaned_track_name = clean_track_name(track_name)
    cleaned_artist_name = clean_artist_name(artist_name)

    live_keywords = ["live", "concert", "performance", "session", "live show"]

    for keyword in live_keywords:
        query = f"{cleaned_track_name} {cleaned_artist_name} {keyword}"
        
        yt_dlp_command = [
            "yt-dlp",
            f"ytsearch20:{query}",  
            "--get-title", "--get-id"
        ]

        try:
            result = subprocess.run(yt_dlp_command, shell=True, capture_output=True, text=True)
            output = result.stdout.strip().split("\n")
            
            if output and len(output) > 1:
                print(f"Found results for {track_name} by {artist_name} using '{keyword}' keyword.")
                for i in range(0, len(output), 2):
                    video_title = output[i]
                    video_id = output[i + 1]
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    print(f"Title: {video_title}\nURL: {video_url}")

                return f"https://www.youtube.com/watch?v={output[1]}"
        except subprocess.CalledProcessError as e:
            print(f"Error searching YouTube for {track_name} by {artist_name} using '{keyword}': {e}")

    print(f"No live video found for {track_name} by {artist_name} using any keyword.")
    return None



def process_first_row(csv_file, counter):
    df = pd.read_csv(csv_file)

    if df.empty:
        print("No songs to process.")
        return

    row_to_process = df.iloc[0]
    
    track_name = row_to_process['Track Name']
    artist_name = row_to_process['Artist Name(s)']
    
    print(f"Processing {track_name} by {artist_name}...")

    video_url = search_youtube(track_name, artist_name)

    download_and_convert(video_url, counter)

    df = df.drop(df.index[0])
    df.to_csv(csv_file, index=False)
    print(f"Processed {track_name} by {artist_name}. Exiting.")

if __name__ == "__main__":
    csv_file = "D:\\Coding Files\\GitHub\\Findtrashsongs Automation\\Playlist.csv"
    counter = 62  
    
    process_first_row(csv_file, counter)
