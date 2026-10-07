from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from configs.logger import get_logger
from configs.settings import settings


logger = get_logger("db session")

engine = create_engine(
    url=settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

db_session = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

#Generator[YieldType, SendType, ReturnType]
def get_db() -> Generator[Session, None, None]:
    
    db = db_session()
    logger.info("Database session is created")
    
    try:
        logger.info("Database session yielded to request")
        yield db

    finally:
        logger.info("Closing database session")
        db.close()
        logger.info("Database session closed")

