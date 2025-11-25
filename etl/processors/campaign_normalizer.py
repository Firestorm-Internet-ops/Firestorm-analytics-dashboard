"""
Campaign ID normalizer
Removes location suffixes from campaign IDs to group variations together
"""
import re

# List of known suffixes to remove
CAMPAIGN_SUFFIXES = [
    '-aw',      # Article widget
    '-dw',      # Desktop widget
    '-auto',    # Auto placement
    '-top',     # Top placement
    '-sb',      # Sidebar
    '-bottom',  # Bottom placement
    '-inline',  # Inline placement
    '-mobile',  # Mobile placement
]

def normalize_campaign_id(campaign_id):
    """
    Remove location suffixes from campaign ID
    
    Examples:
    - "louvre-museum-aw" → "louvre-museum"
    - "louvre-museum-dw" → "louvre-museum"
    - "louvre-museum-top" → "louvre-museum"
    - "eiffel-tower" → "eiffel-tower" (no change)
    """
    if not campaign_id or campaign_id == 'Unknown':
        return campaign_id
    
    campaign_str = str(campaign_id).strip()
    
    # Check each suffix and remove if found at the end
    for suffix in CAMPAIGN_SUFFIXES:
        if campaign_str.endswith(suffix):
            return campaign_str[:-len(suffix)]
    
    return campaign_str
