# City Mapping from Campaign IDs

## Overview

The city mapper automatically extracts city names from campaign IDs when city information is missing or marked as "Unknown". This helps fill in missing location data based on recognizable patterns in campaign names.

## How It Works

The mapper uses keyword matching to identify cities from campaign IDs:

**Examples:**
- `alcatraz-island-day-tour` → **San Francisco**
- `bk-burj-club` → **Dubai** (bk = Burj Khalifa)
- `bp-belvedere-21-museum-ticket` → **Vienna** (bp = Belvedere Palace)
- `louvre-museum` → **Paris**
- `decks-summit` → **New York City** (decks = Top of the Rock)
- `eiffel-tower-tickets` → **Paris**
- `colosseum-tour` → **Rome**

## Supported Cities

The mapper includes 100+ cities worldwide across:
- **North America**: New York, San Francisco, Los Angeles, Miami, Cancun, etc.
- **Europe**: Paris, London, Rome, Barcelona, Amsterdam, Vienna, etc.
- **Middle East**: Dubai, Abu Dhabi, Istanbul, Jerusalem, etc.
- **Asia**: Tokyo, Bangkok, Singapore, Hong Kong, Shanghai, etc.
- **Australia & NZ**: Sydney, Melbourne, Auckland, etc.
- **South America**: Rio de Janeiro, Buenos Aires, Lima, etc.
- **Africa**: Cairo, Cape Town, Marrakech, etc.

## Usage

### For New Data Processing

The city enrichment is automatically applied when processing new data:

```bash
python etl/process_data.py
```

The ETL pipeline will:
1. Process data from all sources (GYG, Tiqets, Viator)
2. Automatically enrich missing city data from campaign IDs
3. Output enriched data to `etl/processed/processed_data.csv`

### For Existing Database

To enrich existing database records:

```bash
python enrich_cities.py
```

This will:
1. Find all records with `city = 'Unknown'`
2. Extract city names from their campaign IDs
3. Update the database with enriched city data

## Adding New City Mappings

To add support for new cities or attractions, edit `etl/processors/city_mapper.py`:

```python
CITY_KEYWORDS = {
    # Add your mappings here
    'new-attraction': 'City Name',
    'keyword': 'City Name',
}
```

**Tips for adding mappings:**
- Use lowercase keywords
- Include common abbreviations
- Add famous landmarks/attractions
- Use hyphens for multi-word keywords

## Fallback Behavior

If no city can be determined from the campaign ID, the value remains as "Unknown". This ensures data integrity and allows manual review of unmapped campaigns.

## Benefits

✅ **Automatic enrichment** - No manual data entry needed
✅ **Consistent naming** - Standardized city names across all sources
✅ **Scalable** - Easy to add new city mappings
✅ **Non-destructive** - Only updates "Unknown" cities, preserves existing data
✅ **Transparent** - Logs show how many records were enriched
