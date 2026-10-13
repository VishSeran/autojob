
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Resume(Base):
    
    __tablename__ = "resumes"
    
    id: Mapped [uuid.UUID] = mapped_column (
        
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    user_id: Mapped [uuid.UUID] = mapped_column (
        
        UUID( as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    
    storage_path: Mapped[str] = mapped_column (
        
        String(255),
        nullable=False
    )
    
    content_type: Mapped[str] = mapped_column (
        
        String(255),
        nullable=True,
        default="application/pdf"
        
    ) 
    
    is_default: Mapped[bool] = mapped_column (
        
        Boolean,
        nullable=False,
        default=False
    )
    
    create_at: Mapped[datetime] = mapped_column (
        
        DateTime(timezone=True),
        nullable=False,
        default= lambda: datetime.now(timezone.utc)
    )