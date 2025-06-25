import sys
import os
import shutil
from pathlib import Path

from config import Config
from video_manager import VideoManager
from shot_detection import shotDetection
from model import Model
from dres_api import DRESClient

from web import create_web_api

print("=== video-content-search ===")
print("(generic name, ikr?)")

print("CWD:", os.getcwd())
print("Launch settings: ", sys.argv)

config_file_path = Path('config.json')
config = Config(config_file_path)

video_manager = VideoManager(config)
print(video_manager)

model = Model(config)

# do actions depending on args
# check for analyze mode
if len(sys.argv) > 1 and sys.argv[1].strip() == "analyze":
	print("Launching analyze mode...")
	os.makedirs(config.data['paths']['out'], exist_ok=True)

	for video in video_manager.list_files():
		# copy to out folder
		filename = os.path.basename(video)
		print(filename)
		shutil.copy2(video, os.path.join(config.data['paths']['out'], filename))
		# shot detection
		shotDetection(video, config)
	model.calculateEmbeddings()
	model.estimate("Car and person")
else:
	print("Launching Web API..")

	# load latest state of the model
	print("Looking existing stuff...")
	model.loadSaved()
	model.estimate("Car and person")

	api = create_web_api(config, model)
	api.run(debug=config.data['web']['debug'], host=config.data['web']['ip'], port=config.data['web']['port'])