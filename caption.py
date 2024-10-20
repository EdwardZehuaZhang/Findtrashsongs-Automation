from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import ColorClip, CompositeVideoClip, TextClip
from spleeter.separator import Separator
import os
import whisper
import lyricsgenius
from fuzzywuzzy import fuzz
import gc
import pandas as pd
import json
import re

def load_song_info(file_path='song_info.json'):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


def extract_vocals(input_video):
    output_folder = os.path.dirname(input_video)
    separator = Separator('spleeter:2stems', multiprocess=False)  
    separator.separate_to_file(input_video, output_folder)
    
    vocal_file_path = os.path.join(output_folder, 'output_with_caption', 'vocals.wav')
    return vocal_file_path


def genius_lyrics(song_name, artist_name):
    genius = lyricsgenius.Genius('lx-O3_R9qvirc4u1di-uzVLtR_bVpNiOYnG4dAMKv-kQBmwLKYwGlOy4hPlfmEvU')
    song = genius.search_song(song_name, artist_name)
    
    cleaned_lyrics = re.sub(r'\[.*?\]', '', song.lyrics)
    
    cleaned_lyrics = cleaned_lyrics.strip()
    
    return cleaned_lyrics


def transcribe_audio_whisper_with_segments(audio_file_path):
    model = whisper.load_model("medium")
    result = model.transcribe(audio_file_path)
    return result["segments"]
def match_correct_lyrics(transcribed_segments, correct_lyrics):
    matched_segments = []
    correct_lyrics_list = correct_lyrics.split("\n")  
    
    max_lines_to_match = 3  
    line_boost_factor = 1.2  

    for segment in transcribed_segments:
        transcribed_text = segment['text'].strip()

        best_match = None
        highest_weighted_score = 0

        for i in range(len(correct_lyrics_list)):
            for n_lines in range(1, max_lines_to_match + 1):
                if i + n_lines <= len(correct_lyrics_list):  
                    correct_lines_slice = " ".join(correct_lyrics_list[i:i + n_lines]).strip()
                    
                    similarity_score = fuzz.ratio(transcribed_text.lower(), correct_lines_slice.lower())

                    weighted_score = similarity_score * (line_boost_factor ** (n_lines - 1))

                    if weighted_score > highest_weighted_score:
                        best_match = correct_lines_slice
                        highest_weighted_score = weighted_score

        print(f"Best match for '{transcribed_text}': '{best_match}' with weighted score {highest_weighted_score}")

        matched_segments.append({
            'start': segment['start'],
            'end': segment['end'],
            'text': best_match if best_match else transcribed_text
        })

    print("\nFinal Matched Segments:")
    for seg in matched_segments:
        print(f"{seg['start']} - {seg['end']}: {seg['text']}")

    return matched_segments

def add_captions_to_video_from_matched(video_path, matched_segments, day, song_name, artist_name):
    video = VideoFileClip(video_path)
    captions = []
    video_height = video.h

    for segment in matched_segments:
        text = segment['text']
        start_time = segment['start']
        end_time = segment['end']

        print(f"Adding caption: {text} from {start_time} to {end_time}")

        temp_caption = TextClip(text, font="OCR-A-Extended", fontsize=37, color='white',
                                size=(video.w - 600, None), method='caption')

        caption_height = temp_caption.size[1]

        y_position = 970 - (caption_height / 2)

        caption = temp_caption.set_position(('center', y_position)) \
                              .set_start(start_time) \
                              .set_duration(end_time - start_time)

        captions.append(caption)

    final_video = CompositeVideoClip([video, *captions])
    
    output_filename = f"Day {day} {song_name} - {artist_name}.mp4"
    
    final_video.write_videofile(output_filename, codec="libx264", audio_codec="aac")
    return output_filename



def run_caption_pipeline():
    vocal_file_path = extract_vocals("output_with_caption.mp4")

    correct_lyrics = genius_lyrics(song_name, artist_name)

    print("\nFull correct lyrics:\n")
    print(correct_lyrics)

    transcribed_segments = transcribe_audio_whisper_with_segments(vocal_file_path)

    matched_segments = match_correct_lyrics(transcribed_segments, correct_lyrics)

    add_captions_to_video_from_matched("output_with_caption.mp4", matched_segments, day, song_name, artist_name)

    gc.collect()


if __name__ == "__main__":
    song_info = load_song_info()
    day = song_info['day']
    song_name = song_info['song_name']
    artist_name = song_info['artist_name']

    run_caption_pipeline()