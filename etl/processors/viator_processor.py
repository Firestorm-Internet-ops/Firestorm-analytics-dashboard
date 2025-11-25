"""Viator data processor"""
import pandas as pd
import logging
import re
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from campaign_normalizer import normalize_campaign_id

logger = logging.getLogger(__name__)

def clean_currency_value(value):
    """
    Extract numeric value from currency string
    Handles: "EUR17.06EUR112.60" → 129.66
    Also handles: "Pending" → 0
    """
    if pd.isna(value):
        return 0.0
    
    value_str = str(value)
    
    # Handle 'Pending' status
    if 'Pending' in value_str or 'pending' in value_str.lower():
        return 0.0
    
    # Remove currency symbols and spaces
    value_str = value_str.replace('€', '').replace('EUR', '').replace(' ', '')
    
    # Extract all numbers (with optional decimal point)
    numbers = re.findall(r'\d+\.?\d*', value_str)
    
    if numbers:
        # Sum all found numbers
        total = sum(float(num) for num in numbers)
        return total
    
    return 0.0


def process_viator(file_path, date):
    """
    Process Viator data
    
    Logic:
    - Traffic sheet: visitors & bookings (uses "Campaign Name")
    - Orders sheet: customer country + commission (uses "Campaign")
    - Match on: Campaign Name (Traffic) = Campaign (Orders)
    - Aggregate by Campaign: SUM all metrics
    - One row per (Date, Source, CampaignId)
    """
    rows = []
    try:
        # Check if sheets exist
        xl_file = pd.ExcelFile(file_path)
        if 'Viator - Orders' not in xl_file.sheet_names or 'Viator - Traffic' not in xl_file.sheet_names:
            logger.info("  ⊘ Viator: sheets not found, skipping")
            return rows
            
        orders_df = pd.read_excel(file_path, sheet_name='Viator - Orders')
        traffic_df = pd.read_excel(file_path, sheet_name='Viator - Traffic')
        
        # Check if required columns exist
        if 'Campaign' not in orders_df.columns:
            logger.warning("  ✗ Viator: 'Campaign' column not found in Orders sheet")
            return rows
        
        if 'Campaign Name' not in traffic_df.columns:
            logger.warning("  ✗ Viator: 'Campaign Name' column not found in Traffic sheet")
            return rows
        
        # Step 1: Normalize campaign IDs (remove suffixes)
        traffic_df['Campaign Normalized'] = traffic_df['Campaign Name'].apply(normalize_campaign_id)
        orders_df['Campaign Normalized'] = orders_df['Campaign'].apply(normalize_campaign_id)
        
        # Aggregate Traffic by normalized Campaign Name
        # SUM: Unique Visitors, Bookings
        traffic_agg = traffic_df.groupby('Campaign Normalized').agg({
            'Unique Visitors': 'sum',
            'Bookings': 'sum'
        }).reset_index()
        
        # Step 2: Clean and aggregate Orders by normalized Campaign
        # Clean Commission, then SUM per Campaign
        # Also get most common Customer country per Campaign
        orders_df['Commission Clean'] = orders_df['Commission (Payout currency)'].apply(clean_currency_value)
        
        orders_agg = orders_df.groupby('Campaign Normalized').agg({
            'Customer country': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Unknown',
            'Commission Clean': 'sum'
        }).reset_index()
        
        # Step 3: Merge Traffic with Orders on normalized campaign
        merged = traffic_agg.merge(orders_agg, on='Campaign Normalized', how='left')
        
        # Step 4: Create output rows
        for _, row in merged.iterrows():
            rows.append({
                'Date': date,
                'Source': 'Viator',
                'City': row.get('Customer country', 'Unknown'),
                'CampaignId': row['Campaign Normalized'],
                'Visitors': int(row['Unique Visitors']),
                'Bookings': int(row['Bookings']),
                'Revenue': float(row.get('Commission Clean', 0))
            })
        
        logger.info(f"  ✓ Viator: {len(rows)} rows")
        
    except Exception as e:
        logger.warning(f"  ✗ Viator processing failed: {e}")
    
    return rows
