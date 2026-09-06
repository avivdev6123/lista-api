import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

# Many-to-many: an item can live in several folders at once
# (this is what powers the "Choose Listaa" multi-select share sheet)
item_folder_association = Table(
    "item_folder_association",
    Base.metadata,
    Column("item_id", UUID(as_uuid=True), ForeignKey("items.id"), primary_key=True),
    Column("folder_id", UUID(as_uuid=True), ForeignKey("folders.id"), primary_key=True),
)


class Folder(Base):
    __tablename__ = "folders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    cover_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    items: Mapped[list["Item"]] = relationship(
        secondary=item_folder_association, back_populates="folders"
    )


class Item(Base):
    __tablename__ = "items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    folders: Mapped[list["Folder"]] = relationship(
        secondary=item_folder_association, back_populates="items"
    )
