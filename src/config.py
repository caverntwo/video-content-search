from pathlib import Path
import torch
import os
import json

class Config:
	
	def __init__(self, config_path):
		self.config_path = config_path
		self.cwd = os.getcwd()

		self.__load_from_json()

		# TODO: Possible JSON Schema validation to config file

		# print config
		self.__print_json_keys(self.data)

		# get device
		print("Checking devices...")
		device_str = "cpu"
		if torch.cuda.is_available(): device_str = "cuda"
		self.device = torch.device(device_str)
		print(f"... found {device_str}!")

		# set seed
		self.seed = self.data['general']['seed']
		print(f"Seed: ", self.seed)
		torch.manual_seed(self.seed)

	def __load_from_json(self):
		if not Path.exists(self.config_path):
			raise FileNotFoundError(f"Config file '{self.config_path.resolve()}' not found!")
		else:
			with open(self.config_path, 'r') as f:
					self.data = json.load(f)

	def __print_json_keys(self, data, prefix=''):
		if isinstance(data, dict):
			for key, value in data.items():
				full_key = f"{prefix}.{key}" if prefix else key
				self.__print_json_keys(value, full_key)
		elif isinstance(data, list):
			for idx, item in enumerate(data):
				self.__print_json_keys(item, f"{prefix}[{idx}]")
		else:
			print(f"{prefix}: {data}")
