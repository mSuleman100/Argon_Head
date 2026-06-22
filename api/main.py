from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from api.audio import play_audio
from api.video import play_video
from api.display import show_image, show_message

app = FastAPI()


class AudioRequest(BaseModel):
    file: str


class VideoRequest(BaseModel):
    file: str


class MessageRequest(BaseModel):
    text: str
    duration: int = 3


class ImageRequest(BaseModel):
    file: str
    duration: int = 0


@app.get("/")
def root():
    return {"robot": "online"}


@app.post("/play_audio")
def audio(req: AudioRequest):
    play_audio(req.file)
    return {"status": "playing", "file": req.file}


@app.post("/play_video")
def video(req: VideoRequest):
    play_video(req.file)
    return {"status": "playing", "file": req.file}


@app.post("/show_message")
def message(req: MessageRequest):
    show_message(req.text, duration=req.duration)
    return {"status": "shown", "message": req.text, "duration": req.duration}


@app.post("/show_image")
def image(req: ImageRequest):
    try:
        show_image(req.file, duration=req.duration)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"status": "shown", "file": req.file, "duration": req.duration}