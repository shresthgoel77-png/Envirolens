import threading
from typing import Any
from ultralytics import YOLO
from core.config import settings
from core.logger import logger


class PollutionDetector:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """Thread-safe Singleton implementation."""
        if not cls._instance:
            with cls._lock:
                # Double-check lock
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize_model()
        return cls._instance

    def _initialize_model(self) -> None:
        """Loads the YOLO model weights into memory exactly once."""
        logger.info(f"Initializing YOLOv8 model from path: {settings.MODEL_PATH}")
        try:
            # Loads local weights (.pt file)
            self.model = YOLO(settings.MODEL_PATH)
            logger.info("YOLOv8 model loaded successfully.")
        except Exception as e:
            logger.critical(f"Failed to load YOLOv8 model: {str(e)}", exc_info=True)
            raise e

    def predict(self, frame: Any) -> Any:
        """Runs object detection/segmentation on a single video frame.
        
        Args:
            frame: A numpy array representing the image (BGR from OpenCV).
        """
        # verbose=False suppresses standard YOLO terminal prints, keeping our JSON logs clean
        results = self.model(frame, verbose=False)
        return results