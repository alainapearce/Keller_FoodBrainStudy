#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --mem-per-cpu=10GB
#SBATCH --time=4:00:00
#SBATCH --partition=open
#SBATCH --output=%x.%j.out

#User inputs:
bids_root_dir="/storage/group/klk37/default/R01_Food_Brain_Study/BIDS/"
singularity_dir="/storage/group/klk37/default/sw/"
openneuro_dir="/storage/group/klk37/default/R01_Food_Brain_Study/openneuro/"
mriqc_code_dir="/storage/group/klk37/default/R01_Food_Brain_Study/BIDS/code/mriqc"

# echo script contents into slurm output
echo "Subject ${subj}"
echo "SLURM script"
echo "--------------------"
cat "$0"
echo "--------------------"

#Run MRIQC
echo ""
echo "Running MRIQC on group"
echo ""

unset PYTHONPATH; singularity run --cleanenv $singularity_dir/mriqc-24.0.0.simg \
/storage/group/klk37/default/R01_Food_Brain_Study/openneuro $bids_root_dir/derivatives/mriqc_openneuro group \
--float32 \
--mem_gb 20 \
    --n_procs 10 \
    --omp-nthreads 10

unset PYTHONPATH; singularity run --cleanenv $singularity_dir/mriqc-24.0.0.simg \
/storage/group/klk37/default/R01_Food_Brain_Study/openneuro $bids_root_dir/derivatives/mriqc_openneuro/FD.9 group \
--float32 \
--mem_gb 20 \
    --n_procs 10 \
    --omp-nthreads 10