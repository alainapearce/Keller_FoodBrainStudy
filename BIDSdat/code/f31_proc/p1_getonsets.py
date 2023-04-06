#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to generate onset files (i.e,. files that contain onset times for parameters of non-interest) 
for the food cue connectivity analyses in Spring 2023 by Bari Fuchs.

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

# Function to get block onsets from foodcue_run_data --- this will be a run-specific events dataset (i.e., sub-XXX_task-foodcue_run-0X_bold_events.tsv)
def _get_officeOnsets(foodcue_RunDat, onsets_Pardat):

        ## Get run number   
        run_num = foodcue_RunDat['run'].iloc[0]

        #get all non-duplicate blocks in run
        blocks = foodcue_RunDat['block'].unique()

        #loop through blocks
        for b in blocks:

            #subset block data from foodcue_data
            block_dat = foodcue_RunDat[foodcue_RunDat['block'] == b]

            # Add block onsets for Office blocks to onsets_dat
            ## Note: 'onset' is the onset time (in seconds) of the event, measured from the beginning of the acquisition of 
            ## the first data point stored in the corresponding task data file. Because this variable is required in the events.tsv file,
            ## it was computed in foodcue_DataOrg.py
            b_condition = block_dat['condition'].iloc[0]
            
            if "Office" in b_condition: 
                onsets_Pardat.at[run_num-1, b_condition] = block_dat['onset'].iloc[0]
        
        return(onsets_Pardat)

def _get_fixOnsets(foodcue_RunDat, fix_Pardat):

        # ## make variable for IBI onset relative to run start

        # # make new variable: "ibi_onset_adjusted" (in seconds) of the event, measured from the beginning of the acquisition of the
        # # first data point stored in the corresponding task data file. Runs started with a 4s fixation, so the onset time of first ibi fixation
        # # should be equal to 4 + 18 (i.e., the block duration) = 22.

        stim1_onset = foodcue_RunDat['stim_onset'].iloc[0]
        foodcue_RunDat['ibi_onset_unrounded'] = ((foodcue_RunDat['ibi_onset'] - stim1_onset)/1000) + 4
        foodcue_RunDat['ibi_onset_adjusted'] = foodcue_RunDat.ibi_onset_unrounded.map(lambda x:round(x))

        ## Get run number   
        run_num = foodcue_RunDat['run'].iloc[0]

        #get all non-duplicate blocks in run
        blocks = foodcue_RunDat['block'].unique()

        #loop through blocks
        for b in blocks:

            #subset block data from foodcue_data
            block_dat = foodcue_RunDat[foodcue_RunDat['block'] == b]

            # Add run and block to fix_Pardat
            fix_Pardat.at[(run_num-1)+ ((run_num-1)*5) + (b-1), 'run'] = block_dat['run'].iloc[0]
            fix_Pardat.at[(run_num-1)+ ((run_num-1)*5) + (b-1), 'block'] = block_dat['block'].iloc[0]

            # Add ibi_onset_adjusted to fix_Pardat
            fix_Pardat.at[(run_num-1)+ ((run_num-1)*5) + (b-1), 'ibi_onset'] = block_dat['ibi_onset_adjusted'].iloc[0]

        return(fix_Pardat)

##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################

