"""GetYourGuide data processor"""
import pandas as pd
import logging
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from campaign_normalizer import normalize_campaign_id

logger = logging.getLogger(__name__)

def process_gyg(file_path, date):
    """
    Process GetYourGuide data
    
    Logic:
    - Traffic sheet: metrics (visitors, bookings, revenue)
    - Orders sheet: only for City mapping
    - Aggregate by Campaign: SUM visitors, bookings, revenue
    - One row per (Date, Source, CampaignId)
    """
    rows = []
    try:
        # Check if sheets exist
        xl_file = pd.ExcelFile(file_path)
        if 'GYG - Orders' not in xl_file.sheet_names or 'GYG - Traffic' not in xl_file.sheet_names:
            logger.info("  ⊘ GYG: sheets not found, skipping")
            return rows
            
        orders_df = pd.read_excel(file_path, sheet_name='GYG - Orders')
        traffic_df = pd.read_excel(file_path, sheet_name='GYG - Traffic')
        
        # Step 1: Build Campaign → City mapping from Orders
        # Take most common City per Campaign
        if 'Campaign' in orders_df.columns and 'City' in orders_df.columns:
            campaign_city_map = orders_df.groupby('Campaign')['City'].agg(
                lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Unknown'
            ).to_dict()
        else:
            campaign_city_map = {}
        
        # Step 2: Normalize campaign IDs (remove suffixes like -aw, -dw, etc.)
        traffic_df['Campaign Normalized'] = traffic_df['Campaign'].apply(normalize_campaign_id)
        
        # Aggregate Traffic by normalized Campaign
        # SUM: Visitors, Bookings, Potential income
        traffic_agg = traffic_df.groupby('Campaign Normalized').agg({
            'Visitors': 'sum',
            'Bookings': 'sum',
            'Potential income': 'sum'
        }).reset_index()
        
        # Step 3: Create output rows
        for _, row in traffic_agg.iterrows():
            campaign = row['Campaign Normalized']
            city = campaign_city_map.get(campaign, 'Unknown')
            
            rows.append({
                'Date': date,
                'Source': 'GYG',
                'City': city,
                'CampaignId': campaign,
                'Visitors': int(row['Visitors']),
                'Bookings': int(row['Bookings']),
                'Revenue': float(row['Potential income'])
            })
        
        logger.info(f"  ✓ GYG: {len(rows)} rows")
        
    except Exception as e:
        logger.warning(f"  ✗ GYG processing failed: {e}")
    
    return rows
