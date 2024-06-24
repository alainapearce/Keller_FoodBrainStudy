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

def create_nuiregressor_files(par_id, fmriprep_path, output_path, overwrite = False):
    """
    This function will import -desc-confounds_timeseries.tsv files (output from fmriprep) for a given participant (par_id) and generate 4 files (2 with headers, 2 without) with the following first-level nuisance regressors:
        (1) trans_x, trans_y, trans_z, rot_x, rot_y, rot_z, csf, white_matter, global_signal, trans_x_derivative1, trans_y_derivative1, trans_z_derivative1, rot_x_derivative1, rot_y_derivative1, rot_z_derivative1
        (2) The same as (1), without global_signal

    Inputs:
        par_id 
        fmriprep_path (str) - path to fmriprep/ directory.
        output_path (str) - path to output directory
        overwrite (boolean) - specify if output files should be overwritten (default = False)
        
    """

    ##############################
    ### Check/setup input args ###
    ##############################

    # set sub with leading zeros
    if not par_id:
        print("sub is not defined")
        raise Exception()
    else:
        sub = str(par_id).zfill(3)

    # set fmriprep_path
    if not fmriprep_path:

        print("fmriprep_path must be string")
        raise Exception()

    elif isinstance(fmriprep_path, str):

        # make input string a path
        fmriprep_path = Path(fmriprep_path)

    else: 
        print("preproc_path must be string")
        raise Exception()

    # set output_path
    if not output_path:

        print("output_path must be string")
        raise Exception()

    elif isinstance(output_path, str):

        # make input string a path
        output_path = Path(output_path)

    else: 
        print("output_path must be string")
        raise Exception()
   
    # check overwrite
    if not isinstance(overwrite, bool):
        print("overwrite must be boolean (True or False)")
        raise Exception()


    #############################
    ### Import confound files ###
    #############################

    # get participant confound files
    confound_files = list(Path(fmriprep_path).rglob('sub-' + str(sub) + '/ses-1/func/*task-foodcue_run*confounds_timeseries.tsv'))

    # exit if no participant confound files
    if len(confound_files) > 5:
        print("sub-" + str(sub) + " has more than 5 confound files. Should have 1 per run at most")
        raise Exception()

    if len(confound_files) < 1:
        print("No confound files found for sub-" + str(sub) + ". Unable to generate regressor files")
        raise Exception()


    ##############################
    ### Create regressor files ###
    ##############################

    # run function to generate dataframe with all nuisance regressors
    all_nuireg_dat = _gen_concatenated_regressor_file(confound_files)

    # create version without global_signal
    nuireg_nogsr_dat = all_nuireg_dat.drop(['global_signal'], axis=1)

    # Make directory for export 
    Path(output_path).mkdir(parents=True, exist_ok=True)

    # Define paths for regressor files with and without columns names (header)
    noheader_gsr_filepath = Path(os.path.join(output_path, 'sub-' + sub + '_f31nuireg-gsr-noheader.tsv'))
    header_gsr_filepath = Path(os.path.join(output_path, 'sub-' + sub + '_f31nuireg-gsr-header.tsv'))
    noheader_nogsr_filepath = Path(os.path.join(output_path, 'sub-' + sub + '_f31nuireg-nogsr-noheader.tsv'))
    header_nogsr_filepath = Path(os.path.join(output_path, 'sub-' + sub + '_f31nuireg-nogsr-header.tsv'))

    for filepath in [noheader_gsr_filepath, header_gsr_filepath, noheader_nogsr_filepath, header_nogsr_filepath]:

        # check if file already exists 
        if not filepath.exists() or overwrite is True:

            filename = str(filepath)
            
            if "nogsr" in filename:
                if "noheader" in filename:
                   nuireg_nogsr_dat.to_csv(filename, sep = '\t', encoding='ascii', index = False, header=False)
                else:
                   nuireg_nogsr_dat.to_csv(filename, sep = '\t', encoding='ascii', index = False)
            else:
                if "noheader" in filename:
                    all_nuireg_dat.to_csv(filename, sep = '\t', encoding='ascii', index = False, header=False)
                else:
                    all_nuireg_dat.to_csv(filename, sep = '\t', encoding='ascii', index = False)