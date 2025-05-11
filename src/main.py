import sys
from pathlib import Path

from config import Config
from video_manager import VideoManager

print("=== video-content-search ===")
print("(generic name, ikr?)")

print("Launch settings: ", sys.argv)

config_file_path = Path('config.json')
config = Config(config_file_path)

video_manager = VideoManager(config)
print(video_manager)

# do actions depending on args
