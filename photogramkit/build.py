#!/usr/bin/env python

"""
A function for building 3D models using Agisoft Metashape
"""

import os
import subprocess
import argparse
import json
import tempfile
import glob

def run_build(input_dir, output_dir, metashape_dir, metashape_script, img_format):
    """
    run the Agisoft Metashape script using the command line.

    Parameters:
        metashape_script: path to the Python script to be executed by Metashape
    """
    # create output_dir if not exist
    os.makedirs(output_dir, exist_ok=True)

    # get dates
    dates = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d)) and not d.startswith('.')]

    # iterate each date folders
    for date in dates:
        # get date folder directory
        date_folder = os.path.join(input_dir, date)

        # iterate each flower folder
        flowers = os.listdir(date_folder)
        for flower in flowers:
            # get species name, site number, accession number and replicate, to create output directory
            species, site, accession, replicate = flower.split("_")
            # create output dir for the species
            species_dir = os.path.join(output_dir, species)
            os.makedirs(species_dir, exist_ok=True)
            project_name = f"2024_{site}_{accession}_{replicate}"

            # recursivley read all photo files from each camera in each flower
            photo_files = []
            cameras = os.listdir(os.path.join(date_folder, flower))
            for camera in cameras:
                photos_dir = glob.glob(os.path.join(date_folder, flower, camera, f"*.{img_format}"))
                for photo_dir in photos_dir:
                    photo_files.append(photo_dir)

            # create a temporary config file to store the input, output and project name
            temp_config_dir = os.path.join(species_dir, "temp_config.json")
            config_data = {
                "photo_files": photo_files,
                "project_name": project_name
            }
            with open(temp_config_dir, "w") as f:
                json.dump(config_data, f)

            # Change working directory to the project folder
            os.chdir(species_dir)

            # run metashape 
            # use -r option to specify the script
            command = [metashape_dir, "-r", metashape_script]

            try:
                subprocess.run(command, check=True)
                print(f"Metashape script executed successfully.{project_name}")
            except subprocess.CalledProcessError as e:
                print(f"Error running Metashape script: {e}")

            # Delete the temporary config file after use
            if os.path.exists(temp_config_dir):
                os.remove(temp_config_dir)


def parse_command_line():
    "parses args for the module function"

    # init parser and add arguments
    parser = argparse.ArgumentParser()

    # add input color folder
    parser.add_argument("-i", "--input", required=True, help="input color calibrated photo folder")

    # add output 3D model folder
    parser.add_argument("-o", "--output", required=True, help="output 3D model folder")

    # add path to Agisoft Metashape
    parser.add_argument("-m", "--metashape", 
        help="path to the Agisoft Metashape./Applications/MetashapePro.app/Contents/MacOS/MetashapePro on mac terminal or MetashapePro on Linux system",
        required=True)

    # add script
    parser.add_argument(
        "-s",
        "--script",
        help="path to the Python script to be executed by Metashape",
        required = True)

    # add image format
    parser.add_argument(
        "-f",
        "--format",
        help="image format, can be CR3, JEPG, PNG and TIFF. Default is CR3",
        default = "tif",
        choices=["CR3", "JPEG", "PNG", "TIFF"],  # restrict to valid options
        required = False)


    # parse args
    args = parser.parse_args()

    return args

def main():
    "run main function on parsed args"

    # get arguments from command line as a dict-like object
    args = parse_command_line()

    # run build models
    run_build(input_dir=args.input, output_dir=args.output, metashape_dir=args.metashape, metashape_script=args.script, img_format=args.format)

if __name__ == "__main__":
    main()