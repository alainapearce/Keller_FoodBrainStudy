#!/bin/bash
#PBS -l nodes=1:ppn=10
#PBS -l walltime=20:00:00
#PBS -j oe
#PBS -M baf44@psu.edu
#PBS -A klk37_b_g_bc_default 

# freesurfer setup
export FREESURFER_HOME=/gpfs/group/klk37/default/sw/freesurfer/6.0.0
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export FS_LICENSE=$FREESURFER_HOME/license.txt

# Set bids directory
bids_dir="/gpfs/group/klk37/default/R01_Food_Brain_Study/BIDS"

# Loop through anatomical scans
for file in "$bids_dir"/raw_data/*/ses-1/anat/*nii*; do

    echo "Processing file: $file"
    
    # Extract the directory path
    dir_path=$(dirname "$file")

    # Extract basename
    file_name=$(basename "$file")
    
    # Assign output name
    output_name="${file_name/_T1w/_T1w-deface}"

    # Deface each file with freesurfer's mideface
    mideface --i "$file" --o "$dir_path/$output_name"

done