import uuid
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from models.event import Event
from storage.disk import EvidenceManager
from core.logger import logger

# Instantiate a single manager to be reused
evidence_manager = EvidenceManager()

async def trigger_alert(
    db: AsyncSession,
    camera_id: uuid.UUID,
    event_type: str,
    severity: float,
    frame_array: Any
) -> Event:
    """
    Handles the full alert lifecycle: saving disk evidence and committing the DB record.
    """
    logger.info(f"Triggering alert for camera {camera_id} - Type: {event_type} [Severity: {severity}]")
    
    # 1. Save the physical evidence to disk
    try:
        image_path = evidence_manager.save_frame(frame_array, camera_id)
    except Exception as e:
        logger.error("Aborting alert creation due to evidence saving failure.")
        raise e

    # 2. Create the database record
    new_event = Event(
        camera_id=camera_id,
        event_type=event_type,
        severity=severity,
        image_path=image_path
    )
    
    db.add(new_event)
    
    # 3. Commit the transaction
    try:
        await db.commit()
        await db.refresh(new_event)
        logger.info(f"Alert event {new_event.id} successfully recorded in database.")
        return new_event
    except Exception as e:
        await db.rollback()
        logger.error(f"Database error while saving event: {str(e)}", exc_info=True)
        raise e