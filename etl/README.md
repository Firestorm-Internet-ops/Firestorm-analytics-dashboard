# ETL Script - Tour/Activity Analytics

## Setup

### 1. Install Python Dependencies

```bash
pip install -r etl/requirements.txt
```

### 2. Folder Structure

```
etl/
├── raw_data/          ← Put your Excel files here
├── processed/         ← Output CSV will be here
├── logs/              ← Processing logs
├── processors/        ← Data transformation logic
└── process_data.py    ← Main script
```

## Usage

### Basic Usage (Process all files)

```bash
python etl/process_data.py
```

This will:
- Scan `etl/raw_data/` for all Excel files
- Process GYG, Tiqets, and Viator data
- Output: `etl/processed/processed_data.csv`

### Dry Run (See what would be processed)

```bash
python etl/process_data.py --dry-run
```

### Custom Folders

```bash
python etl/process_data.py --input my_data --output my_output
```

## Workflow

### Initial Setup (3 months of data)

1. **Put all Excel files in `etl/raw_data/`**
   ```
   etl/raw_data/
   ├── Orders and Traffic data for 01.07.2025.xlsx
   ├── Orders and Traffic data for 02.07.2025.xlsx
   ├── ... (90 files)
   └── Orders and Traffic data for 30.09.2025.xlsx
   ```

2. **Run the script**
   ```bash
   python etl/process_data.py
   ```

3. **Upload the output**
   - Open your app at http://localhost:8080/
   - Click "Upload Data"
   - Select `etl/processed/processed_data.csv`
   - Done!

### Daily Updates

1. Partner sends new Excel → Save to `etl/raw_data/`
2. Run: `python etl/process_data.py`
3. Upload the new CSV

## Output Format

The script produces a CSV with these columns:

```
Date,Source,City,CampaignId,Visitors,Bookings,Revenue
2025-07-01,GYG,New York,CAMP001,1200,85,8500
2025-07-01,Tiqets,Germany,CAMP002,950,62,6200
2025-07-01,Viator,USA,CAMP003,780,45,4500
```

## Troubleshooting

### No files found
- Check that Excel files are in `etl/raw_data/`
- File names must match pattern: `Orders and Traffic data for DD.MM.YYYY.xlsx`

### Missing sheets error
- Some days might not have all partner data
- Script will log warnings and continue

### Check logs
```bash
type etl\logs\processing.log
```

## Mapping Rules

### GetYourGuide (GYG)
- Sheets: `GYG - Orders`, `GYG - Traffic`
- City: From Orders sheet
- Revenue: `Potential income` column

### Tiqets
- Sheets: `Tiqets - Orders`, `Tiqets - Traffic`
- City: `Country` column
- Revenue: `Order Value` (aggregated by campaign)

### Viator
- Sheets: `Viator - Orders`, `Viator - Traffic`
- City: `Customer country`
- Revenue: `Commission (Payout currency)`
