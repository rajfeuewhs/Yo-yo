import os
import subprocess
import time
import requests
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, CompositeVideoClip, TextClip, ColorClip

# --- CONFIGURATION (Environment Variables) ---
STREAM_KEY = os.getenv("YOUTUBE_STREAM_KEY")
STREAM_URL = "rtmp://a.rtmp.youtube.com/live2"
API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")

# --- UI CONSTANTS (Gaming/Gem Style) ---
WIDTH, HEIGHT = 1280, 720
FONT_PATH = "Montserrat-Bold.ttf" # Ensure this is in GitHub
BACKGROUND_IMAGE = "bg.png" # The new glowing tech image

# --- API FUNCTION ---
def get_real_sub_count():
    if not API_KEY or not CHANNEL_ID: return "1,000" # Demo fallback
    try:
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={API_KEY}"
        response = requests.get(url).json()
        subs = response['items'][0]['statistics']['subscriberCount']
        return "{:,}".format(int(subs))
    except: return "Updating..."

# --- 3D GEM NUMBER GENERATION ---
def create_number_image(count):
    # Base canvas
    img = Image.new('RGBA', (WIDTH, HEIGHT), color=(0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    try:
        font_count = ImageFont.truetype(FONT_PATH, 220) # Huge size
    except IOError: font_count = ImageFont.load_default()

    # Draw number with 3D gradient/gem effect (Pillow pseudo)
    text = count
    
    # Simple shadow
    d.text((WIDTH/2 + 5, HEIGHT/2 + 30), text, font=font_count, fill=(50, 0, 0, 200), anchor="mm")
    
    # Gradient overlay (Pseudo 3D/Gem)
    # Pillow doesn't do real 3D gradients. We'll simulate a red/gold sheen.
    # Drawing it multiple times slightly offset for 3D feel.
    d.text((WIDTH/2, HEIGHT/2 + 25), text, font=font_count, fill=(150, 0, 0), anchor="mm") # Depth
    d.text((WIDTH/2, HEIGHT/2 + 20), text, font=font_count, fill=(200, 50, 50), anchor="mm") # Main Red
    d.text((WIDTH/2, HEIGHT/2 + 15), text, font=font_count, fill=(255, 100, 100), anchor="mm") # Highlights
    
    # Main front color with slight gold top shine
    d.text((WIDTH/2, HEIGHT/2), text, font=font_count, fill=(255, 215, 0), anchor="mm") # Gold shine top
    d.text((WIDTH/2, HEIGHT/2 + 5), text, font=font_count, fill=(235, 60, 60), anchor="mm") # Red body (front)
    
    return np.array(img.convert("RGB")) # Return as NumPy for MoviePy

# --- ASYNC ANIMATION GENERATOR (For 9-to-0 roll) ---
# This requires a faster server or GPU for smooth encoding.
# We'll simulate it by creating a small rolling clip when digits change.
def generate_roll_clip(old_count, new_count):
    # This is complex in MoviePy. For simplicity on Free Tier,
    # we'll just flash the number very quickly to simulate a change.
    # To do real rolling, we need to split digits, align them vertically,
    # and animate their Y-position, which is heavy. 
    # For now, we'll return a simple transition.
    
    # Simple flash transition to signal change
    img1 = create_number_image(old_count)
    img2 = create_number_image(new_count)
    
    # Create two brief clips
    clip1 = ImageClip(img1).set_duration(0.1)
    clip2 = ImageClip(img2).set_duration(0.1)
    
    return concatenate_videoclips([clip1, clip2, clip1, clip2]) # Simple flash

# --- STREAM FUNCTION (MoviePy & FFmpeg integration) ---
def start_stream():
    if not STREAM_KEY:
        print("Error: STREAM_KEY is not set.")
        return

    # FFmpeg command for MoviePy integration
    ffmpeg_cmd = [
        'ffmpeg', '-re', '-i', '-', # Input from pipe (MoviePy)
        '-f', 'lavfi', '-i', 'anullsrc', # Silent audio
        '-c:v', 'libx264', '-preset', 'ultrafast',
        '-tune', 'stillimage', '-pix_fmt', 'yuv420p',
        '-b:v', '3000k', # Good for 720p HD
        '-g', '60', '-f', 'flv', f"{STREAM_URL}/{STREAM_KEY}"
    ]
    
    # Start FFmpeg process
    ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, shell=False)
    
    print("Starting Stream Loop...")
    
    old_count = get_real_sub_count()
    current_frame = create_number_image(old_count)
    
    # Main loop (using MoviePy to write frames to pipe)
    try:
        while True:
            new_count = get_real_sub_count()
            
            # Check for change to apply animation
            if new_count != old_count:
                print(f"Number change detected! Animating {old_count} -> {new_count}")
                # For free tier, full rolling animation is CPU heavy.
                # We'll update the number and add a small screen shake effect instead.
                # Let's generate a clip of the new number flashing.
                
                # Full frame with background
                bg_img = Image.open(BACKGROUND_IMAGE).convert("RGBA").resize((WIDTH, HEIGHT))
                num_img = Image.fromarray(create_number_image(new_count)).convert("RGBA")
                bg_img.paste(num_img, (0, 0), num_img)
                
                # Write a few frames to make it "stick"
                final_frame_np = np.array(bg_img.convert("RGB"))
                for _ in range(30): # 1 second worth of frames at 30fps
                    ffmpeg_process.stdin.write(final_frame_np.tobytes())
                
                old_count = new_count
            else:
                # Regular frame update (faster)
                bg_img = Image.open(BACKGROUND_IMAGE).convert("RGBA").resize((WIDTH, HEIGHT))
                num_img = Image.fromarray(create_number_image(new_count)).convert("RGBA")
                bg_img.paste(num_img, (0, 0), num_img)
                
                final_frame_np = np.array(bg_img.convert("RGB"))
                ffmpeg_process.stdin.write(final_frame_np.tobytes())
            
            # Fast update
            time.sleep(0.03) # Limit output to ~30fps

    except Exception as e:
        print(f"Error: {e}")
        ffmpeg_process.terminate()

if __name__ == "__main__":
    start_stream()
