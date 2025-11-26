import requests
from config import SUPABASE_URL, SUPABASE_KEY

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Prefer': 'count=exact'
}

# Get count
response = requests.head(
    f"{SUPABASE_URL}/rest/v1/master_sheet",
    headers=headers
)

if response.status_code in [200, 206]:
    count = response.headers.get('Content-Range', '').split('/')[-1]
    print(f"Total rows in database: {count}")
    
    # Get unique sources
    response2 = requests.get(
        f"{SUPABASE_URL}/rest/v1/master_sheet?select=source",
        headers={'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'}
    )
    
    if response2.status_code == 200:
        data = response2.json()
        sources = set(row['source'] for row in data)
        print(f"Sources in database: {sources}")
else:
    print(f"Error: {response.status_code}")
