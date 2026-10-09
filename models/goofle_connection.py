
import uuid


from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class GoogleConnection(Base):
    
    __tablename__ = "google_connection"
    
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            name="uq_google_connection_user"
        )
    )
    
    id: Mapped[uuid.UUID] = mapped_column(
        
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    user_id