"""
Configuration file for Supabase credentials
Loads from environment variables
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SUPABASE_URL = os.getenv('VITE_SUPABASE_URL')
SUPABASE_KEY = os.getenv('VITE_SUPABASE_PUBLISHABLE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Missing Supabase credentials. Please set VITE_SUPABASE_URL and "
        "VITE_SUPABASE_PUBLISHABLE_KEY in your .env file"
    )
