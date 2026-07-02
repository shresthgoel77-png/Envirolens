from typing import Any
from ai.detector import PollutionDetector


class PollutionTracker:
    def __init__(self):
        # Share the singleton detector instance across memory
        self.detector = PollutionDetector()

    def track_frame(self, frame: Any) -> Any:
        """Processes a video frame to isolate and track targets across time.
        
        Using persist=True tells YOLO to maintain tracking IDs across frames using ByteTrack.
        """
        results = self.detector.model.track(
            frame, 
            persist=True, 
            tracker="bytetrack.yaml", 
            verbose=False
        )
        # Return the primary tracking payload for this frame
        return results[0] if results else None