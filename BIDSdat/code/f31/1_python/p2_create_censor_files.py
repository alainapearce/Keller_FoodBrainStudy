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

#########################################################
####                  Subfunctions                   ####
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

def _gen_run_censorfile(confound_dat, rmsd_thresh, cen_add_tr):
    """Function to determine what TRs (i.e., volumes) need to be censored in first-level analyses based on rmsd threshold and cen_add_TR (censor additional TR) criteria
    Inputs:
        confound_dat (dataframe) - data from a -desc-confounds_timeseries.tsv file
        rmsd_thresh (float) - rmsd threshold
        cen_add_TR (string or FALSE)
            'a' in string indicates censor TR *after* TR where rmsd exceeded
            'b' in string indicates censor TR *before* TR where rmsd exceeded
            FALSE indicates do not censor TRs before or after TR where rmsd exceeded
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

    # Create a boolean mask for each condition
    mask1 = np.arange(len(confound_dat)) < 2
    mask2 = confound_dat['rmsd'] > rmsd_thresh
    if isinstance(cen_add_tr, str):
        mask3 = ('a' in cen_add_tr) & (confound_dat['rmsd'].shift(1) > rmsd_thresh)
        mask4 = ('b' in cen_add_tr) & (confound_dat['rmsd'].shift(-1) > rmsd_thresh) & (np.arange(len(confound_dat)) != len(confound_dat) - 1)
    else:
        mask3 = False
        mask4 = False
    mask5 = confound_dat['non_steady_state_outlier00'] == 1

    # Combine masks using the logical OR operation -- the resulting mask will have the value True wherever at least one of the individual masks has the value True.
    combined_mask = mask1 | mask2 | mask3 | mask4 | mask5

    # Use the combined mask to create the censor_info list -- the ~ (tilde) operator will negate the mask (True becomes False, vice versa)
    censor_info = (~combined_mask).astype(int).tolist()

    return(censor_info)

def _get_summary_file(output_path, censor_str, sub, overwrite):
    """Function to import or generate summary censor file for given censor_str
        File will be imported as a pandas dataframe if censorsummary file exists, otherwise it will be generated. 
        If subject is already in censorsummary dataframe and Overwrite = False, exception will be raised. 
        If subject is already in censorsummary dataframe and Overwrite != False, subject will be removed from summary dataframe.

    Inputs:
        output_path (list) - path where censor files are exported
        censor_str (str) - string that defines TR censor criteria 
        sub (str) - subject ID
        overwrite (bool) - True or False for overwriting subject data in censor summary files
        
    Outputs:
        censor_summary_df (pandas dataframe) - dataframe to add subjects censor summary data to; can be empty or contain summary data for other subjects
    """

    # Set path to summary file
    censor_summary_path = Path(output_path).joinpath('summary_f31censor_' + censor_str + '.tsv')

    ### Manage censor_summary_path ###
    if censor_summary_path.is_file(): # if file exists

        # import database --- converting 'sub' to string will maintain leading zeros
        censor_summary_df = pd.read_csv(str(censor_summary_path), sep = '\t', converters={'sub': lambda x: str(x)})

        # check to see if subject already in dataframe
        if censor_summary_df[(censor_summary_df['sub'] == sub)].shape[0] > 0:
            if overwrite is False:
                print("sub_" + sub + " already in summary_f31censor_" + censor_str + ".tsv. Use overwrite = True to rerun")
                raise Exception()
            else: #overwrite is true
                # remove subject row from censor_summary_df
                censor_summary_df = censor_summary_df.drop(censor_summary_df[(censor_summary_df['sub'] == sub)].index)

    # if database does not exist
    else:
        # create new dataframe 
        censor_summary_df = pd.DataFrame(np.zeros((0, 5)))
        censor_summary_df.columns = ['sub','censor_str', 'n_total_trs', 'n_total_trs_uncensored', 'n_food_trs_uncensored']

    return(censor_summary_df)

def _get_food_onsetTRs(eventsfiles):

    # set length of TR
    TR = 2
    
    # initialize onsets dictionary
    par_food_onset_TRs_dict = {}

    for file in eventsfiles:

        #load data
        foodcue_RunDat = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python')

        # select only variables interested in using for processed data
        foodcue_RunDat = foodcue_RunDat[['sub', 'ses', 'experiment_name' ,'block', 'trial', 'condition', 'stimslide_onsettime', 'stimslide_onsettoonsettime', 'onset', 'duration']]
    
        # rename columns (note: block becomes run, trial becomes block)
        foodcue_RunDat.columns = ['sub', 'ses', 'experiment_name', 'run', 'block', 'condition', 'stim_onset', 'stim_onset2onset', 'onset', 'duration']

        ## Get run number   
        run_num = foodcue_RunDat['run'].iloc[0]

        #get all non-duplicate blocks in run
        blocks = foodcue_RunDat['block'].unique()

        #loop through blocks
        for b in blocks:

            #subset block data from foodcue_data
            block_dat = foodcue_RunDat[foodcue_RunDat['block'] == b]

            # Add food block onset TR to dictionary -- TR will be onset time / TR 
            b_condition = block_dat['condition'].iloc[0]
            if "High" in b_condition or "Low" in b_condition:
                if run_num in par_food_onset_TRs_dict:
                    par_food_onset_TRs_dict[run_num].append(block_dat['onset'].iloc[0]/TR)
                else:
                    par_food_onset_TRs_dict[run_num] = [block_dat['onset'].iloc[0]/TR]

    return(par_food_onset_TRs_dict)

def _gen_food_TR_list(par_food_onset_TRs_dict, confound_files):

    """Function to generate r_int_list based on food block onsets (defined in par_food_onset_TRs_dict)
    Inputs:
        par_food_onset_TRs_dict_dict (dictionary): keys are run numbers, values are food block onsets
        confound_files (list) 
    Outputs:
        food_TR_list (list) - a list of 1s and 0s equal to the length all TRs collected; 0 = TR is not in food block, 1 = TR is in food block
    """

    # initialize empty list where 
    food_TR_list = []

    # sort confound_files
    confound_files.sort()
    
    # loop though confound_files
    for i in range(len(confound_files)):

        #load data
        confound_dat = pd.read_csv(str(confound_files[i]), sep = '\t', encoding = 'utf-8-sig', engine='python')

        # Make a list 0s equal to the length of a run
        run_food_TR_list = [0] * len(confound_dat) # Make a list of 0s equal to the length of confound_dat

        # set run number
        run_num = i + 1

        # loop through onsets for run_num
        for onset in par_food_onset_TRs_dict[run_num]:
            offset = onset + 9  #Get block offset -- note: this will be the first TR after the block of interest
            run_food_TR_list[int(onset):int(offset)] = [1, 1, 1, 1, 1, 1, 1, 1, 1]  #At indices onset to offset-1 in r_int_list, set value to 1 (indicatine TR is in food block)

        # add run data to food_TR_list
        food_TR_list.extend(run_food_TR_list)

    return(food_TR_list)

def _gen_sub_censor_summary(food_TR_list, sub_censor_list):

    if len(food_TR_list) != len(sub_censor_list):
        print("lengths of food_TR_list and sub_censor_list do not match")
        raise Exception()

    n_total = len(sub_censor_list)
    n_uncensored = sub_censor_list.count(1)

    n_food_uncensored = 0
    for i in range(len(sub_censor_list)):
        if food_TR_list[i] == 1:
            if sub_censor_list[i] == 1:
               n_food_uncensored = n_food_uncensored + 1 

    return n_total, n_uncensored, n_food_uncensored

##############################################################################
####                                                                      ####
####                             Main Function                            ####
####                                                                      ####
##############################################################################

def create_censor_files(par_id, bids_raw_path, fmriprep_path, output_path, rmsd_thresh=0.3, cen_add_tr='ba', overwrite = False):
    """
    This function will process -desc-confounds_timeseries.tsv files (output from fmriprep) for 1 participant in preparation for first-level analyses in AFNI. 
    The following steps will occur:
        (1) output a regressor file containing regressor information for all runs -- will be used by AFNI in first-level analyses
        (2) determine which TRs need to be censored from each run based on input criteria
        (3) output a censor file that indicates which TRs to censor across all runs -- will be used by AFNI in first-level analyses

    Inputs:
        par_id 
        rmsd_thresh (int or float): threshold for rmsd. Default set to .3 according to pre-registration
        cen_add_tr (str or FALSE): option for censoring TRs before or after TR exceeding movement threshold. Default set to 'ba' according to pre-registration
             'ba' = censor 1 before and 1 after, 'b' = censor 1 before, FALSE = do not censor additional TRs
        fmriprep_path (str) - path to fmriprep/ directory.
        output_path (str) - path to output directory
        overwrite (boolean) - specify if output files should be overwritten (default = False)
        
    """
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
   
    # get participant confound files
    confound_files = list(Path(fmriprep_path).rglob('sub-' + str(sub) + '/ses-1/func/*task-foodcue_run*confounds_timeseries.tsv'))

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
        
    # make dataframe
    censordata_allruns_df = pd.DataFrame(censordata_allruns)

    # Make directory for export 
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # check if output file already exists 
    filepath = Path(os.path.join(output_path, 'sub-' + sub + '_f31censor_' + str(censor_str) + '.1D'))
    if not filepath.exists() or overwrite is True:
        censordata_allruns_df.to_csv(str(filepath), sep = '\t', encoding='ascii', index = False, header=False)

    ##################################
    ### Update censor summary file ###
    ##################################

    eventsfiles = list(Path(bids_raw_path).rglob('sub-' + str(sub) + '/ses-1/func/*ses-1_task-foodcue*events.tsv'))

    # load or generate censory summary dataframe
    censor_summary_df = _get_summary_file(output_path, censor_str, sub, overwrite)

    # get food block TR onsets
    par_food_onset_TRs_dict = _get_food_onsetTRs(eventsfiles)

    # generate list that indexes which TRs are food (1) and non-food (0)
    food_TR_list = _gen_food_TR_list(par_food_onset_TRs_dict, confound_files)

    # get subject censor summary information
    sub_censor_list = censordata_allruns_df[0].tolist() # convert dataframe to list
    n_total, n_uncensored, n_food_uncensored = _gen_sub_censor_summary(food_TR_list, sub_censor_list)

    # add subject censor summary information to summary database
    sub_censor_summary = pd.DataFrame([[sub, censor_str, n_total, n_uncensored, n_food_uncensored]], columns=['sub','censor_str', 'n_total_trs', 'n_total_trs_uncensored', 'n_food_trs_uncensored'])
    censor_summary_df = pd.concat([censor_summary_df, sub_censor_summary])

    # export censor summary database
    censor_summary_df.to_csv(str(Path(output_path).joinpath('summary_f31censor_' + censor_str + '.tsv')), sep = '\t', encoding='utf-8-sig', index = False, header=True)

    ######################################
    ### Return for integration testing ###
    ######################################

    # return particpant databases with censor info
    return censordata_allruns_df, sub_censor_summary