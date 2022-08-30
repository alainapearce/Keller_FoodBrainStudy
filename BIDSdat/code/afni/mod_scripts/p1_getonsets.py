#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to generate original onset files (i.e,. files that contain condition onset times for every run) 
for the fmri food cue task in Spring 2022 by Bari Fuchs.

Copyright (C) 20120 Bari Fuchs

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
import sys, argparse
#from scipy.stats import norm
#from scipy.stats.morestats import shapiro
from pathlib import Path

##############################################################################
####                                                                      ####
####                        Set up script function                        ####
####                                                                      ####
##############################################################################

# to enter multiple subject arguments in terminal format like:
#-p 2 3

# to overwrite onsets of all input IDs, specify in terminal format like:
#-f

#input arguments setup
parser=argparse.ArgumentParser()
parser.add_argument('--parIDs', '-p', help='participant list', type=float, nargs="+")
parser.add_argument('--overwrite', '-f', help='force overwrite of existing data. all specified IDs will be overwritten', action='store_true')

args=parser.parse_args()

##############################################################################
####                                                                      ####
####                  Subfunctions called within script                   ####
####                                                                      ####
##############################################################################

# Function to get block onsets from foodcue_run_data --- this will be a run-specific events dataset (i.e., sub-XXX_task-foodcue_run-0X_bold_events.tsv)
def get_blockOnsets(foodcue_run_data, onset_data):

        ## Get run number   
        run_num = foodcue_run_data['run'].iloc[0]

        #get all non-duplicate blocks in run
        blocks = foodcue_run_data['block'].unique()
        nblocks = len(blocks)

        #loop through blocks
        for b in blocks:

            #subset block data from foodcue_data
            block_dat = foodcue_run_data[foodcue_run_data['block'] == b]

            # Add block onset to onsets_dat
            ## Note: 'onset' is the onset time (in seconds) of the event, measured from the beginning of the acquisition of 
            ## the first data point stored in the corresponding task data file. Because this variable is required in the events.tsv file,
            ## it was computed in foodcue_DataOrg.py
            b_condition = block_dat['condition'].iloc[0]
            onset_data.at[run_num-1, b_condition] = block_dat['onset'].iloc[0]
        
        return(onset_data)

# Figure out this function
#def get_fixOnsets
#             if b == 1:
#                 rb_start = rb_prev_row + b
#                 rb_row = rb_start
#                 if r == 1:
#                     b_start_run = rb_prev_row + b

#             if r==1 and b ==1:
#                 #final block stim onset
#                 fblock_onset = block_dat["stim_onset_rsync"].iloc[-1]
#                 f_row = 1
#                 f_start = f_row
#             else:
#                 if b == 1:
#                     f_row = f_row + 1
#                     f_start = f_row
#                     fix_data["PrevBlock"].iloc[f_row] = nblocks
# #                    fix_data.PrevBlock(f_row) = nblocks;
# #                    #stim dur = 2.5 sec and inter-block-interval = 0.5
#                     fix_data["FixAfterBlock"].iloc[f_row] = round(block_dat["stim_onset"].iloc[0]/1000) - (fblock_onset+2.5+.5)
# #                    fix_data.FixAfterBlock(f_row) = round(block_dat.StimOnset(1)/1000) - (fblock_onset+2.5+.5);
#                     fblock_onset = block_dat["stim_onset_rsync"].iloc[-1]
#                 else:
#                     f_row = f_row + 1
#                     fix_data["PrevBlock"].iloc[f_row] = b - 1
#                     #stim dur = 2.5 sec and inter-block-interval = 0.5
#                     fix_data["FixAfterBlock"].iloc[f_row] = round(block_dat["stim_onset_rsync"].iloc[0]/1000) - (fblock_onset+2.5+.5)

#                     if b == nblocks:
#                         fblock_onset = round(block_dat["stim_onset"].iloc[-1]/1000)
#                     else:
#                         fblock_onset = round(block_dat["stim_onset_rsync"].iloc[-1]/1000)
        return(onset_data, fix_data)



##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################

# get script location
script_path = Path(__file__).parent.resolve()

# change directory to base directory (BIDSdat) and get path
os.chdir(script_path)
os.chdir('../../..')
base_directory = Path(os.getcwd())

#set specific paths
bids_raw_path = Path(base_directory).joinpath('raw_data')
bids_deriv_onsetfiles = Path(base_directory).joinpath('derivatives/preprocessed/foodcue_onsetfiles/orig')

##check for input arguments and get initial list of subject IDs ##

# if there is 1 or more parID argument
if args.parIDs is not None and len(args.parIDs) >= 1:

    #make sure have integers
    subject_ids = list(map(int, args.parIDs))

    #get leading zeros
    subject_list = [str(item).zfill(3) for item in subject_ids]
        
    #check for raw data
    subs = list(subject_list)

    for sub in subs:

        raw_files = list(Path(bids_raw_path).rglob('sub-' + str(sub) + '/ses-1/func/*foodcue*events.tsv'))

        if len(raw_files) < 1:
            print('No Files found for sub-' + str(sub))
            subject_list.remove(sub)
        
    #check if any files to process
    if subject_list is None:
        sys.exit('No Files found for participants' + args.parIDs)   

