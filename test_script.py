import pandas as pd
from pathlib import Path

print("Starting test...")

input_folder = Path('etl/raw_data')
files = list(input_folder.glob('*.xlsx'))

print(f"Found {len(files)} files")

if files:
    print(f"First file: {files[0].name}")
    
print("Test complete!")
