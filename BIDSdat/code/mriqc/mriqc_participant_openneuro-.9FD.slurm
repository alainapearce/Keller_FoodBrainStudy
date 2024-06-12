#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --mem-per-cpu=10GB
#SBATCH --time=4:00:00
#SBATCH --partition=open
#SBATCH --output=slurm_mriqc_openneuro_%a.out
#SBATCH --array=1-94
#
# Useage: 
### Option A: run mriqc for all subjects in openneuro_dir: sbatch mriqc_participants_openneuro.slurm
### Option B: use input args to specify subjects to run mriqc for (can be 1 or more)
###                  e.g., sbatch mriqc_participants_openneuro.slurm 001 002 003 
###                  e.g., sbatch mriqc_participants_openneuro.slurm 132 


#User inputs:
bids_root_dir="/storage/group/klk37/default/R01_Food_Brain_Study/BIDS/"
singularity_dir="/storage/group/klk37/default/sw/"
openneuro_dir="/storage/group/klk37/default/R01_Food_Brain_Study/openneuro/"
mriqc_code_dir="/storage/group/klk37/default/R01_Food_Brain_Study/BIDS/code/mriqc"

# Define list of subjects to process

# no IDs provided as input
if [ "$#" -eq 0 ]; then

    # Create an array to store the subs to process
    subs=()

    # Loop through subfolders in openneuro_dir with begin with sub-
    for folder in "$openneuro_dir"sub-*; do

        # Extract the string following "sub-" and add it to the array subs
        sub=$(basename "$folder" | sed 's/sub-//')
        subs+=("$sub")

    done

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
echo "SLURM script"
echo "--------------------"
cat "$0"
echo "--------------------"

# Check if subj is blank or out of bounds
if [ -z "$subj" ]; then
    echo "Empty participant ID at index $index."
else

    # check if output already exists
    shopt -s nullglob # Enable nullglob to handle the case where no files match - otherwise, files will contain the non-expanded file sub-${subj}*.html
    files=($bids_root_dir/derivatives/mriqc_openneuro/FD.9/sub-${subj}*.html)

    # if number of html files is greater than 0
    if [ ${#files[@]} -gt 0 ]; then
        echo "MRIQC html files exist. Delete to rerun"
    else 
        #Run MRIQC
        echo ""
        echo "Running MRIQC on participant ${subj}"
        echo ""

        unset PYTHONPATH; singularity run --cleanenv $singularity_dir/mriqc-24.0.0.simg \
        /storage/group/klk37/default/R01_Food_Brain_Study/openneuro $bids_root_dir/derivatives/mriqc_openneuro/FD.9 \
        participant \
        --participant-label ${subj} \
        --fd_thres .9 \
        --float32 \
        --mem_gb 20 \
        --n_procs 10 \
        --omp-nthreads 10
    fi
fi

# Rename the default SLURM output file to custom output file
date=$(date +"%Y-%m-%d")
output_file="$mriqc_code_dir/mriqc.9_${subj}_openneuro_${date}.out"
mv $mriqc_code_dir/slurm_mriqc_openneuro_${SLURM_ARRAY_TASK_ID}.out $output_file

