from pydantic import BaseModel, ConfigDict, Field, HttpUrl
import uuid
from typing import Optional

class CameraBase(BaseModel):
    name: str = Field(..., max_length=100, description="Friendly name of the camera")
    stream_url: str = Field(..., description="RTSP or HTTP stream URL")
    location: str = Field(..., max_length=255, description="Physical location or intersection")

class CameraCreate(CameraBase):
    pass

class CameraResponse(CameraBase):
    id: uuid.UUID
    is_active: bool

    # Pydantic V2 configuration to read from SQLAlchemy ORM models
    model_config = ConfigDict(from_attributes=True)