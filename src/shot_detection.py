import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os
# import ffmpeg
from config import Config
from pathlib import Path


SAMPLING_INT = 25

print(cv.__version__)

def shotDetection(path, config: Config):
	video_id = Path(path).stem
	vid = cv.VideoCapture(path)

	duration = vid.get(cv.CAP_PROP_POS_MSEC)
	frame_count = vid.get(cv.CAP_PROP_FRAME_COUNT)
	fps = vid.get(cv.CAP_PROP_FPS)

	hists = []
	BINS = 64
	ranges=[0, 256]
	SAMPLING_INT = 250
	frameCount = -1
	frameIntervals = []
	frames = []
	frameCounts = []

	success = 1
	while success:
		success, frame = vid.read()
		if frame is None:
			break
		frameCount += 1
		if frameCount % SAMPLING_INT == 0:
			frameIntervals.append(frameCount)
			frames.append(frame)
			frameCounts.append(frameCount)
			frameg = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
			hist = cv.calcHist(images=[frameg], channels=[0], 
								mask=None, histSize=[BINS], ranges=ranges)
			histt = cv.transpose(hist)
			hists.append(histt)

	for i in range(0, len(frames)):
		cv.imwrite(os.path.join(config.data['paths']['out'], f'{video_id}_{int(frameCounts[i])}_{int(1000* round(frameCounts[i] / fps))}_{frameIntervals[i]}.jpg'), frames[i])

	vid.release()

def videoFileFromImage(imageFilePath):
	parts = imageFilePath.split('_')
	if len(parts) >= 3:
		videoId = parts[0]
		frameNum = int(parts[2]) / 10
		#framerateDen = parts[2]
		return (f'{videoId}.mp4', int(frameNum))

