#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The purpose of this script is to organize the source data for the the Space game
into BIDS rawdata format. Written Summer 2021.

@author: Alaina Pearce
"""

import pandas as pd
import os
import shutil
from shutil import copy2
# import pathlib so can detect if Windows or not
from pathlib import Path

##############################################################################
####                                                                      ####
####                  Subfunctions called within script                   ####
####                                                                      ####
##############################################################################


# function to rename SpaceGame raw data
def bidsformat_space_raw(raw_filepath, subname, sesnum):
    # import scipy.io to read .mat files
    import scipy.io as sio
    import numpy as np

    #load data
    space_mat_data = sio.loadmat(raw_filepath)

    #get raw task data
    space_raw_data = space_mat_data['data']
        
    #extract columns
    column_names = ('sub', 'ses', 'block', 'trial', 'timeout_earth', 'timeout_planet',
    'state_earth', 'state_planet', 'stim_left', 'stim_right', 'rt_earth', 'rt_planet', 'choice_earth', 
    'response_earth', 'points', 'stake', 'win', 'score', 'rewards1', 'rewards2', 'missed_earth', 'missed_planet')

    nrows = len(space_raw_data['choice'][0][0])
    trials_array = np.array(range(nrows)) + 1

    spacedat_part1 = pd.DataFrame(np.concatenate((np.vstack(np.repeat(subname, nrows)), np.vstack(np.repeat(sesnum, nrows)), 
                                space_raw_data['block'][0][0], np.vstack(np.array(range(nrows)) + 1), 
                                space_raw_data['timeout'][0][0], space_raw_data['s'][0][0], space_raw_data['stimuli'][0][0],
                                space_raw_data['rt'][0][0], space_raw_data['choice'][0][0]), 1), 
                                columns = column_names[0:13])

    #response earth and win
    spacedat_part1['response'] = np.where(spacedat_part1['stim_left']==spacedat_part1['choice_earth'], 1, 
                                    np.where(spacedat_part1['stim_right']==spacedat_part1['choice_earth'], 2, 3))

    #stakes
    stake_array = np.empty(nrows)        
    stake_array[:] = np.nan

    #update dataset
    spacedat_part2 = spacedat_part1.join(pd.DataFrame(np.concatenate((space_raw_data['points'][0][0], np.vstack(stake_array)), 1), 
                                            columns = column_names[14:16]))

    #win
    spacedat_part2['win'] = np.where(spacedat_part2['points'] > 0, 1, 0)

    #update with rest of data
    spacedat_final = spacedat_part2.join(pd.DataFrame(np.concatenate((space_raw_data['score'][0][0], space_raw_data['rews'][0][0]), 1), 
                        columns = column_names[17:20]))

    #missed
    spacedat_final['rt_earth'] = pd.to_numeric(spacedat_final['rt_earth'])
    spacedat_final['rt_planet'] = pd.to_numeric(spacedat_final['rt_planet'])

    spacedat_final['missed_earth'] = np.where(spacedat_final['rt_earth'] == -1, 1, 0)
    spacedat_final['missed_planet'] = np.where(spacedat_final['rt_planet'] == -1, 1, 0)

    # return pandas dataset
    return(spacedat_final)

##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################

# get script location
script_path = Path(os.path.dirname(__file__))

# change directory to base directory and get path
os.chdir(script_path)
os.chdir('..')
base_directory = Path(os.getcwd())

#set specific paths
bids_source_path = Path(base_directory).joinpath('BIDSdat/sourcedata')
bids_raw_path = Path(base_directory).joinpath('BIDSdat/raw_data')
space_raw_path = Path(base_directory).joinpath('SpaceGame_Raw')

#get list of raw SpaceGame files
space_raw_files = list(Path(space_raw_path).rglob('mbmfNovelStakes_*.mat'))

#error count
n_error = 0

# loop through files in raw SpaceGame directory
for filepath in space_raw_files:

    # get filename
    filename = os.path.basename(filepath)

    # extract subject from filename
    if len(filename) < 23 or len(filename) > 25:
        raw_name_error = 'naming does not follow known naming convention: ' + filename
        print(raw_name_error)
        
        #check errors - if no errors, start error .txt output
        if n_error == 0:
                        
            #open .txt file
            with open(Path(script_path).joinpath('SpaceGame_DataOrg_error.txt'), "w+") as error_file:
                error_file.write(raw_name_error)
                        
                #update error
                n_error = n_error + 1
            
        #if already had error, add to error .txt output
        else:
            with open(Path(script_path).joinpath('SpaceGame_DataOrg_error.txt'), "a") as error_file:
                error_file.write(raw_name_error)
        
        #skip rest of loop/go to next file
        continue
    
    #single digit number    
    elif len(filename) == 23:
        subnum = filename[16:17]
        sesnum = filename[18:19]
    #double digit number
    elif len(filename) == 24:
        subnum = filename[16:18]
        sesnum = filename[19:20]
    #tripple digit number
    elif len(filename) == 25:
        subnum = filename[16:19]
        sesnum = filename[20:21]
        
    # pad subnum with zeros
    subname = str(subnum).zfill(3)
    
    # make BIDS source directory structure if needed
    beh_source_bids_path = Path(bids_source_path).joinpath('sub-' + subname + '/ses-' + sesnum + '/beh')
    Path(beh_source_bids_path).mkdir(parents=True, exist_ok=True) 

    #copy source .mat outputs into sourcedata
    copy2(filepath, Path(beh_source_bids_path))
    
    #copy source json file into sourcedata
    json_template_path = Path(base_directory).joinpath('orgRaw_scripts/templates_json/task-space_source_template.json')
    json_dest_filename = Path(beh_source_bids_path).joinpath('mbmfNovelStakes-' + subnum + '-' + sesnum + '.json')
    shutil.copy(json_template_path, json_dest_filename)

    # make BIDS raw directory structure if needed
    beh_raw_bids_path = Path(bids_raw_path).joinpath('sub-' + subname + '/ses-' + sesnum + '/beh')
    Path(beh_raw_bids_path).mkdir(parents=True, exist_ok=True) 

    # set bids file name to check if file exists
    bids_filename = Path(beh_raw_bids_path).joinpath('sub-' + subname + '_ses-' + sesnum + '_task-space_events.tsv') 
    
    # if file has not been moved, edit column names and save
    if not bids_filename.exists():

        # run funtion to rename columns
        bids_space_data = bidsformat_space_raw(filepath, subname, sesnum) 
        
        # write to tsv file
        bids_space_data.to_csv(bids_filename, sep="\t", encoding='utf-8-sig', index = False)
        
    else:
        # write out participants already processed
        print('sub-' + subname + '_ses-' + sesnum + '_task-space_events.tsv exists')
        
