import pandas as pd
from pathlib import Path

print("Testing Excel reading...")

file_path = Path('etl/raw_data/Orders and Traffic data for 01.07.2025.xlsx')

try:
    # Check what sheets exist
    xl_file = pd.ExcelFile(file_path)
    print(f"Sheets in file: {xl_file.sheet_names}")
    
    # Try reading GYG sheets
    if 'GYG - Orders' in xl_file.sheet_names:
        gyg_orders = pd.read_excel(file_path, sheet_name='GYG - Orders')
        print(f"GYG Orders columns: {list(gyg_orders.columns)}")
        print(f"GYG Orders rows: {len(gyg_orders)}")
    
except Exception as e:
    print(f"Error: {e}")
