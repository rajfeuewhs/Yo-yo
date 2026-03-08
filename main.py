import time
from youtube_api import get_subscribers, update_title
from stream import start_stream
from chat import get_live_chat

CHANNEL_ID = "UCr5ik3Qjslqnl6DB8XwJxDg"
STREAM_KEY = "77cs-jw6x-yfeu-m2ks-82d6"

last_subs = 0

start_stream(STREAM_KEY)

while True:
    subs = get_subscribers(CHANNEL_ID)

    if subs != last_subs:
        print(f"Subscribers: {subs}")
        update_title(subs)

        if subs > last_subs:
            print("New Subscriber!")

        last_subs = subs

    chats = get_live_chat()
    for c in chats:
        print("CHAT:", c)

    time.sleep(5)
