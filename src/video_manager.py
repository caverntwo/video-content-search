import os
from pathlib import Path

from config import Config

# manages all raw video files

class VideoManager:
	def __init__(self, config: Config):
		self.config = config
		self.raw_folder = Path(config.data['paths']['raw'])
		self.videos = self._find_videos()
		self._index = 0 # init

	def list_files(self):
		return self.videos
	
	def __iter__(self):
		self._index = 0; # reset
		return self

	def __next__(self):
		if self._index < len(self.videos):
			file = self.videos[self._index]
			self._index += 1 # increase
			return file
		else:
			raise StopIteration
	
	def __str__(self):
		print(f"VideoManager: Found {len(self.videos)} videos!")
		for video in self.videos:
			print(video)

	def _find_videos(self):
		return sorted([f for f in self.raw_folder.rglob("*.mp4") if f.is_file()])