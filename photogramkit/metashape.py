#!/usr/bin/env python

"""
A Python script to be executed by Agisoft Metashape
"""

import Metashape
import json
import os

def main():
    # get the config file path (assumes the config is in the same directory as this script)
    universal_config_path = os.path.join(os.path.dirname(__file__), "metashape_config.json")
    with open(universal_config_path, 'r') as f:
        config = json.load(f)

    # Load project-specific config
    project_config_path = os.path.join(os.getcwd(), "temp_config.json")
    with open(project_config_path, 'r') as f:
        project_config = json.load(f)

    photo_files = project_config["photo_files"]
    project_name = project_config["project_name"]

    # -- initialize project --
    # get the current project folder from the current working directory (set by build.py)
    current_project = os.getcwd()
    project_path = os.path.join(current_project, f"{project_name}.psz")

    # Open the project specified by project_path
    doc = Metashape.app.document
    # Save initial (empty) project to ensure structure
    # doc.save(project_path)
    chunk = doc.addChunk()

    # -- step1: Add photos to chunk --
    # Find all image files in the folder (common extensions)
    print("********** Step 1/7: Loading photos **********")
    chunk.addPhotos(photo_files)
    print(f"Loaded {len(chunk.cameras)} images")
    # doc.save()

    # -- step2: Apply background mask to all photos --
    print("********** Step 2/7: Importing background mask **********")
    background_path = os.path.join("/Users/yue/Documents/class/25Spring_programming_for_biologists/photogramkit/example-data/", config["background_mask"])
    mask_conf = config["masking"]

    chunk.generateMasks(
        path=background_path,
        masking_mode=getattr(Metashape, mask_conf["method"]),
        mask_operation=getattr(Metashape, mask_conf["operation"]),
        tolerance=mask_conf["tolerance"]
        )
    print("Applied background mask to all images")
    # doc.save()

    # -- step3: Detect coded markers (12-bit circular) --
    print("********** Step 3/7: Detecting markers **********")
    chunk.detectMarkers(
        target_type=getattr(Metashape, config["marker_detection"]["target_type"])
        )
    print("Detected 12-bit circular markers")
    # doc.save()

    # -- step4: Align photos with specified parameters --
    print("********** Step 4/7: Aligning photos **********")
    align_conf = config["photo_alignment"]
    chunk.matchPhotos(
        downscale=align_conf["accuracy_downscale"],
        generic_preselection=align_conf["generic_preselection"],
        reference_preselection=align_conf["reference_preselection"],
        filter_stationary_points=align_conf["filter_stationary_points"],
        keypoint_limit=align_conf["keypoint_limit"],
        tiepoint_limit=align_conf["tiepoint_limit"],
        guided_matching=align_conf["guided_matching"],
        reset_matches=False,
        filter_mask=align_conf["filter_mask"]
    )
    chunk.alignCameras()
    print("Photo matching completed")
    # doc.save()

    # -- step5: Gradual selection: filter tie points by thresholds from config --
    # 1) Reconstruction uncertainty
    # 2) optimize cameras
    # 3) reprojection error
    print("********** Step 5/7: Gradual selection and camera optimization **********")
    recon_thresh = config["gradual_selection"]["reconstruction_uncertainty_threshold"]
    reproj_thresh = config["gradual_selection"]["reprojection_error_threshold"]

    f = Metashape.TiePoints.Filter()
    f.init(chunk, criterion = Metashape.TiePoints.Filter.ReconstructionUncertainty)
    f.removePoints(threshold=recon_thresh)
    print(f"Removed tie points with reconstruction uncertainty > {recon_thresh}")
    # doc.save()

    chunk.optimizeCameras()
    print("Optimized camera parameters")
    # doc.save()

    f.init(chunk, criterion = Metashape.TiePoints.Filter.ReprojectionError)
    f.removePoints(threshold=reproj_thresh)
    print(f"Removed tie points with reprojection error > {reproj_thresh}")
    # doc.save()

    # -- step6: Build mesh --
    print("********** Step 6/7: Building mesh **********")
    mesh_conf = config["mesh_building"]
    chunk.buildDepthMaps(
        downscale=config["depth_maps"]["downscale"],
        filter_mode=getattr(Metashape, config["depth_maps"]["filter_mode"])
    )
    chunk.buildModel(
        source_data=getattr(Metashape, mesh_conf["source_data"]),
        surface_type=getattr(Metashape, mesh_conf["surface_type"]),
        face_count=getattr(Metashape, mesh_conf["face_count"]),
        vertex_colors=mesh_conf["vertex_colors"]
    )
    print(f"Depth maps built (downscale={downscale}, filter={filter_mode_name})")
    # doc.save()

    # -- step7: Build texture --
    print("********** Step 7/7: Building texture **********")
    tex_conf = config["texture_building"]
    chunk.buildUV(mapping_mode=getattr(Metashape, tex_conf["mapping_mode"]))
    chunk.buildTexture(
        blending_mode=getattr(Metashape, tex_conf["blending_mode"]),
        texture_size=tex_conf["texture_size"]
    )
    print("Texture is mapped to the model.")

    # Save project
    doc.save()
    print("Project saved successfully.")


if __name__ == "__main__":
    main()


