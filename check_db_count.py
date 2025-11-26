import requests
from config import SUPABASE_URL, SUPABASE_KEY

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Prefer': 'count=exact'
}

# Get count
response = requests.get(
    f"{SUPABASE_URL}/rest/v1/master_sheet?select=date",
    headers=headers
)

if response.status_code == 200:
    count = response.headers.get('Content-Range', '').split('/')[-1]
    print(f"Total rows in database: {count}")
    
    # Get unique dates
    data = response.json()
    if data:
        dates = sorted(set(row['date'] for row in data))
        print(f"Unique dates: {len(dates)}")
        print(f"Date range: {dates[0]} to {dates[-1]}")
        print(f"\nFirst 10 dates: {dates[:10]}")
        print(f"Last 10 dates: {dates[-10:]}")
else:
    print(f"Error: {response.status_code} - {response.text}")
