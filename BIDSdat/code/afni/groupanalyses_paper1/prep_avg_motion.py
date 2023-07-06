#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This function was created to calculate the average framewise displacement for a subject

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
from cmath import nan
import pandas as pd
import os
from pathlib import Path
import numpy as np


def _get_summary_files(bids_fmriprep_path, sub, overwrite):
    """Function to import or generate framewisedisplacement_summary files. 
        If subject is already in censorsummary database and Overwrite = False, exception will be raised. 
        If subject is already in censorsummary database and Overwrite != False, subject will be removed from summary database.

    Inputs:
        fMRIpreppath (list) - path to import file from
        sub (str) - subject ID
        overwrite (bool) - True or False for overwriting subject data in censor summary files
        
    Outputs:
        RegressPardat (pandas dataframe) - will contain 1 column per regressor variable and (number confound files * length of 1 confound file) rows
    """

    # Set paths to summary file
    fd_summary_path = Path(bids_fmriprep_path).joinpath( str('task-foodcue_avg-fd.tsv'))

    ### Manage censor_summary_path ###
    if fd_summary_path.is_file(): # if database exists

        # import database
        fd_summary_allPar = pd.read_csv(str(fd_summary_path), sep = '\t')

        # convert int to string, then add leading zeros
        fd_summary_allPar['id'] = fd_summary_allPar['id'].astype(str).str.zfill(3)

        # check to see if subject already in database
        if (sub in set(fd_summary_allPar['id'])):
            if overwrite is False:
                print("sub_" + sub + " already in task-foodcue_avg-fd.csv -- Use overwrite = True to rerun")
                raise Exception()
            
            if overwrite is True: #overwrite is true
                # remove subject rows from censor_summary_byrun_path
                print("overwriting for sub_" + sub)
                fd_summary_allPar = fd_summary_allPar[fd_summary_allPar['id'] != sub]

        else:
            print("avg motion for sub_" + sub + " not in task-foodcue_avg-fd.csv -- Calculating...")

    # if database does not exist
    else:
        # create new dataframe 
        fd_summary_allPar = pd.DataFrame(np.zeros((0, 12)))
        fd_summary_allPar.columns = ['id','fd_avg_allruns','fd_avg_run1','fd_avg_run2','fd_avg_run3','fd_avg_run4','fd_avg_run5',
                                            'fd_max_run1', 'fd_max_run2', 'fd_max_run3', 'fd_max_run4', 'fd_max_run5']

    nrow_postfunc = fd_summary_allPar.shape[0]

    return(fd_summary_allPar)



def _compute_avg_fd_allruns(confound_files):
    """Function to compute the average framewise displacement across all TRs in all runs
    Inputs:
        confound_files (list) - list of counfound files from fmriprep. 1 confound file per run
        
    Outputs:
        avg_fd (float)
    """    
    # create dataframe to concatenate values across runs  
    allruns_fd_df = pd.DataFrame(np.zeros((0, 1)))
    allruns_fd_df.columns = ['framewise_displacement']

    # create dictionary to store average values in
    avg_fd = {'all': nan, 1: nan, 2:nan, 3:nan, 4:nan, 5:nan}
    max_fd = {1: nan, 2:nan, 3:nan, 4:nan, 5:nan}

    # extract framewise displacement values from each run
    confound_files.sort()
    for file in confound_files: #loop through runs (each run has its own confoundfile)

        # get run number
        runnum = int(str(file).rsplit('/',1)[-1][31:32])

        #load data
        confound_dat_all = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python')

        # extract framewise_displacement column
        fd_run = pd.DataFrame(confound_dat_all['framewise_displacement'].copy())

        # compute average fd for run and add to dictionary
        run_avg_fd = fd_run["framewise_displacement"].mean()
        avg_fd[runnum] = round(run_avg_fd, 2)

        # get max fd for run and add to dictionary
        run_max_fd = fd_run["framewise_displacement"].max()
        max_fd[runnum] = round(run_max_fd, 2)

        # add run-specific data to overall dataframe
        allruns_fd_df = allruns_fd_df.append(fd_run)

    # get average fd across all runs and add to dictionary
    avg_fd_allruns = allruns_fd_df["framewise_displacement"].mean()
    avg_fd['all'] = round(avg_fd_allruns, 2)

    return avg_fd, max_fd


