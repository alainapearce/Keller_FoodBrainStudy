#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to (1) count the number of subjects to be included in analyses 
based on motion threshold and (2) generate subject index files for AFNI analyses using 
the output of 4_create_censor_files.py. Index files will list subject IDs that should be 
included in analyses, based on the desired motion threshold. Index files be generated 
for the whole group and separete risk groups.

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

# to overwrite onsets of all input IDs, specify in terminal format like:
#-f

#input arguments setup
parser=argparse.ArgumentParser()
parser.add_argument('--TRcensorCriteria', '-c', help='TR censor criteria string. format = fd-X.X_stddvar-X.X', type=str)
parser.add_argument('--RuncensorCriteria', '-r', help='Run censor criteria percentage', type=int)
parser.add_argument('--generateIndex', '-g', help='Generate index files', action='store_true')

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
TR_censor_threshold = args.TRcensorCriteria
run_censor_threshold = args.RuncensorCriteria

# Import censor summary database for TR censor criteria
censor_summary_path = Path(bids_fmriprep_path).joinpath('task-foodcue_censorsummary_' + str(TR_censor_threshold) + '.tsv')
# if database exists
if censor_summary_path.is_file():
    # import database
    censor_summary_allPar = pd.read_csv(str(Path(bids_fmriprep_path).joinpath('task-foodcue_censorsummary_' + str(TR_censor_threshold) + '.tsv')), sep = '\t')
else:
    print("censor summary file does not exist")

###### get list of subjects with >2 acceptable runs ######

# subset data to remove runs with less than RuncensorCriteria acceptable TRs
good_runs = censor_summary_allPar[censor_summary_allPar["p_censor"] < run_censor_threshold]

# get number of good runs per subject
n_good_persub = good_runs.groupby('sub').size().reset_index(name='n_good_runs')

# Subset data to include subjects with >2 good runs
sub_include = n_good_persub[n_good_persub["n_good_runs"] > 2]

# rename sub column to id to facilitate merge
sub_include=sub_include.rename(columns = {'sub':'id'})

# Add risk information to sub_include
anthro_df = pd.read_spss(Path(database_path).joinpath('anthro_data.sav'))
sub_include = pd.merge(sub_include,anthro_df[['id','risk_status_mom']],on='id', how='left')

# subset based on low and high risk
high_risk_df = sub_include[sub_include["risk_status_mom"] == "High Risk"]
low_risk_df = sub_include[sub_include["risk_status_mom"] == "Low Risk"]

# Get lists of subjects with leading zeros
all_list = [str(sub).zfill(3) for sub in sub_include['id']]
highrisk_list = [str(sub).zfill(3) for sub in high_risk_df['id']]
lowrisk_list = [str(sub).zfill(3) for sub in low_risk_df['id']]

# count total number of subjects to include
print("TR criteria:", TR_censor_threshold, "run %:", run_censor_threshold)
print("N evaluated:", censor_summary_allPar['sub'].nunique())
print("N with >2 good runs:", len(all_list))
print("N high risk with >2 good runs:", len(highrisk_list))
print("N low risk with >2 good runs:", len(lowrisk_list))

# Generate index files for each list
for name in (['all_list', 'highrisk_list', 'lowrisk_list']):
    # get group name
    group = name.split('_', 1)[0]
    # get list of IDs 
    list = globals()[name]
    # define output path
    file = bids_path.joinpath('derivatives/analyses/FoodCue-fmri/Level2GLM/index-' + group + '_' + TR_censor_threshold + '_r' + str(run_censor_threshold) + '.txt')
    # write to file
    with open(file, 'w') as indexFile:
        joined_list = "  ".join(list)
        print(joined_list , file = indexFile)


