
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class GoogleConnection(Base):
    
    __tablename__ = "google_connection"
    
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            name="uq_google_connection_user"
        ),
    )
    
    id: Mapped[uuid.UUID] = mapped_column(
        
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
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
    
    
    google_email: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    access_token_encrpt: Mapped[str | None] = mapped_column(
        
        Text,
        nullable=True
    )
    
    refresh_token_encrpt: Mapped[str | None] = mapped_column(
        
        Text,
        nullable=True
    )
    
    token_expiry: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    
    scope: Mapped[str | None] = mapped_column(
        
        Text,
        nullable=True
    )
    
    create_at:Mapped[datetime] = mapped_column(
        
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    updated_at:Mapped[datetime] = mapped_column(
        
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    