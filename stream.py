import time
from youtube_api import get_subscribers
from stream import start_stream

CHANNEL_ID = "UCr5ik3Qjslqnl6DB8XwJxDg"
STREAM_KEY = "YOUR_STREAM_KEY"

last_subs = 0

start_stream(STREAM_KEY)

while True:
    subs = get_subscribers(CHANNEL_ID)

    if subs != last_subs:
        print(f"Subscribers: {subs}")

        if subs > last_subs:
            print("New Subscriber!")

        last_subs = subs

    time.sleep(5)
