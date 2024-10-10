from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.all import crop
from moviepy.editor import ColorClip, CompositeVideoClip, TextClip
from pkg_resources import parse_version
from PIL import Image
from spleeter.separator import Separator
import os
import whisper
import pathlib
import lyricsgenius
from fuzzywuzzy import fuzz



if parse_version(Image.__version__) >= parse_version('10.0.0'):
    Image.ANTIALIAS = Image.LANCZOS

def edit_video_body(path):

    clip = VideoFileClip(path)

    cut_clip = clip.subclip(10, 40)

    cropped_clip = crop(cut_clip, x_center=clip.w // 2, y_center=clip.h // 2, width=866, height=1080)

    resize_clip = cropped_clip.resize(height=1188)

    white_background = ColorClip(size=(1080, 1920), color=(255, 255, 255), duration=resize_clip.duration)

    final_clip_with_bg = CompositeVideoClip([white_background, resize_clip.set_position(('center', 420))])
    final_clip_with_bg = final_clip_with_bg.set_audio(resize_clip.audio)

    final_resized_clip = final_clip_with_bg.resize(height=1920)

    final_resized_clip_with_audio = final_resized_clip.set_audio(cut_clip.audio)
    final_resized_clip_with_audio.audio.write_audiofile("temp_audio.wav")

    text1 = TextClip("Day 62 of dumping on trash songs for you", font='Arial-Narrow-Bold', fontsize=57, color='black')
    text2 = TextClip("so you don't have to", font='Arial-Narrow-Bold', fontsize=57, color='black')
    text1 = text1.set_position(("center", 245)).set_duration(final_resized_clip_with_audio.duration)
    text2 = text2.set_position((70, 312)).set_duration(final_resized_clip_with_audio.duration)

    final_output = CompositeVideoClip([final_resized_clip_with_audio, text1, text2])
    final_output.write_videofile("output_with_caption.mp4", fps=24)

edit_video_body("video_62_premiere.mp4")



def extract_vocals(input_video):
    output_folder = os.path.dirname(input_video)
    separator = Separator('spleeter:2stems')
    separator.separate_to_file(input_video, output_folder)
    
    vocal_file_path = os.path.join(output_folder, 'vocals', 'vocals.wav')
    return vocal_file_path

extract_vocals("output_with_caption.mp4")



def genius_lyrics(song_name, artist_name):
    genius = lyricsgenius.Genius('lx-O3_R9qvirc4u1di-uzVLtR_bVpNiOYnG4dAMKv-kQBmwLKYwGlOy4hPlfmEvU')
    song = genius.search_song(song_name, artist_name)
    return song.lyrics


def transcribe_audio_whisper_with_segments(audio_file_path):
    model = whisper.load_model("medium")
    result = model.transcribe(audio_file_path)
    return result["segments"]


def match_correct_lyrics(transcribed_segments, correct_lyrics):
    matched_segments = []
    correct_lyrics_list = correct_lyrics.split("\n")  
    for segment in transcribed_segments:
        transcribed_text = segment['text'].strip()
        
        best_match = None
        highest_score = 0

        for correct_line in correct_lyrics_list:
            similarity_score = fuzz.ratio(transcribed_text.lower(), correct_line.strip().lower())
            
            if similarity_score > highest_score:
                best_match = correct_line.strip()
                highest_score = similarity_score

        print(f"Best match for '{transcribed_text}': '{best_match}' with score {highest_score}")

        matched_segments.append({
            'start': segment['start'],
            'end': segment['end'],
            'text': best_match if best_match else transcribed_text 
        })

    print("\nFinal Matched Segments:")
    for seg in matched_segments:
        print(f"{seg['start']} - {seg['end']}: {seg['text']}")

    return matched_segments


def add_captions_to_video_from_matched(video_path, matched_segments):
    video = VideoFileClip(video_path)
    captions = []
    video_height = video.h

    for segment in matched_segments:
        text = segment['text']
        start_time = segment['start']
        end_time = segment['end']

        print(f"Adding caption: {text} from {start_time} to {end_time}")
        
        caption = TextClip(text, font="OCR-A-Extended", fontsize=37, color='white', 
                           size=(video.w - 600, None), method='caption')
        
        caption = caption.set_position(('center', 940)) \
                         .set_start(start_time) \
                         .set_duration(end_time - start_time)

        captions.append(caption)

    final_video = CompositeVideoClip([video, *captions])
    final_video.write_videofile("video_with_matched_lyrics_wrapped.mp4", codec="libx264", audio_codec="aac")



correct_lyrics = genius_lyrics("Astronaut in the Ocean", "Masked Wolf")
transcribed_segments = transcribe_audio_whisper_with_segments("output_with_caption/vocals.wav")

matched_segments = match_correct_lyrics(transcribed_segments, correct_lyrics)

add_captions_to_video_from_matched("output_with_caption.mp4", matched_segments)

import platform
platform.architecture()