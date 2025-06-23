from sentence_transformers import SentenceTransformer 
from PIL import Image #to open images
import glob
import os
import numpy as np
import json
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
		self.model, self.preprocess = clip.load("ViT-B/32", device = self.config.device)

	def calculateEmbeddings(self):
		print("Calculating embeddings using device", self.config.device)
		files = glob.glob(f'{self.out_folder}/*.jpg')
		print('Found', len(files), 'shots!')

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




		# 	img_list.append(img.copy())
		# 	img.close()
		# 	filename = os.path.basename(file)
		# 	_file = Path(file)
		# 	filepath = _file.absolute()
		# 	self.filename_list.append(filename)
		# # len(img_list)

		self.embeddings = torch.cat(embeddings, dim=0)
		torch.save({
			'embeddings': self.embeddings,
			'filenames': self.filename_list
		}, self.embedding_path)

		# with open(self.filename_path, "w") as f:
		# 	for path in self.filename_list:
		# 		f.write(str(path) + "\n")


		# model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").eval()
		# processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

		# model.to(self.config.device)

		# embeddings = []

		# for img in img_list:
		# 	with torch.no_grad():
		# 		img_embed = model.get_image_features()


		# # old shit
		# self.model = SentenceTransformer('clip-ViT-B-32')

		# self.embeddings = self.model.encode(img_list, batch_size=32, normalize_embeddings=True)
		# # len(embeddings) #Amount of pictures
		# # embeddings.shape #Number of embeddings

		# print(len(self.embeddings), "shots found, filenames:", self.filename_list)
		# # data = {name: emb.tolist() for name, emb in zip(filename_list, self.embeddings)}

		# localEmbeddings = self.embeddings.cpu()
		# np.save(self.embedding_path, localEmbeddings)
		# with open(self.embedding_path, "w") as f:
		# 	json.dump(data, f, indent=2)

	def loadSaved(self):

		data = torch.load(self.embedding_path)
		self.embeddings = data['embeddings']
		self.filename_list = data['filenames']
		# # with open(self.embedding_path, "r") as f:
		# # 	embedding_data = json.load(f)
		# # self.embeddings = {k: np.array(v) for k, v in embedding_data.items()}
		# localEmbeddings = np.load(self.embedding_path)
		# self.embeddings = localEmbeddings

		# with open(self.filename_path, "r") as f:
		# 	self.filename_list = [line.strip() for line in f.readlines()]

	def estimate(self, query):
		annoy_index = AnnoyIndex(512, metric='angular')
		for idx, embedding in enumerate(self.embeddings):
			annoy_index.add_item(idx, embedding)
		annoy_index.build(200)

		result = []
		with torch.no_grad():
			print("Query:", query)
			text = clip.tokenize([query]).to(self.config.device)
			features = self.model.encode_text(text)
			print(f"Query shape: {features.shape}")
			result = annoy_index.get_nns_by_vector(features[0], 50)
			print(f"Most likely frames: {result}")

		paths = []
		for res in result:
			filename = self.filename_list[res]
			videofile, frame = shot_detection.videoFileFromImage(filename)
			paths.append((filename, videofile, frame))

		return paths

	# doing model stuff

		# annoy_index = AnnoyIndex(512, metric="angular" ) #Dimension and metric to compute distance
		# #Could also use cosine and more
		# print(query)

		# for idx, embedding in enumerate(self.embeddings):
		# 	annoy_index.add_item(idx, embedding) #Number of the index, actual embeddings
			
		# annoy_index.build(200)#Number of branches in your index 10, up to 100 200, the higher the more accurate, but will be a larger file

		# query_text = self.model.encode([query])
		# print(f"Query shape: {query_text.shape}") #Text query encoded

		# result = annoy_index.get_nns_by_vector(query_text[0], 50) #nns = nearest neighbour. So five nearest neighbours
		# print(f"Most likely frames: {result}") #Image ID of most likely frame

		# # lookup paths and return them (image url, video url, frame)
		# paths = []
		# for res in result:
		# 	filename = self.filename_list[res]
		# 	videofile, frame = shot_detection.videoFileFromImage(filename)
		# 	paths.append((filename, videofile, frame))

		# # paths = [self.filename_list[i] for i in result]

		# # for item in result:
		# # 	#print(item, print(files[item]))
		# # 	display(img_list[item])
		# return paths
