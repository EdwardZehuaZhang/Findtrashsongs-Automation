from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.all import crop
from moviepy.editor import ColorClip, CompositeVideoClip, TextClip
from pkg_resources import parse_version
from PIL import Image
import json

print(TextClip.list('font'))