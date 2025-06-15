from sentence_transformers import SentenceTransformer 
from PIL import Image #to open images
import glob
import os
import json
from config import Config
from annoy import AnnoyIndex #Checks for similarity of vectors

def embeds(config: Config):
	out_folder = config.data['paths']['out']
	files = glob.glob(f'{out_folder}/**/*.jpg')
	print('Found', len(files), 'shots!')

	img_list = []
	filename_list = []

	for file in files:
		img = Image.open(file)
		img_list.append(img.copy())
		img.close()
		filename = os.path.basename(file)
		filename_list.append(filename)
		
	len(img_list)

	model = SentenceTransformer('clip-ViT-B-32')

	embeddings = model.encode(img_list, batch_size=32)
	len(embeddings) #Amount of pictures
	embeddings.shape #Number of embeddings

	print(filename_list)
	data = {name: emb.tolist() for name, emb in zip(filename_list, embeddings)}

	with open("embeddings.json", "w") as f:
		json.dump(data, f, indent=2)

	annoy_index = AnnoyIndex(512, metric="angular" ) #Dimension and metric to compute distance
	#Could also use cosine and more

	for idx, embedding in enumerate(embeddings):
		annoy_index.add_item(idx, embedding) #Number of the index, actual embeddings
		
	annoy_index.build(200)#Number of branches in your index 10, up to 100 200, the higher the more accurate, but will be a larger file

	query_text = model.encode(["Man in black and white martial arts"])
	print(f"Query shape: {query_text.shape}") #Text query encoded

	result = annoy_index.get_nns_by_vector(query_text[0], 10) #nns = nearest neighbour. So five nearest neighbours
	print(f"Most likely frames: {result}") #Image ID of most likely frame

	# for item in result:
	# 	#print(item, print(files[item]))
	# 	display(img_list[item])