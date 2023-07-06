#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
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
import sys

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


##############################################################################
####                                                                      ####
####                             Main Function                            ####
####                                                                      ####
##############################################################################

def gen_index_byrun(onset_dir, nruns, preproc_path = False):

    """Function to generate an index file that lists subjects with a sufficient 
        number of good runs (nruns) to be included in analyses. 
    
    Inputs:
        onset_dir (string): name of directory where censored onsetfiles are located (e.g., 'fd-0.9_b20')
        nruns (int): minimum number of "good" runs that a subject needs to be included in analyses
        preproc_path (string, optional): path to directory above foodcue_onsetfiles/

    Outputs:
        3 "index files" (text files) with list of subject IDs -- 1 for whole sample, low risk sample, and high risk sample

    """

    # set base_directory
    if preproc_path is False:

        # get script location
        script_path = Path(__file__).parent.resolve()

        # change directory to base directory (BIDSdat) and get path
        os.chdir(script_path)
        os.chdir('../../..')
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

    # check onset_dir does not 'by-block' string
    if 'by-block' in onset_dir:        
        print("onset_dir must NOT contain 'by-block'")
        raise Exception

    # Set onset directory
    onset_directory = Path(bids_onset_path).joinpath( str(onset_dir))

    # check onset directory exists
    if onset_directory.is_dir() is False:
        print("onset directory does not exist")
        raise Exception

    ###########################################
    #### Make list of IDs with enough runs ####
    ###########################################

    # get list of subjects with onset files
    onsetfiles = []
    for file in onset_directory.rglob('*'):  # loop recursively over all subdirectories
        onsetfiles.append(file.name)

    onsetfiles = [file.stem for file in onset_directory.rglob('*')]
    subs = [re.split('_|-',file)[1] for file in onsetfiles]
    subs = list(set(subs)) # get unique list of subjects
    subs = (sorted(subs))

    # get list of subjects with >= nruns
    subs_to_include = []
    for sub in subs:

        # read in HighLarge onset file -- the same runs will be censored from every condition, so only need to assess 1 onset file
        HL_onset = Path(onset_directory).joinpath('sub-' + str(sub) + '_HighLarge-AFNIonsets.txt')
        HL_file = pd.read_csv(HL_onset, sep = '\t', encoding = 'utf-8-sig', engine='python', header=None)

        nruns_sub = 0
        # Loop through rows in onset file (row i corresponds to run i+1)
        for i in range(len(HL_file)):
            if _represents_float(HL_file[0].iloc[i]):
                nruns_sub = nruns_sub + 1
        
        if nruns_sub >= nruns:
            subs_to_include.append(sub)

    #########################################
    #### Remove subjects based on fmri QC ###
    #########################################

    # make dataframe from subs_to_include list
    sub_include_df = pd.DataFrame({'id':subs_to_include})

    # remove subjects from dataframe who should be excluded from analyses
    sub_include_df = sub_include_df[sub_include_df['id'] != '105'] # exclude due to extreme FOV cut-off in fmri data
    sub_include_df = sub_include_df[sub_include_df['id'] != '119'] # exclude due to extreme FOV cut-off in fmri data
    sub_include_df = sub_include_df[sub_include_df['id'] != '031'] # exclude due to ADHD diagnosis
    sub_include_df = sub_include_df[sub_include_df['id'] != '034'] # exclude due to ADHD diagnosis

    ##################################
    #### Make lists by risk group ####
    ##################################

    # Import and format dataframe with risk info
    anthro_df = pd.read_spss(Path(database_path).joinpath('anthro_data.sav'))
    anthro_df['id']= anthro_df['id'].astype(int) #change to integer to remove decimals
    anthro_df['id']= anthro_df['id'].astype(str) #change to string
    anthro_df['id'] = anthro_df['id'].str.zfill(3) #add leading zeros

    # Merge risk into into sub_include_df
    sub_include_df = pd.merge(sub_include_df,anthro_df[['id','risk_status_mom']],on='id', how='left')

    # subset based on low and high risk
    high_risk_df = sub_include_df[sub_include_df["risk_status_mom"] == "High Risk"]
    low_risk_df = sub_include_df[sub_include_df["risk_status_mom"] == "Low Risk"]


    ################################################
    #### Generate index files for each dataframe ###
    ################################################

    # Convert dataframes to lists
    all = [str(sub) for sub in sub_include_df['id']]
    highrisk = [str(sub) for sub in high_risk_df['id']]
    lowrisk = [str(sub) for sub in low_risk_df['id']]

    # add lists to dictionary
    index_dict = {}
    index_dict['all'] = all
    index_dict['highrisk'] = highrisk
    index_dict['lowrisk'] = lowrisk

    # define output path
    censor_string = str(onset_dir)

    # loop through groups 
    for group in index_dict:
        
        # set file name
        file = base_directory.joinpath('derivatives/analyses/foodcue-paper1/level2/index_' + group + '_' + str(censor_string) + '_' + str(nruns) + 'runs.txt')
       
       # write ids to file
        with open(file, 'w') as indexFile:
            joined_list = "  ".join(index_dict[group])
            print(joined_list , file = indexFile)