import requests
from config import SUPABASE_URL, SUPABASE_KEY

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
}

# Fetch data in pages to get all sources
all_sources = set()
page = 0
page_size = 1000

while True:
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/master_sheet?select=source&limit={page_size}&offset={page * page_size}",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        if not data:
            break
        
        for row in data:
            all_sources.add(row['source'])
        
        print(f"Page {page + 1}: fetched {len(data)} rows, sources so far: {all_sources}")
        
        if len(data) < page_size:
            break
        
        page += 1
    else:
        print(f"Error: {response.status_code}")
        break

print(f"\n{'='*60}")
print(f"FINAL RESULT:")
print(f"Unique sources in database: {all_sources}")
print(f"Total pages fetched: {page + 1}")
print(f"{'='*60}")
