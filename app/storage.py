from supabase import create_client, Client
from fastapi.encoders import jsonable_encoder

SUPABASE_URL="https://gzoxocgqsfhpwonwjdzs.supabase.co"
SUPABASE_KEY="sb_publishable_-oYThbnput0ioruD1Be5lg_XnGT8z43"
        
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_data():
  results = supabase.table('issues').select('*').execute()
  if results.data is not None:
    content = results.data
    return content

def save_data(issue):
  data = jsonable_encoder(issue)
  supabase.table('issues').insert(data).execute()

def update_data(data):
  id = data.get("id")
  supabase.table('issues').update(data).eq('id', id).execute()

def delete_data(id):
  return supabase.table("issues").delete().eq("id", id).execute()