
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class UserSession(Base):
    
    __tablename__ = "user_sessions"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default= uuid.uuid4
    )
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )
    
    hashed_refresh_token:Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    
    expires_at: Mapped[datetime] = mapped_column(
        
        DateTime(timezone=True),
        nullable=False
    )
    
    revoke: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    
    created_at: Mapped[datetime] = mapped_column(
        
        DateTime(timezone=True),
        default= lambda: datetime.now(timezone.utc),
        nullable=False
    )