import subprocess
import time
from youtube_api import get_subscribers

CHANNEL_ID = "UCr5ik3Qjslqnl6DB8XwJxDg"
STREAM_KEY = "77cs-jw6x-yfeu-m2ks-82d6"

subs = "0"

def start_stream():

    global subs

    while True:

        subs = str(get_subscribers(CHANNEL_ID))

        text = f"LIVE SUBSCRIBER COUNT : {subs}"

        command = [
            "ffmpeg",
            "-re",
            "-f","lavfi",
            "-i","color=c=purple:s=1280x720:r=30",
            "-f","lavfi",
            "-i","anullsrc=channel_layout=stereo:sample_rate=44100",
            "-vf",f"drawtext=text='{text}':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=(h-text_h)/2",
            "-c:v","libx264",
            "-preset","veryfast",
            "-pix_fmt","yuv420p",
            "-b:v","2500k",
            "-maxrate","2500k",
            "-bufsize","5000k",
            "-c:a","aac",
            "-b:a","128k",
            "-ar","44100",
            "-f","flv",
            f"rtmp://x.rtmp.youtube.com/live2/{STREAM_KEY}"
        ]

        process = subprocess.Popen(command)
        time.sleep(5)
        process.kill()
