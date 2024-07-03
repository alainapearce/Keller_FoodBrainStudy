#!/bin/bash
#
#useage: bash proc3_extract.sh     $1             
#		                        ParicipantID
#
# This script extracts timeseries data from ROIs
# Written by Bari Fuchs

###################### set up initial variables  ###########################

#set input argument 1 to variable 'subID' and make sure it has leading zeros

#remove leading zeros if they were included -- trying to add leading zeros to numbers with leading zeros can lead to issues (https://stackoverflow.com/questions/8078167/printf-in-bash-09-and-08-are-invalid-numbers-07-and-06-are-fine)
ID_nozero=$(echo $1 | sed 's/^0*//')

# add leading zeros back
ID=`printf %03d $ID_nozero`
subID="sub-$ID"

###################### setup and check directories  ########################### 

#go to and set BIDS main directory
cd ../../../
bidsdir=$(pwd)
echo "bidsdir is $bidsdir"

#set directories
f31_dir="$bidsdir/derivatives/analyses/f31"
mask_dir="$f31_dir/rois/" #directory with ROI spheres

###################### Extract  ########################### 

## extract timeseries from models with and without GSR
## update for loop for bash, not tsch
# foreach str (gsr nogsr)

#     if ("$str" == "gsr") then
#         set procdir = $f31_dir/afniproc_gsr
#         outdir = $bidsdir/derivatives/analyses/f31/timeseries_gsr
#     else
#         set procdir = $f31_dir/afniproc_nogsr
#         outdir = $bidsdir/derivatives/analyses/f31/timeseries_nogsr
#     endif

    # mask with ROIs with unique value each are stored in derivatives/analyses/f31/rois/rois_mask_diffvalues+tlrc
    # https://www.andysbrainblog.com/andysbrainblog/2017/5/5/extracting-timecourses-with-3dmaskdump

    # https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/tutorials/rois_corr_vis/afni11_roi_cmds.html#calculating-stats-from-separate-rois
    # see Averaging quantities within a mask 

    # need to resample ROIs so they match resolution of func data??

    # use mrange option to extract from each ROI
    # need to output to 1D or txt file ok?
    # https://www.youtube.com/watch?v=H1ZsN88iV6A&t=5s see 4:40
    # https://afni.nimh.nih.gov/afni/community/board/read.php?1,65523,65557#msg-65557 ## input needs to be timeseries dataset (errts)
     #3dmaskave -quiet -mask $bidsdir/derivatives/analyses/f31/rois/rois_mask_diffvalues+tlrc. $TIMESERIES_DATA > output.txt 

procdir="$f31_dir/afniproc_gsr/$subID.results/"
outdir="$f31_dir/timeseries_gsr"
outfile="${subID}_timeseries_gsr.txt"

# make outdir if it doesnt exist
if [ ! -d "$outdir" ]; then
        echo "making outdir"
		mkdir -p "$outdir"
fi

# below did not differentiate between ROIs 
#3dmaskave -quiet -mask $mask_dir/rois_mask_diffvalues+tlrc. $procdir/errts.$subID+tlrc. > $outdir/$outfile

#https://www.brown.edu/carney/mri/researchers/analysis-pipelines/resting-state-fmri#meantimeseries

for roi in l_amyg l_ang l_caudate l_dlpfc l_ifg l_insula l_ofc r_amyg r_ifg r_insula r_mfg r_smarg
#for roi in l_amyg
do 
    mask="$mask_dir/${roi}_roi+tlrc."
    #3dROIstats -mask $mask -1DRformat $procdir/errts.$subID+tlrc > $outdir/${subID}_${roi}.1D
    #3dROIstats -quiet -mask $mask -1DRformat $procdir/errts.$subID+tlrc > $outdir/quiet_${subID}_${roi}.1D
    3dROIstats -quiet -mask $mask $procdir/errts.$subID+tlrc > $outdir/${subID}_${roi}.txt

done
