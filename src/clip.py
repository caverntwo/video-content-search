import requests
import torch
import json
import pathlib
from pathlib import Path
from PIL import Image
from transformers import AutoProcessor, AutoModel

model = AutoModel.from_pretrained("openai/clip-vit-base-patch32", torch_dtype=torch.bfloat16, attn_implementation="sdpa")
processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
model = model.to(device)

with open("imagenet-simple-labels.json", "r") as f:
    labels = json.load(f)

image_folder = Path("output/_Afew")

all_results = {}
top5_labels = []

for image_path in image_folder.glob("*.jpg"):

    top5_labels = []
    image = Image.open(image_path)
    inputs = processor(text=labels, images=image, return_tensors="pt", padding=True).to(device)

    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)
    most_likely_idx = probs.argmax(dim=1).item()
    most_likely_label = labels[most_likely_idx]

    top5 = probs.topk(5) # Returns top 5 highest probability labels
    print(top5)

    for idx in top5.indices[0]:
        all_results.update("image": image_path, "label": [] image labels[idx])

    print(f"Most likely label: {most_likely_label} with probability: {probs[0][most_likely_idx].item():.3f}")

with open("all_clip_results.json", "w") as f:
    json.dump(all_results, f, indent=2)