#!/bin/tcsh
#
#useage: ./resample masks

# The purpose of this script is to resample appetitve and cerebellum masks that were generated in MarsBars

###################### setup and check directories  ###########################   
#go to and set BIDS main directory
cd ../../../
set bidsdir = "$cwd"
set maskdir = $bidsdir/derivatives/analyses/foodcue-paper2/masks
set tempdir = $bidsdir/derivatives/templates/tpl-MNIPediatricAsym/cohort-3

###################### resample  ########################

3dresample -master $tempdir/tpl-MNIPediatricAsym_cohort-3_res-1_T1w.nii.gz -prefix $maskdir/app_mask_resamp -input $maskdir/appetitive_mask.nii

3dresample -master $tempdir/tpl-MNIPediatricAsym_cohort-3_res-1_T1w.nii.gz -prefix $maskdir/cer_mask_resamp -input $maskdir/cerebellum_aal_mask.nii
