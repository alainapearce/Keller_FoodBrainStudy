#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to generate a dataframe for analyses with 3dMVM. 

Written by Bari Fuchs in Fall 2022

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
def gen_dataframe(l1_res_folder, index_file):

    # get script location
    script_path = Path(__file__).parent.resolve()

    # change directory to base directory (BIDSdat) and get path
    os.chdir(script_path)
    os.chdir('../../..')
    bids_dir = Path(os.getcwd())

    #set specific paths
    lev2_dirpath = Path(bids_dir).joinpath('derivatives/analyses/foodcue-paper1/level2/')
    covfile_path = Path(bids_dir).joinpath('derivatives/analyses/foodcue-paper1/level2/ttest-covariates.txt')
    indexfile_path = Path(lev2_dirpath).joinpath( str(index_file))

    # load index file
    if indexfile_path.is_file(): # if database exists
        indexfile = open(indexfile_path, "r") #open file
        subs_str = indexfile.read() #read file
        subs_str = subs_str.strip() #strip /n from string
        subs_list = subs_str.split("  ") #split string into list
        indexfile.close() #close file
    else:
        print("index file does not exist")
        raise Exception()

    # load covariate file
    if covfile_path.is_file():
        covfile = pd.read_table(covfile_path)
        covfile['Subj'] = covfile['Subj'].astype(str).str.zfill(3)  # change Subj to string with leading zeros
    else:
        print("covariate file does not exist")
        raise Exception()

    # subset covariate file to subjects included in analyses 
    sample_df = covfile[covfile['Subj'].isin(subs_list)]

    ##########################################################################################################
    #### Generate DataTable for 3dMVM -- portion size contrasts by cue type (hED, lED, office) with covars ###
    ##########################################################################################################

    MVMdatatable = pd.DataFrame(columns=['Subj','cuetype', 'sex', 'ff_premri', 'fd_avg','InputFile'])

    for row in sample_df.itertuples():

        # get values
        id = row.Subj
        sex = row.sex
        ff = row.ff_premri
        fd = row.fd_avg_allruns

        # create and append row for high ED cue, portion size contrast
        hED_path = '/gpfs/group/klk37/default/R01_Food_Brain_Study/BIDS/derivatives/analyses/foodcue-paper1/level1/sub-' + id + '/' + l1_res_folder + '/stats.sub-' + id + '+tlrc.HEAD[HighLarge-Small_GLT#0_Coef]'
        hED_row = [id, 'hED', sex, ff, fd, hED_path]
        MVMdatatable = MVMdatatable.append(pd.DataFrame([hED_row],
            columns=['Subj','cuetype', 'sex', 'ff_premri', 'fd_avg','InputFile']),
            ignore_index=True)

        # create and append row for low ED cue, portion size contrast
        lED_path = '/gpfs/group/klk37/default/R01_Food_Brain_Study/BIDS/derivatives/analyses/foodcue-paper1/level1/sub-' + id + '/' + l1_res_folder + '/stats.sub-' + id + '+tlrc.HEAD[LowLarge-Small_GLT#0_Coef]'
        lED_row = [id, 'lED', sex, ff, fd, lED_path]
        MVMdatatable = MVMdatatable.append(pd.DataFrame([lED_row],
            columns=['Subj','cuetype', 'sex', 'ff_premri', 'fd_avg','InputFile']),
            ignore_index=True)

        # create and append row for low ED cue, portion size contrast
        office_path = '/gpfs/group/klk37/default/R01_Food_Brain_Study/BIDS/derivatives/analyses/foodcue-paper1/level1/sub-' + id + '/' + l1_res_folder + '/stats.sub-' + id + '+tlrc.HEAD[OfficeLarge-Small_GLT#0_Coef]'
        office_row = [id, 'office', sex, ff, fd, office_path]
        MVMdatatable = MVMdatatable.append(pd.DataFrame([office_row],
            columns=['Subj','cuetype', 'sex', 'ff_premri', 'fd_avg','InputFile']),
            ignore_index=True)

    # get full censor string from index file name, with .txt at the end
    censor_str_txt = re.split('index_all_',index_file)[1]
    censor_str = re.split('.txt',censor_str_txt)[0]


    # write dataframe with covariates
    MVMdatatable.to_csv(str(Path(lev2_dirpath).joinpath('mvm-table_' + str(censor_str) + '.csv')), sep = '\t', encoding='ascii', index = False)