def getonsets(par_id, overwrite = False):

    # get script location
    script_path = Path(__file__).parent.resolve()

    # change directory to base directory (BIDSdat) and get path
    os.chdir(script_path)
    os.chdir('../..')
    base_directory = Path(os.getcwd())

    #set specific paths
    bids_raw_path = Path(base_directory).joinpath('raw_data')
    bids_deriv_onsetfiles = Path(base_directory).joinpath('derivatives/preprocessed/f31_onsetfiles')

    # make orig directory if it doesnt exist
    if os.path.exists(bids_deriv_onsetfiles) is False:
        os.makedirs(bids_deriv_onsetfiles)

    #############################
    ### Get participant files ###
    #############################

    # set sub with leading zeros
    sub = str(par_id).zfill(3)

    raw_files = list(Path(bids_raw_path).rglob('sub-' + str(sub) + '/ses-1/func/*foodcue*events.tsv'))

    if len(raw_files) < 1:
        print('No *events.tsv files found for sub ' + str(sub))
        raise Exception()
        
    ## if no overwrite option selected, remove IDs from subject list that already have onset files ##
    if overwrite is False:

        # get list of existing onset files 
        onset_files = list(Path(bids_deriv_onsetfiles).rglob('*AFNIonsets.txt'))

        # get unique ids from onset_files
        ##pathlib library -- .relative_to give all the path that follows bids_deriv_onsetfiles
        #                   .parts[0] extracts the first directory in remaining path to get
        #                       list of subjects
        files_exist = [item.relative_to(bids_deriv_onsetfiles).parts[0] for item in onset_files]
        
        ##set is finding only unique values
        subs_exist_str = list(set([item[4:7] for item in files_exist]))   

        # Exit of sub already has orig onsets
        if sub in subs_exist_str:
            print(str(sub) + ' - orig onset files already exist. Use overwrite = True to overwrite')
            raise Exception()

    ##########################
    ### Create onset files ###
    ##########################

    # get events files -- Note: each events fils corresponds to 1 foodcue run
    eventsfiles = list(Path(bids_raw_path).rglob('sub-' + str(sub) + '/ses-1/func/*foodcue*events.tsv'))

    # get number of runs -- Note: each events fils corresponds to 1 foodcue run
    nruns = len(eventsfiles)

    # create onset data per participant
    onsets_Pardat = pd.DataFrame(np.zeros((nruns, 2)))
    onsets_Pardat.columns = ['OfficeLarge', 'OfficeSmall']

    #create fixation data per participant
    fix_Pardat = pd.DataFrame(np.zeros((nruns*6, 3)))
    fix_Pardat.columns = ['run', 'block', 'ibi_onset']
    
    # loop through eventsfiles
    for file in eventsfiles:

        #load data
        foodcue_RunDat = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python')

        # select only variables interested in using for processed data
        foodcue_RunDat = foodcue_RunDat[['sub', 'ses', 'experiment_name' ,'block', 'trial', 'condition', 'stimslide_onsettime', 'stimslide_onsettoonsettime', 'onset', 'duration', 'interblockinterval_onsettime', 'interblockinterval_duration']]
    
        # rename columns (note: block becomes run, trial becomes block)
        foodcue_RunDat.columns = ['sub', 'ses', 'experiment_name', 'run', 'block', 'condition', 'stim_onset', 'stim_onset2onset', 'onset', 'duration', 'ibi_onset', 'ibi_duration']

        #extract timing info
        onsets_Pardat = _get_officeOnsets(foodcue_RunDat, onsets_Pardat)
        fix_Pardat = _get_fixOnsets(foodcue_RunDat, fix_Pardat)

    #output Office block onsets
    for c in onsets_Pardat.columns:
        onsets_cond = pd.DataFrame(np.zeros((nruns, 2)))
        onsets_cond.columns = ['cond', 'star']
        onsets_cond['cond'] = onsets_Pardat[c]
        onsets_cond['star'] = '*'
        onsets_cond.to_csv(str(Path(bids_deriv_onsetfiles).joinpath('sub-' + sub + '_' + c + '-AFNIonsets.txt')), sep = '\t', encoding='ascii', index = False, header=None)

    # make fix_Pardat wide so there is 1 column per block, run column becomes index
    fix_Pardat_wide = pd.pivot(fix_Pardat, index='run', columns='block', values='ibi_onset')

    # sort by index
    fix_Pardat_wide = fix_Pardat_wide.sort_index()

    #output IBI fixation onsets
    fix_Pardat_wide.to_csv(str(Path(bids_deriv_onsetfiles).joinpath('sub-' + sub + '_IBI-AFNIonsets.txt')), sep = '\t', encoding='ascii', index = False, header=None)

