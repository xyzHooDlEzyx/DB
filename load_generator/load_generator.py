import os ,threading, time

import requests


TARGET_URL = os.environ.get(
    "TARGET_URL", "http://flask-gunicorn-balancer-1991448715.eu-north-1.elb.amazonaws.com:8000/api/accounts"
)
BASIC_AUTH = os.environ.get("BASIC_AUTH", "YWRtaW46cGFzc3dvcmQ=")
THREADS = int(os.environ.get("THREADS", "50"))
SLEEP_SECONDS = float(os.environ.get("SLEEP_SECONDS", "0.01"))
REQUEST_TIMEOUT = float(os.environ.get("REQUEST_TIMEOUT", "1"))

HEADERS = {
    "accept": "application/json",
    "authorization": f"Basic {BASIC_AUTH}",
}


def _spam():
    session = requests.Session()
    session.headers.update(HEADERS)
    while True:
        try:
            response = session.get(TARGET_URL, timeout=REQUEST_TIMEOUT)
            print(response.status_code)
        except Exception as exc:
            print("Error:", exc)
        time.sleep(SLEEP_SECONDS)


def main():
    threads = []
    for _ in range(THREADS):
        worker = threading.Thread(target=_spam)
        worker.daemon = True
        worker.start()
        threads.append(worker)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
