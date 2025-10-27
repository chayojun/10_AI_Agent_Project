import datetime


def log(msg: str):
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{time}] {msg}")
