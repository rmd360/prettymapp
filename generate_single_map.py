#!/usr/bin/env python3
"""Generate a single prettymapp"""

import sys
import os
import matplotlib
matplotlib.use('Agg')

from prettymapp.geo import get_aoi
from prettymapp.osm import get_osm_geometries
from prettymapp.plotting import Plot
from prettymapp.settings import STYLES

def generate_map(location_name, coordinates, radius, style_name):
    print(f"Generating map for {location_name}...")
    print(f"  Coordinates: {coordinates}")
    print(f"  Radius: {radius} meters")
    
    try:
        # Get area of interest
        print("  Getting area of interest...")
        aoi = get_aoi(
            coordinates=coordinates,
            radius=radius,
            rectangular=False
        )
        print(f"  AOI bounds: {aoi.bounds}")
        
        # Get OSM geometries
        print("  Fetching OSM data...")
        df = get_osm_geometries(aoi=aoi)
        print(f"  Found {len(df)} geometries")
        
        # Create plot
        print("  Creating plot...")
        fig = Plot(
            df=df,
            aoi_bounds=aoi.bounds,
            draw_settings=STYLES[style_name],
        ).plot_all()
        
        # Save as PNG
        output_path = f"{location_name}.png"
        print(f"  Saving to {output_path}...")
        fig.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
        
        # Verify file
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / (1024 * 1024)
            print(f"✓ Successfully saved: {output_path} ({file_size:.2f} MB)")
        else:
            print(f"✗ File was not saved: {output_path}")
            return False
        
        # Clean up
        import matplotlib.pyplot as plt
        plt.close(fig)
        return True
        
    except Exception as e:
        print(f"✗ Error generating map for {location_name}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python generate_single_map.py <name> <lat> <lon> <radius>")
        sys.exit(1)
    
    location_name = sys.argv[1]
    lat = float(sys.argv[2])
    lon = float(sys.argv[3])
    radius = int(sys.argv[4])
    
    success = generate_map(location_name, (lat, lon), radius, "Peach")
    sys.exit(0 if success else 1)
