import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os
import ffmpeg
from pathlib import Path

print(cv.__version__)

def shotDetection(title):

    vid = cv.VideoCapture(f"raw/V3C1_200/{title}")
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
            cv.imshow(f"Frame {frameCount}", frameg)
            plt.plot(hist, label=f'{frameCount}')
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

    os.makedirs("output", exist_ok=True)
    os.makedirs(f"output/{title}", exist_ok=True)
   
    for i in range(0,len(labels)):
        lbl = labels[i][0]        
        cv.imwrite(f'output/{title}/{lbl}_{frameIntervals[i]}.jpg', frames[i])
    vid.release()


directory = os.fsencode("raw/V3C1_200")
#D:\Github\video-content-search\raw\V3C1_200
#D:\Github\video-content-search\src\shot-detection

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    filepath = os.path.join("raw/V3C1_200", filename)
    if filename.endswith(".mp4"):
        shotDetection(filename)
        continue
    else:
        continue



