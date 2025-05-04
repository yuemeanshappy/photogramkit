# photogramkit: a Toolkit for Photogrammetry-based 3D model construnction

`photogramkit` is a Python package designed to streamline the process of building 3D models in batch, reducing repetitive manual labor.
It automates:
1. **Photo sorting**: organizes photos from SD cards to separate folders for each model based on timestamps.
2. **Photo color calibration**: applies color correction in batch using `darktable-cli` command-line tool.
3. **3D model building**: automates model construction with minial human input using `Agisoft Metashape Pro`.

#### Inputs
- **Unsorted photos** from SD cards (supports `.CR3`, `.DNG`, `.JEPG`, `.PNG`, `.TIFF`)
- **Color profile file** in `.dcp` format

#### Outputs
- **Sorted, color-calibrated photos**
- **3D model projects** in `.psx` format
- **3D mesh files** in `.obj` format or `.ply` format

## Prerequisites
**Required software**
- [Darktable](https://www.darktable.org/install/) (free, for color calibration)
- [Agisoft Metashape Pro](https://www.agisoft.com/downloads/installer/) (commerical, educational license available($549) or 30-day free trial)

**Required Python packages**
- exiftool (0.4.13)
```bash
pip install pyexiftool==0.4.13
```

## Installation
```bash
git clone  https://github.com/yuemeanshappy/photogram.git
cd ./photogramkit
pip install -e .
```

## Example usage
#### 0. check help manual
```bash
# overall help manual
photogramkit -h

# help manual for sorting photos
photogramkit sort -h

# help manual for color calibration
photogramkit color -h

# help manual for model building
photogramkit build -h

# help manual for the full pipeline
photogramkit relax -h
```

#### 1. sort photos
```bash
photogramkit sort -i <input_photo_dir> \
-o <output_photo_dir> \
-f <photo_format> # default is CR3, but can also be set as DNG, TIFF, JPEG, PNG
```
**Example:**
```bash
photogramkit sort -i ./example-data/photos-sdcards -o ./example-data/photos-organized
```
**Before and after sorting**
- [Before sorting](https://tree.nathanfriend.com/?s=(%27options!(%27fancyT~fullPath!false~trailingSlashT~rootDotT)~Y(%27Y%27J070424LKbottom*329V0V1V2V3V4V5V6V7V8w6w7w8w9W0W1W2W3W4k395HLKmiddle*341X2X3X4X5X6X7X8X9B50W7W8W9Q0Q1Q2Q3Q4Q5k406HLJtopj449N0N1N2N3N4N5N6N7N8q5q6q7q8q9x0x1x2x3HLEJO7514H%27)~version!%271%27)*FKO1-HjA%E2%94%80%E2%94%80%20BH*3EZZFL%E2%94%82%C2%A0%C2%A0%20H.CR3J%E2%94%94AK%E2%94%9CAL%5CnEN-45OIMG_QH*40T!trueU-5VB3WB9XB4Ysource!Z%20%20jLEKO7kHFJO1qU0wB8xU1%01xwqkjZYXWVUTQONLKJHFEBA-*)
- [After sorting](https://tree.nathanfriend.com/?s=(%27options!(%27fancy!true~fullPath!false~trailingSlash!true~rootDot!true)~source!(%27source!%27F070424LA-colorprofiles_namelabelsL*-q1L*BX*BBKBBJk29H*BBUk29j*BY*BBKBBJk41H*BBUk41j*Bx*NA%20KNA%20J7449H*NA%20U7449j*Fq2L*AX**K*Jk29H**Uk29j*AY**K*Jk41H**Uk41j*Ax*AAKAAJ7449H*AAU7449jA-q1L*X*BJk32T33T34T35T36T37H*BUk38H*Y*BJk43T44T45T46T47T48T49H*BUk50H*xW1HW2HW3HW4HW5HW6HW7H*AU7458HAFq2LAAXA*Jk86Q387Q388Q389z0z1z2z3z4HA*Uk95HAAYA*Jk97z8z9Q400Q401Q402Q403Q404Q405HA*U1406HAAxAAAJ7505V06V07V08V09V10V11V12VkHAAAU7514.CR3%27)~version!%271%27)*AB-%E2%94%9CZA%20%20%20%20BN%20F%E2%94%94ZH.CR3LJ-IMG_K-Canon%20EOS%20R100.dcpL*L%5CnN%E2%94%82%C2%A0%C2%A0QHA*J1TH*BJkUFIMG_VHAAAJ75W*AJ745X-bottomLY-middleLZ%E2%94%80%E2%94%80%20j.dngLk13qflowerxFtopLzQ39%01zxqkjZYXWVUTQNLKJHFBA-*)


#### 2. color calibrate photos
```bash
photogramkit color -i <input_photo_dir> \
-o <output_photo_dir> \
-d <path_to_darktable-cli> \
-f <photo_format> # default is CR3, but can also be set as DNG, TIFF, JPEG, PNG
```
**Example**
```bash
photogramkit color -i ./example-data/photos-organized \
-o ./example-data/photos-color-calibrated \
-d /Applications/darktable.app/Contents/MacOS/darktable-cli

```

#### 3. build models 
```bash
photogramkit build -i <input_photo_dir> \
-o <output_model_dir> \
-m <path_to_agisoft_metashape>
-s <script_to_run_agisoft_metashape>
-f <photo_format> # default is CR3, but can also be set as DNG, TIFF, JPEG, PNG
```
**Example**
```bash
photogramkit build -i ./example-data/photos-color-calibrated \
-o ./example-data/3d-models/ \
-m /Applications/MetashapePro.app/Contents/MacOS/MetashapePro \
-s ./photogramkit/metashape.py
```

#### 4. run the full pipiline
```bash
photogramkit relax -i <input_photo_dir> \
-s <output_sorted_photos> \
-c <output_color_calibrated_photos> \
-m <output_3D_models> \
--metashape <path_to_agisoft_metashape> \
--script <script_to_run_agisoft_metashape> \
--darktable <path_to_darktable-cli> \
--img_format <photo_format> 
```
**Example**
```bash
photogramkit relax -i ./example-data/photos-sdcards \
-s ./example-data/relax/sort/ \
-c ./example-data/relax/color-calibrated/ \
-m ./example-data/relax/models \
--metashape /Applications/MetashapePro.app/Contents/MacOS/MetashapePro \
--script ./photogramkit/metashape.py \
--darktable /Applications/darktable.app/Contents/MacOS/darktable-cli \
--img_format CR3

```

## Next steps
1. Generalize photo sorting to accommodate different file tree structures
2. Run photo color calibration and model construction in parallel


## Reference
- [darktable-cli manual](https://docs.darktable.org/usermanual/4.0/en/special-topics/program-invocation/darktable-cli/)
- [Agisoft Metashape manual](https://www.agisoft.com/pdf/metashape-pro_2_1_en.pdf)