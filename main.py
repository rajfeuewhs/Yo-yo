import cv2
import numpy as np
import subprocess
import threading
import time
from youtube_api import get_subscribers

CHANNEL_ID = "UCr5ik3Qjslqnl6DB8XwJxDg"
STREAM_KEY = "77cs-jw6x-yfeu-m2ks-82d6"

width = 1280
height = 720
fps = 30

current_subs = 0


def update_subs():
    global current_subs
    while True:
        current_subs = get_subscribers(CHANNEL_ID)
        print("Subscribers:", current_subs)
        time.sleep(5)


def start_stream():

    command = [
        "ffmpeg",
        "-y",
        "-f","rawvideo",
        "-vcodec","rawvideo",
        "-pix_fmt","bgr24",
        "-s",f"{width}x{height}",
        "-r",str(fps),
        "-i","-",
        "-f","lavfi",
        "-i","anullsrc",
        "-c:v","libx264",
        "-pix_fmt","yuv420p",
        "-preset","veryfast",
        "-c:a","aac",
        "-b:a","128k",
        "-f","flv",
        f"rtmp://x.rtmp.youtube.com/live2/{STREAM_KEY}"
    ]

    pipe = subprocess.Popen(command, stdin=subprocess.PIPE)

    while True:

        frame = np.zeros((height,width,3),np.uint8)

        frame[:] = (120,0,200)   # neon purple

        text1 = "LIVE SUBSCRIBER COUNT"
        text2 = str(current_subs)

        cv2.putText(frame,text1,(300,200),
                    cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),3)

        cv2.putText(frame,text2,(500,400),
                    cv2.FONT_HERSHEY_SIMPLEX,3,(255,255,255),5)

        pipe.stdin.write(frame.tobytes())


threading.Thread(target=update_subs).start()

start_stream()
