import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os
# import ffmpeg
from config import Config
from pathlib import Path

print(cv.__version__)

def shotDetection(path, config: Config):
	video_id = Path(path).stem
	vid = cv.VideoCapture(path)
	hists = []
	BINS = 64
	ranges=[0, 256]
	SAMPLING_INT = 250
	frameCount = -1
	frameIntervals = []
	frames = []

	while True:
		ret, frame = vid.read()
		if frame is None:
			break
		frameCount += 1
		if frameCount % SAMPLING_INT == 0:
			frameIntervals.append(frameCount)
			frames.append(frame)
			frameg = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
			hist = cv.calcHist(images=[frameg], channels=[0], 
								mask=None, histSize=[BINS], ranges=ranges)
			histt = cv.transpose(hist)
			hists.append(histt)
			# cv.imshow(f"Frame {frameCount}", frameg)
			# plt.plot(hist, label=f'{frameCount}')
   #plt.legend()
   #plt.show()



	#k-means clustering
	samples = np.zeros((len(hists), BINS))
	i = 0
	for h in hists:
		samples[i] = h
		i += 1

	samples = np.float32(samples) 
	numClusters = 10
	flags = cv.KMEANS_RANDOM_CENTERS

	criteria = (cv.TERM_CRITERIA_MAX_ITER + cv.TERM_CRITERIA_EPS, 10, 1.0)

	compactness,labels,centers = cv.kmeans(data=samples, K=numClusters, bestLabels=None, criteria=criteria, attempts=10, flags=flags)

	os.makedirs(os.path.join(config.data['paths']['out'], video_id), exist_ok=True)
   
	for i in range(0,len(labels)):
		lbl = labels[i][0]
		cv.imwrite(os.path.join(config.data['paths']['out'], video_id, f'{lbl}_{frameIntervals[i]}.jpg'), frames[i])
		# cv.imwrite(f'output/{video_id}/{lbl}_{frameIntervals[i]}.jpg', frames[i])
	vid.release()


# directory = os.fsencode("../../raw/V3C1_200")
# #D:\Github\video-content-search\raw\V3C1_200
# #D:\Github\video-content-search\src\shot-detection

# for file in os.listdir(directory):
#     filename = os.fsdecode(file)
#     filepath = os.path.join("raw/V3C1_200", filename)
#     if filename.endswith(".mp4"):
#         shotDetection(filename)
#         continue
#     else:
#         continue



