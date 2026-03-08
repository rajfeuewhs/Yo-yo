import requests

API_KEY = ""AIzaSyB1kbXAnaSOc_Oxu6n7DJD-jwMABDqGMtk"

def get_subscribers(channel_id):

    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={API_KEY}"

    try:
        data = requests.get(url).json()
        return int(data["items"][0]["statistics"]["subscriberCount"])
    except:
        return 0
