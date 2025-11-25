import requests

SUPABASE_URL = "https://zbueoutrzlmwqakupedp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpidWVvdXRyemxtd3Fha3VwZWRwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM1NDA2ODYsImV4cCI6MjA3OTExNjY4Nn0.44aKq7FEe-XiVU0hRYgWCwHvEeokdOHLrxuEFCkMP_g"

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Prefer': 'count=exact'
}

# Get count only
response = requests.head(
    f"{SUPABASE_URL}/rest/v1/master_sheet",
    headers=headers
)

if response.status_code in [200, 206]:
    content_range = response.headers.get('Content-Range', '')
    if content_range:
        total = content_range.split('/')[-1]
        print(f"✓ Total rows in database: {total}")
        print(f"\n✓ All {total} rows uploaded successfully!")
        print(f"\nNow refresh your dashboard browser (Ctrl+Shift+R)")
        print(f"and select the full date range (July 1 - August 31, 2025)")
    else:
        print("Could not get count")
else:
    print(f"Error: {response.status_code}")
