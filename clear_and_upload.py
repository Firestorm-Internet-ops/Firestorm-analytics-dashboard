"""
Clear database and upload all data in batches
"""
import pandas as pd
import requests
import json

SUPABASE_URL = "https://zbueoutrzlmwqakupedp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpidWVvdXRyemxtd3Fha3VwZWRwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM1NDA2ODYsImV4cCI6MjA3OTExNjY4Nn0.44aKq7FEe-XiVU0hRYgWCwHvEeokdOHLrxuEFCkMP_g"

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal'
}

# Step 1: Clear existing data
print("Step 1: Clearing existing data...")
response = requests.delete(
    f"{SUPABASE_URL}/rest/v1/master_sheet?id=neq.00000000-0000-0000-0000-000000000000",
    headers=headers
)

if response.status_code in [200, 204]:
    print("✓ Database cleared successfully")
else:
    print(f"✗ Failed to clear: {response.status_code} - {response.text}")
    exit(1)

# Step 2: Read CSV
print("\nStep 2: Reading CSV file...")
df = pd.read_csv('etl/processed/processed_data.csv')
print(f"Total rows to upload: {len(df)}")

# Step 3: Convert to records
print("\nStep 3: Preparing data...")

records = []
for _, row in df.iterrows():
    date_obj = pd.to_datetime(row['Date'])
    
    # Ensure all values are JSON serializable
    campaign_id = None if pd.isna(row['CampaignId']) or row['CampaignId'] == '' else str(row['CampaignId'])
    city = 'Unknown' if pd.isna(row['City']) or row['City'] == '' else str(row['City'])
    
    records.append({
        'date': str(row['Date']),
        'day': str(date_obj.day),
        'month': str(date_obj.month),
        'year': str(date_obj.year),
        'source': str(row['Source']),
        'city': city,
        'campaign_id': campaign_id,
        'visitors': int(row['Visitors']) if not pd.isna(row['Visitors']) else 0,
        'bookings': int(row['Bookings']) if not pd.isna(row['Bookings']) else 0,
        'revenue': float(row['Revenue']) if not pd.isna(row['Revenue']) else 0.0
    })

# Step 4: Upload in batches
BATCH_SIZE = 500  # Smaller batches for reliability
total_batches = (len(records) + BATCH_SIZE - 1) // BATCH_SIZE

print(f"\nStep 4: Uploading in {total_batches} batches of {BATCH_SIZE} rows each...")

uploaded = 0
failed = 0

for i in range(0, len(records), BATCH_SIZE):
    batch = records[i:i + BATCH_SIZE]
    batch_num = (i // BATCH_SIZE) + 1
    
    print(f"Batch {batch_num}/{total_batches} ({len(batch)} rows)...", end=" ")
    
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/master_sheet",
        headers=headers,
        data=json.dumps(batch)
    )
    
    if response.status_code in [200, 201]:
        uploaded += len(batch)
        print(f"✓ ({uploaded}/{len(records)} total)")
    else:
        failed += len(batch)
        print(f"✗ Failed: {response.status_code}")
        print(f"   Error: {response.text[:200]}")

print(f"\n{'='*60}")
print(f"Upload complete!")
print(f"Successfully uploaded: {uploaded}/{len(records)} rows")
if failed > 0:
    print(f"Failed: {failed} rows")
print(f"{'='*60}")
