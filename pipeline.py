import os
import subprocess
import gc
import time
import shutil
import sys
import pandas as pd
import json
import logging
import numpy as np

def save_song_info_to_file(day, song_name, artist_name, file_path='song_info.json'):
    day = int(day) if isinstance(day, (pd.Int64Dtype, pd.Series, np.int64)) else day
    song_info = {
        "day": day,  
        "song_name": song_name,
        "artist_name": artist_name
    }
    with open(file_path, 'w') as json_file:
        json.dump(song_info, json_file)



def load_song_info(file_path='song_info.json'):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

def process_first_row(csv_file):
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file, encoding='ISO-8859-1')

    if df.empty:
        logging.error("No songs to process.")
        return None, None, None

    row_to_process = df.iloc[0]
    day = row_to_process['Day']
    song_name = row_to_process['Track Name']
    artist_name = row_to_process['Artist Name(s)'].split(',')[0].split('&')[0].strip()

    logging.info(f"Processing {song_name} by {artist_name} for Day {day}...")

    df = df.drop(df.index[0])
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')  

    return day, song_name, artist_name


def run_subprocess_with_realtime_output(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    process.poll()

def run_pipeline():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('pipeline_log.txt'), 
            logging.StreamHandler(sys.stdout)  
        ]
    )

    day, song_name, artist_name = process_first_row(csv_file)
    if not day or not song_name or not artist_name:
        logging.error("Song information missing. Exiting pipeline.")
        return
    save_song_info_to_file(day, song_name, artist_name)

    song_info = load_song_info()
    day = song_info['day']
    song_name = song_info['song_name']
    artist_name = song_info['artist_name']

    logging.info("Starting description generation...")
    run_subprocess_with_realtime_output([r"D:/Coding Files/GitHub/Findtrashsongs Automation/.venv/Scripts/python.exe", "description.py"])

    logging.info("Starting download pipeline...")
    run_subprocess_with_realtime_output([r"D:/Coding Files/GitHub/Findtrashsongs Automation/.venv/Scripts/python.exe", "download.py"])

    logging.info("Starting video editing...")
    run_subprocess_with_realtime_output([r"D:/Coding Files/GitHub/Findtrashsongs Automation/.venv/Scripts/python.exe", "edit.py"])

    time.sleep(20)
    gc.collect()

    logging.info("Starting caption pipeline...")
    run_subprocess_with_realtime_output([r"D:/Coding Files/GitHub/Findtrashsongs Automation/.venv/Scripts/python.exe", "caption.py"])

    gc.collect()

    logging.info("Cleaning up unnecessary files...")

    output_with_caption_folder = "output_with_caption"
    output_with_caption_file = "output_with_caption.mp4"
    temp_audio_file = "temp_audio.aac"

    if os.path.exists(output_with_caption_folder):
        shutil.rmtree(output_with_caption_folder)
        logging.info(f"Deleted folder: {output_with_caption_folder}")

    if os.path.exists(output_with_caption_file):
        os.remove(output_with_caption_file)
        logging.info(f"Deleted file: {output_with_caption_file}")

    if os.path.exists(temp_audio_file):
        os.remove(temp_audio_file)
        logging.info(f"Deleted file: {temp_audio_file}")

    logging.info("Cleanup complete.")

    main_script_path = os.path.join(os.path.dirname(__file__), 'upload', 'main.py')

    logging.info("Starting the final upload script...")
    run_subprocess_with_realtime_output([r"D:/Coding Files/GitHub/Findtrashsongs Automation/.venv/Scripts/python.exe", main_script_path])

    logging.info("All tasks completed.")

if __name__ == "__main__":
    csv_file = "D:\\Coding Files\\GitHub\\Findtrashsongs Automation\\Playlist.csv"
    run_pipeline()
