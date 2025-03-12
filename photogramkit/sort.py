#!/usr/bin/env python

"""
A function for sorting photos into folders.

    An example input folder:

    ./photos-sdcards
    ├── 070324
    │   ├── bottom
    │   ├── middle
    │   └── top
    └── 070424
        ├── bottom
        ├── middle
        └── top

    An example output folder:

    ./photos-organized
    ├── 070324
    │   ├── colorprofiles_namelabels
    │   ├── flower1
    │   └── flower2
    ├── 070424
    │   ├── colorprofiles_namelabels
    │   ├── flower1
    │   └── flower2
    └── bug.txt

"""
import argparse
from datetime import datetime, timedelta # convert time strings into timestamps
import glob # to sort CR3 files
import os
import shutil # to copy photos
from exiftool import ExifTool # only need the ExifTool Class within the exiftool package


def parse_command_line():
    "parses args for the module function"

    # init parser and add arguments
    parser = argparse.ArgumentParser()

    # add input folder
    parser.add_argument(
        "--input",
        help="input folder of unorganized photos")

    # add output folder
    parser.add_argument(
        "--output",
        help="output folder of organized photos")

    # parse args
    args = parser.parse_args()

    return args

def extract_time_for_photos_in_one_camera(date_folder, camera):
    """
    extract creation times for all the photos in one *camera folder*.
    suppose your input folder has a structure like this:
    ./photos-sdcards (input_folder)
    ├── 070324 (date_folder)
    │   ├── bottom (camera_folder)
    │   ├── middle (camera_folder)
    │   └── top (camera_folder)
    └── 070424 (date_folder)
        ├── bottom (camera_folder)
        ├── middle (camera_folder)
        └── top (camera_folder)

    Parameters:
        date_folder: a directory of date folder (like the 070324 and 070424 folders above)
        camera: a string of bottom, middle or top

    Outputs:
        timestamps: a list of tuple 
        where in each tuple there are two elements (photo name and timestamp)
    """

    # Get camera folder
    camera_folder = os.path.join(date_folder, camera)

    # Use glob to directly get only .CR3 files, sort photos
    photo_dirs = sorted(glob.glob(os.path.join(camera_folder, "*.CR3")))

    # Initialize a list of tuple (photo_name, timestamp)
    timestamps = []

    # iterate through each photo, extract datetime, 
    # and store the results into a tuple (photo_name, timestamp)
    with ExifTool() as et:
        for photo_dir in photo_dirs:
            # extract meta
            metadata = et.get_metadata(photo_dir)
            dt_orig = metadata.get("EXIF:DateTimeOriginal")
            #subsec_time_origi = metadata.get("EXIF:SubSecTimeOriginal")
            #precise_timestamp = f"{dt_orig}.{subsec_time_origi}"

            # format the precise timestamp
            #precise_formatted = datetime.strptime(precise_timestamp, '%Y:%m:%d %H:%M:%S.%f')
            dt_format = datetime.strptime(dt_orig, '%Y:%m:%d %H:%M:%S')

            # add to the list
            #timestamps.append((os.path.basename(photo_dir),precise_formatted))
            timestamps.append((os.path.basename(photo_dir),dt_format))

    return timestamps


def group_photos_by_timestamp(timestamps, max_time_diff=timedelta(minutes=3)):
    """
    divide photos in the same camera folder into groups based on timestamp.

    Parameters:
        timestamps: a list of tuples from extract_time_for_photos_in_one_camera function.
        max_time_diff: a time

    Outputs:
        groups: a list of lists 
        where each list is a group of images that have time differences smaller than max_time_diff.
                For example:
                    [[img1], [img2, img3], [img4, img5, img6, img7, img8]]

    """

    # create an empty list to store the sorted photos
    groups = []

    # put photos that have similar timestamps into the same group
    current_group = []

    # iterate through each photo
    for idx, (photo, timestamp) in enumerate(timestamps):
        # put the first photo into the first group
        if idx == 0:
            current_group.append(photo)
        # for the rest of the photos, 
        # check timestamp to decide if put this photo into the current group or a new group
        else:
            # get the timestamp of the previous photo
            prev_timestamp = timestamps[idx-1][1]

            # If time difference is within threshold, add to current group
            if timestamp - prev_timestamp <= max_time_diff:
                current_group.append(photo)
            else:
                groups.append(current_group)  # Store completed group
                current_group = [photo]  # Start new group

    # Append the last group if not empty
    if current_group:
        groups.append(current_group)

    return groups


