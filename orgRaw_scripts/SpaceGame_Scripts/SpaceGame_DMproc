#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l pmem=2gb
#PBS -l walltime=20:00:00
#PBS -A klk37_a_g_bc_default
#PBS -j oe
#
#Useage: ./SpaceGame_DMproc
#
#
######## SpaceGame Decision Making ACI script ########
#
#The purpose of this script is to run the
#matlab script mfit_wrapper_PearceF32.m
#which runs Kool et al.'s decision making
#model:

######## Set up script/cluster variables  ########
#load needed modules
module load matlab/R2017b
  
#set top/base directory
topdir="/gpfs/group/klk37/default/F32_SpaceGame/"
 
######## Set up output preamble ########
#date
today=`date +%m-%d-%y`

#write to output file
echo "##Group analyses was processed on ${today}"
echo "## Job started: `date`"

echo ""
cd $topdir/SpaceGame_Scripts/Kool2016_Model/
matlab -nodisplay -nosplash -r "mfit_wrapper_PearceF32_aci"
echo ""

echo "## Job Ended: `date`"

