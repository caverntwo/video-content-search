# Video-Content-Search
AI-based video content search browser...

## Overview
This application consists of 2 parts:
* Backend: Python-based, exposes an API, connects to DRES API
* Web app: Vue-based frontend, uses API

### Backend
The backend is based on Python 3.12.2, uses [CLIP](https://github.com/openai/CLIP) and opencv.
It exposes a [Flask API](https://flask.palletsprojects.com/en/stable/) to which the web API connects to.

### Web App
Vue/Vite based, rudimentary front-end, consisting of a search bar and a video list, which updates on change of the search text. A video can be clicked on, opening the video viewer. There, a submission to the DRES API can be made.

## Installation
The installation is rather simple. If the goal is to just run the build, run the latest docker container.

### Docker
**Requirements:**
* Docker

The docker container only contains the 200 videos used for the small competition, it cannot be used to train the system for new videos. For this, follow the next session.

For this, run the `docker-compose.yml` file using `docker compose up`:
```yml
services:
  backend:
    image: caverntwo/video-content-search-backend
    ports:
      - "3456:3456"
    networks:
      - video-network
  web:
    image: caverntwo/video-content-search-web
    ports: 
      - "3457:3457"
    networks:
      - video-network
networks:
  video-network: {}
```

If you check out this repository, the `docker-compose.yml` file is in the root folder.

### Native Setup
**Requirements:**
* [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) (doesn't matter what version, I used Miniconda)
* [Bun](https://bun.sh/)

Follow the official installation guides.

**Steps:**
1. Make `conda` environment: `conda create --name vid python=3.12.2`
2. Install [PyTorch](https://pytorch.org/get-started/locally/) for your hardware
3. *pip* packages: `pip3 install --no-cache-dir -r requirements.txt`
4. Run backend: `python main.py`
5. Go to `web` folder: `cd web`
6. Install *bun* packages: `bun install`
7. Run web app: `bun dev`

The application is functional, yet nothing will happen. It needs to be configured and trained to the videos first!

#### Training on Videos
Now, to get the system ready for video browsing, add videos into the `raw` folder (`.mp4` files directly in `raw` folder without sub-folders!)

First, check the `config.json` file and adjust if necessary.
Then, the system needs to be trained: `python main.py analyze`
This rocess will run for a while, extracting the shots from the videos first and then analyzing them with *CLIP*.

After the process is done, run the backend and frontend again with:
* `python main.py`
* `bun dev` (from within `web` folder)

## Warning
I'm aware that the `config.json` file contains credentials. This is obviously not of any good practice and definitely not recommended!