def sort_photos(groups, camera, date_folder, sorted_folder):
    """
    sort photos based on the groups information where assign consecutive small groups (fewer than 6 images)
    to the colorprofile folder and assign consecutive big groups (more than 6 images) to the camera folder.

    Parameters:
        groups: a list of list generated by group_photos_by_timestamp function
        camera: a string of bottom, middle and top
        date_folder: a directory of date folder (like the 070324 and 070424 folders above)
        sorted_folder: a directory of output folder

    Outputs:
        a sorted photo folder. For example:
        ./photos-organized
            ├── 070324
            │   ├── colorprofiles_namelabels
            │   ├── flower1
            │   └── flower2
            ├── 070424
                ├── colorprofiles_namelabels
                ├── flower1
                └── flower2


    """
    # get the number of groups from the last function
    num_groups = len(groups)

    # I want to create a bunch of flower models to store photos from the same flower
    # In each flower model, there are three folders
    # cameras (bottom, middle or top)
    # For each date, there is a color profile folder:
    # which store photos that might contain color profiles or sample labels

    # set flower folder index (flower1, flower2, flower3 for different flowers)
    flower_idx = 1

    # set group index (from 0, 1, 2, to the num_groups)
    group_idx = 0

    # iterate each group in groups
    while group_idx < num_groups:
        # create a new flower folder with its two subfolders
        flower_folder = os.path.join(sorted_folder, f"flower{flower_idx}")
        colorprofiles_folder = os.path.join(sorted_folder, "colorprofiles_namelabels", f"flower{flower_idx}", camera)
        camera_folder = os.path.join(flower_folder, camera)

        # create if not exist
        os.makedirs(colorprofiles_folder, exist_ok=True)
        os.makedirs(camera_folder, exist_ok=True)

        # In each group, assign consecutive small groups (fewer than 6 images) to the colorprofile folder
        group = groups[group_idx]

        if len(group) < 6:
            # copy photo to the colorprofile folder
            for photo in group:
                photo_path = os.path.join(date_folder, camera, photo)
                shutil.copy(photo_path, colorprofiles_folder)

        # if the next group is large (6 or more images), assign it to the camera folder.
        else:
            # copy photo to the camera_folder
            for photo in group:
                photo_path = os.path.join(date_folder, camera, photo)
                shutil.copy(photo_path, camera_folder)

            # move to the next flower
            flower_idx += 1

        # move to the next group
        group_idx += 1


def check_bugs(sorted_folder):

    """
    check bugs. sometimes if the number of consecutive flower images is smaller than 6, the flower images will be
    falsely copied to the colorprofile folder rather than the camera folder. so here after sorting photos, check if each
    flower has three camera folders (bottom, middle, top)

    Parameters:
        sorted_folder: a directory of output directory

    Outputs:
        if there is an error, will write flower ID to the bug.txt which located within the output folder

    """

    # Create or open the bug.txt file to log missing folders
    with open(os.path.join(os.path.dirname(sorted_folder),'bug.txt'), 'a') as bug_file:

        subfolders = os.listdir(sorted_folder)

        # iterate each subfolder
        for subfolder in subfolders:
            subfolder_dir = os.path.join(sorted_folder, subfolder)

            # go to flower folder
            if subfolder.startswith("flower"):
                # Check for the presence of the "top", "middle", and "bottom" cameras
                missing_cameras = []
                required_cameras = ["top", "middle", "bottom"]

                # Check each required camera
                for camera in required_cameras:
                    if not os.path.isdir(os.path.join(subfolder_dir, camera)):
                        missing_cameras.append(camera)

                    # If any required subfolder is missing, log the issue in bug.txt
                    if missing_cameras:
                        bug_file.write(f"{subfolder_dir} is missing: {', '.join(missing_cameras)} camera\n. Please go to species's corresponding colorprofile_namelabels to check.\n")


def main():
    "run main function on parsed args"

    # get arguments from command line as a dict-like object
    args = parse_command_line()

    # get dates
    dates = os.listdir(args.input)

    # define cameras
    cameras = ["bottom", "middle", "top"]

    # iterate each date folders
    for date in dates:
        # get date folder directory
        date_folder = os.path.join(args.input, date)

        # define output directory
        sorted_folder = os.path.join(args.output, date)

        # iterate each camera in each date folder
        for camera in cameras:

            # get timestamps of all the photos in each camera
            timestamps = extract_time_for_photos_in_one_camera(date_folder = date_folder, camera = camera)

            # group photos
            groups = group_photos_by_timestamp(timestamps, max_time_diff=timedelta(minutes=3))

            # sort photos
            sort_photos(groups, camera = camera, date_folder = date_folder,
                        sorted_folder=sorted_folder)


        # check bugs
        check_bugs(sorted_folder)


if __name__ == "__main__":
    main()

