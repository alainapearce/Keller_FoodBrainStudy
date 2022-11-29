#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to generate subject index files for AFNI analyses using 
task-foodcue_bycond-censorsummary_$censorcritera.tsv files (output of 4_create_censor_files.py). 

Index files will list subject IDs that should be included in analyses, based on the desired motion threshold. 
Index files be generated for the whole group.

Written by Bari Fuchs in Spring 2022

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

def _represents_float(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

def _count_food_conditions(condition_index_dir, sub):
    cond_count = 0 # set conditon count to 0
    conditions = ['HighLarge', 'HighSmall', 'LowLarge', 'LowSmall']
    for condition in conditions:
        if sub in condition_index_dir[condition]:
            cond_count = cond_count + 1
    return cond_count

##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################

def gen_index_byblock(onset_dir, nblocks, preproc_path = False):

    """Function to generate an index files for AFNI analyses that lists subjects with a
    sufficient number of good blocks (nblocks) to be included in analyses. 
    Index files will be generated for the whole group
    Inputs:
        onset_dir (string): name of directory where censored onsetfiles are located (e.g., 'fd-0.9_by-block-7')
        nblocks (int): minimum number of "good" blocks needed for a block to be included in analyses
    Outputs:

    """

    # set base_directory
    if preproc_path is False:

        # get script location
        script_path = Path(__file__).parent.resolve()

        # change directory to base directory (BIDSdat) and get path
        os.chdir(script_path)
        os.chdir('../..')
        base_directory = Path(os.getcwd())

        # set path to onset files
        bids_onset_path = Path(base_directory).joinpath('derivatives/preprocessed/foodcue_onsetfiles')

        # change directory to Databases and get path
        os.chdir('../Databases')
        database_path = Path(os.getcwd())

    elif isinstance(preproc_path, str):
        # make input string a path
        preprocessed_directory = Path(preproc_path)

        #set specific paths
        bids_onset_path = Path(preprocessed_directory).joinpath('foodcue_onsetfiles')

        # change directory to Databases and get path
        os.chdir('../Databases')
        database_path = Path(os.getcwd())

    else: 
        print("preproc_path must be string")
        raise Exception()

    # check onset_dir contains 'by-block' string
    if 'by-block' not in onset_dir:        
        print("onset_dir must contain 'by-block'")
        raise Exception

    # Set onset directory
    onset_directory = Path(bids_onset_path).joinpath( str(onset_dir))

    # check onset directory exists
    if onset_directory.is_dir() is False:
        print("onset directory does not exist")
        raise Exception


    ######################################
    #### Make index files by condition ###
    ######################################

    # get list of subjects with onset files
    onsetfiles = []
    for file in onset_directory.rglob('*'):  # loop recursively over all subdirectories
        onsetfiles.append(file.name)

    onsetfiles = [file.stem for file in onset_directory.rglob('*')]
    subs = [re.split('_|-',file)[1] for file in onsetfiles]
    subs = list(set(subs)) # get unique list of subjects
    subs = (sorted(subs))

    # initialize dictionary
    condition_index_dir = {}

    for condition in (['HighLarge', 'HighSmall', 'LowLarge', 'LowSmall', 'OfficeLarge', 'OfficeSmall']):

        # initiate empty list to append subjects to
        cond_sub_list = []

        for sub in subs:
   
            # read in condition onset file
            onset_path = Path(onset_directory).joinpath('sub-' + str(sub) + '_' + str(condition) + '-AFNIonsets.txt')
            onset_file = pd.read_csv(onset_path, sep = '\t', encoding = 'utf-8-sig', engine='python', header=None)

            nblocks_cond = 0
            # Loop through rows in onset file (row i corresponds to run i+1)
            for i in range(len(onset_file)):
                if _represents_float(onset_file[0].iloc[i]):
                    nblocks_cond = nblocks_cond + 1
            
            if nblocks_cond >= nblocks:
                cond_sub_list.append(sub)
        
        # add list to dictionary
        condition_index_dir[condition] = cond_sub_list

    #############################################
    #### Write index files for each condition ###
    #############################################

    # loop through groups 
    for condition in condition_index_dir:
        
        # set file name
        file = base_directory.joinpath('derivatives/analyses/FoodCue-fmri/Level2GLM/Activation_Univariate/ses-1/index-' + condition + '_' + str(onset_dir) + "_" + str(nblocks) + 'blocks.txt')

       # write ids to file
        with open(file, 'w') as indexFile:
            joined_list = "  ".join(condition_index_dir[condition])
            print(joined_list , file = indexFile)


    ##############################################################################
    #### Make index file for subs (all and by risk) with all 4 food conditions ###
    ##############################################################################
    
    anthro_df = pd.read_spss(Path(database_path).joinpath('anthro_data.sav'))
    anthro_df['id']= anthro_df['id'].astype(int) #change to integer to remove decimals
    anthro_df['id']= anthro_df['id'].astype(str) #change to string
    anthro_df['id'] = anthro_df['id'].str.zfill(3) #add leading zeros

    # # initiate empty list to append subjects to
    all_food_indexlist = []
    hr_food_indexlist = []
    lr_food_indexlist = []

    for sub in subs:

        # count number of food conditions that child meets criteria for
        cond_count = _count_food_conditions(condition_index_dir = condition_index_dir, sub = sub)

        if cond_count == 4:
            # add child to all_food_indexlist
            all_food_indexlist.append(sub)

            # if subject is high risk ## Fix if statement
            if anthro_df.loc[anthro_df['id'] == sub, 'risk_status_mom'].squeeze() == "High Risk":
                hr_food_indexlist.append(sub)

            # if subject is low risk ## Fix if statement
            if anthro_df.loc[anthro_df['id'] == sub, 'risk_status_mom'].squeeze() == "Low Risk":
                lr_food_indexlist.append(sub)



    # define output paths
    all_sub_file = base_directory.joinpath('derivatives/analyses/FoodCue-fmri/Level2GLM/Activation_Univariate/ses-1/index_all_' + str(onset_dir) + "_" + str(nblocks) + 'blocks.txt')
    hr_sub_file = base_directory.joinpath('derivatives/analyses/FoodCue-fmri/Level2GLM/Activation_Univariate/ses-1/index_highrisk_' + str(onset_dir) + "_" + str(nblocks) + 'blocks.txt')
    lr_sub_file = base_directory.joinpath('derivatives/analyses/FoodCue-fmri/Level2GLM/Activation_Univariate/ses-1/index_lowrisk_' + str(onset_dir) + "_" + str(nblocks) + 'blocks.txt')

    # write all sub to file
    with open(all_sub_file, 'w') as indexFile:
        joined_list = "  ".join(all_food_indexlist)
        print(joined_list , file = indexFile)

    # write high risk to file
    with open(hr_sub_file, 'w') as indexFile:
        joined_list = "  ".join(hr_food_indexlist)
        print(joined_list , file = indexFile)

    # write low risk to file
    with open(lr_sub_file, 'w') as indexFile:
        joined_list = "  ".join(lr_food_indexlist)
        print(joined_list , file = indexFile)



