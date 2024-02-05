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


##############################################################################
####                                                                      ####
####                             Main Function                            ####
####                                                                      ####
##############################################################################

def gen_index_PM():

    """Function to generate index files that list subjects to be included in parametric analyses. 
        Subjects included will those included in index_all_fd-0.9_b20_3runs.txt (generated by prep_index_byrun.py) with 
        the exception of subjects with missing behavioral data or insufficient variability in behavioral data. 
        Subjects to be excluded were determined using beh_analyses.Rmd and analyze_ratings.Rmd
    
    Outputs:
        2 "index files" (text files) with list of subject IDs to be included in parametric analyses

    """

    # get script location
    script_path = Path(__file__).parent.resolve()

    # change directory to base directory (BIDSdat) and get path
    os.chdir(script_path)
    os.chdir('../../..')
    base_directory = Path(os.getcwd())

    # set path to level 2 directory 
    lev2_path = Path(base_directory).joinpath('derivatives/analyses/foodcue-paper1/level2')

    # Set index file
    index_file_path = Path(lev2_path).joinpath( str('index_all_fd-0.9_b20_3runs.txt'))

    # Raise Exception if index_file_path is not a file, else process it 
    if index_file_path.is_file() is False:
        print("index_all_fd-0.9_b20_3runs.txt. Run prep_index_byrun() first")
        raise Exception
    else:
        # open and read in file
        index_file = index_file_path.open('r') # open index file
        index_string = index_file.read() # read index file
        index_file.close() # close index file

        # replace end of line('/n') with ' ', split into list on tab
        index_list = index_string.replace('\n', ' ').split("  ")
        
        # initialize PM index lists
        index_list_pwant_ED = []
        index_list_pwant_PS = []
        index_list_pwant_office = []

        # add subs to PM index lists if they are not listed
            # 011, 020, 028, 039 -- excluded from all lists for %want analyses due to missing data for at least 1 block
            # 004, 040, 058 -- excluded from index_list_PM_ED due to lack of variability in at least 1 condition when grouping by ED
            # 004, 040 -- excluded from index_list_PM_PS due to lack of variability in at least 1 condition when grouping by PS
            # 004, 017, 026, 049, 056, 084, 089, 116 -- excluded from index_list_PM_office due to lack of variability in office conditon

        for sub in index_list:
            if sub not in ('011', '020', '028', '039','004', '040', '058'):
                index_list_pwant_ED.append(sub)
            if sub not in ('011', '020', '028', '039','004', '040'):
                index_list_pwant_PS.append(sub)
            if sub not in ('011', '020', '028', '039','004', '017', '026', '049', '056', '084', '089', '116'):
                index_list_pwant_office.append(sub)

        # create index lists for sensitivity analyses without 054. this subject is missing data for snack_intake covariate                
        sensitivity_index_list_pwant_ED = [value for value in index_list_pwant_ED if value != '054']
        sensitivity_index_list_pwant_PS = [value for value in index_list_pwant_PS if value != '054']
        sensitivity_index_list_pwant_office = [value for value in index_list_pwant_office if value != '054']

        # set file names
        file_pwant_ED = lev2_path.joinpath('index_fd-0.9_b20_3runs_PM-ED.txt')
        file_pwant_PS = lev2_path.joinpath('index_fd-0.9_b20_3runs_PM-PS.txt')
        file_pwant_office = lev2_path.joinpath('index_fd-0.9_b20_3runs_PM-office.txt')
        file_pwant_ED_sensitivity = lev2_path.joinpath('index_sensitivity_fd-0.9_b20_3runs_PM-ED.txt')
        file_pwant_PS_sensitivity = lev2_path.joinpath('index_sensitivity_fd-0.9_b20_3runs_PM-PS.txt')
        file_pwant_office_sensitivity = lev2_path.joinpath('index_sensitivity_fd-0.9_b20_3runs_PM-office.txt')

        # write ids to file
        with open(file_pwant_ED, 'w') as output_file_name:
            joined_list = "  ".join(index_list_pwant_ED)
            print(joined_list , file = output_file_name)

        with open(file_pwant_PS, 'w') as output_file_name:
            joined_list = "  ".join(index_list_pwant_PS)
            print(joined_list , file = output_file_name)

        with open(file_pwant_office, 'w') as output_file_name:
            joined_list = "  ".join(index_list_pwant_office)
            print(joined_list , file = output_file_name)

        with open(file_pwant_ED_sensitivity, 'w') as output_file_name:
            joined_list = "  ".join(sensitivity_index_list_pwant_ED)
            print(joined_list , file = output_file_name)

        with open(file_pwant_PS_sensitivity, 'w') as output_file_name:
            joined_list = "  ".join(sensitivity_index_list_pwant_PS)
            print(joined_list , file = output_file_name)

        with open(file_pwant_office_sensitivity, 'w') as output_file_name:
            joined_list = "  ".join(sensitivity_index_list_pwant_office)
            print(joined_list , file = output_file_name)
