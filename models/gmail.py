
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class GmailModel(Base):
    
    __tablename__ = "gmail_history"
    
    id: Mapped[uuid.UUID] = mapped_column(
        
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default= uuid.uuid4
    )
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        
        UUID(as_uuid=True),
        ForeignKey (
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )
    
    resend_email_id: Mapped[str | None] = mapped_column (
        String(255),
        nullable=True,
    )
    
    reply_email: Mapped[str] = mapped_column (
        String(255),
        nullable=True,
    )
    
    company_mail: Mapped[str] = mapped_column (
        
        String(255),
        nullable=False
    )
    
    subject: Mapped [str] = mapped_column (
        
        String(255),
        nullable=False
        
    )
    
    email_body: Mapped [str] = mapped_column (
        
        String(255),
        nullable=False
    )
    
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="pending",
    )
    
    create_at: Mapped[datetime] = mapped_column(
        
        DateTime(timezone=True),
        nullable=False,
        default= lambda: datetime.now(timezone.utc)
    )
    
    
    
    