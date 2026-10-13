
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

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
    
    