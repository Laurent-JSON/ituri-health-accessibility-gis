"""
Data loader module for Ituri health accessibility analysis
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import logging

logging.basicConfig(level=logging.INFO)

def load_settlements_data(filepath):
    df = pd.read_csv(filepath)
    logging.info(f"Loaded {len(df)} settlements")
    return df

def create_geodataframe(df, lat_col='lat', lon_col='lon', crs='EPSG:4326'):
    geometry = [Point(x, y) for x, y in zip(df[lon_col], df[lat_col])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=crs)
    return gdf

def save_to_geojson(gdf, output_path):
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    gdf.to_file(output_path, driver='GeoJSON')
    logging.info(f"Saved GeoJSON to {output_path}")