# if there are no parID arguments entered
else:
    #find all foodcue*events.tsv files
    foodcue_raw_files = list(Path(bids_raw_path).rglob('sub-*/ses-1/func/*foodcue*events.tsv'))

    # get unique ids from foodcue_raw_files
    ##pathlib library -- .relative_to give all the path that follows raw_data_path
    ##                  .parts[0] extracts the first directory in remaining path to get
    ##                       list of subjects
    foodcue_raw_subs = [item.relative_to(bids_raw_path).parts[0] for item in foodcue_raw_files]

    ##set is finding only unique values
    subject_list = list(set([item[4:7] for item in foodcue_raw_subs]))   


## if no overwrite option selected, remove IDs from subject list that already have onset files ##
if args.overwrite is False:

    # get list of existing onset files 
    onset_files = list(Path(bids_deriv_onsetfiles).rglob('*AFNIonsets.txt'))

    # get unique ids from onset_files
    ##pathlib library -- .relative_to give all the path that follows bids_deriv_onsetfiles
    #                   .parts[0] extracts the first directory in remaining path to get
    #                       list of subjects
    files_exist = [item.relative_to(bids_deriv_onsetfiles).parts[0] for item in onset_files]
    
    ##set is finding only unique values
    subs_exist_str = list(set([item[4:7] for item in files_exist]))   

    #compare subject_list to subs_exist

    #get intersection
    match_subs = list(set.intersection(set(subject_list), set(subs_exist_str)))
    
    #report
    for sub in match_subs:
        #remove sub if in list that exists in database already
        print('Skipping sub-' + str(sub) + ' - original onset files already exist.')

    #modify subject_list to remove IDs that already have onset files
    subject_list = list(set(subject_list) -  set(match_subs))

    #exit if there are no files to process
    if len(subject_list) < 1:
        #exit if no files exist
        sys.exit('No new subjects to generate original onset files for')   


## Loop through subject_list and create onset files ##
subs = list(subject_list)
for sub in subs:

    # get events files -- Note: each events fils corresponds to 1 foodcue run
    eventsfiles = list(Path(bids_raw_path).rglob('sub-' + str(sub) + '/ses-1/func/*foodcue*events.tsv'))

    # get number of runs -- Note: each events fils corresponds to 1 foodcue run
    nruns = len(eventsfiles)

    # create onset data per participant
    onsets_Pardat = pd.DataFrame(np.zeros((nruns, 6)))
    onsets_Pardat.columns = ['HighLarge', 'HighSmall', 'LowLarge', 'LowSmall', 'OfficeLarge', 'OfficeSmall']

    #create fixation data per participant
    fix_Pardat = pd.DataFrame(np.zeros((nruns*6, 4)))
    fix_Pardat.columns = ['ParticipantID', 'Run', 'PrevBlock', 'FixAfterBlock']
    
    # set variable to zero
    r_prev_row = 0 #no runs yet
    rb_prev_row = 0 #no runs/blocks yet

    # loop through eventsfiles
    for file in eventsfiles:

        #load data
        foodcue_RunDat = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python')

        # select only variables interested in using for processed data
        foodcue_RunDat = foodcue_RunDat[['sub', 'ses', 'experiment_name' ,'block', 'trial', 'condition', 'filename', 'stimslide_onsettime', 'stimslide_onsettoonsettime', 'stimslide_resp', 'stimslide_rt', 'onset', 'duration']]
    
        # rename columns (note: block becomes run, trial becomes block)
        foodcue_RunDat.columns = ['sub', 'ses', 'experiment_name', 'run', 'block', 'condition', 'stim', 'stim_onset', 'stim_onset2onset', 'want_resp', 'want_rt', 'onset', 'duration']

        # Modify stimulus condition names
        foodcue_RunDat.loc[foodcue_RunDat['condition'] == "HighSmallED", "condition"] = "HighSmall"
        foodcue_RunDat.loc[foodcue_RunDat['condition'] == "HighLargeED", "condition"] = "HighLarge"
        foodcue_RunDat.loc[foodcue_RunDat['condition'] == "LowSmallED", "condition"] = "LowSmall"
        foodcue_RunDat.loc[foodcue_RunDat['condition'] == "LowLargeED", "condition"] = "LowLarge"

        #extract timing info
        onsets_Pardat = get_blockOnsets(foodcue_RunDat, onsets_Pardat)
        #fix_Pardat = get_fixOnsets(foodcue_ProcData, fix_Pardat)

    #output onsets
    for c in onsets_Pardat.columns:
        onsets_cond_filename = Path(bids_deriv_onsetfiles).joinpath('sub-' + sub + '_' + c + '-AFNIonsets.txt')
        onsets_cond = pd.DataFrame(np.zeros((nruns, 2)))
        onsets_cond.columns = ['cond', 'star']
        onsets_cond['cond'] = onsets_Pardat[c]
        onsets_cond['star'] = '*'
        onsets_cond.to_csv(str(Path(bids_deriv_onsetfiles).joinpath('sub-' + sub + '_' + c + '-AFNIonsets.txt')), sep = '\t', encoding='utf-8-sig', index = False, header=None)

