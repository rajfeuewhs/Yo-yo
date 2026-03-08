import pytchat

video_id = "YOUR_LIVE_VIDEO_ID"

chat = pytchat.create(video_id=video_id)

def get_live_chat():
    messages = []

    if chat.is_alive():
        for c in chat.get().sync_items():
            messages.append(f"{c.author.name}: {c.message}")

    return messages
