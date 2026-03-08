import requests

API_KEY = "AIzaSyB1kbXAnaSOc_Oxu6n7DJD-jwMABDqGMtk"

def get_subscribers(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={API_KEY}"
    data = requests.get(url).json()

    try:
        return int(data["items"][0]["statistics"]["subscriberCount"])
    except:
        return 0


def update_title(subs):
    title = f"🔴 LIVE SUBSCRIBER COUNT - {subs}"
    print("Updating title:", title)
