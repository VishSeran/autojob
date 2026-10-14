
from supabase import Client, create_client

from configs.settings import settings


client:Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SECRET_KEY
)