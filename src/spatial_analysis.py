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

def calculate_nearest_facility(settlements_gdf, facilities_gdf):
    settlements_rad = np.radians(settlements_gdf.geometry.apply(lambda p: (p.y, p.x)))
    facilities_rad = np.radians(facilities_gdf.geometry.apply(lambda p: (p.y, p.x)))
    
    tree = BallTree(facilities_rad, metric='haversine')
    distances, indices = tree.query(settlements_rad, k=1)
    distances_km = distances.flatten() * 6371
    
    settlements_gdf['distance_to_facility_km'] = distances_km
    settlements_gdf['nearest_facility'] = facilities_gdf.iloc[indices.flatten()]['name'].values
    
    logging.info(f"Distance - min: {distances_km.min():.1f}km, max: {distances_km.max():.1f}km")
    return settlements_gdf

def calculate_population_without_access(gdf, threshold_km=15):
    no_access = gdf[gdf['distance_to_facility_km'] > threshold_km]
    stats = {
        'total_population': gdf['population'].sum(),
        'population_no_access': no_access['population'].sum(),
        'percentage_no_access': (no_access['population'].sum() / gdf['population'].sum()) * 100,
        'settlements_no_access': len(no_access)
    }
    return stats