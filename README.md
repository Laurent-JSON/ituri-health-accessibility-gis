# 🇨🇩 Ituri Health Accessibility GIS Analysis

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://python.org)
[![GeoPandas](https://img.shields.io/badge/GeoPandas-0.14%2B-green)](https://geopandas.org)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)]()

## Overview

A professional GIS analysis project assessing **health facility accessibility** in Ituri Province, Democratic Republic of Congo, with focus on **Bunia** and surrounding settlements.

### Thematic Focus
**"Mapping Healthcare Deserts in Post-Conflict Regions"**

## Key Findings

| Metric | Value |
|--------|-------|
| Total settlements analyzed | 10 |
| Total population | 342,000 |
| Population without access (15km) | ~78,000 (22.8%) |
| Settlements without health facilities | 6 |

## Project Structure
ituri-health-accessibility-gis/
├── data/raw/
│ └── ituri_settlements.csv # Settlements data (Bunia, Aru, Mahagi, etc.)
├── src/
│ ├── data_loader.py # CSV → GeoDataFrame conversion
│ ├── spatial_analysis.py # Distance calculation with BallTree
│ ├── visualization.py # Map and plot generation
│ └── main.py # Complete analysis pipeline
├── outputs/
│ ├── figures/ # PNG maps and plots
│ └── geojson/ # GIS-ready GeoJSON files
└── README.md


## Installation

```bash
# Clone the repository
git clone https://github.com/Laurent-JSON/ituri-health-accessibility-gis.git
cd ituri-health-accessibility-gis

# Install dependencies
pip install -r requirements.txt

# Run the complete analysis
python src/main.py

Output Examples
Health Access Map
Color-coded map showing:

🟢 Green = Good access (General Hospital nearby)

🟠 Orange = Limited access (Basic clinic only)

🔴 Red = Poor access (No health facility)

Population Analysis
Bar chart showing population distribution by access level.

Data Sources
Settlement	Population	Health Facility	Type
Bunia	120,000	Yes	General Hospital
Aru	45,000	Yes	Referral Center
Mahagi	38,000	Yes	Health Center
Mongbwalu	22,000	Yes	Clinic
Gety	14,000	Yes	Clinic
Irumu	25,000	No	None
Nia Nia	15,000	No	None
Komanda	18,000	No	None
Aveba	8,000	No	None
Boga	12,000	No	None
Data estimates based on Humanitarian OpenStreetMap Team + local sources

Methodology
Data preprocessing - Convert CSV to GeoDataFrame

Access classification - Categorize settlements (Good/Limited/Poor)

Distance analysis - BallTree algorithm for nearest facility calculation (haversine distance)

Population impact - Calculate underserved population percentages

Visualization - Generate maps and statistical plots

Results
Total settlements analyzed: 10
Total population: 342,000
Population without access (15km): 78,000 (22.8%)

Priority settlements for intervention:

Irumu (25,000 people) - 47km from nearest facility

Komanda (18,000 people) - 52km from nearest facility

Nia Nia (15,000 people) - 68km from nearest facility

Technologies
GeoPandas - Spatial operations

Shapely - Geometric objects

Matplotlib - Visualization

Scikit-learn - BallTree algorithm

NumPy - Numerical computations

Next Steps
Integrate OpenStreetMap road network for realistic travel times

Add elevation data for cost surface analysis

Create interactive Folium web map

Add time-series analysis for facility construction

Author
Laurent-JSON

GitHub: @Laurent-JSON

License
MIT License

Built with ❤️ for the Ituri community