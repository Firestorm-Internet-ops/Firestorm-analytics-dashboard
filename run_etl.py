import pandas as pd
import re
from datetime import datetime
from pathlib import Path
import sys
import os

# Add processors directory to path
sys.path.insert(0, 'etl/processors')

from gyg_processor import process_gyg
from tiqets_processor import process_tiqets
from viator_processor import process_viator

def extract_date_from_filename(filename):
    """Extract date from filename"""
    try:
        match = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', filename)
        if match:
            day, month, year = match.groups()
            date_str = f"{year}-{month}-{day}"
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        return None
    except Exception as e:
        print(f"Error parsing date: {e}")
        return None

def process_file(file_path, date):
    """Process a single Excel file"""
    all_rows = []
    
    print(f"Processing: {file_path.name} (Date: {date})")
    
    all_rows.extend(process_gyg(file_path, date))
    all_rows.extend(process_tiqets(file_path, date))
    all_rows.extend(process_viator(file_path, date))
    
    return all_rows

# Main execution
print("="*60)
print("ETL SCRIPT STARTING")
print("="*60)

input_folder = Path('etl/raw_data')
output_folder = Path('etl/processed')
output_folder.mkdir(parents=True, exist_ok=True)

excel_files = list(input_folder.glob('*.xlsx'))

print(f"\nFound {len(excel_files)} Excel files\n")

all_data = []
stats = {'processed': 0, 'failed': 0, 'total_rows': 0}

for i, file_path in enumerate(excel_files, 1):
    try:
        print(f"\n[{i}/{len(excel_files)}] ", end="")
        date = extract_date_from_filename(file_path.name)
        if not date:
            print(f"SKIPPED: Could not extract date from {file_path.name}")
            stats['failed'] += 1
            continue
        
        rows = process_file(file_path, date)
        all_data.extend(rows)
        stats['processed'] += 1
        stats['total_rows'] += len(rows)
        print(f"  → Total rows from this file: {len(rows)}")
        
    except Exception as e:
        print(f"ERROR processing {file_path.name}: {e}")
        stats['failed'] += 1

print("\n" + "="*60)
print("PROCESSING COMPLETE")
print("="*60)

if all_data:
    df = pd.DataFrame(all_data)
    output_file = output_folder / 'processed_data.csv'
    df.to_csv(output_file, index=False)
    
    print(f"Files processed: {stats['processed']}")
    print(f"Files failed: {stats['failed']}")
    print(f"Total rows: {stats['total_rows']}")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Sources: {', '.join(df['Source'].unique())}")
    print(f"\nOutput file: {output_file}")
    print(f"File size: {output_file.stat().st_size / 1024:.1f} KB")
    print("="*60)
else:
    print("ERROR: No data was processed!")
