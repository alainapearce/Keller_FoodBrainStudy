#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to (1) count the number of subjects to be included in analyses 
based on motion threshold and (2) generate subject index files for AFNI analyses using 
task-foodcue..censorsummary_$censorcritera.tsv files (output of 4_create_censor_files.py). 
Index files will list subject IDs that should be included in analyses, based on the desired motion threshold. 
Index files be generated for the whole group, and can be generated for risk groups using the -byrisk input arg

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
parser.add_argument('--censorsumfile', '-c', help='name of censor summary file (e.g., task-foodcue_censorsummary_fd-1.0.tsv', type=str)
parser.add_argument('--pthresh_r', '-r', help='threshold for censoring runs based on percent of TRs censored across the whole run', type=int)
parser.add_argument('--pthresh_b', '-b', help='threshold for censoring runs based on percent of TRs censored in blocks of interest', type=int)
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
censorsummary_file = args.censorsumfile

# Import censor summary database for TR censor criteria
censor_summary_path = Path(bids_fmriprep_path).joinpath( str(censorsummary_file))

# if database exists
if censor_summary_path.is_file():
    # import database
    censor_summary_allPar = pd.read_csv(str(censor_summary_path), sep = '\t')
else:
    print("censor summary file does not exist")

###### get list of subjects with N acceptable runs ######

# subset data to remove sub 999 
censor_summary_allPar = censor_summary_allPar[censor_summary_allPar["sub"] != 999]

# subset data to remove runs with less than RuncensorCriteria acceptable TRs

# if censoring based on blocks of interest
if (args.pthresh_b is not None) and (args.pthresh_r is None):
    p_thresh_block = args.pthresh_b
    good_runs = censor_summary_allPar[censor_summary_allPar["p_censor_interest"] < p_thresh_block]
    exclude_string = "b" + str(p_thresh_block)
# if censoring based on total run and blocks of interest
elif (args.pthresh_b is not None) and (args.pthresh_r is not None):
    p_thresh_block = args.pthresh_b
    p_thresh_run = args.pthresh_r
    exclude_string = "r" + str(p_thresh_run) + "b" + str(p_thresh_block)
    #good_runs = censor_summary_allPar[censor_summary_allPar["p_censor"] < p_thresh_run]
# if censoring based on total run 
elif (args.pthresh_b is None) and (args.pthresh_r is not None):
    p_thresh_run = args.pthresh_r
    good_runs = censor_summary_allPar[censor_summary_allPar["p_censor"] < p_thresh_run]
    exclude_string = "r" + str(p_thresh_run)

# get number of good runs per subject
n_good_persub = good_runs.groupby('sub').size().reset_index(name='n_good_runs')

# Subset data to include subjects with >2 good runs
sub_include_3runs = n_good_persub[n_good_persub["n_good_runs"] >= 3]
sub_include_2runs = n_good_persub[n_good_persub["n_good_runs"] >= 2]

# rename sub column to id to facilitate merge
sub_include_3runs=sub_include_3runs.rename(columns = {'sub':'id'})
sub_include_2runs=sub_include_2runs.rename(columns = {'sub':'id'})

# Add risk information to sub_include
anthro_df = pd.read_spss(Path(database_path).joinpath('anthro_data.sav'))
sub_include_3runs = pd.merge(sub_include_3runs,anthro_df[['id','risk_status_mom']],on='id', how='left')
sub_include_2runs = pd.merge(sub_include_2runs,anthro_df[['id','risk_status_mom']],on='id', how='left')

# subset based on low and high risk
high_risk_df_3runs = sub_include_3runs[sub_include_3runs["risk_status_mom"] == "High Risk"]
low_risk_df_3runs = sub_include_3runs[sub_include_3runs["risk_status_mom"] == "Low Risk"]

high_risk_df_2runs = sub_include_2runs[sub_include_2runs["risk_status_mom"] == "High Risk"]
low_risk_df_2runs = sub_include_2runs[sub_include_2runs["risk_status_mom"] == "Low Risk"]

# Get lists of subjects with leading zeros
all_3runs = [str(sub).zfill(3) for sub in sub_include_3runs['id']]
highrisk_3runs = [str(sub).zfill(3) for sub in high_risk_df_3runs['id']]
lowrisk_3runs = [str(sub).zfill(3) for sub in low_risk_df_3runs['id']]

all_2runs = [str(sub).zfill(3) for sub in sub_include_2runs['id']]
highrisk_2runs = [str(sub).zfill(3) for sub in high_risk_df_2runs['id']]
lowrisk_2runs = [str(sub).zfill(3) for sub in low_risk_df_2runs['id']]


###########################################
#### Output summary numbers to terminal ###
###########################################

print("N evaluated:", censor_summary_allPar['sub'].nunique())
print("")
print("N with at least 3 good runs:", len(all_3runs))
print("N high risk with at least 3 good runs:", len(highrisk_3runs))
print("N low risk with at least 3 good runs:", len(lowrisk_3runs))
print("")
print("N with at least 2 good runs:", len(all_2runs))
print("N high risk with at least 2 good runs:", len(highrisk_2runs))
print("N low risk with at least 2 good runs:", len(lowrisk_2runs))

###########################################
#### Generate index files for each list ###
###########################################

for name in (['all_3runs', 'highrisk_3runs', 'lowrisk_3runs', 'all_2runs', 'highrisk_2runs', 'lowrisk_2runs']):
    print(name)
    # get group name
    #group = name.split('_', 1)[0]
    group = name
    # get list of IDs 
    list = globals()[name]
    # define output path
    censor_string = censorsummary_file.rsplit('summary_',1)[1][0:-4]
    file = bids_path.joinpath('derivatives/analyses/FoodCue-fmri/Level2GLM/Activation_Univariate/ses-1/index-' + group + '_' + str(censor_string) + "_" + str(exclude_string) + '.txt')
    # write to file
    with open(file, 'w') as indexFile:
        joined_list = "  ".join(list)
        print(joined_list , file = indexFile)


