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

	@api.route('/videos', methods=['GET', 'POST'])
	def videos():
		search = request.args.get('search')

		try:
			# if search is not None:
				search = request.get_data(as_text=True)
				print(search)
				results = model.estimate(search)
				webresults = [{'thumbnail': f'/stream/{result[0]}', 'video': f'/stream/{result[1]}', 'frame': result[2]} for result in results]

				return jsonify(webresults)
			# else: #list all videos
			# 	return 
		except:
			return "Error", 400

	@api.route('/stream/<path:filename>')
	def stream(filename):
		print(config.cwd)
		imagefolder = os.path.join(config.cwd, config.data['paths']['out'])
		print(imagefolder, filename)
		return send_from_directory(imagefolder, filename)
	return api