#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to generate onset files with parametric modulator using
previously generated onset files and behavioral data

Written by Bari Fuchs in Fall 2023

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
import pandas as pd
import os
from pathlib import Path
import re

#########################################################
####                                                 ####
####                  Subfunctions                   ####
####                                                 ####
#########################################################

def _gen_new_onset_file(sub, file, foodcue_beh_dat):
    """Function to generate onset files that censor runs with excessive motion based on specified threshold
    Inputs:
        sub
        file
        foodcue_beh_dat
    Outputs:
    """
    
    #load data
    onsetfile_dat = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python', header=None)
    onsetfile_dat[0] = onsetfile_dat[0].astype(str)
    
    #get filename
    filename = str(file).rsplit('/',1)[-1]

    #get conditon
    cond = re.split('_|-',filename)[2]

    # Loop through rows in onset file (row i corresponds to run i+1)
    for i in range(len(onsetfile_dat)):

        # check if run is excluded
        if onsetfile_dat.at[i, 0] != "*":

            # get run number
            runnum = i + 1

            # get p_want_of_resp for condition and run 
            row = foodcue_beh_dat[(foodcue_beh_dat['id'] == sub) & (foodcue_beh_dat['run'] == int(runnum)) & (foodcue_beh_dat['cond'] == cond)] #select row based on sub, runnum, and condition
            p_want = float(row['p_want_of_resp'])

            # add p_want to onsetfile_dat
            onset = onsetfile_dat.at[i, 0]
            onsetfile_dat.at[i, 0] = str(onset) + "*" + str(p_want)

    return(cond, onsetfile_dat)


##############################################################################
####                                                                      ####
####                             Main Function                            ####
####                                                                      ####
##############################################################################

def gen_onsets(par_id, onset_folder, preproc_path = False):
    """Function to generate onset files that censor runs with excessive motion based on specified threshold
    Inputs:
        par_id (int): participant ID 
        onset_folder (str): name of folder in foodcue_onsetfiles that contains onset files to base off of (e.g., orig, fd-0.9_b20)
        Path (str) - path to direcory that contains foodcue_onsetfiles/ and fmriprep/ directories.
    Outputs:
        onsetfile_dat: 1 onset dataframe per condition, exported as a csv
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
        bids_onset_path = Path(base_directory).joinpath('derivatives/preprocessed/foodcue_onsetfiles')

    elif isinstance(preproc_path, str):
        # make input string a path
        preprocessed_directory = Path(preproc_path)

        #set specific paths
        bids_onset_path = Path(preprocessed_directory).joinpath('foodcue_onsetfiles')

    else: 
        print("preproc_path must be string")
        raise Exception()


    # set sub with leading zeross
    sub = str(par_id).zfill(3)

    # get participant confound and onset files
    base_onsetfiles = list(Path(bids_onset_path).rglob(onset_folder + '/sub-' + str(sub) + '*AFNIonsets.txt'))

    # exit if number of onset files is not 6
    if len(base_onsetfiles) != 6:
        print("sub-" + str(sub) + "does not have 6 onset files in " + str(onset_folder) + ". Should have 1 per condition")
        raise Exception()

    # set path to behavioral database 
    foodcue_beh_path = Path(base_directory).joinpath('derivatives/preprocessed/beh/task-foodcue_summary.tsv')

    # Import foodcue task behavior file
    if foodcue_beh_path.is_file(): # if database exists
        # import database --- converting 'sub' to string will maintain leading zeros
        foodcue_beh_dat = pd.read_csv(str(foodcue_beh_path), sep = '\t', converters={'id': lambda x: str(x)})
        # DO THIS: Check that subject exists in beh data base -- else raise Exception()
    else:
        print("task-foodcue_summary.tsv not found. Quitting")        
        raise Exception()


    #########################################
    #### Generate new onset timing files ####
    #########################################

    # dictionary to save data frames
    onset_dict={}

    base_onsetfiles.sort()
    for file in base_onsetfiles: #loop through runs (each run has its own confoundfile)

        # generate new onset file with behavioral info
        cond, onsetfile_dat = _gen_new_onset_file(sub, file, foodcue_beh_dat)

        # add to dictionary
        onset_dict[cond] = onsetfile_dat

    ## To do: make onset files that combine across conditions??? (e.g., all food cue onsets)

    #######################################
    #### Output new onset timing files ####
    #######################################

    # set path to PM onset directory
    new_onset_path = Path(bids_onset_path).joinpath(str(onset_folder) + "_PM")
    
    # Check whether the onset directory exists or not
    isExist = os.path.exists(new_onset_path)
    if not isExist:
        # make new path
        os.makedirs(new_onset_path)
            
    # loop through keys in dictionary 
    for condition_key in onset_dict:
        # set output name
        outputname = "sub-" + sub + "_" + condition_key + "-AFNIonsets.txt"

        # extract onset info
        onsetfile_dat = onset_dict[condition_key]

        # write file
        onsetfile_dat.to_csv(str(Path(new_onset_path).joinpath(outputname)), sep = '\t', encoding='ascii', index = False, header=False)

    #return onset dictionary for integration testing
    #return onset_dict