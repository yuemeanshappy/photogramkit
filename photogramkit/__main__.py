#!/usr/bin/env python

"""
Command line interface to photogramkit
"""

import argparse
import sort
import color
import build
import relax


def parse_command_line():
    "parses args for the module function"

    # init parser and add arguments
    parser = argparse.ArgumentParser()

    # add args to sort photos
    parser.add_argument(
        "--sort",
        help="sort photos into folders",
        action="store_true")

    # add args to do color calibration
    parser.add_argument(
        "--color",
        help="apply color profiles to photos",
        action="store_true")

    # add args to build 3D models
    parser.add_argument(
        "--build",
        help="build 3D models using Agisoft Metashape Pro",
        action="store_true")

    # add args to do everything all at once
    parser.add_argument(
        "--relax",
        help="sort photos, do color calibration and build 3D models. All at once.",
        action="store_true")

    # parse args
    args = parser.parse_args()

    # check that user only entered one action arg
    if sum([args.sort, args.color, args.build, args.relax]) > 1:
        raise SystemExit(
           "only one of 'sort', 'color','build' or 'relax' at a time.")
    return args


def main():
    "run main function on parsed args"

    # get arguments from command line as a dict-like object
    args = parse_command_line()

    # pass argument to call module function
    if args.sort:
        sort()
    elif args.color:
        color()
    elif args.build:
        build()
    elif args.relax:
    	relax()
    else:
    	print("Error. Need to use '--sort', '--color', '--build' or '--relax'")


if __name__ == "__main__":
	main()
