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
    """
    Calculate distance (km) to nearest health facility using BallTree algorithm.
    Earth radius = 6371 km for haversine distance.
    """
    logging.info("Calculating nearest health facilities...")
    
    # Extract coordinates as (lat, lon) and convert to radians
    settlements_coords = np.radians(np.array([(geom.y, geom.x) for geom in settlements_gdf.geometry]))
    facilities_coords = np.radians(np.array([(geom.y, geom.x) for geom in facilities_gdf.geometry]))
    
    # Build BallTree for efficient nearest neighbor search
    tree = BallTree(facilities_coords, metric='haversine')
    
    # Query nearest facility for each settlement
    distances, indices = tree.query(settlements_coords, k=1)
    
    # Convert distances from radians to kilometers
    distances_km = distances.flatten() * 6371
    
    settlements_gdf['distance_to_facility_km'] = distances_km
    settlements_gdf['nearest_facility'] = facilities_gdf.iloc[indices.flatten()]['name'].values
    
    logging.info(f"Distance stats - min: {distances_km.min():.1f}km, "
                f"max: {distances_km.max():.1f}km, mean: {distances_km.mean():.1f}km")
    
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