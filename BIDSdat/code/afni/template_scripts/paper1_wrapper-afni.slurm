#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --mem=12GB
#SBATCH --time=24:00:00
#SBATCH --account=klk37
#SBATCH --partition=sla-prio 
#SBATCH --output=%x.%j
#
#Useage: sbatch paper1_wrapper-afni.slurm


######## Set up inital variables ########

#don't log AFNI programs in ~/.afni.log
AFNI_DONT_LOGFILE="YES"

#dont try version checks
ANFI_VRSION_CHECK="NO"

##don't auto-compress output files
AFNI_COMPRESSOR="NONE"

#set number of processors for AFNI to match the number of cores
# see https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dTfitter.html
OMP_NUM_THREADS="10"

#date
today=`date +%m-%d-%y`

#set top/base directory
topdir="/storage/group/klk37/default/R01_Food_Brain_Study/BIDS/"


#write to output file
echo "## sub_PARNUM_paper1_wrapper-afni was run on ${today}"
echo "## Job started: `date`"


#Load afni singularity and run afniscript
cd $topdir/code/afni/sub-PARNUM
singularity exec /storage/group/klk37/default/sw/AFNI.simg bash sub-PARNUM_paper1_wrapper-afni
