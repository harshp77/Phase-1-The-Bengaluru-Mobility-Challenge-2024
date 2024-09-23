FROM pytorch/pytorch:latest
WORKDIR /app
COPY . /app
RUN pip install opencv-contrib-python ultralytics omegaconf scipy joblib scikit-learn statsmodels lapx &&\
    apt-get update && apt-get install ffmpeg libsm6 libxext6 git  -y
CMD ["python", "app.py"]

