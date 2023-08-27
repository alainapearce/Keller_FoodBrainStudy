#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to run python functions related to generating onsets and censorfiles 
that will be used for analyses with AFNI. 

Written by Bari Fuchs in August 2022

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
from pathlib import Path
import os

# import data processing functions
import p1_getonsets
import p2_create_censor_files
import p3_censor_summary


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

# change directory to bids directory (BIDSdat) and get path
os.chdir(script_path)
os.chdir('../../..')
bids_directory = Path(os.getcwd())

#set specific paths
bids_raw_path = Path(bids_directory).joinpath('raw_data')
bids_deriv_onsetfiles = Path(bids_directory).joinpath('derivatives/preprocessed/foodcue_onsetfiles/orig')


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
#subs = ['004']

## For testing with test fixtures
#subs = ['999']

###################################
### call functions for each sub ###
###################################

for sub in subs:

     # set inputs
      if sub == '999':
          preproc_path = str('/Users/baf44/Keller_FoodBrainStudy/BIDSdat/code/foodcue_proc/fixtures/preprocessed')
          censorsum_file_byrun = str('fixture_task_byrun-foodcue_censorsummary_fd-1.0.tsv')
          censorsum_file_bycond = str('fixture_task-foodcue_byblock-censorsummary_fd-1.0.tsv')

      else:
          preproc_path = False
          censorsum_file_byrun = str('task-foodcue_byrun-censorsummary_fd-0.9.tsv')
          censorsum_file_bycond = str('task-foodcue_byblock-censorsummary_fd-0.9.tsv')

      try:
          p1_getonsets.getonsets(par_id = sub, overwrite=False)
      except:
          print("Discontinuing p1_getonsets() for sub_" + sub)

      try:
           p2_create_censor_files.create_censor_files(par_id = sub, overwrite=True, cen_add_tr=False ,preproc_path=preproc_path)
      except:
         print("Discontinuing p2_create_censor_files() for sub_" + sub)

     #  try:
     #      p3_censor_summary.censor_sum(par_id = sub, overwrite=True, preproc_path=preproc_path)
     #  except:
     #      print("Discontinuing p3_censor_summary for sub_" + sub)
