#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to generate a dataframe for analyses with 3dlme using "by block" cleaning critiera. 

(1) count the number of subjects to be included in analyses 
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
from xxlimited import foo
import pandas as pd
import os
from pathlib import Path
import re


##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################
def gen_dataframe(template, censor_str):
    """Function to 

        inputs:
            example censor_str = 'fd-0.9_by-block-7_3blocks'
    """

    # get script location
    script_path = Path(__file__).parent.resolve()

    # change directory to base directory (BIDSdat) and get path
    os.chdir(script_path)
    os.chdir('../../..')
    pardata_directory = Path(os.getcwd())
    #bids_directory = Path(os.getcwd())

    #set specific paths
    bids_path = Path(pardata_directory).joinpath('BIDSdat')
    bids_indexpath = Path(pardata_directory).joinpath('BIDSdat/derivatives/analyses/FoodCue-fmri/Level2GLM/Activation_Univariate/ses-1/')
    database_path = Path(pardata_directory).joinpath('Databases')

    # set list of food conditions
    food_cond_dict = dict.fromkeys(["HighLarge", "HighSmall", "LowLarge", "LowSmall"])

    for cond in food_cond_dict:
        print(cond)

        # import index file
        indexfile_path = Path(bids_indexpath).joinpath('index-' + str(cond) + '_' + str(censor_str) + '.txt')

        if indexfile_path.is_file():
            indexfile = open(indexfile_path, "r") #open file
            subs_str = indexfile.read() #read file
            subs_str = subs_str.strip() #strip /n from string
            subs_list = subs_str.split("  ") #split string into list
            food_cond_dict[cond] = subs_list # save list to dictionary
            indexfile.close() #close file
        else:
            print("index file does not exist")
            raise Exception()


    # get level1 folder from index_file
    index_split = censor_str.split("_") # split index_file by '_' into a list
    lev1_censor_str = "_".join(index_split[0:2]) # join the 1st and 2nd items from temp
    folder = str(template) + '_' + str(lev1_censor_str)

    ####################################
    #### Generate DataTable for 3dlme
    ####################################
    lme_df = pd.DataFrame(columns=['Subj', 'ED', 'PS' ,'InputFile', '\\'])

    for cond in food_cond_dict.keys():

        # get energy density conditions
        if 'High' in cond:
            ED = 'High'
        else:
            ED = 'Low'

        # get portion size condition
        if 'Large' in cond:
            PS = 'Large'
        else:
            PS = 'Small'
        
        for sub in food_cond_dict[cond]:

            # create and append row for subject and condition
            input_file = '/gpfs/group/klk37/default/R01_Food_Brain_Study/BIDS/derivatives/analyses/FoodCue-fmri/Level1GLM/sub-' + str(sub) + '/' + folder + '/stats.sub-' + str(sub) + '+tlrc.HEAD[' + str(cond) + '#0_Coef]'
            subject_row = [sub, ED, PS ,input_file, '\\']
            lme_df = lme_df.append(pd.DataFrame([subject_row],
                columns=['Subj', 'ED', 'PS' ,'InputFile', '\\']),
                ignore_index=True)

    # remove '\' from last row in datatable
    lme_df.loc[lme_df.index[-1], '\\']= ""

    # write dataframe
    lme_df.to_csv(str(Path(bids_path).joinpath('derivatives/analyses/FoodCue-fmri/Level2GLM/Activation_Univariate/ses-1/lme_ED-PS_' + str(censor_str) + '.txt')), sep = '\t', encoding='ascii', index = False)
