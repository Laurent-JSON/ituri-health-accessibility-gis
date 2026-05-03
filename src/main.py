#!/usr/bin/env python3
"""
Main execution script - Ituri Health Accessibility Analysis
Complete GIS workflow for health facility access assessment

Author: Laurent-JSON
Date: 2026-05-03
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

from data_loader import load_settlements_data, create_geodataframe, save_to_geojson
from spatial_analysis import (classify_health_access, create_facilities_gdf,
                               calculate_nearest_facility, calculate_population_without_access)
from visualization import create_health_access_map, create_population_analysis_plot

def setup_directories():
    """Create necessary output directories"""
    directories = ['outputs/figures', 'outputs/geojson']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✓ Output directories created")

def main():
    print("=" * 60)
    print("🌍 I T U R I   H E A L T H   A C C E S S I B I L I T Y")
    print("=" * 60)
    print("Analyzing health facility access in Ituri Province, DRC")
    print("Focus region: Bunia and surrounding settlements")
    print("=" * 60)
    
    # Setup directories
    setup_directories()
    
    try:
        # Step 1: Load data
        print("\n📂 Step 1: Loading settlements data...")
        raw_data = load_settlements_data("data/raw/ituri_settlements.csv")
        print(f"   → Loaded {len(raw_data)} settlements")
        
        # Step 2: Create GeoDataFrame
        print("\n🗺️ Step 2: Creating GeoDataFrame...")
        gdf = create_geodataframe(raw_data)
        print(f"   → CRS: {gdf.crs}")
        
        # Step 3: Classify health access
        print("\n🏥 Step 3: Classifying health access levels...")
        gdf['access_category'] = gdf.apply(classify_health_access, axis=1)
        
        # Display classification summary
        print("   → Classification results:")
        for category in ['Good', 'Limited', 'Poor']:
            count = len(gdf[gdf['access_category'] == category])
            print(f"      - {category}: {count} settlement(s)")
        
        # Step 4: Extract facilities
        print("\n📍 Step 4: Identifying health facilities...")
        facilities = create_facilities_gdf(gdf)
        print(f"   → {len(facilities)} health facilities identified")
        for idx, row in facilities.iterrows():
            print(f"      - {row['name']}: {row['health_center_type']}")
        
        # Step 5: Calculate distances
        print("\n📏 Step 5: Calculating distances to nearest facility...")
        gdf = calculate_nearest_facility(gdf, facilities)
        print(f"   → Distance range: {gdf['distance_to_facility_km'].min():.1f}km - {gdf['distance_to_facility_km'].max():.1f}km")
        print(f"   → Average distance: {gdf['distance_to_facility_km'].mean():.1f}km")
        
        # Step 6: Population statistics
        print("\n👥 Step 6: Analyzing population without access (15km threshold)...")
        stats = calculate_population_without_access(gdf, threshold_km=15)
        print(f"   → Total population assessed: {stats['total_population']:,}")
        print(f"   → Population WITHOUT access: {stats['population_no_access']:,}")
        print(f"   → Percentage underserved: {stats['percentage_no_access']:.1f}%")
        
        # Step 7: Save GeoJSON
        print("\n💾 Step 7: Saving GeoJSON output...")
        save_to_geojson(gdf, "outputs/geojson/ituri_health_facilities.geojson")
        
        # Step 8: Generate visualizations
        print("\n🎨 Step 8: Generating maps and plots...")
        create_health_access_map(gdf, "outputs/figures/health_access_map.png")
        create_population_analysis_plot(gdf, "outputs/figures/population_analysis.png")
        
        # Final summary
        print("\n" + "=" * 60)
        print("✅ A N A L Y S I S   C O M P L E T E")
        print("=" * 60)
        print("\n📊 Key Findings:")
        print(f"   • Total settlements: {len(gdf)}")
        print(f"   • Total population: {stats['total_population']:,}")
        print(f"   • Population without access (15km): {stats['population_no_access']:,}")
        print(f"   • Percentage underserved: {stats['percentage_no_access']:.1f}%")
        print(f"   • Settlements without health facilities: {stats['settlements_no_access']}")
        
        # Priority settlements
        print("\n⚠️ Priority settlements (no health access):")
        no_access = gdf[gdf['has_health_center'] == 'No']
        for idx, row in no_access.iterrows():
            print(f"   • {row['name']}: {row['population']:,} people - nearest facility: {row['nearest_facility']} ({row['distance_to_facility_km']:.1f}km)")
        
        print("\n" + "=" * 60)
        print("📁 Output files generated:")
        print("   • outputs/figures/health_access_map.png")
        print("   • outputs/figures/population_analysis.png")
        print("   • outputs/geojson/ituri_health_facilities.geojson")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        raise

if __name__ == "__main__":
    main()