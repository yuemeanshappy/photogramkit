# photogramkit
sort photos from SD cards to folders, and use Agisoft Metashape Pro from command lines to build 3D models.

### Installation
```bash
conda install [list dependencies here...] -c conda-forge ...

git clone  https://github.com/yuemeanshappy/photogram.git
cd ./mini-project
pip install -e .
```

### Example usage
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
