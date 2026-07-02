import cv2
import time
import threading
import uuid
from ai.detector import PollutionDetector
from core.logger import logger
from ai.pipeline import ProcessingPipeline

class VideoIngestor:
    def __init__(self, camera_id: uuid.UUID, stream_url: str):
        self.camera_id = camera_id
        self.stream_url = stream_url
        
        # Thread controller flags
        self.is_running = False
        self._thread: threading.Thread | None = None
        
        # Access the singleton detector instance
        self.pipeline = ProcessingPipeline(camera_id=self.camera_id)

    def start(self) -> None:
        """Launches the stream reader in a background thread."""
        if self.is_running:
            logger.warning(f"Ingestor for camera {self.camera_id} is already running.")
            return

        self.is_running = True
        self._thread = threading.Thread(
            target=self._read_stream, 
            name=f"CamReader-{self.camera_id}", 
            daemon=True
        )
        self._thread.start()
        logger.info(f"Started ingestion thread for camera: {self.camera_id}")

    def stop(self) -> None:
        """Signals the background thread to safely spin down."""
        logger.info(f"Stopping ingestion thread for camera: {self.camera_id}")
        self.is_running = False
        if self._thread:
            self._thread.join(timeout=5)

    def _read_stream(self) -> None:
        """Internal loop executing inside the background thread."""
        while self.is_running:
            logger.info(f"Connecting to RTSP stream: {self.stream_url}")
            cap = cv2.VideoCapture(self.stream_url)
            
            # Reduce buffer size to minimize lag on live RTSP streams
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            if not cap.isOpened():
                logger.error(f"Failed to open RTSP stream for camera {self.camera_id}. Retrying in 10s...")
                cap.release()
                time.sleep(10)
                continue

            last_sampled_time = 0.0
            sample_interval = 1.0  # Force exactly 1 FPS sampling

            while self.is_running:
                current_time = time.time()
                
                # Grab frames continuously to keep the CV2 buffer fresh
                ret = cap.grab()
                if not ret:
                    logger.error(f"Lost stream connection for camera {self.camera_id}. Attempting reconnect...")
                    break

                # Check if 1 second has elapsed before decoding and processing
                if current_time - last_sampled_time >= sample_interval:
                    last_sampled_time = current_time
                    
                    # Retrieve and decode the frame matrix
                    ret_retrieve, frame = cap.retrieve()
                    if not ret_retrieve:
                        continue
                    
                    try:
                        # Forward frame to our Singleton AI Model
                        alerts = self.pipeline.process_frame(frame)
                        
                        # Trace processing metrics (Ready for metadata extraction in downstream modules)
                        logger.debug(f"Frame processed for camera {self.camera_id} at 1 FPS.")
                        
                    except Exception as e:
                        logger.error(f"Error during AI pipeline execution for camera {self.camera_id}: {str(e)}")

            cap.release()
            if self.is_running:
                time.sleep(5)  # Cooldown before attempting reconnection loop

        logger.info(f"Background thread safely stopped for camera: {self.camera_id}")