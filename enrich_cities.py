"""
Enrich existing database with city names extracted from campaign IDs
"""
import sys
import os
sys.path.insert(0, 'etl/processors')

from city_mapper import extract_city_from_campaign
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('VITE_SUPABASE_URL')
SUPABASE_KEY = os.getenv('VITE_SUPABASE_PUBLISHABLE_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def enrich_database_cities():
    """Update database records with enriched city data"""
    print("Fetching records with Unknown cities...")
    
    # Fetch all records with Unknown city
    page_size = 1000
    offset = 0
    total_updated = 0
    
    while True:
        response = supabase.table('master_sheet')\
            .select('id, campaign_id, city')\
            .eq('city', 'Unknown')\
            .range(offset, offset + page_size - 1)\
            .execute()
        
        records = response.data
        if not records:
            break
        
        print(f"Processing {len(records)} records (offset {offset})...")
        
        # Update each record
        updates = []
        for record in records:
            campaign_id = record['campaign_id']
            new_city = extract_city_from_campaign(campaign_id)
            
            if new_city != 'Unknown':
                updates.append({
                    'id': record['id'],
                    'city': new_city
                })
        
        # Batch update
        if updates:
            for update in updates:
                supabase.table('master_sheet')\
                    .update({'city': update['city']})\
                    .eq('id', update['id'])\
                    .execute()
            
            total_updated += len(updates)
            print(f"  ✓ Updated {len(updates)} records")
        
        if len(records) < page_size:
            break
        
        offset += page_size
    
    print(f"\n{'='*50}")
    print(f"ENRICHMENT COMPLETE")
    print(f"{'='*50}")
    print(f"Total records updated: {total_updated}")
    print(f"{'='*50}")

if __name__ == '__main__':
    enrich_database_cities()
