import os

from supabase import create_client, Client
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def load_data():
    results = supabase.table("issues").select("*").execute()
    if results.data is not None:
        content = results.data
        return content


def save_data(issue):
    data = jsonable_encoder(issue)
    supabase.table("issues").insert(data).execute()


def update_data(data):
    id = data.get("id")
    supabase.table("issues").update(data).eq("id", id).execute()


def delete_data(id):
    return supabase.table("issues").delete().eq("id", id).execute()
