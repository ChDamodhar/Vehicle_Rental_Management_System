import os
from functools import lru_cache
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

@lru_cache()
def get_supabase():
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
    if not SUPABASE_URL.startswith("https://"):
        raise RuntimeError("SUPABASE_URL seems invalid")
    return create_client(SUPABASE_URL, SUPABASE_KEY)
