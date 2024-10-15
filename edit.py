from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.all import crop
from moviepy.editor import ColorClip, CompositeVideoClip, TextClip
from pkg_resources import parse_version
from PIL import Image
import json

#TextClip.list('font')

if parse_version(Image.__version__) >= parse_version('10.0.0'):
    Image.ANTIALIAS = Image.LANCZOS

def load_song_info(file_path='song_info.json'):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

def edit_video_body(path):

    clip = VideoFileClip(path)
    try:
        cut_clip = clip.subclip(45, 75)

        cropped_clip = crop(cut_clip, x_center=clip.w // 2, y_center=clip.h // 2, width=866, height=1080)

        resize_clip = cropped_clip.resize(height=1188)

        white_background = ColorClip(size=(1080, 1920), color=(255, 255, 255), duration=resize_clip.duration)

        final_clip_with_bg = CompositeVideoClip([white_background, resize_clip.set_position(('center', 420))])
        final_clip_with_bg = final_clip_with_bg.set_audio(resize_clip.audio)

        final_resized_clip = final_clip_with_bg.resize(height=1920)

        final_resized_clip_with_audio = final_resized_clip.set_audio(cut_clip.audio)
        final_resized_clip_with_audio.audio.write_audiofile("temp_audio.wav")

        text1 = TextClip(f"Day {day} of dumping on trash songs for you", font='Arial-Narrow-Bold', fontsize=57, color='black')
        text2 = TextClip("so you don't have to", font='Arial-Narrow-Bold', fontsize=57, color='black')
        text1 = text1.set_position(("center", 245)).set_duration(final_resized_clip_with_audio.duration)
        text2 = text2.set_position((70, 312)).set_duration(final_resized_clip_with_audio.duration)

        final_output = CompositeVideoClip([final_resized_clip_with_audio, text1, text2])
        final_output.write_videofile("output_with_caption.mp4", fps=24)
        final_output.close()
        
    finally:
        clip.reader.close()
        if clip.audio:
            clip.audio.reader.close_proc()
        del clip
        

if __name__ == "__main__":
    song_info = load_song_info()
    day = song_info['day']
    song_name = song_info['song_name']
    artist_name = song_info['artist_name']

    edit_video_body("video_premiere.mp4")