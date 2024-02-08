#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --mem-per-cpu=20GB
#SBATCH --time=48:00:00
#SBATCH --partition=open
#SBATCH --output=%x.%j
#
#Useage: sbatch sensitivity_G4_1sampleT_FMI.slurm
#
#


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
echo "## sensitivity_G4_1sampleT_FMI was run on ${today}"
echo "## Job started: `date`"


#Load afni singularity and run afniscript
cd $topdir/code/afni/groupanalyses_paper1
singularity exec /storage/group/klk37/default/sw/AFNI.simg tcsh sensitivity_G4_1sampleT_FMI Ped run fd-0.9_b20_3runs_noGSR
