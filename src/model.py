from sentence_transformers import SentenceTransformer 
from PIL import Image #to open images
import glob
import os
import numpy as np
import json
import time
import shot_detection
from pathlib import Path
from config import Config
from annoy import AnnoyIndex #Checks for similarity of vectors
from transformers import CLIPProcessor, CLIPModel
import torch
import clip

class Model():
	def __init__(self, config: Config):
		self.config = config
		self.out_folder = self.config.data['paths']['out']
		self.embedding_path = os.path.join(self.out_folder, self.config.data['paths']['embeddings_file_name'])
		self.annoy_index_path = os.path.join(self.out_folder, self.config.data['paths']['annoy_index_file_name'])
		self.model, self.preprocess = clip.load("ViT-B/32", device = self.config.device)

	def calculateEmbeddings(self):
		start_time = time.time()
		print(round(time.time()-start_time,3), "Calculating embeddings using device", self.config.device)
		files = glob.glob(f'{self.out_folder}/*.jpg')
		print(round(time.time()-start_time,3), 'Found', len(files), 'shots!')


		print(round(time.time()-start_time,3), "Generating embeddings...")
		self.filename_list = []
		embeddings = []

		for file in files:
			try:
				filename = os.path.basename(file)
				self.filename_list.append(filename)
				img = self.preprocess(Image.open(file).convert("RGB")).unsqueeze(0).to(self.config.device)

				with torch.no_grad():
					embedding = self.model.encode_image(img)
					embedding = embedding / embedding.norm(dim=-1, keepdim=True)  # normalize
					embeddings.append(embedding.cpu())

			except Exception as err:
				print("Err", err)
				return
		print(round(time.time()-start_time,3), "Saving embeddings...")

		self.embeddings = torch.cat(embeddings, dim=0)
		torch.save({
			'embeddings': self.embeddings,
			'filenames': self.filename_list
		}, self.embedding_path)

		print(round(time.time()-start_time,3), "Building annoy index...")
		self.annoy_index = AnnoyIndex(512, metric='angular')

		for idx, embedding in enumerate(self.embeddings):
			self.annoy_index.add_item(idx, embedding)
		self.annoy_index.build(200)

		self.annoy_index.save(self.annoy_index_path)

		print(round(time.time()-start_time,3), "Done calculating embeddings!")

	def loadSaved(self):

		print("Loading saved model...")
		data = torch.load(self.embedding_path)
		self.embeddings = data['embeddings']
		self.filename_list = data['filenames']

		print("Loading annoy index...")
		self.annoy_index = AnnoyIndex(512, metric='angular')
		self.annoy_index.load(self.annoy_index_path)

		print("Loaded successfully!")

	def estimate(self, query):
		start_time = time.time()
		print(round(time.time()-start_time,3), "Estimating query", query)
		

		print(round(time.time()-start_time,3), "Annoy Index built")

		result = []
		with torch.no_grad():
			print("Query:", query)
			text = clip.tokenize([query]).to(self.config.device)
			features = self.model.encode_text(text)
			print(f"Query shape: {features.shape}")
			result = self.annoy_index.get_nns_by_vector(features[0], 50)
			print(round(time.time()-start_time,3), f"Most likely frames: {result}")

		paths = []
		for res in result:
			filename = self.filename_list[res]
			videofile, frame = shot_detection.videoFileFromImage(filename)
			paths.append((filename, videofile, frame))

		print(round(time.time()-start_time,3), "done, returning...")
		return paths
