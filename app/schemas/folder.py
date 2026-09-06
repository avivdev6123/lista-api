import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FolderCreate(BaseModel):
    name: str
    cover_image_url: str | None = None


class FolderUpdate(BaseModel):
    name: str | None = None
    cover_image_url: str | None = None


class FolderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    cover_image_url: str | None
    item_count: int = 0
    created_at: datetime
    updated_at: datetime
