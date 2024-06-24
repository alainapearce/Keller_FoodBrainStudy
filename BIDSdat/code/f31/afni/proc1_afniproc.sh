#!/bin/tcsh
#usage: ./proc1_afni_proc $1
#                    subject ID (e.g., 001)

### This script will setup up and apply afni_proc.py to each individual 
###

###################### set up initial variables  ###########################

#go to and set BIDs as main directory
cd ../../../
set bidsdir = $cwd

#set input argument 1 to variable 'parID' and make sure it has leading zeros
set parID = "sub-$1"

# set subject's fmriprep session 1 directory
set fmriprep_sesDir = $bidsdir/derivatives/preprocessed/fmriprep/${parID}/ses-1/

# set path to directory with onsets, censor and regressor files
set pythonproc_dir = $bidsdir/derivatives/preprocessed/f31_python_proc/

# set onset directory
set onsetDir = $pythonproc_dir/onsets/


###################### AFNI: afni_proc.py  ###########################

# run afni proc with and without global_signal regressor (gsr)

#foreach str (gsr nogsr)
foreach str (gsr)

    if ("$str" == "gsr") then
        set reg_fil = ${pythonproc_dir}/${parID}_f31nuireg-gsr-noheader.tsv
        set outdir = $bidsdir/derivatives/analyses/f31/afniproc_gsr
    else
        set reg_fil = ${pythonproc_dir}/${parID}_f31nuireg-nogsr-noheader.tsv
        set outdir = $bidsdir/derivatives/analyses/f31/afniproc_nogsr
    endif

    # make outdir if it doesnt exist
    if (! -d "$outdir") then
        mkdir -p "$outdir"
    endif

    # move to output directory
    cd $outdir

    # generate afniproc script
    afni_proc.py -subj_id ${parID} -script proc_${parID}   \
        -blocks blur scale regress                            \
        -dsets ${fmriprep_sesDir}/func/${parID}_ses-1_task-foodcue_run-?_space-MNIPediatricAsym_cohort-3_res-1_desc-preproc_bold.nii.gz                                              \
        -copy_anat ${fmriprep_sesDir}/anat/${parID}_ses-1_desc-preproc_T1w.nii.gz                              \
        -regress_motion_file ${reg_fil}            \
        -blur_size 6.0                                                                              \
        -regress_stim_times $onsetDir/${parID}*OfficeLarge*.txt               			\
            $onsetDir/${parID}*OfficeSmall*.txt                          		                \
            $onsetDir/${parID}*IBI*.txt                          		                \
        -regress_stim_labels OfficeLarge OfficeSmall Fixation         				\
        -regress_basis_multi 'BLOCK(18,1)' 'BLOCK(18,1)' 'BLOCK(8,1)'                               \
        -regress_censor_extern ${pythonproc_dir}/${parID}_f31censor_rmsd-0.3_c-ba.1D    \
        -regress_bandpass         0.01 0.1                             				\
        -regress_opts_3dD                                                                           \
            -jobs 2                                                                                 \
        -regress_no_fitts                                                                      \
        -regress_make_ideal_sum sum_ideal.1D                                                        \
        -regress_run_clustsim no

    # execute script
    tcsh -xef proc_sub-001 |& tee output.proc_sub-001