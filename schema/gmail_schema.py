
from pydantic import BaseModel


class GmailRequest(BaseModel):
    
    company_mail: str
    subject: str
    email_body: str
    
    