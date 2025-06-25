from flask import jsonify, Flask, request, send_from_directory
from flask_cors import CORS
from config import Config
from model import Model
from dres_api import DRESClient
import os

def create_web_api(config: Config, model: Model):
	api = Flask(__name__, root_path=config.cwd)
	CORS(api, origins=["http://localhost:3457", "http://127.0.0.1:3457"]) # CORS to make web app work

	dres_api = DRESClient(config)
	dres_api.setup()

	@api.route('/')
	def index():
		return "Hello world! Use GET/POST /videos with parameter 'search'!"

	@api.route('/videos')
	def videos():
		search = request.args.get('search')

		try:
			results = []
			if search:
				print(search)
				results = model.estimate(search)
			else: #list all videos
				results = model.list_all()
			
			webresults = [{'id': result[0], 'thumbnail': f'/stream/{result[1]}', 'video': f'/stream/{result[2]}', 'frame': result[3], 'time': result[4]} for result in results]
			return jsonify(webresults)
		except:
			return "Error", 400

	@api.route('/stream/<path:filename>')
	def stream(filename):
		print(config.cwd)
		imagefolder = os.path.join(config.cwd, config.data['paths']['out'])
		print(imagefolder, filename)
		return send_from_directory(imagefolder, filename)

	@api.route('/submit/<videoId>', methods=['POST'])
	def submit(videoId:str):
		
		try:
			data = request.get_json()
			text = data.get('text')
			start = int(data.get('start') * 1000 + 0.5)
			end = int(data.get('end') * 1000 + 0.5)

			print("/submit")
			res = dres_api.submit(text, videoId, start, end)
			return res

		except:
			return "Error", 400

	return api