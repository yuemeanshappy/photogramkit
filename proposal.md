# photogramkit
## What task/goal will the project accomplish and why is this useful?
The goal for photogramkit is to streamline the process of building 3D models in batch. It helps reduce the manual effort required for organizing photos, saves time for users building multiple models (>10 models), and provides a user-friendly interface to integrate different software tools, minimizing the learning curve.


## What type of data/input will a user provide to the program?
Photos (can be in any format) from one to multiple SD cards/cameras.

## Where will the data come from?
Photos will be provided by the user.

## How will a user interact with the program?
```bash
# sort photos from three SD cards into folders
photogramkit --sort <input_photo_dir> <output_photo_dir> [--n <number_of_sd_cards>] [--l <species_name_list>]

# color calibrate photos
photogramkit --color <input_photo_dir> <output_photo_dir> <---icc-file <color_profile_dir>>

# build models
photogramkit --build <input_photo_dir> <output_model_dir> [--p <parameter_file>]

# sort photos, do color calibration and build models all at once
photogramkit --relax <input_photo_dir> <output_model_dir> <--icc-file <color_profile_dir>> [-p <parameter_file_for_building_3D_models>]


```

## What type of output will the program produce (e.g., text, plots)?
The program will generate the following outputs:
- Sorted photos: Each species' photos will be organized into folders for 3D model building.
- Color calibrated photos: Images adjusted for accurate color representation.
- 3D models: Final reconstructed models from the processed photos.


## What other tools currently exist to do this task, or something similar?
Existing tools include color calibration software (e.g., Lightroom, Darktable) and 3D model-building programs (e.g., Agisoft Metashape, COLMAP). Some tools also allow batch processing via command-line interface. However, to the best of my knowledge, no tool integrates photo sorting, color calibration, and 3D model building into a streamlined batch-processing workflow.







