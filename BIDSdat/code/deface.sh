#!/bin/bash


## Notes: pydeface is installed in a conda environemnt pydeface_env. to activate, run:
##	>> conda activate pydeface_env
## pydeface requires fsl. to load, run:
##	>> module load fsl

# Set bids directory
bids_dir="/gpfs/group/klk37/default/R01_Food_Brain_Study/BIDS"

# Loop through anatomical scans
for anat_dir in "$bids_dir"/raw_data/*/ses-1/anat/; do

# for testing
#for anat_dir in "$bids_dir"/raw_data/sub-005/ses-1/anat/; do

	# check if defaced nii already exists
	if [ -e "$anat_dir"*defaced* ]; then
		echo "Defaced nii already exists in "$anat_dir". skipping"
	else
		echo "Calling pydeface"
		pydeface "$anat_dir"*nii*
	fi
done
