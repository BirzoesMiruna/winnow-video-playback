from pathlib import Path
import subprocess


class PlaybackController:
    def __init__(self, video_dir: str = "videos"):
        self.video_dir = Path(video_dir)
        self.state = "idle"
        self.current_video = None
        self.process = None
        self.vlc_path = Path(r"C:\Program Files\VideoLAN\VLC\vlc.exe")

    def play(self, video_name: str):
        if self.process and self.process.poll() is None:
            raise RuntimeError("A video is already playing.")

        video_path = self.video_dir / video_name

        if not video_path.exists():
            raise FileNotFoundError(f"Video '{video_name}' not found.")

        if not self.vlc_path.exists():
            raise FileNotFoundError(f"VLC not found at: {self.vlc_path}")

        try:
            self.process = subprocess.Popen(
                [str(self.vlc_path), "--fullscreen", str(video_path.resolve())]
            )
            self.state = "playing"
            self.current_video = video_name
        except Exception as e:
            self.state = "error"
            raise RuntimeError(f"Failed to start playback: {e}")

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()

        self.process = None
        self.state = "idle"
        self.current_video = None

    def get_status(self):
        if self.process and self.process.poll() is not None:
            self.process = None
            self.state = "idle"
            self.current_video = None

        return {
            "state": self.state,
            "current_video": self.current_video
        }