"""Tiqets data processor"""
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
    Handles: "€71.99€27.99€71.99" → 171.97
    """
    if pd.isna(value):
        return 0.0
    
    value_str = str(value)
    
    # Remove currency symbols and spaces
    value_str = value_str.replace('€', '').replace('EUR', '').replace(' ', '')
    
    # Extract all numbers (with optional decimal point)
    numbers = re.findall(r'\d+\.?\d*', value_str)
    
    if numbers:
        # Sum all found numbers
        total = sum(float(num) for num in numbers)
        return total
    
    return 0.0


def process_tiqets(file_path, date):
    """
    Process Tiqets data
    
    Logic:
    - Traffic sheet: visitors & converted visitors
    - Orders sheet: country + order value
    - Aggregate by Campaign: SUM all metrics
    - One row per (Date, Source, CampaignId)
    """
    rows = []
    try:
        # Check if sheets exist
        xl_file = pd.ExcelFile(file_path)
        if 'Tiqets - Orders' not in xl_file.sheet_names or 'Tiqets - Traffic' not in xl_file.sheet_names:
            logger.info("  ⊘ Tiqets: sheets not found, skipping")
            return rows
            
        orders_df = pd.read_excel(file_path, sheet_name='Tiqets - Orders')
        traffic_df = pd.read_excel(file_path, sheet_name='Tiqets - Traffic')
        
        # Step 1: Normalize campaign IDs (remove suffixes)
        traffic_df['Campaign Normalized'] = traffic_df['Campaign'].apply(normalize_campaign_id)
        orders_df['Campaign Normalized'] = orders_df['Campaign'].apply(normalize_campaign_id)
        
        # Aggregate Traffic by normalized Campaign
        # SUM: Visitors, Converted Visitors
        traffic_agg = traffic_df.groupby('Campaign Normalized').agg({
            'Visitors': 'sum',
            'Converted Visitors': 'sum'
        }).reset_index()
        
        # Step 2: Clean and aggregate Orders by normalized Campaign
        # Clean Order Value, then SUM per Campaign
        # Also get most common Country per Campaign
        orders_df['Order Value Clean'] = orders_df['Order Value'].apply(clean_currency_value)
        
        orders_agg = orders_df.groupby('Campaign Normalized').agg({
            'Country': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Unknown',
            'Order Value Clean': 'sum'
        }).reset_index()
        
        # Step 3: Merge Traffic with Orders on normalized campaign
        merged = traffic_agg.merge(orders_agg, on='Campaign Normalized', how='left')
        
        # Step 4: Create output rows
        for _, row in merged.iterrows():
            rows.append({
                'Date': date,
                'Source': 'Tiqets',
                'City': row.get('Country', 'Unknown'),
                'CampaignId': row['Campaign Normalized'],
                'Visitors': int(row['Visitors']),
                'Bookings': int(row['Converted Visitors']),
                'Revenue': float(row.get('Order Value Clean', 0))
            })
        
        logger.info(f"  ✓ Tiqets: {len(rows)} rows")
        
    except Exception as e:
        logger.warning(f"  ✗ Tiqets processing failed: {e}")
    
    return rows
