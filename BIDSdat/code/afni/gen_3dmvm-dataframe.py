#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to generate a dataframe for analyses with 3dMVM. 

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
import pandas as pd
import os
from pathlib import Path


##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################
def gen_dataframe(index_file):

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

    # Import index file
    indexfile_path = Path(bids_indexpath).joinpath( str(index_file))

    # if database exists
    if indexfile_path.is_file():
        indexfile = open(indexfile_path, "r") #open file
        subs_str = indexfile.read() #read file
        subs_str = subs_str.strip() #strip /n from string
        subs_list = subs_str.split("  ") #split string into list
        indexfile.close() #close file
    else:
        print("index file does not exist")

    ## Make a dataframe with subjects for analyses
    sub_include = pd.DataFrame() #create empty dataframe
    sub_include['id'] = subs_list #add subjects to column sub

    # Add risk information to sub_include
    anthro_df = pd.read_spss(Path(database_path).joinpath('anthro_data.sav')) # import anthro database
    anthro_df['id'] = anthro_df['id'].astype(int) # get rid of decimal place
    anthro_df['id'] = anthro_df['id'].astype(str) # convert to string -- needed for zfill
    anthro_df['id'] = anthro_df['id'].str.zfill(3) # add leading zeros

    sub_include = pd.merge(sub_include,anthro_df[['id','risk_status_mom']],on='id', how='left')

    ################################################################
    #### Generate DataTable for 3dMVM -- ED contrast x PS x risk ###
    ################################################################
    MVMdatatable = pd.DataFrame(columns=['Subj','PS', 'risk', 'InputFile', '\\'])

    for i in range(len(sub_include)):

        # get subject
        id_nozeros = int(sub_include.loc[i,['id']])
        sub_id = str(id_nozeros).zfill(3)

        # get risk status
        risk = sub_include.loc[i,['risk_status_mom']][0]
        if risk == 'High Risk':
            risk = 'High'
        if risk == 'Low Risk':
            risk = 'Low'

        # level 1 folder
        folder = 'ped_fd-1.0_b20'

        # create and append row for Large PS ED contrast
        Largepath = '/gpfs/group/klk37/default/R01_Food_Brain_Study/BIDS/derivatives/analyses/FoodCue-fmri/Level1GLM/sub-' + sub_id + '/' + folder + '/stats.sub-' + sub_id + '+tlrc.HEAD[LargeHigh-Low_GLT#0_Coef]'
        LargePSrow = [sub_id, 'Large', risk, Largepath, '\\' ]
        MVMdatatable = MVMdatatable.append(pd.DataFrame([LargePSrow],
            columns=['sub','PS', 'risk', 'InputFile', '\\']),
            ignore_index=True)

        # create and append row for Small PS ED contrast
        Smallpath = '/gpfs/group/klk37/default/R01_Food_Brain_Study/BIDS/derivatives/analyses/FoodCue-fmri/Level1GLM/sub-' + sub_id + '/' + folder + '/stats.sub-' + sub_id + '+tlrc.HEAD[SmallHigh-Low_GLT#0_Coef]'
        SmallPSrow = [sub_id, 'Small', risk, Smallpath, '\\']
        MVMdatatable = MVMdatatable.append(pd.DataFrame([SmallPSrow],
            columns=['sub','PS', 'risk', 'InputFile', '\\']),
            ignore_index=True)

    # write dataframe
    MVMdatatable.to_csv(str(Path(bids_path).joinpath('derivatives/analyses/FoodCue-fmri/Level2GLM/Activation_Univariate/ses-1/dataframe-EDcon-fd-1.0_b20.txt')), sep = '\t', encoding='utf-8-sig', index = False)

