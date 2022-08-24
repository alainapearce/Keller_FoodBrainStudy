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
from email import header
from pickle import TRUE
from aem import con
import numpy as np
import pandas as pd
import os
import sys, argparse
#from scipy.stats import norm
from scipy.stats.morestats import shapiro
from pathlib import Path

##############################################################################
####                                                                      ####
####                        Set up script function                        ####
####                                                                      ####
##############################################################################

#input arguments setup
parser=argparse.ArgumentParser()
parser.add_argument('--censorsumfile', '-c', help='name of censor summary file (e.g., task-foodcue_bycond-censorsummary_fd-1.0.tsv', type=str)
args=parser.parse_args()

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
pardata_directory = Path(os.getcwd())
#bids_directory = Path(os.getcwd())

#set specific paths
bids_path = Path(pardata_directory).joinpath('BIDSdat')
bids_fmriprep_path = Path(pardata_directory).joinpath('BIDSdat/derivatives/preprocessed/fmriprep')
database_path = Path(pardata_directory).joinpath('Databases')

# set framewise displacement and std_dvar threshold variables
censorsummary_file = args.censorsumfile

# Import censor summary database for TR censor criteria
censor_summary_path = Path(bids_fmriprep_path).joinpath( str(censorsummary_file))

# if database exists
if censor_summary_path.is_file():
    # import database
    censor_summary_allPar = pd.read_csv(str(censor_summary_path), sep = '\t')
else:
    print("censor summary file does not exist")

# extract criteria used to censor TRs based on censor summary database name
substring = censorsummary_file.split("summary_",1)[1]
TR_cen_critera = substring.split(".tsv",1)[0]

# set minimum number of TRs per block
#min_blockTR = args.minblockTR
min_blockTR = 7

# set minimum number of blocks for condition to be used
min_block = 3

# subset data to remove sub 999 
censor_summary_allPar = censor_summary_allPar[censor_summary_allPar["sub"] != 999]

## Loop through subject_list and create onset files ##
subs = censor_summary_allPar['sub'].unique() # get list of unique subjects to loop through

###### get list of subjects with N acceptable blocks ######


for condition in (['HighLarge', 'HighSmall', 'LowLarge', 'LowSmall', 'OfficeLarge', 'OfficeSmall']):

    # initiate empty list to append subjects to
    temp = []

    for sub in subs:

        # select rows for subject
        sub_df = censor_summary_allPar.loc[censor_summary_allPar['sub'] == sub]

        # count the number of blocks with good TRs > min_blockTR
        column = sub_df[condition]
        nblocks = column[column >= min_blockTR].count()

        # if number of good blocks is above threshold, add ID to list
        if nblocks >= min_block:
            temp.append(sub)

    # format IDs -- pad with zeros to 3 digits 
    temp = [str(sub).zfill(3) for sub in temp]

    # define output path
    file = bids_path.joinpath('derivatives/analyses/FoodCue-fmri/Level2GLM/Activation_Univariate/ses-1/index-' + condition + '_' + str(TR_cen_critera) + "_" + str(min_blockTR) + 'tr-' + str(min_block) + 'b.txt')
    
    # write to file
    with open(file, 'w') as indexFile:
        joined_list = "  ".join(temp)
        print(joined_list , file = indexFile)
