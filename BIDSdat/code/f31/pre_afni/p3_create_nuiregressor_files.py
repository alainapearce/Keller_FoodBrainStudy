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
        confound_dat_all = pd.read_csv(str(file), sep = '\t', encoding = 'ascii', engine='python')

        # add counfound file (i.e., run-specific) regressor data to overall regressor file
        RegressRun = confound_dat_all[RegressLev1].copy()
        RegressPardat = pd.concat([RegressPardat, RegressRun ])

    # for first row [0] of motion derivative variables in regress_Pardat, replace NA with 0. This will allow deriv variables to be entered into AFNI's 3ddeconvolve
    deriv_vars = ['trans_x_derivative1', 'trans_y_derivative1', 'trans_z_derivative1', 'rot_x_derivative1', 'rot_y_derivative1', 'rot_z_derivative1']
    RegressPardat.loc[0, deriv_vars] = RegressPardat.loc[0, deriv_vars].fillna(value=0)

    return(RegressPardat)


 

##############################################################################
####                                                                      ####
####                             Main Function                            ####
####                                                                      ####
##############################################################################

def create_nuiregressor_files(par_id, overwrite = False, preproc_path = False):
    """
    This function will process -desc-confounds_timeseries.tsv files (output from fmriprep) for 1 participant in preparation for first-level analyses in AFNI. 
    The following steps will occur:
        (1) output a regressor file containing regressor information for all runs -- will be used by AFNI in first-level analyses

    Inputs:
        par_id 
        overwrite (bool)
        Path (str) - path to direcory that contains fmriprep/ directory.
        
    """

    # set bids_directory
    if preproc_path is False:

        # get script location
        script_path = Path(__file__).parent.resolve()

        # change directory to base directory (BIDSdat) and get path
        os.chdir(script_path)
        os.chdir('../../..')
        bids_directory = Path(os.getcwd())

        #set specific paths
        bids_fmriprep_path = Path(bids_directory).joinpath('derivatives/preprocessed/fmriprep')


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


    ##############################
    ### Create regressor files ###
    ##############################

    # run function to generate dataframe with all nuisance regressors
    regress_Pardat = _gen_concatenated_regressor_file(confound_files)

    # Export participant regressor file with and without columns names
    regress_Pardat.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'sub-' + sub + '_f31-allruns_confounds-noheader.tsv')), sep = '\t', encoding='ascii', index = False, header=False)
    regress_Pardat.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'sub-' + sub + '_f31-allruns_confounds-header.tsv')), sep = '\t', encoding='ascii', index = False)
