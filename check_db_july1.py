import requests
from config import SUPABASE_URL, SUPABASE_KEY

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
}

# Get all July 1 data
response = requests.get(
    f"{SUPABASE_URL}/rest/v1/master_sheet?date=eq.2025-07-01&select=source,visitors,bookings,revenue",
    headers=headers
)

if response.status_code == 200:
    data = response.json()
    
    total_visitors = sum(row['visitors'] for row in data)
    total_bookings = sum(row['bookings'] for row in data)
    total_revenue = sum(row['revenue'] for row in data)
    
    print(f"Database - July 1, 2025:")
    print(f"Total rows: {len(data)}")
    print(f"Total Visitors: {total_visitors}")
    print(f"Total Bookings: {total_bookings}")
    print(f"Total Revenue: €{total_revenue:.2f}")
    print(f"Conversion Rate: {(total_bookings/total_visitors*100):.2f}%")
    
    # By source
    by_source = {}
    for row in data:
        source = row['source']
        if source not in by_source:
            by_source[source] = {'visitors': 0, 'bookings': 0, 'revenue': 0}
        by_source[source]['visitors'] += row['visitors']
        by_source[source]['bookings'] += row['bookings']
        by_source[source]['revenue'] += row['revenue']
    
    print("\nBy Source:")
    for source, metrics in by_source.items():
        print(f"  {source}: {metrics['visitors']} visitors, {metrics['bookings']} bookings, €{metrics['revenue']:.2f}")
else:
    print(f"Error: {response.status_code}")
