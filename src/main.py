import sys
from pathlib import Path

from config import Config
from video_manager import VideoManager
from shot_detection import shotDetection
import embeds

from web import create_web_api

print("=== video-content-search ===")
print("(generic name, ikr?)")

print("Launch settings: ", sys.argv)

config_file_path = Path('config.json')
config = Config(config_file_path)

video_manager = VideoManager(config)
print(video_manager)

# do actions depending on args
# check for analyze mode
if len(sys.argv) > 1 and sys.argv[1].strip() == "analyze":
	print("Launching analyze mode...")

	for video in video_manager.list_files():
		# shot detection
		shotDetection(video, config)
	embeds.embeds(config)
else:
	print("Launching Web API..")

	# load latest state of the model
	print("Looking existing stuff...")
	# model = Model(config)
	# model.load_latest_model()

	# api = create_web_api(config, model)
	# api.run(debug=config.app_config["debug"], host=config.app_config["ip"], port=config.app_config["port"])