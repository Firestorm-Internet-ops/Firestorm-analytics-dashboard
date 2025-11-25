import pandas as pd

# Read CSV
df = pd.read_csv('etl/processed/processed_data.csv')

print("="*80)
print("CSV DUPLICATE ANALYSIS")
print("="*80)

# Check for exact duplicates
exact_dupes = df.duplicated(keep=False)
print(f"\nTotal rows in CSV: {len(df)}")
print(f"Exact duplicate rows: {exact_dupes.sum()}")

# Check July 1 specifically
july1 = df[df['Date'] == '2025-07-01']
print(f"\nJuly 1 rows: {len(july1)}")

# Check for duplicates by key fields
key_dupes = df.duplicated(subset=['Date', 'Source', 'CampaignId'], keep=False)
print(f"Duplicate by (Date, Source, Campaign): {key_dupes.sum()}")

if key_dupes.any():
    print("\nShowing duplicate examples:")
    dupes_df = df[key_dupes].sort_values(['Date', 'Source', 'CampaignId'])
    print(dupes_df[['Date', 'Source', 'City', 'CampaignId', 'Visitors', 'Bookings', 'Revenue']].head(20))
    
    # Show July 1 duplicates
    july1_dupes = dupes_df[dupes_df['Date'] == '2025-07-01']
    if len(july1_dupes) > 0:
        print(f"\nJuly 1 duplicates: {len(july1_dupes)} rows")
        print(july1_dupes[['Source', 'City', 'CampaignId', 'Visitors', 'Bookings', 'Revenue']])

# Check if ETL ran twice on same files
print("\n" + "="*80)
print("CHECKING IF SAME DATA APPEARS TWICE")
print("="*80)

# Group by all fields and count
grouped = df.groupby(['Date', 'Source', 'City', 'CampaignId', 'Visitors', 'Bookings', 'Revenue']).size().reset_index(name='count')
duplicated_groups = grouped[grouped['count'] > 1]

if len(duplicated_groups) > 0:
    print(f"\n⚠️  Found {len(duplicated_groups)} groups that appear multiple times!")
    print("\nExamples:")
    print(duplicated_groups.head(10))
else:
    print("✓ No duplicate groups found")
