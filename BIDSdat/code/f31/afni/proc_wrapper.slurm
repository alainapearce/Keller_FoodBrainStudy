#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --mem-per-cpu=10GB
#SBATCH --time=4:00:00
#SBATCH --partition=open
#SBATCH --output=slurm_wrapper_%a.out
#SBATCH --array=1-94
#
# Useage: 
### Option A: run wrapper for all subjects in XXXX: sbatch proc_wrapper.slurm
### Option B: use input args to specify subjects to run proc_wrapper for (can specify 1 or more)
###                  e.g., sbatch proc_wrapper.slurm 001 002 003 
###                  e.g., sbatch proc_wrapper.slurm 132 


#User inputs:
bids_root_dir="/storage/group/klk37/default/R01_Food_Brain_Study/BIDS/"
rawdata_dir="$bids_root_dir/raw_data/"
singularity_dir="/storage/group/klk37/default/sw/"
wrapper_code_dir="$bids_root_dir/code/f31/afni/"

# Define list of subjects to process

# if no IDs provided as input
if [ "$#" -eq 0 ]; then

    # Create an array to store the subs to process
    subs=()

    # Loop through subfolders in rawdata_dir that with begin with sub-
    for folder in "$rawdata_dir"sub-*; do

        # Extract the string following "sub-" and add it to the array subs
        sub=$(basename "$folder" | sed 's/sub-//')
        subs+=("$sub")

    done

# if IDs provided as input
else 
    # assign input args to subs 
    subs=("$@")
fi

# Get the index of the current task
index=$(($SLURM_ARRAY_TASK_ID - 1))

# Get the participant ID for the current task
subj=${subs[$index]}

# echo script contents into slurm output
echo "Subject ${subj}"
echo "Wrapper script"
echo "--------------------"
cat "$0"
echo "--------------------"

# Check if subj is blank or out of bounds
if [ -z "$subj" ]; then
    echo "Empty participant ID at index $index."
else

	#Load afni singularity and run processing scripts
	singularity exec $singularity_dir/AFNI.simg tcsh $wrapper_code_dir/proc1_afniproc.sh "$subj"
    #singularity exec $singularity_dir/AFNI.simg bash $wrapper_code_dir/proc2_check_roi_coverage.sh "$subj"
	#singularity exec $singularity_dir/AFNI.simg bash $wrapper_code_dir/proc3_extract.sh "$subj"

fi

# Rename the default SLURM output file to custom output file
date=$(date +"%Y-%m-%d")
output_file="$wrapper_code_dir/wrapper_${subj}_${date}.out"
mv $wrapper_code_dir/slurm_wrapper_${SLURM_ARRAY_TASK_ID}.out $output_file

