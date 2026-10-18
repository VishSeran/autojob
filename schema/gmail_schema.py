
from pydantic import BaseModel


class GmailRequest(BaseModel):
    
    reply_email: str
    company_mail: str
    subject: str
    email_body: str
    
    