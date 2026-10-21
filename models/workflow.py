

import uuid
from datetime import datetime, timezone

from sqlalchemy import UUID, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class WorkflowData(Base):
    
    __tablename__ = "workflow_data"
    
    id:Mapped[uuid.UUID] = mapped_column(
        
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    ) 
    
    thread_id: Mapped[uuid.UUID] = mapped_column(
        
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
        default=uuid.uuid4
    )
    
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )
    
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default= lambda: datetime.now(timezone.utc)
    )
    
    