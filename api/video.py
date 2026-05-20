import vlc

player = vlc.MediaPlayer()


def play_video(file):

    media = vlc.Media(
        f"media/video/{file}"
    )

    player.set_media(media)

    player.play()