def _compute_avg_fd_includedruns(confound_files, runlist):
     """Function to compute the average framewise displacement across all TRs in runs included in analyses
    Inputs:
        confound_files (list) - list of counfound files from fmriprep. 1 confound file per run
        
    Outputs:
        avg_fd (float)
    """

##############################################################################
####                                                                      ####
####                             Main Function                            ####
####                                                                      ####
##############################################################################

def get_avg_fd(par_id, overwrite = False, preproc_path = False):

    """Function to generate onset files that censor blocks with excessive motion based on specified threshold
    Inputs:
        par_id (int): participant ID 
        censorsumfile (string): name of censor summary file (e.g., task-foodcue_byblock-censorsummary_fd-1.0.tsv
        overwrite =
        preproc_path
    Outputs:

    """

    # set base_directory
    if preproc_path is False:

        # get script location
        script_path = Path(__file__).parent.resolve()

        # change directory to base directory (BIDSdat) and get path
        os.chdir(script_path)
        os.chdir('../../..')
        base_directory = Path(os.getcwd())

        #set specific paths
        bids_onset_path = Path(base_directory).joinpath('derivatives/preprocessed/foodcue_onsetfiles')
        bids_fmriprep_path = Path(base_directory).joinpath('derivatives/preprocessed/fmriprep')


    elif isinstance(preproc_path, str):
        # make input string a path
        preprocessed_directory = Path(preproc_path)

        #set specific paths
        bids_onset_path = Path(preprocessed_directory).joinpath('foodcue_onsetfiles')
        bids_fmriprep_path = Path(preprocessed_directory).joinpath('fmriprep')

    else: 
        print("preproc_path must be string")
        raise Exception()

    # set sub with leading zeros
    sub = str(par_id).zfill(3)

    # import or generate framewise displacement summary dataframe
    fd_summary_allPar = _get_summary_files(bids_fmriprep_path, sub, overwrite)

    # get participant confound and onset files
    confound_files = list(Path(bids_fmriprep_path).rglob('sub-' + str(sub) + '/ses-1/func/*task-foodcue_run*confounds_timeseries.tsv'))

    # exit if no participant confound files or onset files
    if len(confound_files) < 1:
        print("No confound files found for sub-" + str(sub) + ". Unable to calculate average framewise displacement")
        raise Exception()

    # compute average framewise displacement across all runs
    avg_fd, max_fd = _compute_avg_fd_allruns(confound_files)

    # make dataframe row of participant data to add to fd_summary_allPar
    row_append = pd.DataFrame(data=[sub, avg_fd['all'], avg_fd[1], avg_fd[2], avg_fd[3], avg_fd[4], avg_fd[5], max_fd[1], max_fd[2], max_fd[3], max_fd[4], max_fd[5]]).T
    row_append.columns = ['id','fd_avg_allruns','fd_avg_run1','fd_avg_run2','fd_avg_run3','fd_avg_run4','fd_avg_run5',
                                            'fd_max_run1', 'fd_max_run2', 'fd_max_run3', 'fd_max_run4', 'fd_max_run5']
    
    # add particpant data to fd_summary_allPar
    fd_summary_allPar = pd.concat([fd_summary_allPar, row_append])

    #Export summary dataframe
    fd_summary_allPar.to_csv(str(Path(bids_fmriprep_path).joinpath('task-foodcue_avg-fd.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

    #return onset dictionary for integration testing
    return avg_fd, max_fd