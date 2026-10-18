
from fastapi import APIRouter, Response, Depends

from configs.logger import get_logger
from database.session import get_db
from dependencies.auth import get_current_user
from schema.gmail_schema import GmailRequest
from sqlalchemy.orm import Session


logger = get_logger("gmail-router")

gmail_router = APIRouter(
    prefix="/gmail",
    tags=["gmail"]
)


@gmail_router.post("/send")
def send_mail(request: GmailRequest, 
              response:Response,
              db:Session = Depends(get_db),
              current_user = Depends(get_current_user))

