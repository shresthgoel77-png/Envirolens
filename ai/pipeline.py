import uuid
from typing import Any, Dict, List
from ai.tracker import PollutionTracker
from ai.severity import calculate_severity
from core.logger import logger


class ProcessingPipeline:
    def __init__(self, camera_id: uuid.UUID):
        self.camera_id = camera_id
        self.tracker = PollutionTracker()
        
        # State tracking: mapping tracking_id -> total consecutive frame visibility count
        self.persistence_registry: Dict[int, int] = {}

    def process_frame(self, frame: Any) -> List[Dict[str, Any]]:
        """Executes full tracking lifecycle assessment over a frame sample."""
        validated_alerts = []
        
        # 1. Pipeline Execution Step: Object Detection & Tracking Correlation
        tracked_frame_data = self.tracker.track_frame(frame)
        
        if tracked_frame_data is None or tracked_frame_data.boxes is None:
            return validated_alerts

        # Cache geometry metrics to calculate pixel coverage density scales
        frame_h, frame_w = frame.shape[:2]
        frame_area = frame_h * frame_w
        
        # Keep track of IDs seen in *this specific frame*
        active_ids_in_frame = set()

        # 2. Iterate and evaluate all tracking boxes found in the frame
        for box in tracked_frame_data.boxes:
            # If tracking drops or cannot safely identify an object ID yet, skip
            if box.id is None:
                continue
                
            track_id = int(box.id[0].item())
            active_ids_in_frame.add(track_id)
            
            # Update history frequency registry
            self.persistence_registry[track_id] = self.persistence_registry.get(track_id, 0) + 1
            consecutive_frames = self.persistence_registry[track_id]
            
            # Requirement: Confirm anomaly persistence over 5 consecutive cycles (seconds)
            if consecutive_frames >= 5:
                class_idx = int(box.cls[0].item())
                class_name = tracked_frame_data.names[class_idx]
                confidence = float(box.conf[0].item())
                
                # Derive bounding box area from spatial coordinates (x1, y1, x2, y2)
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                bbox_area = (x2 - x1) * (y2 - y1)
                
                # 3. Pipeline Execution Step: Risk Metric Calculations
                severity_score = calculate_severity(
                    class_name=class_name,
                    confidence=confidence,
                    bbox_area=bbox_area,
                    frame_area=frame_area
                )
                
                validated_alerts.append({
                    "camera_id": str(self.camera_id),
                    "track_id": track_id,
                    "class_name": class_name,
                    "confidence": round(confidence, 2),
                    "severity_score": severity_score,
                    "bbox": [round(coord, 1) for coord in [x1, y1, x2, y2]]
                })
                
                logger.warning(
                    f"CRITICAL POLLUTION ALERT -> Cam: {self.camera_id} | "
                    f"Track ID: {track_id} | Type: {class_name} | Severity: {severity_score}"
                )

        # Clean up stale tracks: if an ID is missing from this frame, drop its persistence history
        stale_ids = set(self.persistence_registry.keys()) - active_ids_in_frame
        for stale_id in stale_ids:
            del self.persistence_registry[stale_id]

        return validated_alerts