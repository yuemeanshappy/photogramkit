# Goal of the project:
*Is it clear to you from the proposal how the goal can be accomplished using Python and specific packages?*

This program will allow users to streamline the process of photo sorting, color correcting, and 3D model building in an all-in-one Python package. 
- Use Agisoft Metashape Pro command-line packages 
- Calls on several modules within the Python standard library:
	 `argparse`, `datetime`, `glob`, `os`, `shutil`, and `exiftool`

# Input/Output Data:
*Is it clear to you from the proposal as to what the data for this project is, or will look like?*

The user input data should be (color) photos from an SD card

The user output data will be categorized into three separate program-generated folders:
1. Sorted Photos - organized by taxanomic identity 
2. Color Corrected Photos - adjusted for color
3. Modeled Photos - constructed into 3D models 

# Code:
*based only on what has been written thus far*

- **does current code include a proper skeleton (pseudocode) for starting this project?**

The [README.md](./README.md) contains pseudocode to guide users through dependency installation and repo cloning. It also contains example pseudocode for calling on the program within the command line interface (CLI).

The [__main__.py](./*__main__.py) contains functions that allow the program `photogramkit` to be called on in the CLI. From first glance it appears that the first function within this script generates three empty folders in which the user output data (photos) will later be stored. 

The [sort.py](./*sort.py) contains functions to sort the 'final' photos into their appropriate folders. Photos will be grouped by timestamp using the `group_photos_by_timestamp` function & then moved. 

- **what can this code do so far?**

I had trouble installing program in my terminal and instead recieved an error message saying that the setup.py script was unsuccessfully run. However, this could be because I have to install the correct package dependencies.  

- **given project discription, what are some *individual* functions that could be written to accomplish *parts* of this goal?**

 # Code Contribution/Ideas:








