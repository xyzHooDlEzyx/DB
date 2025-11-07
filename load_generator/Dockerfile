FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY load_generator.py ./load_generator.py

ENV TARGET_URL="http://localhost:8000/api/accounts"
ENV BASIC_AUTH="YWRtaW46cGFzc3dvcmQ="
ENV THREADS="200"
ENV SLEEP_SECONDS="0.02"
ENV REQUEST_TIMEOUT="1"

CMD ["python", "load_generator.py"]
