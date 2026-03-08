import os
import subprocess
import time
import requests
from PIL import Image, ImageDraw, ImageFont

# --- SETTINGS (Render Dashboard mein Environment Variables mein dalein) ---
STREAM_KEY = os.getenv("YOUTUBE_STREAM_KEY")
STREAM_URL = "rtmp://a.rtmp.youtube.com/live2"
API_KEY = os.getenv("YOUTUBE_API_KEY") # Google Cloud Console se milega
CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID") # Aapke channel ki ID

def get_real_sub_count():
    if not API_KEY or not CHANNEL_ID:
        return "Setup API"
    
    try:
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={API_KEY}"
        response = requests.get(url).json()
        subs = response['items'][0]['statistics']['subscriberCount']
        return "{:,}".format(int(subs)) # Numbers mein comma lagane ke liye
    except Exception as e:
        print(f"API Error: {e}")
        return "Updating..."

def create_frame(count):
    # 480p resolution (Standard for Free Servers)
    width, height = 854, 480
    img = Image.new('RGB', (width, height), color=(10, 10, 10)) # Dark Grey
    d = ImageDraw.Draw(img)
    
    # Text design
    d.text((320, 150), "LIVE SUBSCRIBERS", fill=(200, 200, 200))
    d.text((350, 220), count, fill=(255, 0, 0)) # Red color for count
    d.text((310, 350), "Road to Next Milestone!", fill=(100, 100, 100))
    
    img.save("frame.jpg")

def start_stream():
    if not STREAM_KEY:
        print("Error: STREAM_KEY missing!")
        return

    # FFmpeg command optimized for low-end servers
    ffmpeg_cmd = [
        'ffmpeg', '-re', '-loop', '1', '-i', 'frame.jpg',
        '-f', 'lavfi', '-i', 'anullsrc', # Silent audio stream
        '-c:v', 'libx264', 
        '-preset', 'ultrafast', # CPU bachane ke liye sabse fast preset
        '-tune', 'stillimage', 
        '-pix_fmt', 'yuv420p',
        '-b:v', '1000k', # Low bitrate (Best for Free Tier)
        '-maxrate', '1000k',
        '-bufsize', '2000k',
        '-g', '60', # Keyframe interval
        '-f', 'flv', f"{STREAM_URL}/{STREAM_KEY}"
    ]

    create_frame("Loading...")
    process = subprocess.Popen(ffmpeg_cmd)

    try:
        while True:
            # Har 30 second mein update karein (API limit bachane ke liye)
            current_subs = get_real_sub_count()
            create_frame(current_subs)
            print(f"Current Subs: {current_subs}")
            time.sleep(30)
    except Exception as e:
        print(f"Stream Stopped: {e}")
        process.terminate()

if __name__ == "__main__":
    start_stream()
