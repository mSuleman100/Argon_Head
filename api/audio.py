import os
import pygame


def _ensure_audio_initialized():
    if not pygame.mixer.get_init():
        pygame.mixer.init()


def play_audio(file):
    _ensure_audio_initialized()
    path = f"media/audio/{file}"
    if not os.path.exists(path):
        raise FileNotFoundError(f"Audio file not found: {path}")
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
