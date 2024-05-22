#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --mem-per-cpu=10GB
#SBATCH --time=4:00:00
#SBATCH --partition=open
#SBATCH --output=slurm_mriqc_openneuro_%a.out
#SBATCH --array=1-94
#
#Useage: sbatch mriqc.sh
#
#

#User inputs:
bids_root_dir="/storage/group/klk37/default/R01_Food_Brain_Study/BIDS/"
singularity_dir="/storage/group/klk37/default/sw/"
openneuro_dir="/storage/group/klk37/default/R01_Food_Brain_Study/openneuro/"
mriqc_code_dir="/storage/group/klk37/default/R01_Food_Brain_Study/BIDS/code/mriqc"

# Create an array to store the subs to process
subs=()

# Loop through subfolders in openneuro_dir with begin with sub-
for folder in "$openneuro_dir"sub-*; do
    # Extract the string following "sub-" and add it to the array subs
    sub=$(basename "$folder" | sed 's/sub-//')
    subs+=("$sub")
done

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

# dont run if html output files exist
files=($bids_root_dir/derivatives/mriqc_openneuro/$sub*.html)

# if there are html files
if [ ${#files[@]} -gt 0 ]; then
    echo "MRIQC html files exist. Delete to rerun"
else

    #Run MRIQC
    echo ""
    echo "Running MRIQC on participant ${subj}"
    echo ""

    unset PYTHONPATH; singularity run --cleanenv $singularity_dir/mriqc-24.0.0.simg \
    /storage/group/klk37/default/R01_Food_Brain_Study/openneuro $bids_root_dir/derivatives/mriqc_openneuro \
    participant \
    --participant-label ${subj} \
    --float32 \
    --mem_gb 20 \
    --n_procs 10 \
    --omp-nthreads 10

fi

# Rename the default SLURM output file to custom output file
date=$(date +"%Y-%m-%d")
output_file="$mriqc_code_dir/mriqc_${subj}_openneuro_${date}.out"
mv $mriqc_code_dir/slurm_mriqc_openneuro_${SLURM_ARRAY_TASK_ID}.out $output_file

