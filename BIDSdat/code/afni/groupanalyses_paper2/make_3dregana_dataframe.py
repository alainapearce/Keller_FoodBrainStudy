#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to generate a dataframe for brain and intake analyses with 3dRegAna. 

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
import re


##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################
def gen_dataframe(template, index_file):

    # get script location
    script_path = Path(__file__).parent.resolve()

    # change directory to base directory (BIDSdat) and get path
    os.chdir(script_path)
    os.chdir('../../..')
    pardata_directory = Path(os.getcwd())
    #bids_directory = Path(os.getcwd())

    #set specific paths
    bids_path = Path(pardata_directory).joinpath('BIDSdat')
    bids_indexpath = Path(pardata_directory).joinpath('BIDSdat/derivatives/analyses/foodcue-paper2/level2')
    database_path = Path(pardata_directory).joinpath('Databases')
    intake_res_path = Path(pardata_directory).joinpath('BIDSdat/derivatives/analyses/intake/')

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
        raise Exception()

    # get level1 folder from index_file
    index_split = index_file.split("_") # split index_file by '_' into a list
    lev1_censor_str = "_".join(index_split[2:4]) # join the 2nd and 3rd items from temp
    folder = str(template) + '_' + str(lev1_censor_str)

    ## Make a dataframe with subjects for analyses
    sub_include = pd.DataFrame() #create empty dataframe
    sub_include['sub'] = subs_list #add subjects to column sub

    # Add intake information to sub_include
    feis_df = pd.read_csv(Path(intake_res_path).joinpath('intake_feis.csv')) # import anthro database
    feis_df['sub'] = feis_df['sub'].astype(int) # get rid of decimal place
    feis_df['sub'] = feis_df['sub'].astype(str) # convert to string -- needed for zfill
    feis_df['sub'] = feis_df['sub'].str.zfill(3) # add leading zeros

    sub_include = pd.merge(sub_include,feis_df[['sub','kcal_ps_lin',]],on='sub', how='inner') #innter means only include keys found in both dataframes

    ###############################################################
    #### Generate DataTable for 3dRegAna -- kcal_lin vs PS contrast 
    ###############################################################
    regana_table = pd.DataFrame(columns=['-xydata', 'kcal_lin', 'InputFile', '\\'])

    for i in range(len(sub_include)):

        # get subject
        id_nozeros = int(sub_include.loc[i,['sub']])
        sub_id = str(id_nozeros).zfill(3)

        # get kcal_ps_lin
        kcal_ps_lin = sub_include.loc[i,['kcal_ps_lin']][0]

        # create and append row for Large PS ED contrast
        input_file = '/gpfs/group/klk37/default/R01_Food_Brain_Study/BIDS/derivatives/analyses/foodcue-paper2/level1/sub-' + sub_id + '/' + folder + '/stats.sub-' + sub_id + '+tlrc.HEAD[Food-Office_GLT#0_Coef]'
        subject_row = ['-xydata', kcal_ps_lin, input_file, '\\' ]
        regana_table = regana_table.append(pd.DataFrame([subject_row],
            columns=['-xydata', 'kcal_lin', 'InputFile', '\\']),
            ignore_index=True)

    # remove '\' from last row in datatable
    regana_table.loc[regana_table.index[-1], '\\']= ""

    # get full censor string from index file name, with .txt at the end
    censor_str = re.split('index_all_',index_file)[1]

    # write dataframe
    regana_table.to_csv(str(Path(bids_path).joinpath('derivatives/analyses/foodcue-paper2/level2/regana_PScon-intake-' + str(censor_str))), sep = '\t', encoding='ascii', index = False)

 
    # get list of subject ids 
    sub_list = list(sub_include['sub'])

    # set index file name
    file = bids_path.joinpath(('derivatives/analyses/foodcue-paper2/level2/index_regana_PScon-intake-' + str(censor_str) + '.txt'))

    # write index file with subject IDs
    with open(file, 'w') as indexFile:
        indexFile.write("\n".join(sub_list))
