import subprocess

def start_stream(stream_key):

    command = [
        "ffmpeg",
        "-re",
        "-loop", "1",
        "-i", "bg.png",
        "-f", "lavfi",
        "-i", "anullsrc",
        "-vcodec", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-f", "flv",
        f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"
    ]

    subprocess.Popen(command)
