import pandas as pd

# Read the processed CSV
df = pd.read_csv('etl/processed/processed_data.csv')

# Filter for July 1, 2025
july1_data = df[df['Date'] == '2025-07-01']

print("="*80)
print("JULY 1, 2025 - RAW DATA BREAKDOWN")
print("="*80)

# Group by Source
by_source = july1_data.groupby('Source').agg({
    'Visitors': 'sum',
    'Bookings': 'sum',
    'Revenue': 'sum'
}).reset_index()

print("\nBy Source:")
print(by_source)
print(f"\nTotal Visitors: {july1_data['Visitors'].sum()}")
print(f"Total Bookings: {july1_data['Bookings'].sum()}")
print(f"Total Revenue: €{july1_data['Revenue'].sum():.2f}")
print(f"Conversion Rate: {(july1_data['Bookings'].sum() / july1_data['Visitors'].sum() * 100):.2f}%")

print("\n" + "="*80)
print("DETAILED BREAKDOWN BY CAMPAIGN")
print("="*80)

# Show top campaigns
by_campaign = july1_data.groupby(['Source', 'CampaignId', 'City']).agg({
    'Visitors': 'sum',
    'Bookings': 'sum',
    'Revenue': 'sum'
}).reset_index().sort_values('Visitors', ascending=False)

print(by_campaign.head(20))

print("\n" + "="*80)
print(f"Total rows for July 1: {len(july1_data)}")
print("="*80)
