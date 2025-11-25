import requests

SUPABASE_URL = "https://zbueoutrzlmwqakupedp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpidWVvdXRyemxtd3Fha3VwZWRwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM1NDA2ODYsImV4cCI6MjA3OTExNjY4Nn0.44aKq7FEe-XiVU0hRYgWCwHvEeokdOHLrxuEFCkMP_g"

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Prefer': 'count=exact'
}

# Get total count
response = requests.head(
    f"{SUPABASE_URL}/rest/v1/master_sheet",
    headers=headers
)

if response.status_code in [200, 206]:
    count = response.headers.get('Content-Range', '').split('/')[-1]
    print(f"✓ Total rows in database: {count}")
    
    if int(count) == 10548:
        print("✓ Database has correct number of rows!")
        print("\nNow refresh your browser (Ctrl+Shift+R)")
        print("You should see all 3 sources: GYG, Tiqets, Viator")
    else:
        print(f"⚠️  Expected 10548 rows but found {count}")
        print("Delete all and run: python3 upload_clean.py")
