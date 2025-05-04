#!/usr/bin/env python

"""
Command line interface to photogramkit
"""

import argparse
from photogramkit import sort
from photogramkit import color
from photogramkit import build
from photogramkit import relax


def parse_command_line():
    "parses args for the module function"

    # init parser and add arguments
    parser = argparse.ArgumentParser()

    # create subparsers
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 'sort' subcommand
    sort_parser = subparsers.add_parser("sort", help="sort photos into folders")
    sort_parser.add_argument("-i", "--input", required=True, help="input folder")
    sort_parser.add_argument("-o", "--output", required=True, help="output folder")
    sort_parser.add_argument("-f",
        "--format",
        help="image format, can be CR3, JEPG, PNG and TIFF. Default is CR3",
        default = "CR3",
        choices=["CR3", "JPEG", "PNG", "TIFF", "DNG"],  # restrict to valid options
        required = False)

    # 'color' subcommand
    color_parser = subparsers.add_parser("color", help="apply color profiles to photos")
    color_parser.add_argument("-i", "--input", required=True, help="input folder")
    color_parser.add_argument("-o", "--output", required=True, help="output folder")
    color_parser.add_argument("-d","--darktable", 
        help="path to the darktable-cli. /Applications/darktable.app/Contents/MacOS/darktable-cli on mac terminal or darktable-cli on Linux system",
        required = True)
    color_parser.add_argument("-f",
        "--format",
        help="image format, can be CR3, JEPG, PNG and TIFF. Default is CR3",
        default = "CR3",
        choices=["CR3", "JPEG", "PNG", "TIFF"],  # restrict to valid options
        required = False)

    # 'build' subcommand
    build_parser = subparsers.add_parser("build", help="build 3D models using Agisoft Metashape Pro")
    build_parser.add_argument("-i", "--input", required=True, help="input color calibrated photo folder")
    build_parser.add_argument("-o", "--output", required=True, help="output 3D model folder")
    build_parser.add_argument("-m", "--metashape", 
        required=True, 
        help="path to the Agisoft Metashape./Applications/MetashapePro.app/Contents/MacOS/MetashapePro on mac terminal or MetashapePro on Linux system")
    build_parser.add_argument("-s", "--script", required=True, help="the path to the Python script to be executed by Metashape")
    build_parser.add_argument(
        "-f",
        "--format",
        help="image format, can be CR3, JEPG, PNG and TIFF. Default is CR3",
        default = "tif",
        choices=["CR3", "JPEG", "PNG", "TIFF"],  # restrict to valid options
        required = False)

    # 'relax' subcommand
    relax_parser = subparsers.add_parser("relax", help="do everything: sort, color, and build")
    relax_parser.add_argument("-i", "--input_raw", required=True, help="input raw photo folder (for sorting)")
    relax_parser.add_argument("-s", "--output_sort", required=True, help="output sorted folder (for color step)")
    relax_parser.add_argument("-c", "--output_color", required=True, help="output color calibrated folder (for build step)")
    relax_parser.add_argument("-m", "--output_model", required=True, help="output 3D model folder")
    relax_parser.add_argument("--metashape", required=True, help="path to Agisoft Metashape app")
    relax_parser.add_argument("--script", required=True, help="path to the Python script to be executed by Metashape")
    relax_parser.add_argument("--darktable", required=True, help="path to darktable-cli for color step")
    relax_parser.add_argument("--img_format", help="image format, can be CR3, JEPG, PNG and TIFF. Default is CR3",
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

    # pass argument to call module function
    if args.command == "sort":
        sort.run_sort(args.input, args.output, args.format)
    elif args.command == "color":
        color.run_color(args.input, args.output, args.format)
    elif args.command == "build":
        build.run_build(args.input, args.output, args.metashape, args.script, args.format)
    elif args.command == "relax":
        relax.run_relax(args.input_raw, args.output_sort, args.output_color, args.output_model, args.metashape, args.script, args.darktable, args.img_format)


if __name__ == "__main__":
	main()
