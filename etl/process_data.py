"""
ETL Script for Tour/Activity Analytics
Processes daily Excel files and outputs unified CSV
"""

import pandas as pd
import re
from datetime import datetime
from pathlib import Path
import argparse
import logging
import sys
import os

# Add processors directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'processors'))

from gyg_processor import process_gyg
from tiqets_processor import process_tiqets
from viator_processor import process_viator
from city_mapper import enrich_city_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl/logs/processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def extract_date_from_filename(filename):
    """Extract date from filename like 'Orders and Traffic data for 01.07.2025.xlsx'"""
    try:
        match = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', filename)
        if match:
            day, month, year = match.groups()
            date_str = f"{year}-{month}-{day}"
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        return None
    except Exception as e:
        logger.error(f"Error parsing date from {filename}: {e}")
        return None


def process_file(file_path, date):
    """Process a single Excel file"""
    all_rows = []
    
    logger.info(f"Processing: {file_path.name} (Date: {date})")
    
    all_rows.extend(process_gyg(file_path, date))
    all_rows.extend(process_tiqets(file_path, date))
    all_rows.extend(process_viator(file_path, date))
    
    return all_rows


def main():
    parser = argparse.ArgumentParser(description='Process tour/activity data')
    parser.add_argument('--input', default='etl/raw_data', help='Input folder')
    parser.add_argument('--output', default='etl/processed', help='Output folder')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be processed')
    args = parser.parse_args()
    
    input_folder = Path(args.input)
    output_folder = Path(args.output)
    output_folder.mkdir(parents=True, exist_ok=True)
    Path('etl/logs').mkdir(parents=True, exist_ok=True)
    
    excel_files = list(input_folder.glob('*.xlsx'))
    
    if not excel_files:
        logger.error(f"No Excel files found in {input_folder}")
        return
    
    logger.info(f"Found {len(excel_files)} Excel files")
    
    if args.dry_run:
        logger.info("DRY RUN - Files that would be processed:")
        for f in excel_files:
            date = extract_date_from_filename(f.name)
            logger.info(f"  - {f.name} → {date}")
        return
    
    all_data = []
    stats = {'processed': 0, 'failed': 0, 'total_rows': 0}
    
    for file_path in excel_files:
        try:
            date = extract_date_from_filename(file_path.name)
            if not date:
                stats['failed'] += 1
                continue
            
            rows = process_file(file_path, date)
            all_data.extend(rows)
            stats['processed'] += 1
            stats['total_rows'] += len(rows)
            
        except Exception as e:
            logger.error(f"Failed to process {file_path.name}: {e}")
            stats['failed'] += 1
    
    if all_data:
        df = pd.DataFrame(all_data)
        
        # Enrich city data from campaign IDs
        logger.info("Enriching city data from campaign IDs...")
        df = enrich_city_data(df)
        cities_enriched = (df['City'] != 'Unknown').sum()
        logger.info(f"  ✓ {cities_enriched} rows have city information")
        
        output_file = output_folder / 'processed_data.csv'
        df.to_csv(output_file, index=False)
        
        logger.info("\n" + "="*50)
        logger.info("PROCESSING COMPLETE")
        logger.info("="*50)
        logger.info(f"Files processed: {stats['processed']}")
        logger.info(f"Files failed: {stats['failed']}")
        logger.info(f"Total rows: {stats['total_rows']}")
        logger.info(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
        logger.info(f"Sources: {', '.join(df['Source'].unique())}")
        logger.info(f"Output: {output_file}")
        logger.info("="*50)
    else:
        logger.error("No data was processed!")


if __name__ == '__main__':
    main()
