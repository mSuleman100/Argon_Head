import vlc


def play_video(file):
    try:
        player = vlc.MediaPlayer()
    except Exception as exc:
        raise RuntimeError(
            "VLC is not available in this environment. Install libvlc or ensure VLC is configured correctly."
        ) from exc

    media = vlc.Media(f"media/video/{file}")
    player.set_media(media)
    player.play()
