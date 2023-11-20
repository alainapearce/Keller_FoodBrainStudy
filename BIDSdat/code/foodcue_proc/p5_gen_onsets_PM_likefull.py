#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to generate onset files with post-scan liking and fullness ratings as a 
parametric modulator (PM) using previously generated onset files and behavioral data

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
import pandas as pd
import os
from pathlib import Path
import re

#########################################################
####                                                 ####
####                  Subfunctions                   ####
####                                                 ####
#########################################################

def _gen_new_onset_file(sub, file, rating_dat, rating_type):
    """Function to generate dataframe with 1 column for block onset and 1 column for block p_want_of_resp
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

    #set rating variable
    avg_rating_var = "avg_" + rating_type

    # Loop through rows in onset file (row i corresponds to run i+1)
    for i in range(len(onsetfile_dat)):

        # check if run is excluded
        if onsetfile_dat.at[i, 0] != "*":

            # get run number
            runnum = i + 1

            # get p_want_of_resp for condition and run 
            row = rating_dat[(rating_dat['id'] == sub) & (rating_dat['run'] == int(runnum)) & (rating_dat['cond'] == cond)] #select row based on sub, runnum, and condition
            avg_rating = round(float(row[avg_rating_var]),2)

            # exit if p_want is missing (nan)
            if pd.isna(avg_rating):
                print ("sub " + sub + " has missing data for" + rating_type + ". Quitting")
                raise Exception
            # else add p_want to onsetfile_dat
            else:
                onset = onsetfile_dat.at[i, 0]
                onsetfile_dat.at[i, 0] = str(onset) + "*" + str(avg_rating)

    return(cond, onsetfile_dat)


##############################################################################
####                                                                      ####
####                             Main Function                            ####
####                                                                      ####
##############################################################################

def gen_onsets(par_id, onset_folder, preproc_path = False):
    """Function to generate onset files for parametric analyses
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

    # set path to rating databases
    liking_path = Path(base_directory).joinpath('derivatives/analyses/foodcue-paper1/R/liking_ratings_byblock.csv')
    fullness_path = Path(base_directory).joinpath('derivatives/analyses/foodcue-paper1/R/fullness_ratings_byblock.csv')

    # Import liking data file
    if liking_path.is_file(): # if database exists
        # import database
        liking_dat = pd.read_csv(str(liking_path), sep = ',')
        # convert id to string and add leading zeros
        liking_dat['id'] = liking_dat['id'].astype(str).str.zfill(3)

        # raise exception if subject not in database
        if sub not in liking_dat['id'].values:
            print("sub " + sub + " not found in liking_ratings_byblock.csv. Quitting")  
            raise Exception()
    else:
        print("liking_ratings_byblock.csv not found. Quitting")        
        raise Exception()
    
    # Import fullness data file
    if fullness_path.is_file(): # if database exists
        # import database
        fullness_dat = pd.read_csv(str(fullness_path), sep = ',')
        # convert id to string and add leading zeros
        fullness_dat['id'] = fullness_dat['id'].astype(str).str.zfill(3)

        # raise exception if subject not in database
        if sub not in fullness_dat['id'].values:
            print("sub " + sub + " not found in fullness_ratings_byblock.csv. Quitting")  
            raise Exception()
    else:
        print("fullness_ratings_byblock.csv not found. Quitting")        
        raise Exception()

    ##############################################
    #### Combine onset and p_want information ####
    ##############################################

    base_onsetfiles.sort()

    # initialize dictionaries to save data frames
    liking_onset_dict={}
    fullness_onset_dict={}

    for rating_type in ['liking', 'fullness']:
        
        for file in base_onsetfiles: #loop through runs (each run has its own confoundfile)

            # generate new onset file with behavioral info
            if rating_type == "liking":
                cond, onsetfile_dat = _gen_new_onset_file(sub, file, liking_dat, rating_type)
                liking_onset_dict[cond] = onsetfile_dat # add to dictionary
            elif rating_type == "fullness":
                filename = str(file).rsplit('/',1)[-1]
                cond = re.split('_|-',filename)[2] #get conditon
                if "Office" not in cond:
                    cond, onsetfile_dat = _gen_new_onset_file(sub, file, fullness_dat, rating_type)
                    fullness_onset_dict[cond] = onsetfile_dat # add to dictionary
                
    ## Combine onsets across conditions
    liking_onset_dict['HighED'] = pd.concat([liking_onset_dict['HighLarge'][0], liking_onset_dict['HighSmall'][0]], axis=1)
    liking_onset_dict['LowED'] = pd.concat([liking_onset_dict['LowLarge'][0], liking_onset_dict['LowSmall'][0]], axis=1)
    liking_onset_dict['LargePSfood'] = pd.concat([liking_onset_dict['HighLarge'][0], liking_onset_dict['LowLarge'][0]], axis=1)
    liking_onset_dict['SmallPSfood'] = pd.concat([liking_onset_dict['HighSmall'][0], liking_onset_dict['LowSmall'][0]], axis=1)
    liking_onset_dict['Office'] = pd.concat([liking_onset_dict['OfficeLarge'][0], liking_onset_dict['OfficeSmall'][0]], axis=1)
    liking_onset_dict['Food'] = pd.concat([liking_onset_dict['HighLarge'][0], liking_onset_dict['HighSmall'][0],liking_onset_dict['LowLarge'][0], liking_onset_dict['LowSmall'][0] ], axis=1)

    ## Combine onsets across conditions
    fullness_onset_dict['HighED'] = pd.concat([fullness_onset_dict['HighLarge'][0], fullness_onset_dict['HighSmall'][0]], axis=1)
    fullness_onset_dict['LowED'] = pd.concat([fullness_onset_dict['LowLarge'][0], fullness_onset_dict['LowSmall'][0]], axis=1)
    fullness_onset_dict['LargePSfood'] = pd.concat([fullness_onset_dict['HighLarge'][0], fullness_onset_dict['LowLarge'][0]], axis=1)
    fullness_onset_dict['SmallPSfood'] = pd.concat([fullness_onset_dict['HighSmall'][0], fullness_onset_dict['LowSmall'][0]], axis=1)
    fullness_onset_dict['Food'] = pd.concat([fullness_onset_dict['HighLarge'][0], fullness_onset_dict['HighSmall'][0],fullness_onset_dict['LowLarge'][0], fullness_onset_dict['LowSmall'][0] ], axis=1)


    ######################################
    #### Output PM onset timing files ####
    ######################################

    # set path to PM onset directory
    new_onset_path = Path(bids_onset_path).joinpath(str(onset_folder) + "_PM_likefull")
    
    # Check whether the onset directory exists or not
    isExist = os.path.exists(new_onset_path)
    if not isExist:
        # make new path
        os.makedirs(new_onset_path)
            
    # loop through keys in dictionary 
    for condition_key in liking_onset_dict:

        if condition_key in ['HighED', 'LowED', 'LargePSfood', 'SmallPSfood', 'Office', 'Food']:
            # set output name
            outputname = "sub-" + sub + "_liking_" + condition_key + "-AFNIonsets.txt"

            # extract onset info
            onsetfile_dat = liking_onset_dict[condition_key]

            # write file
            onsetfile_dat.to_csv(str(Path(new_onset_path).joinpath(outputname)), sep = '\t', encoding='ascii', index = False, header=False)

    # loop through keys in dictionary 
    for condition_key in fullness_onset_dict:

        if condition_key in ['HighED', 'LowED', 'LargePSfood', 'SmallPSfood', 'Food']:
            # set output name
            outputname = "sub-" + sub + "_fullness_" + condition_key + "-AFNIonsets.txt"

            # extract onset info
            onsetfile_dat = fullness_onset_dict[condition_key]

            # write file
            onsetfile_dat.to_csv(str(Path(new_onset_path).joinpath(outputname)), sep = '\t', encoding='ascii', index = False, header=False)
