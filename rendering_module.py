import os
import logging
import shutil
import subprocess

def sfm_runner(video_uuid: str, item_id : int):
    source_path = "data/"+video_uuid
    use_gpu = 1
    camera = "OPENCV"
    
    os.makedirs(source_path + "/distorted/sparse", exist_ok=True)
    
    ## Feature extraction
    feat_extracton_cmd = "colmap feature_extractor "\
        "--database_path " + source_path + "/distorted/database.db \
        --image_path " + source_path + "/input \
        --ImageReader.single_camera 1 \
        --ImageReader.camera_model " + camera + " \
        --SiftExtraction.use_gpu " + str(use_gpu)
    exit_code = os.system(feat_extracton_cmd)
    if exit_code != 0:
        logging.error(f"Feature extraction failed with code {exit_code}. Exiting.")
        exit(exit_code)
        
    ## Feature matching
    feat_matching_cmd = "colmap exhaustive_matcher \
        --database_path " + source_path + "/distorted/database.db \
        --SiftMatching.use_gpu " + str(use_gpu)
    exit_code = os.system(feat_matching_cmd)
    if exit_code != 0:
        logging.error(f"Feature matching failed with code {exit_code}. Exiting.")
        exit(exit_code)
        
    ### Bundle adjustment
    # The default Mapper tolerance is unnecessarily large,
    # decreasing it speeds up bundle adjustment step.
    mapper_cmd = ("colmap" + " mapper \
        --database_path " + source_path + "/distorted/database.db \
        --image_path "  + source_path + "/input \
        --output_path "  + source_path + "/distorted/sparse \
        --Mapper.ba_global_function_tolerance=0.000001")
    exit_code = os.system(mapper_cmd)
    if exit_code != 0:
        logging.error(f"Mapper failed with code {exit_code}. Exiting.")
        exit(exit_code)
        
    ### Image undistortion
    ### We need to undistort our images into ideal pinhole intrinsics.
    img_undist_cmd = ("colmap" + " image_undistorter \
    --image_path " + source_path + "/input \
    --input_path " + source_path + "/distorted/sparse/0 \
    --output_path " + source_path + "\
    --output_type COLMAP")
    exit_code = os.system(img_undist_cmd)
    if exit_code != 0:
        logging.error(f"Mapper failed with code {exit_code}. Exiting.")
        exit(exit_code)
        
    files = os.listdir(source_path+"/sparse")
    os.makedirs(source_path+"/sparse/0", exist_ok=True)
    
    for file in files:
        if file == '0':
            continue
        source_file = os.path.join(source_path, "sparse", file)
        destination_file = os.path.join(source_path, "sparse", "0", file)
        shutil.move(source_file, destination_file)
    
    print("Done.")
    
    
    #training
    os.environ["BW_IMPLEMENTATION"] = "1"
    os.environ["BALANCE_THRESHOLD"] = "8"
    os.environ["OAR_JOB_ID"] = video_uuid
    os.environ["ITEM_ID"] = str(item_id)
    
    subprocess.Popen(['sh','run_train.sh'])
    
    # exit_code = os.system("OAR_JOB_ID="+video_uuid+" python -s data/"+video_uuid)
    # if exit_code != 0:
    #     logging.error(f"Mapper failed with code {exit_code}. Exiting.")
    #     exit(exit_code)
    
    
    
if __name__ == "__main__":
    sfm_runner("dkqcnrss")