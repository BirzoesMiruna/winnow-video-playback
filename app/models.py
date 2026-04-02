from pydantic import BaseModel


class PlayRequest(BaseModel):
    video: str


class StatusResponse(BaseModel):
    state: str
    current_video: str | None = None