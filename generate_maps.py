#!/usr/bin/env python3
"""Generate prettymaps for Oxford UK, California USA, and Texas USA"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import gc

from prettymapp.geo import get_aoi
from prettymapp.osm import get_osm_geometries
from prettymapp.plotting import Plot
from prettymapp.settings import STYLES

# Define locations with radius in meters (using coordinates to avoid geocoding delays)
locations = {
    "Oxford_UK": {
        "coordinates": (51.7520, -1.2577),  # Oxford, UK latitude, longitude
        "radius": 1500,
        "style": "Peach"
    },
    "California_USA": {
        "coordinates": (34.0522, -118.2437),  # Los Angeles, California latitude, longitude
        "radius": 15000,
        "style": "Peach"
    },
    "Texas_USA": {
        "coordinates": (32.7767, -96.7970),  # Dallas, Texas latitude, longitude
        "radius": 15000,
        "style": "Peach"
    }
}

# Generate maps
for location_name, config in locations.items():
    print(f"Generating map for {location_name}...")
    
    try:
        # Get area of interest
        aoi = get_aoi(
            coordinates=config["coordinates"],
            radius=config["radius"],
            rectangular=False
        )
        
        # Get OSM geometries
        df = get_osm_geometries(aoi=aoi)
        
        # Create plot
        fig = Plot(
            df=df,
            aoi_bounds=aoi.bounds,
            draw_settings=STYLES[config["style"]],
        ).plot_all()
        
        # Save as PNG
        output_path = f"{location_name}.png"
        fig.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
        print(f"✓ Saved: {output_path}")
        
        # Clean up memory
        del fig, df, aoi
        gc.collect()
        
    except Exception as e:
        print(f"✗ Error generating map for {location_name}: {e}")

print("\nDone! Maps saved as PNG files.")
