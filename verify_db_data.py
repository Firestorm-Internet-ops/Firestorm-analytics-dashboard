import requests
from config import SUPABASE_URL, SUPABASE_KEY

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
}

# Get all data with high limit
response = requests.get(
    f"{SUPABASE_URL}/rest/v1/master_sheet?select=date",
    headers={**headers, 'Range': '0-50000'}
)

if response.status_code == 200:
    data = response.json()
    dates = sorted(set(row['date'] for row in data))
    
    print(f"Total rows fetched: {len(data)}")
    print(f"Unique dates: {len(dates)}")
    print(f"Date range: {dates[0]} to {dates[-1]}")
    print(f"\nAll dates:")
    for date in dates:
        count = sum(1 for row in data if row['date'] == date)
        print(f"  {date}: {count} rows")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
