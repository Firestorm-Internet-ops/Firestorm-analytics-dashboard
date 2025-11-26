"""
Test Supabase connection with new credentials
"""
from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client

print("Testing Supabase connection...")
print(f"URL: {SUPABASE_URL}")
print(f"Key: {SUPABASE_KEY[:20]}..." if SUPABASE_KEY else "Key: None")

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Try to query the master_sheet table
    response = supabase.table('master_sheet').select('*').limit(1).execute()
    
    print("\n✅ Connection successful!")
    print(f"✅ Can access master_sheet table")
    print(f"✅ Found {len(response.data)} record(s)")
    
except Exception as e:
    print(f"\n❌ Connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check that your .env file has the correct credentials")
    print("2. Verify the key is the anon/public key (not service_role)")
    print("3. Make sure the key hasn't expired")
