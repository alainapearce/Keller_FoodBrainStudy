#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Written by Bari Fuchs in Spring 2023

Copyright (C) 2023 Bari Fuchs

     This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
     along with this program.  If not, see <https://www.gnu.org/licenses/>.
     
This script is not guaranteed to work for new data or under new directory 
configurations, however, it should work if no changes are made to directories
or raw data configurations.

@author: baf44
"""

#set up packages    
import numpy as np
import pandas as pd
import os
from pathlib import Path
import re

#########################################################
####                                                 ####
####                  Subfunctions                   ####
####                                                 ####
#########################################################

def _get_censorstr(rmsd_thresh, cen_add_tr):
    """Function to generate string to identify censor criteria 

    Inputs:
        rmsd (float)
        cen_add_tr (string or False)

    Outputs:
        censor_str (str)

    """

    if isinstance(cen_add_tr, str):
        censor_str = 'rmsd-' + str(rmsd_thresh) + '_c-' + str(cen_add_tr)
    elif cen_add_tr is False:
        censor_str = 'rmsd-' + str(rmsd_thresh)

    return(censor_str)

def _gen_concatenated_regressor_file(confound_files):
    """Function to generate 1 regressor file 
    Inputs:
        confound_files (list) - list of counfound files from fmriprep. 1 confound file per run
        
    Outputs:
        RegressPardat (pandas dataframe) - will contain 1 column per regressor variable and (number confound files * length of 1 confound file) rows
    """
    # Make list of variables to regress in Level 1 analyses
    RegressLev1=['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z', 'csf', 'white_matter', 'global_signal', 'trans_x_derivative1', 'trans_y_derivative1', 'trans_z_derivative1', 'rot_x_derivative1', 'rot_y_derivative1', 'rot_z_derivative1']
    
    # create overall regressor dataframe for participant
    RegressPardat = pd.DataFrame(np.zeros((0, len(RegressLev1))))
    RegressPardat.columns = RegressLev1

    confound_files.sort()
    for file in confound_files: #loop through runs (each run has its own confoundfile)

        #load data
        confound_dat_all = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python')

        # add counfound file (i.e., run-specific) regressor data to overall regressor file
        RegressRun = confound_dat_all[RegressLev1].copy()
        RegressPardat = pd.concat([RegressPardat, RegressRun ])

    # for first row [0] of motion derivative variables in regress_Pardat, replace NA with 0. This will allow deriv variables to be entered into AFNI's 3ddeconvolve
    deriv_vars = ['trans_x_derivative1', 'trans_y_derivative1', 'trans_z_derivative1', 'rot_x_derivative1', 'rot_y_derivative1', 'rot_z_derivative1']
    RegressPardat.loc[0, deriv_vars] = RegressPardat.loc[0, deriv_vars].fillna(value=0)

    return(RegressPardat)

def _gen_run_censorfile(confound_dat, rmsd_thresh, cen_add_tr):
    """Function to determine what TRs (i.e., volumes) need to be censored in first-level analyses based on framewise displacement and std_dvars thresholds
    Inputs:
        confound_dat (dataframe) - data from a -desc-confounds_timeseries.tsv file
        rmsd_thresh (float) - rmsd threshold
        cen_add_TR (string)
            'a' in string indicates censor TR *after* TR where rmsd exceeded
            'b' in string indicates censor TR *before* TR where rmsd exceeded
    Outputs:
        censor_info (list) - length equal to number of TRs in input dataset; 
            0 = TR is to be censored, 1 = TR is to be included in analyses
    """

    confound_dat = confound_dat.reset_index()  # make sure indexes pair with number of rows

    # censor TR if: 
    #   (1) First or second TR (datapoints 0 and 1)
    #   (2) rmsd > rmsd_thresh
    #   (3) rmsd on the previous TR > rmsd, if cen_add_TR contains 'a' string
    #   (4) rmsd on the next TR > rmsd, if cen_add_TR contains 'b' string
    #   (5) TR was detected by fmriprep as a steady state outlier
    
    censor_info = []

    for index, row in confound_dat.iterrows():

        # if first or second TR
        if (index < 2):
            censor_info.append(0) # censor TR
        # else if rmsd of current TR > threshold
        elif (row['rmsd'] > rmsd_thresh):
            censor_info.append(0) # censor TR
        # else if rmsd of previous TR > threshold, and 'a' in cen_add_TR (indicates censoring the TR *after* a TR rmsd > rmsd_thresh)
        elif ('a' in cen_add_tr) and (confound_dat.loc[index-1, 'rmsd']) > rmsd_thresh:
            censor_info.append(0) # censor TR
        # else if not final row, and rmsd of next TR > threshold, and 'b' in cen_add_TR (indicates censoring the TR *before* a TR rmsd > rmsd_thresh)
        elif (index != len(confound_dat) - 1) and ('a' in cen_add_tr) and (confound_dat.loc[index+1, 'rmsd']) > rmsd_thresh:
            censor_info.append(0) # censor TR
        # else if steady state outlier
        elif (row['non_steady_state_outlier00'] == 1):
            censor_info.append(0) # censor TR
        else:
            censor_info.append(1) # do not censor TR

    return(censor_info)

 

##############################################################################
####                                                                      ####
####                             Main Function                            ####
####                                                                      ####
##############################################################################

def create_censor_files(par_id, rmsd_thresh=0.3, cen_add_tr='ba', overwrite = False, preproc_path = False):
    """
    This function will process -desc-confounds_timeseries.tsv files (output from fmriprep) for 1 participant in preparation for first-level analyses in AFNI. 
    The following steps will occur:
        (1) output a regressor file containing regressor information for all runs -- will be used by AFNI in first-level analyses
        (2) determine which TRs need to be censored from each run based on input criteria
        (3) output a censor file that indicates which TRs to censor across all runs -- will be used by AFNI in first-level analyses

    Inputs:
        par_id 
        rmsd_thresh (int or float): threshold for rmsd. Default set to .3 according to pre-registration
        cen_add_tr (str): option for censoring TRs before or after TR exceeding movement threshold. Default set to 'ba' according to pre-registration
             'ba' = censor 1 before and 1 after, 'b' = censor 1 before, False = do not censor additional TRs
        overwrite (bool)
        Path (str) - path to direcory that contains fmriprep/ directory.
        
    """

    # set base_directory
    if preproc_path is False:

        # get script location
        script_path = Path(__file__).parent.resolve()

        # change directory to base directory (BIDSdat) and get path
        os.chdir(script_path)
        os.chdir('../..')
        base_directory = Path(os.getcwd())

        #set specific paths
        bids_fmriprep_path = Path(base_directory).joinpath('derivatives/preprocessed/fmriprep')


    elif isinstance(preproc_path, str):
        # make input string a path
        preprocessed_directory = Path(preproc_path)

        #set specific paths
        bids_fmriprep_path = Path(preprocessed_directory).joinpath('fmriprep')

    else: 
        print("preproc_path must be string")
        raise Exception()


    # set sub with leading zeros
    sub = str(par_id).zfill(3)
   
    # get participant confound files
    confound_files = list(Path(bids_fmriprep_path).rglob('sub-' + str(sub) + '/ses-1/func/*task-foodcue_run*confounds_timeseries.tsv'))

    # exit if no participant confound files
    if len(confound_files) > 5:
        print("sub-" + str(sub) + " has more than 5 confound files. Should have 1 per run at most")
        raise Exception()

    if len(confound_files) < 1:
        print("No confound files found for sub-" + str(sub) + ". Unable to generate regressor and censor files")
        raise Exception()

    # check rmsd input
    if isinstance(rmsd_thresh, int) or isinstance(rmsd_thresh, float):
            rmsd_thresh = float(rmsd_thresh)
    else:
        print("rmsd must be integer or float")
        raise Exception()

    # set censor string 
    censor_str = _get_censorstr(rmsd_thresh, cen_add_tr)

    ##############################
    ### Create regressor files ###
    ##############################

    # run function to generate concatenated level-1-regressor dataframe
    regress_Pardat = _gen_concatenated_regressor_file(confound_files)

    # Export participant regressor file with and without columns names
    #regress_Pardat.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'F31_sub-' + sub + '_foodcue-allruns_confounds-noheader.tsv')), sep = '\t', encoding='utf-8-sig', index = False, header=False)
    #regress_Pardat.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'F31_sub-' + sub + '_foodcue-allruns_confounds-header.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

    ###########################
    ### Create censor files ###
    ###########################

    # create empty list for censor data
    censordata_allruns = []

    confound_files.sort()
    for file in confound_files:

        #load data
        confound_dat_all = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python')

        # get run number
        runnum = int(str(file).rsplit('/',1)[-1][31:32])

        # select variables generating censor files
        confound_dat = confound_dat_all[['rmsd']].copy()

        # add non-steady-state outlier column (only exists in confound.tsv files with non-steady-state outliers)
        if 'non_steady_state_outlier00' in confound_dat_all:
            confound_dat['non_steady_state_outlier00'] = confound_dat_all['non_steady_state_outlier00']
        else: 
            confound_dat['non_steady_state_outlier00'] = 0

        # run function to generate run censor data
        run_censordata = _gen_run_censorfile(confound_dat, rmsd_thresh, cen_add_tr)
        
        # add run-specific censor data to overall censor file
        censordata_allruns.extend(run_censordata)
        
    # Export participant censor file (note: afni expects TSV files to have headers -- so export with header=True)
    censordata_allruns_df = pd.DataFrame(censordata_allruns)
    censordata_allruns_df.columns = ['header']
    censordata_allruns_df.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'F31_sub-' + sub + '_foodcue-allruns_censor_' + str(censor_str) + '.tsv')), sep = '\t', encoding='utf-8-sig', index = False, header=True)

    # return particpant databases for integration testing
    return censordata_allruns_df

#if __name__ == "__main__":
#    p2_create_censor_files(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
