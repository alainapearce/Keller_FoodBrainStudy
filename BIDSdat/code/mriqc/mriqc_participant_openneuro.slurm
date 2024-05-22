#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --mem-per-cpu=10GB
#SBATCH --time=4:00:00
#SBATCH --partition=open
#SBATCH --output=%x.%j
#SBATCH --array=1-94
#
#Useage: sbatch mriqc.sh
#
#

#User inputs:
bids_root_dir="/storage/group/klk37/default/R01_Food_Brain_Study/BIDS/"
singularity_dir="/storage/group/klk37/default/sw/"
openneuro_dir="/storage/group/klk37/default/R01_Food_Brain_Study/openneuro/"

# Create an array to store the subs to process
subs=()

# Loop through subfolders in openneuro_dir with begin with sub-
for folder in "$openneuro_dir"sub-*; do
	echo $folder
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

#Make derivative/mriqc/sub-{label} directories
if [ ! -d "$bids_root_dir/derivatives/mriqc_openneuro/sub-${subj}" ]; then
    mkdir -p "$bids_root_dir/derivatives/mriqc_openneuro/sub-${subj}"
else
    echo "output directory exists"
    exit
fi

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
