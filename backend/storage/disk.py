import cv2
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from core.logger import logger

class EvidenceManager:
    def __init__(self, storage_dir: str = "evidence"):
        # Resolve absolute path relative to the project root
        self.storage_dir = Path(__file__).parent.parent / storage_dir
        
        # Ensure the directory exists upon initialization
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_frame(self, frame_array: Any, camera_id: uuid.UUID) -> str:
        """
        Converts an OpenCV frame to JPEG and saves it to disk.
        Returns the relative file path to be stored in the database.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{camera_id}_{timestamp}.jpg"
        file_path = self.storage_dir / filename
        
        try:
            # OpenCV expects BGR arrays by default
            success = cv2.imwrite(str(file_path), frame_array)
            if not success:
                raise IOError(f"OpenCV failed to write image to {file_path}")
            
            logger.debug(f"Evidence saved successfully: {file_path}")
            # Return relative path for database storage (e.g., "evidence/cam_time.jpg")
            return f"evidence/{filename}"
            
        except Exception as e:
            logger.error(f"Failed to save evidence for camera {camera_id}: {str(e)}")
            raise