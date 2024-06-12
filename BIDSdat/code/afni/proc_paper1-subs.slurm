#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
#SBATCH --mem-per-cpu=10GB
#SBATCH --time=24:00:00
#SBATCH --account=klk37
#SBATCH --partition=sla-prio 
#SBATCH --output=%x.%j
#
#Useage: sbatch proc_paper1-subs.slurm
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

# make array of subs to process
declare -a subs=(001 002 003 004 005 011 017 020 021 022 023 026 028 030 031 033 036 037 039 040 041 043 045 047 048 049 051 054 055 056 058 069 070 071 073 074 075 078 080 083 084 089 090 094 095 096 101 103 104 109 110 111 116 118 120 121 126 128 129 131 132 133)

# loop through subs
for sub in "${subs[@]}"; do


	#write to output file
	echo "## sub_${sub} paper1_afni-wrapper was run on ${today}"
	echo "## Job started: `date`"


	#Load afni singularity and run afniscript
	cd $topdir/code/afni/sub-${sub}
	singularity exec /storage/group/klk37/default/sw/AFNI.simg bash sub-${sub}_paper1_wrapper-afni

done
