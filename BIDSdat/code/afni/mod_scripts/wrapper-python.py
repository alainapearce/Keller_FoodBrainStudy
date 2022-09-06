#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to run python functions related to generating onsets and censorfiles 
that will be used for analyses with AFNI. 

Written by Bari Fuchs in August 2022

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
from aem import con
from pathlib import Path
import os

# import data processing functions
import p1_getonsets
import p2_create_censor_files
import p4a_gen_byrun_onsets
import p4b_gen_byblock_onsets


##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################

##############
### Set up ###
##############

# get script location
script_path = Path(__file__).parent.resolve()

# change directory to base directory (BIDSdat) and get path
os.chdir(script_path)
os.chdir('../../..')
base_directory = Path(os.getcwd())

#set specific paths
bids_raw_path = Path(base_directory).joinpath('raw_data')
bids_deriv_onsetfiles = Path(base_directory).joinpath('derivatives/preprocessed/foodcue_onsetfiles/orig')
    

###############################
### Get list of subject IDs ###
###############################

#find all foodcue*events.tsv files
foodcue_raw_files = list(Path(bids_raw_path).rglob('sub-*/ses-1/func/*foodcue*events.tsv'))

# get unique ids from foodcue_raw_files
##pathlib library -- .relative_to give all the path that follows raw_data_path
##                  .parts[0] extracts the first directory in remaining path to get
##                       list of subjects
foodcue_raw_subs = [item.relative_to(bids_raw_path).parts[0] for item in foodcue_raw_files]

##set is finding only unique values
subs = list(set([item[4:7] for item in foodcue_raw_subs]))   

# For testing
#subs = ['001', '002']

###################################
### call functions for each sub ###
###################################

for sub in subs:

     try:
          p1_getonsets.p1_getonsets(par_id = sub, overwrite=False)
     except:
          print("Discontinuing p1_getonsets() for sub_" + sub)

     try:
          p2_create_censor_files.p2_create_censor_files(par_id = sub, framewise_displacement = 0.9, std_vars=False, cen_prev_tr=False, overwrite=True)
     except:
          print("Discontinuing p2_create_censor_files() for sub_" + sub)

     try:
          p4a_gen_byrun_onsets.p4a_gen_byrun_onsets(par_id = sub, censorsum_file = 'task-foodcue_censorsummary_fd-0.9.tsv', p_thresh_run = False, p_thresh_block = 20)
     except:
          print("Discontinuing p4a_gen_byrun_onsets() for sub_" + sub)

     try:
          p4b_gen_byblock_onsets.p4b_gen_byblock_onsets(par_id = sub, censorsum_file = 'task-foodcue_bycond-censorsummary_fd-0.9.tsv', minblockTR = 7)
     except:
          print("Discontinuing p4b_gen_byblock_onsets() for sub_" + sub)
