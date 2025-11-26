"""
Clean upload with duplicate prevention
"""
import pandas as pd
import requests
import json
import time
from config import SUPABASE_URL, SUPABASE_KEY

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal'
}

# Step 1: Verify database is empty
print("Step 1: Verifying database is empty...")
response = requests.head(
    f"{SUPABASE_URL}/rest/v1/master_sheet",
    headers={**headers, 'Prefer': 'count=exact'}
)

if response.status_code in [200, 206]:
    count = response.headers.get('Content-Range', '').split('/')[-1]
    if count != '0':
        print(f"⚠️  WARNING: Database has {count} rows!")
        print("Please delete all records manually first.")
        exit(1)
    else:
        print("✓ Database is empty")
else:
    print(f"Could not verify database status: {response.status_code}")

# Step 2: Read and deduplicate CSV
print("\nStep 2: Reading and deduplicating CSV...")
df = pd.read_csv('etl/processed/processed_data.csv')
print(f"Total rows in CSV: {len(df)}")

# Check for duplicates
duplicates = df.duplicated(subset=['Date', 'Source', 'City', 'CampaignId'], keep='first')
if duplicates.any():
    print(f"⚠️  Found {duplicates.sum()} duplicate rows - removing them")
    df = df[~duplicates]
    print(f"Rows after deduplication: {len(df)}")
else:
    print("✓ No duplicates found")

# Step 3: Prepare data
print("\nStep 3: Preparing data...")
records = []
for _, row in df.iterrows():
    date_obj = pd.to_datetime(row['Date'])
    
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

print(f"✓ Prepared {len(records)} records")

# Step 4: Upload in batches
BATCH_SIZE = 500
total_batches = (len(records) + BATCH_SIZE - 1) // BATCH_SIZE

print(f"\nStep 4: Uploading in {total_batches} batches...")

uploaded = 0
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
        print(f"✗ Failed: {response.status_code}")
        print(f"   Error: {response.text[:200]}")
        break
    
    time.sleep(0.1)  # Small delay between batches

print(f"\n{'='*60}")
print(f"Upload complete!")
print(f"Successfully uploaded: {uploaded}/{len(records)} rows")
print(f"{'='*60}")

# Step 5: Verify upload
print("\nStep 5: Verifying upload...")
response = requests.head(
    f"{SUPABASE_URL}/rest/v1/master_sheet",
    headers={**headers, 'Prefer': 'count=exact'}
)

if response.status_code in [200, 206]:
    final_count = response.headers.get('Content-Range', '').split('/')[-1]
    print(f"✓ Database now has {final_count} rows")
    
    if int(final_count) == len(records):
        print("✓ Upload verified - counts match!")
    else:
        print(f"⚠️  Warning: Expected {len(records)} but database has {final_count}")
