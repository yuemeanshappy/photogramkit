#!/usr/bin/env python

"""
A function for automatically doing photo sorting, color calibration and model buildings 
"""
from photogramkit import sort
from photogramkit import color
from photogramkit import build

def run_relax(input_raw, output_sort, output_color, output_model, metashape, script, darktable, img_format):
    print("Starting full relax pipeline...")

    # 1. Sort
    print("Step 1/3: Sorting photos...")
    sort.run_sort(input_raw, output_sort, img_format)

    # Pause for user to generate color profiles
    input("\n✅ Photo sorting complete. Please generate color profiles now. Type 'ok' and press Enter to continue... ")

    # 2. Color
    print("Step 2/3: Applying color calibration...")
    color.run_color(output_sort, output_color, darktable, img_format)

    # 3. Build
    print("Step 3/3: Building 3D models...")
    build.run_build(output_color, output_model, metashape, script, img_format="tif")

    print("Relax pipeline completed successfully!")
