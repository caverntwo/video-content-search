FROM python:3.12.2-bookworm

WORKDIR /usr/src/app

# Install pip packages
COPY requirements.txt ./

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN  pip3 install --index-url https://software.repos.intel.com/python/pypi --extra-index-url https://pypi.org/simple mkl_fft mkl_random


RUN pip3 install --no-cache-dir -r requirements.txt

# Copy files
COPY . .
COPY config_docker.json config.json

# Run
CMD ["python", "./src/main.py"]