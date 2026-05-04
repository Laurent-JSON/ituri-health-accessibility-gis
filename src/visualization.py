"""
Visualization module for Ituri health accessibility maps
Author: Your Name
Date: 2026-05-03
"""

import matplotlib.pyplot as plt
import geopandas as gpd
import logging
import os

logging.basicConfig(level=logging.INFO)

def create_health_access_map(gdf, output_path):
    """
    Create professional map showing health access levels.
    Green = Good, Orange = Limited, Red = Poor access.
    """
    logging.info("Creating health access map...")
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    color_map = {
        'Good': '#2ecc71',      # Green
        'Limited': '#f39c12',   # Orange
        'Poor': '#e74c3c'       # Red
    }
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Plot each category
    for category, color in color_map.items():
        subset = gdf[gdf['access_category'] == category]
        if not subset.empty:
            sizes = subset['population'] / 1500
            subset.plot(ax=ax, marker='o', color=color, edgecolor='black',
                       markersize=sizes, alpha=0.8, label=f'{category} Access')
    
    # Add labels for major towns (population > 20k)
    major_towns = gdf[gdf['population'] > 20000]
    for idx, row in major_towns.iterrows():
        ax.annotate(f"{row['name']}\n({row['population']:,})",
                   xy=(row.geometry.x, row.geometry.y),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=9, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    # Add smaller labels for other settlements
    other_towns = gdf[gdf['population'] <= 20000]
    for idx, row in other_towns.iterrows():
        ax.annotate(row['name'],
                   xy=(row.geometry.x, row.geometry.y),
                   xytext=(3, 3), textcoords='offset points',
                   fontsize=7, alpha=0.8)
    
    ax.set_title("Health Facility Accessibility in Ituri Province, DRC\n"
                f"Assessment of {len(gdf)} Settlements | Focus on Bunia Region",
                fontsize=14, fontweight='bold')
    ax.set_xlabel("Longitude", fontsize=11)
    ax.set_ylabel("Latitude", fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='lower right', framealpha=0.9)
    
    # Add bounds around Ituri
    ax.set_xlim(28.4, 31.6)
    ax.set_ylim(1.0, 3.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    logging.info(f"Map saved to {output_path}")
    plt.close()

def create_health_access_map_with_basemap(gdf, output_path):
    """
    Create professional map with basemap showing health access levels.
    Green = Good, Orange = Limited, Red = Poor access.
    """
    import contextily as ctx
    
    logging.info("Creating health access map WITH basemap...")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    color_map = {
        'Good': '#2ecc71',      # Green
        'Limited': '#f39c12',   # Orange
        'Poor': '#e74c3c'       # Red
    }
    
    fig, ax = plt.subplots(figsize=(14, 12))
    
    # Plot each category
    for category, color in color_map.items():
        subset = gdf[gdf['access_category'] == category]
        if not subset.empty:
            sizes = subset['population'] / 1500
            subset.plot(ax=ax, marker='o', color=color, edgecolor='black',
                       markersize=sizes, alpha=0.8, label=f'{category} Access')
    
    # Add labels for ALL settlements
    for idx, row in gdf.iterrows():
        offset = 8 if row['population'] > 20000 else 5
        fontsize = 9 if row['population'] > 20000 else 7
        
        ax.annotate(f"{row['name']}\n({row['population']:,})",
                   xy=(row.geometry.x, row.geometry.y),
                   xytext=(5, offset), textcoords='offset points',
                   fontsize=fontsize, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    # Set map bounds (Ituri region)
    ax.set_xlim(28.4, 31.6)
    ax.set_ylim(1.0, 3.3)
    
    # Add basemap (real map tiles)
    try:
        ctx.add_basemap(ax, crs=gdf.crs, source=ctx.providers.CartoDB.Positron)
        logging.info("Basemap added successfully")
    except Exception as e:
        logging.warning(f"Could not add basemap: {e}")
    
    ax.set_title("Health Facility Accessibility in Ituri Province, DRC (with Basemap)\n"
                f"Assessment of {len(gdf)} Settlements | Focus on Bunia Region",
                fontsize=14, fontweight='bold')
    ax.set_xlabel("Longitude", fontsize=11)
    ax.set_ylabel("Latitude", fontsize=11)
    ax.legend(loc='lower right', framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    logging.info(f"Map with basemap saved to {output_path}")
    plt.close()
    
def create_population_analysis_plot(gdf, output_path):
    """Create bar chart of population by access category"""
    logging.info("Creating population analysis plot...")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    access_pop = gdf.groupby('access_category')['population'].sum()
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    bars = ax.bar(access_pop.index, access_pop.values, color=colors, edgecolor='black')
    
    # Add value labels on bars
    for bar, value in zip(bars, access_pop.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
               f'{value:,}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_title('Population by Health Access Level - Ituri Province', fontsize=12, fontweight='bold')
    ax.set_ylabel('Population', fontsize=10)
    ax.set_xlabel('Access Category', fontsize=10)
    ax.set_ylim(0, access_pop.max() * 1.15)
    
    # Add a subtle grid
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    logging.info(f"Analysis plot saved to {output_path}")
    plt.close()

if __name__ == "__main__":
    print("Visualization module ready")