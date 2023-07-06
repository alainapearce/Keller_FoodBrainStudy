#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to run python functions related to generating index files and covariate table for AFNI

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
from pathlib import Path
import os

# import functions
import prep_index_byrun
import prep_index_byblock
import prep_avg_motion
import prep_3dttest_covTable
import prep_index_PM

#########################################################
### Get list of subjects with processed fmriprep data ###
#########################################################

# get script location
script_path = Path(__file__).parent.resolve()

# change directory to base directory (BIDSdat) and get path
os.chdir(script_path)
os.chdir('../../..')
base_directory = Path(os.getcwd())

#set specific paths
bids_fmriprep_path = Path(base_directory).joinpath('derivatives/preprocessed/fmriprep')
lev1 = Path(base_directory).joinpath('derivatives/analyses/foodcue_paper1/level1/')

#find all confounds_timeseries.tsv
confound_files = list(Path(bids_fmriprep_path).rglob('sub-*/ses-1/func/*task-foodcue_run*confounds_timeseries.tsv'))

# get unique ids from foodcue_raw_files that start with 'sub'
confound_subs = [item.relative_to(bids_fmriprep_path).parts[0] for item in confound_files]
confound_subs_clean = [x for x in confound_subs if x.startswith('sub')]

##set is finding only unique values
subs = list(set([item[4:7] for item in confound_subs_clean]))   

#####################
### Run functions ###
#####################

# Generate index files

prep_index_byrun.gen_index_byrun(onset_dir = 'fd-0.9_b20', nruns = 3, preproc_path = False)

# Calculate average motion variables -- included in covariate table by make_3dttest_covTable()
for sub in subs:

     try:
           prep_avg_motion.get_avg_fd(par_id = sub, preproc_path=False, overwrite=False)
     except:
            print("Discontinuing calc_avg_motion() for sub_" + sub)

## Generate covariate table
prep_3dttest_covTable.gen_dataframe()

# Generate index file for PM analyses
prep_index_PM.gen_index_PM()

