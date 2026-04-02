# Design Description – Winnow Video Playback Service

## 1. Problem Statement

The Winnow Vision system needs repeatable test scenarios in order to validate computer vision models and system behavior. Instead of using physical objects, prerecorded videos can be displayed on a screen in front of the camera to simulate waste events.

Automated tests therefore need a way to programmatically control video playback on a local machine. The tool should allow tests to start a specific video scenario, stop playback, and check whether the system is currently idle or playing a video.

---

## 2. High-Level Solution

The proposed solution is a lightweight local HTTP service that controls a video player process. Automated tests send HTTP requests to this service to trigger playback of specific video files stored locally.

The system acts as a bridge between automated test scripts and a local video player.

High-level flow:

Automated Test → HTTP Request → Playback Service → VLC Player → Screen → Camera → Vision System

---

## 3. System Components

The system is divided into the following components:

### 3.1 API Layer (FastAPI)

Responsible for:
- Receiving HTTP requests from automated tests
- Validating input data
- Returning JSON responses
- Exposing endpoints:
  - POST /play
  - POST /stop
  - GET /status

FastAPI was chosen because it is lightweight, easy to implement, and automatically provides API documentation.

### 3.2 Playback Controller

Responsible for:
- Starting video playback
- Stopping video playback
- Tracking current system state
- Ensuring only one video plays at a time
- Handling errors (missing file, playback failure)

This component isolates playback logic from the API layer, making the code easier to maintain and extend.

### 3.3 VLC Media Player

VLC is used as the video playback engine because:
- It supports command-line control
- It can run in fullscreen
- It supports many video formats
- It is stable and widely available

The service starts VLC as a subprocess and controls it through the operating system.

### 3.4 Video Directory

All test scenario videos are stored in a local directory (`videos/`).  
Automated tests select which scenario to run by specifying the video filename.

---

## 4. API Design

The API is intentionally simple to make integration with automated tests easy.

### POST /play
Starts playback of a specified video file.

Possible responses:
- 200 – playback started
- 404 – video file not found
- 409 – a video is already playing
- 500 – playback failed

### POST /stop
Stops the current playback.

### GET /status
Returns the current system state:
- idle
- playing
- error

Automated tests can call `/status` to verify that the system is ready before starting the next scenario.

---

## 5. State Management

The system maintains a simple state machine:

- **idle** → no video playing
- **playing** → video currently playing
- **error** → playback failed

State transitions:

- idle → playing (when /play is called)
- playing → idle (when video finishes or /stop is called)
- any → error (if playback fails)

This allows automated tests to reliably determine when a scenario has started or finished.

---

## 6. Handling Edge Cases

### Case 1 – Play request while video is already playing
The system returns HTTP 409 Conflict and does not start another video.  
This prevents multiple videos from playing at the same time and keeps tests deterministic.

### Case 2 – Video file not found
The system returns HTTP 404 Not Found.

### Case 3 – VLC cannot be started
The system returns HTTP 500 Internal Server Error and switches state to "error".

### Case 4 – Video finishes naturally
The system checks whether the VLC process has exited and resets the state to "idle".

---

## 7. Assumptions

- Video files are stored locally
- VLC media player is installed on the same machine
- The service runs on the same machine as the video player
- Only one test scenario runs at a time
- Automated tests communicate with the service over HTTP
- The solution is a prototype and not production-ready

---

## 8. Limitations

- State is stored only in memory
- Only one video can play at a time
- VLC path is hardcoded
- No authentication or security
- No playback queue
- Limited error handling
- No logging system
- Designed for local use only

---

## 9. Future Improvements

If more time were available, the following improvements could be implemented:

- Configurable VLC path and video directory
- Logging and monitoring
- Automated API tests
- Playback queue support
- Health check endpoint
- Docker container for deployment
- Remote control over network
- Better playback lifecycle detection

---

## 10. Conclusion

This prototype demonstrates how automated tests can programmatically control video playback to simulate repeatable vision system scenarios. The design focuses on simplicity, clear API design, and reliable control of video playback, which are important for automated testing environments.