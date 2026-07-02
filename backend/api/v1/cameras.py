import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend.db.database import get_db
from backend.models.camera import Camera
from backend.schemas.camera import CameraCreate, CameraResponse
from backend.core.logger import logger

router = APIRouter(tags=["Cameras"])

@router.post("/", response_model=CameraResponse, status_code=status.HTTP_201_CREATED)
async def register_camera(camera_in: CameraCreate, db: AsyncSession = Depends(get_db)):
    """Register a new CCTV camera."""
    new_camera = Camera(**camera_in.model_dump())
    db.add(new_camera)
    
    try:
        await db.commit()
        await db.refresh(new_camera)
        logger.info(f"Registered new camera: {new_camera.id}")
        return new_camera
    except IntegrityError:
        await db.rollback()
        logger.warning(f"Failed to register camera. Stream URL {camera_in.stream_url} already exists.")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A camera with this stream URL already exists."
        )

@router.get("/", response_model=List[CameraResponse])
async def list_cameras(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    """Retrieve all registered cameras."""
    query = select(Camera).offset(skip).limit(limit)
    result = await db.execute(query)
    cameras = result.scalars().all()
    return cameras

@router.get("/{camera_id}", response_model=CameraResponse)
async def get_camera(camera_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve a single camera by its ID."""
    camera = await db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found.")
    return camera

@router.delete("/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_camera(camera_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Delete a camera from the system."""
    camera = await db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found.")
    
    await db.delete(camera)
    await db.commit()
    logger.info(f"Deleted camera: {camera_id}")
    return None