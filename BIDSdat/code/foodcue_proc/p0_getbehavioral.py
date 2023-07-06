#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to extract behavioral data
for the fmri food cue task in Spring 2022 by Bari Fuchs.

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
from pickle import TRUE
import numpy as np
import pandas as pd
import os
from pathlib import Path


##########################################################
####                                                  ####
####                  Subfunctions                    ####
####                                                  ####
##########################################################

def _get_summary_files(deriv_beh_path, sub, overwrite):
    """Function to import or generate behavior summary files. 
        If subject is already in database and Overwrite = False, exception will be raised. 
        If subject is already in database and Overwrite != False, subject will be removed from summary database.

    Inputs:
        deriv_beh_path - path to summary file 
        sub (str) - subject ID
        overwrite (bool) - True or False for overwriting subject data in censor summary files
        
    Outputs:
        beh_summary_allPar (pandas dataframe)
    """

    ### Manage censor_summary_path ###
    if deriv_beh_path.is_file(): # if database exists

        # import database
        beh_summary_allPar = pd.read_csv(str(deriv_beh_path), sep = '\t')

        # convert int to string, then add leading zeros
        beh_summary_allPar['id'] = beh_summary_allPar['id'].astype(str).str.zfill(3)

        # check to see if subject already in database
        if (sub in set(beh_summary_allPar['id'])):
            if overwrite is False:
                print("sub_" + sub + " already in task-foodcue_summary.tsv -- Use overwrite = True to rerun")
                raise Exception()
            
            if overwrite is True: #overwrite is true
                # remove subject rows from censor_summary_byrun_path
                print("overwriting for sub_" + sub)
                beh_summary_allPar = beh_summary_allPar[beh_summary_allPar['id'] != sub]

        else:
            print("beh data for sub_" + sub + " not in task-foodcue_summary.tsv -- Extracting...")

    # if database does not exist
    else:
        # create new dataframe 
        beh_summary_allPar = pd.DataFrame(np.zeros((0, 8)))
        beh_summary_allPar.columns = ['id','run','cond', 'n_trials', 'n_responses', 'n_omissions', 'n_want', 'p_want_of_resp']

    return(beh_summary_allPar)


# Function to get behavioral data from foodcue_run_data --- this will be a run-specific events dataset (i.e., sub-XXX_task-foodcue_run-0X_bold_events.tsv)
def _extract_behavior(file):

    #load data
    foodcue_run_dat = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python')

    # select variables for processing
    foodcue_run_dat = foodcue_run_dat[['experiment_name','sub', 'block', 'condition', 'procedure_trial', 'filename', 'stimslide_resp', 'stimslide_rt']]
    
    # rename columns (note: block becomes run)
    foodcue_run_dat.columns = ['experiment_name', 'sub', 'run', 'condition', 'block_proc', 'stim', 'want_resp', 'want_rt']

    # Modify stimulus condition names
    foodcue_run_dat['condition'].mask(foodcue_run_dat['condition'] == 'HighSmallED', 'HighSmall' , inplace=True )
    foodcue_run_dat['condition'].mask(foodcue_run_dat['condition'] == 'HighLargeED', 'HighLarge' , inplace=True )
    foodcue_run_dat['condition'].mask(foodcue_run_dat['condition'] == 'LowSmallED', 'LowSmall' , inplace=True )
    foodcue_run_dat['condition'].mask(foodcue_run_dat['condition'] == 'LowLargeED', 'LowLarge' , inplace=True )

    # make participant dataframe
    beh_run_sub = pd.DataFrame(np.zeros((0, 10)))
    beh_run_sub.columns = ['id','task_ver', 'run', 'block_proc', 'cond', 'n_trials', 'n_responses', 'n_omissions', 'n_want', 'p_want_of_resp']

    # get sub number
    sub = foodcue_run_dat['sub'].iloc[0]

    # get task ver
    if 'VA' in foodcue_run_dat['experiment_name'].iloc[0]:
        ver = 'A'
    elif 'VB' in foodcue_run_dat['experiment_name'].iloc[0]:
        ver = 'B'

    # get run number   
    run_num = foodcue_run_dat['run'].iloc[0]

    #get list of conditions
    conditions = foodcue_run_dat['condition'].unique()

    #loop through conditions
    for condition in conditions:

        #subset condition data from foodcue_data
        cond_dat = foodcue_run_dat[foodcue_run_dat['condition'] == condition]

        # get block_proc (first 2 characters of 'block_proc')
        block_proc = (cond_dat['block_proc'].iloc[0])[0:2]

        # count number of trials 
        n_trials = len(cond_dat)

        # count number of responses 
        n_responses = cond_dat['want_resp'].count()

        # count number of ommisions 
        n_omissions = n_trials - n_responses

        # count number of wants (thumb responses -- a or d)
        n_want = len(cond_dat[(cond_dat['want_resp']=='d') | (cond_dat['want_resp']=='a')])

        # percent want of responses made -- only calculate if has responses
        if n_responses > 0:
            p_want = round(n_want/n_responses, 2)
        else:
            p_want = 'NaN'

        # make a dataframe row with behavioral data
        beh_row = pd.DataFrame(data=[sub, ver, run_num, block_proc, condition, n_trials, n_responses, n_omissions, n_want, p_want]).T
        beh_row.columns = ['id','task_ver', 'run', 'block_proc', 'cond', 'n_trials', 'n_responses', 'n_omissions', 'n_want', 'p_want_of_resp']
    
        # add row to beh_run_sub
        beh_run_sub = pd.concat([beh_run_sub, beh_row])

    return(beh_run_sub)

##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################

def getbehavior(par_id, overwrite = False):


    # get script location
    script_path = Path(__file__).parent.resolve()

    # change directory to base directory (BIDSdat) and get path
    os.chdir(script_path)
    os.chdir('../..')
    bids_directory = Path(os.getcwd())

    #set specific paths
    bids_raw_path = Path(bids_directory).joinpath('raw_data') # path to raw data directory
    deriv_beh_path = Path(bids_directory).joinpath('derivatives/preprocessed/beh/task-foodcue_summary.tsv') # path to behavioral data file

    # set sub with leading zeros
    sub = str(par_id).zfill(3)

    # import or generate summary dataframe
    beh_summary_allPar = _get_summary_files(deriv_beh_path, sub, overwrite)

    ###################################
    ### Get participant event files ###
    ###################################

    eventsfiles = list(Path(bids_raw_path).rglob('sub-' + str(sub) + '/ses-1/func/*foodcue*events.tsv'))

    if len(eventsfiles) < 1:
        print('No *events.tsv files found for sub ' + str(sub))
        raise Exception()
    
    ###########################
    ### Get behavioral data ###
    ###########################

    # loop through eventsfiles (i.e, run data)
    for file in eventsfiles:
        
        # extract behavioral data from each event file
        beh_run_sub = _extract_behavior(file)

        # add participant data to summary dataframe 
        beh_summary_allPar = pd.concat([beh_summary_allPar, beh_run_sub])


    #output summary file
    beh_summary_allPar.to_csv(str(deriv_beh_path), sep = '\t', encoding='utf-8-sig', index = False)
