#!/bin/tcsh
#usage: ./1_afni_proc

### This script will setup up and apply afni_proc.py to each individual 
###

###################### set up initial variables  ###########################

#go to and set BIDs as main directory
cd ../../../
set bidsdir = $cwd

#set input argument 1 to variable 'parID' and make sure it has leading zeros
set parID = "sub-$1"

# set onset directory
set onsetDir = $bidsdir/derivatives/preprocessed/f31_onsetfiles/

# set subject's fmriprep session 1 directory
set fmriprep_sesDir = $bidsdir/derivatives/preprocessed/fmriprep/${parID}/ses-1/

# set output directory
set outdir = $bidsdir/derivatives/analyses/f31/afniproc

###################### setup and check directories  ###########################

# Things to update:
# input to regress_motion_file -- can this have derivatives, wm, csf?
# input to regress_censor_extern -- should be for F31 analyses

###################### AFNI: afni_proc.py  ###########################
cd $outdir

afni_proc.py -subj_id ${parID} -script proc_${parID}   \
    -blocks blur scale regress                            \
    -dsets ${fmriprep_sesDir}/func/${parID}_ses-1_task-foodcue_run-?_space-MNIPediatricAsym_cohort-3_res-1_desc-preproc_bold.nii.gz                                              \
    -copy_anat ${fmriprep_sesDir}/anat/${parID}_ses-1_desc-preproc_T1w.nii.gz                              \
    -regress_motion_file ${fmriprep_sesDir}/func/${parID}_foodcue-allruns_confounds-noheader.tsv                       \
    -blur_size 6.0                                                                              \
    -regress_stim_times $onsetDir/${parID}*OfficeLarge*.txt               			\
        $onsetDir/${parID}*OfficeSmall*.txt                          		                \
        $onsetDir/${parID}*IBI*.txt                          		                \
    -regress_stim_labels OfficeLarge OfficeSmall Fixation         				\
    -regress_basis_multi 'BLOCK(18,1)' 'BLOCK(18,1)' 'BLOCK(8,1)'                               \
    -regress_censor_extern ${fmriprep_sesDir}/func/${parID}_f31-allruns_censor_rmsd-0.3.1D    \
	-regress_bandpass         0.01 0.1                             				\
    -regress_opts_3dD                                                                           \
        -jobs 2                                                                                 \
    -regress_reml_exec                                                                          \
    -regress_compute_fitts                                                                      \
    -regress_make_ideal_sum sum_ideal.1D                                                        \
    -regress_run_clustsim no