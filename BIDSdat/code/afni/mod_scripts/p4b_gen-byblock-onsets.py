#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to generate onset files that censor blocks with bad motion based on specified threshold
This script will reference task-foodcue_bycond-censorsummary_fd-XX.tsv, generated by 4c_byblock-motion-summary.py

Written by Bari Fuchs in Summer 2022

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
import pandas as pd
import os
from pathlib import Path
import re


##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################

def p4b_gen_byblock_onsets(par_id, censorsum_file, minblockTR):

    """Function to generate onset files that censor blocks with excessive motion based on specified threshold
    Inputs:
        par_id (int): participant ID 
        censorsumfile (string): name of censor summary file (e.g., task-foodcue_censorsummary_fd-1.0.tsv
        minblockTR (int): threshold for censoring blocks. This is the minimum number of uncensored TRs for a block to be included
    Outputs:
        onsetfile_dat: 1 onset dataframe per condition, exported as a csv. Onsets for blocks with motion that exceeds
            minblockTR will replaced with '*'
    """

    # get script location
    script_path = Path(__file__).parent.resolve()

    # change directory to base directory (BIDSdat) and get path
    os.chdir(script_path)
    os.chdir('../../..')
    base_directory = Path(os.getcwd())

    #set specific paths
    bids_onset_path = Path(base_directory).joinpath('derivatives/preprocessed/foodcue_onsetfiles')
    bids_origonset_path = Path(base_directory).joinpath('derivatives/preprocessed/foodcue_onsetfiles/orig')
    bids_fmriprep_path = Path(base_directory).joinpath('derivatives/preprocessed/fmriprep')

    # set sub with leading zeros
    sub = str(par_id).zfill(3)

    # Import censor summary database
    censor_summary_path = Path(bids_fmriprep_path).joinpath( str(censorsum_file))

    # extract criteria used to censor TRs based on censor summary database name
    substring = censorsum_file.split("summary_",1)[1]
    TR_cen_critera = substring.split(".tsv",1)[0]

    if censor_summary_path.is_file(): # if database exists
        # import database
        censor_summary_allPar = pd.read_csv(str(censor_summary_path), sep = '\t')

        # check that subject ID is in censor_summary_allPar
        if (sub not in set(censor_summary_allPar['sub'])):
            print(sub + "has no data in in censorsum_file")
            exit
    else:
        print("censor summary file does not exist")
        exit

    #########################################
    #### Generate new onset timing files ####
    #########################################

    # Get original onset files -- sub needs to be padded with leading zeros
    orig_onsetfiles = list(Path(bids_origonset_path).rglob('sub-' + str(sub).zfill(3) + '*AFNIonsets.txt'))

    # Loop through onset files (there is 1 onset file per condition)
    for onsetfile in orig_onsetfiles:

        # get file name
        filename = onsetfile.stem

        # get condition 
        cond = re.split('_|-',filename)[2]
    
        #load file
        onsetfile_dat = pd.read_csv(str(onsetfile), sep = '\t', encoding = 'utf-8-sig', engine='python', header=None)

        # Loop through rows in onset file (row i corresponds to run i+1)
        for i in range(len(onsetfile_dat)):

            # get run number
            runnum = i + 1

            # get number of uncensored TRs in block for condition and run
            row = censor_summary_allPar[(censor_summary_allPar['sub'] == sub) & (censor_summary_allPar['run'] == int(runnum))] #select row based on sub and runnum
            block_goodTRs = int(row[cond]) #get value from column that matches condition

            ## if number of uncensored TRs < min_blockTR 
            if block_goodTRs < minblockTR:

                # Change corresonding value in onset file to "*"
                pd.options.mode.chained_assignment = None  # disable SettingWithCopyWarning
                onsetfile_dat[0].iloc[i] = '*' ## gives SettingWithCopyWarning

        ## output new onsetfile ##

        # set path to new onset directory
        new_onset_path = Path(bids_onset_path).joinpath(str(TR_cen_critera) + '_by-block-' + str(minblockTR))

        # Check whether the onset directory exists or not
        isExist = os.path.exists(new_onset_path)
        if not isExist:
            # make new path
            os.makedirs(new_onset_path)
            
        # write file
        onsetfile_dat.to_csv(str(Path(new_onset_path).joinpath(filename + '.txt')), sep = '\t', encoding='utf-8-sig', index = False, header=False)