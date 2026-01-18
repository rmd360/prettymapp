#!/usr/bin/env python3
"""Display the generated maps using matplotlib"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# Load and display the maps
maps = {
    'Oxford, UK': 'Oxford_UK.png',
    'California, USA': 'California_USA.png',
    'Texas, USA': 'Texas_USA.png'
}

print("Checking map files...")
for title, filename in maps.items():
    if os.path.exists(filename):
        file_size = os.path.getsize(filename) / (1024 * 1024)
        print(f"✓ Found: {filename} ({file_size:.2f} MB)")
    else:
        print(f"✗ Missing: {filename}")

print("\nCreating combined visualization...")
fig, axes = plt.subplots(1, 3, figsize=(20, 7))
fig.suptitle('Prettymapp Generated Maps', fontsize=20, fontweight='bold')

for idx, (title, filename) in enumerate(maps.items()):
    try:
        img = mpimg.imread(filename)
        axes[idx].imshow(img)
        axes[idx].set_title(title, fontsize=14, fontweight='bold')
        axes[idx].axis('off')
        print(f"✓ Loaded and displayed: {title}")
    except Exception as e:
        print(f"✗ Error loading {title}: {e}")
        axes[idx].text(0.5, 0.5, f'Error loading {filename}', ha='center', va='center')

plt.tight_layout()
output_file = 'all_maps_combined.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight')
file_size = os.path.getsize(output_file) / (1024 * 1024)
print(f"\n✓ Combined map saved as: {output_file} ({file_size:.2f} MB)")
plt.close()

print("Done!")
