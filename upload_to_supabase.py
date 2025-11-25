"""
Upload processed CSV to Supabase in batches
"""
import pandas as pd
import requests
import json

# Supabase credentials
SUPABASE_URL = "https://zbueoutrzlmwqakupedp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpidWVvdXRyemxtd3Fha3VwZWRwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM1NDA2ODYsImV4cCI6MjA3OTExNjY4Nn0.44aKq7FEe-XiVU0hRYgWCwHvEeokdOHLrxuEFCkMP_g"

# Read CSV
print("Reading CSV file...")
df = pd.read_csv('etl/processed/processed_data.csv')
print(f"Total rows to upload: {len(df)}")

# Convert to records
records = []
for _, row in df.iterrows():
    date_obj = pd.to_datetime(row['Date'])
    records.append({
        'date': row['Date'],
        'day': str(date_obj.day),
        'month': str(date_obj.month),
        'year': str(date_obj.year),
        'source': row['Source'],
        'city': row['City'],
        'campaign_id': row['CampaignId'] if pd.notna(row['CampaignId']) else None,
        'visitors': int(row['Visitors']),
        'bookings': int(row['Bookings']),
        'revenue': float(row['Revenue'])
    })

# Upload in batches
BATCH_SIZE = 1000
total_batches = (len(records) + BATCH_SIZE - 1) // BATCH_SIZE

print(f"\nUploading in {total_batches} batches of {BATCH_SIZE} rows each...")

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal'
}

uploaded = 0
for i in range(0, len(records), BATCH_SIZE):
    batch = records[i:i + BATCH_SIZE]
    batch_num = (i // BATCH_SIZE) + 1
    
    print(f"Uploading batch {batch_num}/{total_batches} ({len(batch)} rows)...", end=" ")
    
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/master_sheet",
        headers=headers,
        data=json.dumps(batch)
    )
    
    if response.status_code in [200, 201]:
        uploaded += len(batch)
        print(f"✓ Success ({uploaded}/{len(records)} total)")
    else:
        print(f"✗ Failed: {response.status_code} - {response.text}")
        break

print(f"\n{'='*60}")
print(f"Upload complete!")
print(f"Total rows uploaded: {uploaded}/{len(records)}")
print(f"{'='*60}")
