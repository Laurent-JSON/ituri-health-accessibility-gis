"""
Spatial analysis module for health facility accessibility
"""

import numpy as np
import logging
from sklearn.neighbors import BallTree

logging.basicConfig(level=logging.INFO)

def classify_health_access(row):
    if row['has_health_center'] == 'Yes':
        if row['health_center_type'] in ['General Hospital', 'Referral Center']:
            return 'Good'
        else:
            return 'Limited'
    return 'Poor'

def create_facilities_gdf(gdf):
    facilities = gdf[gdf['has_health_center'] == 'Yes'].copy()
    logging.info(f"Identified {len(facilities)} health facilities")
    return facilities