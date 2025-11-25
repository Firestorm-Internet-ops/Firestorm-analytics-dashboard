import pandas as pd
import requests

print("="*60)
print("CSV vs DATABASE - SOURCE COMPARISON")
print("="*60)

# Check CSV
df = pd.read_csv('etl/processed/processed_data.csv')
csv_sources = df['Source'].value_counts()
print("\nCSV Sources:")
for source, count in csv_sources.items():
    print(f"  {source}: {count} rows")
print(f"Total CSV rows: {len(df)}")

# Check Database
SUPABASE_URL = "https://zbueoutrzlmwqakupedp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpidWVvdXRyemxtd3Fha3VwZWRwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM1NDA2ODYsImV4cCI6MjA3OTExNjY4Nn0.44aKq7FEe-XiVU0hRYgWCwHvEeokdOHLrxuEFCkMP_g"

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
}

response = requests.get(
    f"{SUPABASE_URL}/rest/v1/master_sheet?select=source",
    headers=headers
)

if response.status_code == 200:
    data = response.json()
    db_sources = {}
    for row in data:
        source = row['source']
        db_sources[source] = db_sources.get(source, 0) + 1
    
    print("\nDatabase Sources:")
    for source, count in db_sources.items():
        print(f"  {source}: {count} rows")
    print(f"Total DB rows: {len(data)}")
    
print("\n" + "="*60)
print("ACTION NEEDED:")
print("="*60)
print("1. Delete all records in Supabase Table Editor")
print("2. Run: python3 upload_clean.py")
print("3. Refresh browser")
print("="*60)
