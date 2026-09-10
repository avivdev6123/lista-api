import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.folder import Folder
from app.schemas.folder import FolderCreate, FolderOut, FolderUpdate

router = APIRouter()


@router.get("", response_model=list[FolderOut])
def list_folders(db: Session = Depends(get_db)):
    """Powers the Home screen's rotating bubble carousel."""
    folders = db.query(Folder).all()
    return [
        FolderOut.model_validate(f, from_attributes=True).model_copy(
            update={"item_count": len(f.items)}
        )
        for f in folders
    ]


@router.post("", response_model=FolderOut, status_code=201)
def create_folder(payload: FolderCreate, db: Session = Depends(get_db)):
    """Powers the '+' new-folder-bubble flow."""
    folder = Folder(
        name=payload.name, cover_image_url=payload.cover_image_url, owner_id=uuid.uuid4()
    )
    db.add(folder)
    db.commit()
    db.refresh(folder)
    return folder


@router.patch("/{folder_id}", response_model=FolderOut)
def update_folder(folder_id: uuid.UUID, payload: FolderUpdate, db: Session = Depends(get_db)):
    """Powers inline rename + cover image edit from the '...' menu."""
    folder = db.get(Folder, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    if payload.name is not None:
        folder.name = payload.name
    if payload.cover_image_url is not None:
        folder.cover_image_url = payload.cover_image_url
    db.commit()
    db.refresh(folder)
    return folder


@router.delete("/{folder_id}", status_code=204)
def delete_folder(folder_id: uuid.UUID, db: Session = Depends(get_db)):
    folder = db.get(Folder, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    db.delete(folder)
    db.commit()
