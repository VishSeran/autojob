

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class User(Base):
    
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(
        
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    email: Mapped[str] = mapped_column(
        
        String(length=255),
        unique=True,
        nullable=False,
        index=True
    )
    
    name: Mapped[str | None] = mapped_column(
        
        String(255),
        nullable=True
    )
    
    create_at: Mapped[datetime] = mapped_column(
        
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        
        DateTime(timezone=True),
        default= lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    
    