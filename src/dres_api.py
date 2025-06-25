import requests
import json
from typing import List, Dict
from config import Config
from pathlib import Path
from typing import Optional

class ApiClientAnswer:
	def __init__(
		self,
		text: Optional[str] = None,
		mediaItemName: Optional[str] = None,
		mediaItemCollectionName: Optional[str] = None,
		start: Optional[int] = None,
		end: Optional[int] = None
	):
		self.text = text
		self.mediaItemName = mediaItemName
		self.mediaItemCollectionName = mediaItemCollectionName
		self.start = start
		self.end = end

		self.is_setup = False

	def to_dict(self):
		return {
			"text": self.text,
			"mediaItemName": self.mediaItemName,
			"mediaItemCollectionName": self.mediaItemCollectionName,
			"start": self.start,
			"end": self.end,
		}

class ApiClientAnswerSet:
	def __init__(self, taskId: str, taskName: str, answers: List[ApiClientAnswer]):
		self.taskId = taskId
		self.taskName = taskName
		self.answers = answers

	def to_dict(self):
		return {
			"taskId": self.taskId,
			"taskName": self.taskName,
			"answers": [a.to_dict() for a in self.answers]
		}


class DRESClient:
	def __init__(self, config: Config):
		self.config = config
		self.base_url = config.data['dres']['base_url'].rstrip('/')
		self.token = None


	def login(self) -> bool:
		url = f"{self.base_url}/api/v2/login"

		payload = json.dumps({
		"username": self.config.data['dres']['username'],
		"password": self.config.data['dres']['password']
		})
		headers = {
			'Content-Type': 'application/json'
		}

		response = requests.request("POST", url, headers=headers, data=payload)
		if response.status_code == 200:
			self.sessionId = response.json().get("sessionId")
			print("[DRES] Login successful!")
			return True
		print("[DRES] Login failed!", response, response.status_code, response.content)
		return False
		
	
	def list_evaluations(self) -> List[Dict]:
		url = f"{self.base_url}/api/v2/evaluation/info/list"

		payload = {}
		headers = {
			'Cookie': f'SESSIONID={self.sessionId}'
		}

		response = requests.request("GET", url, headers=headers, data=payload)

		if response.status_code == 200:
			res = response.json()
			print(f"[DRES] Listing evaluation successful, found {len(res)} evaluations! Reponse: ", response, response.json)

			return res
		print("[DRES] Listing evaluations failed! Response: ", response, response.status_code, response.content)
		return None
	
	def submit_evaluation(self, evaluationId: str, taskName: str, text: str, videoId: str, start: int, end: int) -> bool:
		url = f"{self.base_url}/api/v2/submit/{evaluationId}?name={taskName}"

		answer_set_list = [
			ApiClientAnswerSet(
				taskId=evaluationId,
				taskName=taskName,
				answers=[
					ApiClientAnswer(text=text, mediaItemName=videoId, mediaItemCollectionName="IVADL", start=start, end=end,),
				]
			)
		]

		submission = {
			"answerSets": [a.to_dict() for a in answer_set_list]
		}
		payload = json.dumps(submission)
		headers = {
			'Cookie': f'SESSIONID={self.sessionId}'
		}

		response = requests.request("POST", url, headers=headers, data=payload)
		if response.status_code in (200, 201):

			print(f"[DRES] Submit response: ", response, response.json)
			
			res = response.json()
			print(f"[DRES] Submitted, Success: {res["submission"] == 'WRONG'}")
			return res
		print(f"[DRES] Submit request failed! Response: ", response, response.status_code, response.content)
		return response.content
		

	def setup(self):
		print("setting up API")
		if self.login():
			res = self.list_evaluations()
			self.evalId = res[0]['id']
			self.evalName = res[0]['name']
			print("Received Task", self.evalId, self.evalName)
			self.is_setup = True

	def submit(self, text:str, videoId:str, start:int, end:int):
		if self.is_setup:
			return self.submit_evaluation(self.evalId, self.evalName, text, videoId, start, end)
		return None
	
# config_file_path = Path('config.json')
# config = Config(config_file_path)
# client = DRESClient(config)
# if client.login():
# 	res = client.list_evaluations()
# 	evalId = res[0]["id"]
# 	name = res[0]['name']
# 	print(evalId, name)
# 	anser = ApiClientAnswer()
# 	client.submit_evaluation(evalId, name, "text1", "00001", 1234, 1234 )
