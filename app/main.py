from fastapi import FastAPI, HTTPException
from app.models import PlayRequest, StatusResponse
from app.controller import PlaybackController

app = FastAPI(title="Winnow Video Playback Service")

controller = PlaybackController()


@app.get("/")
def root():
    return {"message": "Winnow Video Playback Service is running"}


@app.post("/play")
def play_video(request: PlayRequest):
    try:
        controller.play(request.video)
        return {"message": f"Playing video: {request.video}"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stop")
def stop_video():
    controller.stop()
    return {"message": "Playback stopped"}


@app.get("/status", response_model=StatusResponse)
def get_status():
    return controller.get_status()