from flask import jsonify, Flask, request, send_from_directory
from flask_cors import CORS
from config import Config
from model import Model
import os

def create_web_api(config: Config, model: Model):
	api = Flask(__name__, root_path=config.cwd)
	CORS(api, origins=["http://localhost:3457", "http://127.0.0.1:3457"]) # CORS to make web app work

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
	
	@api.route('/enable')
	def enable():
		try:
			print('/enable')
			if not config.dres_api.is_setup:
				config.dres_api.setup()
				return "set up"
			else:
				print("already set up")
				return "already set up"
		except:
			return "Error", 500


	@api.route('/submit/<videoId>')
	def submit(text, videoId, start, end):
		text = request.args.get('text')
		videoId = request.args.get('videoId')
		start = int(request.args.get('start'))
		end = int(request.args.get('end'))

		try:
			print("/submit")
			res = config.dres_api.submit(text, videoId, start, end)
			return res

		except:
			return "Error", 400

	return api