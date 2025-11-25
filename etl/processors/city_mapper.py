"""
City Mapper - Extract city names from campaign IDs
Maps campaign IDs to cities based on known patterns and keywords
"""

# City mapping based on campaign keywords
CITY_KEYWORDS = {
    # US Cities
    'alcatraz': 'San Francisco',
    'golden-gate': 'San Francisco',
    'sf-': 'San Francisco',
    'decks': 'New York City',
    'empire-state': 'New York City',
    'statue-liberty': 'New York City',
    'nyc-': 'New York City',
    'ny-': 'New York City',
    'brooklyn': 'New York City',
    'manhattan': 'New York City',
    'times-square': 'New York City',
    'central-park': 'New York City',
    'cancun': 'Cancun',
    'miami': 'Miami',
    'vegas': 'Las Vegas',
    'los-angeles': 'Los Angeles',
    'la-': 'Los Angeles',
    'hollywood': 'Los Angeles',
    'chicago': 'Chicago',
    'boston': 'Boston',
    'seattle': 'Seattle',
    'space-needle': 'Seattle',
    'washington': 'Washington DC',
    'dc-': 'Washington DC',
    
    # European Cities
    'paris': 'Paris',
    'eiffel': 'Paris',
    'louvre': 'Paris',
    'versailles': 'Paris',
    'arc-de-triomphe': 'Paris',
    'notre-dame': 'Paris',
    'london': 'London',
    'tower-bridge': 'London',
    'big-ben': 'London',
    'buckingham': 'London',
    'westminster': 'London',
    'rome': 'Rome',
    'colosseum': 'Rome',
    'vatican': 'Rome',
    'trevi': 'Rome',
    'barcelona': 'Barcelona',
    'sagrada': 'Barcelona',
    'gaudi': 'Barcelona',
    'madrid': 'Madrid',
    'prado': 'Madrid',
    'amsterdam': 'Amsterdam',
    'anne-frank': 'Amsterdam',
    'rijksmuseum': 'Amsterdam',
    'van-gogh': 'Amsterdam',
    'berlin': 'Berlin',
    'brandenburg': 'Berlin',
    'reichstag': 'Berlin',
    'vienna': 'Vienna',
    'belvedere': 'Vienna',
    'schonbrunn': 'Vienna',
    'bp-': 'Vienna',  # Belvedere Palace
    'prague': 'Prague',
    'budapest': 'Budapest',
    'athens': 'Athens',
    'acropolis': 'Athens',
    'parthenon': 'Athens',
    'venice': 'Venice',
    'gondola': 'Venice',
    'florence': 'Florence',
    'uffizi': 'Florence',
    'milan': 'Milan',
    'duomo': 'Milan',
    'munich': 'Munich',
    'dachau': 'Munich',
    'neuschwanstein': 'Munich',
    'lisbon': 'Lisbon',
    'porto': 'Porto',
    'dublin': 'Dublin',
    'edinburgh': 'Edinburgh',
    'copenhagen': 'Copenhagen',
    'stockholm': 'Stockholm',
    'oslo': 'Oslo',
    'helsinki': 'Helsinki',
    
    # Middle East
    'dubai': 'Dubai',
    'burj': 'Dubai',
    'bk-': 'Dubai',  # Burj Khalifa
    'abu-dhabi': 'Abu Dhabi',
    'jerusalem': 'Jerusalem',
    'tel-aviv': 'Tel Aviv',
    'istanbul': 'Istanbul',
    'hagia-sophia': 'Istanbul',
    
    # Asia
    'tokyo': 'Tokyo',
    'kyoto': 'Kyoto',
    'osaka': 'Osaka',
    'bangkok': 'Bangkok',
    'singapore': 'Singapore',
    'hong-kong': 'Hong Kong',
    'shanghai': 'Shanghai',
    'beijing': 'Beijing',
    'forbidden-city': 'Beijing',
    'great-wall': 'Beijing',
    'seoul': 'Seoul',
    'taipei': 'Taipei',
    'kuala-lumpur': 'Kuala Lumpur',
    'petronas': 'Kuala Lumpur',
    'bali': 'Bali',
    'phuket': 'Phuket',
    'hanoi': 'Hanoi',
    'ho-chi-minh': 'Ho Chi Minh City',
    'saigon': 'Ho Chi Minh City',
    
    # Australia & NZ
    'sydney': 'Sydney',
    'opera-house': 'Sydney',
    'melbourne': 'Melbourne',
    'brisbane': 'Brisbane',
    'perth': 'Perth',
    'auckland': 'Auckland',
    'wellington': 'Wellington',
    
    # South America
    'rio': 'Rio de Janeiro',
    'christ-redeemer': 'Rio de Janeiro',
    'sao-paulo': 'São Paulo',
    'buenos-aires': 'Buenos Aires',
    'lima': 'Lima',
    'machu-picchu': 'Cusco',
    'bogota': 'Bogotá',
    'santiago': 'Santiago',
    
    # Africa
    'cairo': 'Cairo',
    'pyramids': 'Cairo',
    'marrakech': 'Marrakech',
    'cape-town': 'Cape Town',
    'table-mountain': 'Cape Town',
    'johannesburg': 'Johannesburg',
    'nairobi': 'Nairobi',
}

def extract_city_from_campaign(campaign_id):
    """
    Extract city name from campaign ID based on keywords
    
    Args:
        campaign_id: Campaign identifier string
        
    Returns:
        City name if found, otherwise 'Unknown'
    """
    if not campaign_id or campaign_id == 'Unknown':
        return 'Unknown'
    
    campaign_lower = str(campaign_id).lower()
    
    # Check each keyword
    for keyword, city in CITY_KEYWORDS.items():
        if keyword in campaign_lower:
            return city
    
    return 'Unknown'

def enrich_city_data(df):
    """
    Enrich dataframe with city names extracted from campaign IDs
    Updates 'City' column where it's 'Unknown' or empty
    
    Args:
        df: Pandas DataFrame with 'CampaignId' and 'City' columns
        
    Returns:
        DataFrame with enriched city data
    """
    # Only update rows where City is Unknown or empty
    mask = (df['City'] == 'Unknown') | (df['City'].isna()) | (df['City'] == '')
    
    if mask.any():
        df.loc[mask, 'City'] = df.loc[mask, 'CampaignId'].apply(extract_city_from_campaign)
    
    return df
