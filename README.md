
# Winnow Video Playback Service

## Overview

This project is a small proof-of-concept service built for the Winnow Software Test Engineer Internship take-home exercise.

The goal of this tool is to allow automated tests to trigger playback of prerecorded scenario videos on a local machine. These videos can be displayed on a screen placed in front of a camera-based vision system so that test scenarios can be replayed in a repeatable and automated way.

This service exposes a simple HTTP API that allows automated tests to start, stop, and check the status of video playback.

---

## Features

- Play a local video by name
- Stop the current playback
- Check the current playback status
- Simple HTTP API for automated test integration
- Designed as a minimal proof-of-concept for automated vision testing

---

## Tech Stack

- Python
- FastAPI
- Uvicorn
- VLC Media Player
- Subprocess (to control VLC)

---

## Project Structure

```text
winnow-video-playback/
├── app/
│   ├── main.py
│   ├── controller.py
│   └── models.py
├── videos/
│   └── test.mp4
├── requirements.txt
├── README.md
└── DESIGN.md
```

---

## API Endpoints

### POST /play

Starts playback of a local video.

Request body:
```json
{
  "video": "test.mp4"
}
```

Success response:
```json
{
  "message": "Playing video: test.mp4"
}
```

Error cases:
- 404 if video file is not found
- 409 if a video is already playing
- 500 if playback fails

---

### POST /stop

Stops the current playback.

Response:
```json
{
  "message": "Playback stopped"
}
```

---

### GET /status

Returns the current playback state.

Example response:
```json
{
  "state": "playing",
  "current_video": "test.mp4"
}
```

Possible states:
- idle
- playing
- error

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd winnow-video-playback
```

### 2. Create virtual environment
```bash
python -m venv .venv
```

### 3. Activate virtual environment (Windows)
```bash
.venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Install VLC Media Player

Download and install VLC from:
https://www.videolan.org/vlc/

Make sure VLC is installed at:
C:\Program Files\VideoLAN\VLC\vlc.exe

### 6. Add a test video

Place a video file in the videos/ folder, for example:
videos/test.mp4

---

## Running the Service

Start the API server:
```bash
uvicorn app.main:app --reload
```

The service will be available at:
http://127.0.0.1:8000

Interactive API documentation (Swagger UI):
http://127.0.0.1:8000/docs

---

## Example Usage (from automated tests)

### Check status
```bash
curl http://127.0.0.1:8000/status
```

### Start playback
```bash
curl -X POST http://127.0.0.1:8000/play ^
  -H "Content-Type: application/json" ^
  -d "{\"video\":\"test.mp4\"}"
```

### Stop playback
```bash
curl -X POST http://127.0.0.1:8000/stop
```

---

## Assumptions

- Video files are stored locally in the videos/ directory
- VLC Media Player is installed on the same machine
- The service runs on the same machine that controls video playback
- Only one video needs to be played at a time
- Automated tests communicate with the service via HTTP
- The solution is a prototype and not a production-ready system

---

## Limitations

- Playback state is stored only in memory (no persistence)
- Only one playback session is supported at a time
- VLC executable path is currently hardcoded for Windows
- The /stop endpoint terminates the VLC process but does not handle all edge cases
- There is no queueing or scheduling of playback requests
- Error handling and logging are minimal
- No authentication or security is implemented
- The solution is designed for local use only

---

## Future Improvements

If I had more time, I would improve the solution by:

- Making the VLC path configurable via environment variables
- Adding automated unit and integration tests
- Improving playback completion detection
- Adding structured logging
- Supporting a playback queue or scheduled playback
- Allowing configuration of the video directory
- Adding better error handling and health checks
- Packaging the service with Docker for easier deployment

---

## Design Summary

The solution is implemented as a lightweight FastAPI service that acts as a local video playback controller. Automated tests can send HTTP requests to start or stop playback of predefined scenario videos.

The system is structured into three main components:

- API Layer (FastAPI) – exposes HTTP endpoints (/play, /stop, /status)
- Playback Controller – manages the playback state and controls the VLC process
- Video Player (VLC) – plays the selected video file in fullscreen mode

The controller ensures that only one video can play at a time and keeps track of the current system state (idle, playing, error). This allows automated tests to check whether the system is ready before triggering the next test scenario.

I intentionally kept the prototype API-only, because the main integration point is automated tests rather than human users. A frontend could be added later for manual debugging or demo purposes.

The design focuses on simplicity, clarity, and reliability, which are important for automated testing environments.
