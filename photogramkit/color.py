#!/usr/bin/env python

"""
A function for doing photo color calibration
"""

import os
import glob
import subprocess
import argparse


def run_color(input_dir, output_dir, darktable_dir, img_format):
    """
    use darktable-cli to run color calirbation

    Parameters:
        input_dir: photos
        output_dir: color calibrated photos
        color_profile: icc file

    Outputs:
        color calirbated photos
    """
    # create output_dir if not exist
    os.makedirs(output_dir, exist_ok=True)

    # get dates
    dates = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d)) and not d.startswith('.')]

    # iterate each date folders
    for date in dates:
        # get date folder directory
        date_folder = os.path.join(input_dir, date)

        # get color profile directory
        colorprofiles_dir = os.path.join(date_folder, "colorprofiles_namelabels")

        # iterate each flower folders
        # ignore hidden folders (folder.startswith("."))
        # ignore color profile folders (folder != 'colorprofiles_namelabels')
        flowers = [
            folder for folder in os.listdir(date_folder)
            if os.path.isdir(os.path.join(date_folder, folder))
            and not folder.startswith('.')
            and folder != 'colorprofiles_namelabels'
        ]

        for flower in flowers:
            # iterate each camera
            cameras = os.listdir(os.path.join(date_folder,flower))
            for camera in cameras:
                # iterate each photo
                photos_dir = glob.glob(os.path.join(date_folder, flower, camera, f"*.{img_format}"))
                for photo_dir in photos_dir:
                    # get photo name
                    photo_name = os.path.splitext(os.path.basename(photo_dir))[0]
                    # get color calibrated photo directory
                    calibrated_photo_dir = os.path.join(output_dir, date, flower, camera, f"{photo_name}.tiff")
                    # make the direcotry if not exist
                    os.makedirs(os.path.dirname(calibrated_photo_dir), exist_ok=True)

                    # get all DCP files in the color profile folder
                    dcp_files = glob.glob(os.path.join(colorprofiles_dir, flower, camera, "*.dcp"))
                    # check if there is exactly one .dcp file
                    if len(dcp_files) == 1:
                        color_profile_dir = dcp_files[0]  # Get the first (and only) .dcp file

                    # run darktable-cli on mac terminal
                    cmd = [darktable_dir, photo_dir, calibrated_photo_dir, "--icc-file",color_profile_dir]
                    subprocess.run(cmd, check=True)

def parse_command_line():
    "parses args for the module function"

    # init parser and add arguments
    parser = argparse.ArgumentParser()

    # add input folder
    parser.add_argument(
        "-i",
        "--input",
        help="input folder of unorganized photos",
        required = True)

    # add output folder
    parser.add_argument(
        "-o",
        "--output",
        help="output folder of organized photos",
        required = True)

    # add color profile
    # parser.add_argument(
    #    "-p",
    #    "--profile",
    #    help="directory of the color profile (dcp format)",
    #    required = True)

    # add path to darktable-cli
    parser.add_argument(
        "-d",
        "--darktable",
        help="path to the darktable-cli. /Applications/darktable.app/Contents/MacOS/darktable-cli on mac terminal or darktable-cli on Linux system",
        required = True
        )

    # add image format
    parser.add_argument(
        "-f",
        "--format",
        help="image format, can be CR3, JEPG, PNG and TIFF. Default is CR3",
        default = "CR3",
        choices=["CR3", "JPEG", "PNG", "TIFF"],  # restrict to valid options
        required = False)

    # parse args
    args = parser.parse_args()

    return args

def main():
    "run main function on parsed args"

    # get arguments from command line as a dict-like object
    args = parse_command_line()

    # run color calibration
    run_color(input_dir = args.input, output_dir = args.output, darktable_dir = args.darktable, img_format = args.format)

if __name__ == "__main__":
    main()




