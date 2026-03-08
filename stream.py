import subprocess

def start_stream(stream_key):

    command = [
        "ffmpeg",
        "-re",
        "-f", "lavfi",
        "-i", "color=c=purple:s=1280x720:r=30",
        "-f", "lavfi",
        "-i", "anullsrc",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        "-f", "flv",
        f"rtmp://x.rtmp.youtube.com/live2/{stream_key}"
    ]

    subprocess.Popen(command)
