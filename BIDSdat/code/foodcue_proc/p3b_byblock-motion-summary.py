#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to summarize BY BLOCK motion info from censorysummary files generated by 4_create_censor_files. 

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
import pandas as pd
import os
from pathlib import Path

##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################

# get script location
script_path = Path(__file__).parent.resolve()

# change directory to base directory (BIDSdat) and get path
os.chdir(script_path)
os.chdir('../..')
base_directory = Path(os.getcwd())

#set specific paths
bids_onset_path = Path(base_directory).joinpath('derivatives/preprocessed/foodcue_onsetfiles')
bids_origonset_path = Path(base_directory).joinpath('derivatives/preprocessed/foodcue_onsetfiles/orig')
bids_fmriprep_path = Path(base_directory).joinpath('derivatives/preprocessed/fmriprep')

#find all censor summary files
censorsum_files = list(Path(bids_fmriprep_path).rglob('task-foodcue_bycond-censorsummary*'))

#make empty block count summary dataframe -- this table will have 1 row per person, 1 column per condition
nblock_sum = pd.DataFrame(columns=['sub','HighLarge','HighSmall', 'LowLarge', 'LowSmall', 'OfficeLarge', 'OfficeSmall'])

#make empty subject count summary dataframe -- this table will have 1 row per censor threshold
nsub_sum = pd.DataFrame(columns=['censorsum','HighLarge','HighSmall', 'LowLarge', 'LowSmall', 'OfficeLarge', 'OfficeSmall', 'all4food', 'atleast1food', 'bothHighED', 'bothLowED', 'bothLarge', 'bothSmall' ])

# specify list of conditions
conditions = ['HighLarge','HighSmall', 'LowLarge', 'LowSmall', 'OfficeLarge', 'OfficeSmall']

# set minimum number of TRs per block
min_blockTR = 7

############################################################
#### Get number of blocks per condition for each subject ###
############################################################


for i in range(len(censorsum_files)):

    # get file name
    file = censorsum_files[i]

    # load file
    censorsum_df = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python')

    # extract file name without .tsv
    filename = os.path.basename(file).split('.tsv')[0]

    # subset data to remove sub 999 
    censorsum_df = censorsum_df[censorsum_df["sub"] != 999]

    # get unique subjects
    subs = censorsum_df['sub'].unique()

    #loop through subjects
    for s in range(len(subs)):

        # get sub ID
        subnum = subs[s]

        # add subject to summary dataframe in row s
        nblock_sum.at[s, 'sub'] = subnum

        # subset dataframe
        sub_df = censorsum_df.loc[censorsum_df['sub'] == subnum]

        # loop through conditions
        for condition in conditions:

            # select column for condition
            column = sub_df[condition]

            # change column values to integers
            column = column.astype('int')

            # count number of blocks (rows) with 6 or more good TRs
            block_count = column[column >= min_blockTR].count()

            #add summary to table
            nblock_sum.at[s, condition] = block_count

    ############################################################
    #### Get number of subjects with N blocks per condition ####
    ############################################################

    #add file name to table in row i
    nsub_sum.at[i, 'censorsum'] = filename

    # loop through conditions
    for condition in conditions:

        # select column for condition
        column = nblock_sum[condition]
        
        # count number of subjects with 3 or more blocks
        sub_count = column[column >= 3].count()

        #add summary to table
        nsub_sum.at[i, condition] = sub_count

        # print condition and count to terminal
        #print(condition, ": ", sub_count)


    # set minimum number of blocks per condition
    min_block = 3

    # Compute number of participants with enough good blocks for combinations of conditions
    all4foods = nblock_sum[(nblock_sum['HighLarge'] >= min_block) & (nblock_sum['HighSmall'] >= min_block) & (nblock_sum['LowLarge'] >= min_block) & (nblock_sum['LowSmall'] >= min_block)]
    atleast1food = nblock_sum[(nblock_sum['HighLarge'] >= min_block) | (nblock_sum['HighSmall'] >= min_block) | (nblock_sum['LowLarge'] >= min_block) | (nblock_sum['LowSmall'] >= min_block)]
    bothHigh = nblock_sum[(nblock_sum['HighLarge'] >= min_block) & (nblock_sum['HighSmall'] >= min_block)]
    bothLow = nblock_sum[(nblock_sum['LowLarge'] >= min_block) & (nblock_sum['LowSmall'] >= min_block)]
    bothLarge = nblock_sum[(nblock_sum['HighLarge'] >= min_block) & (nblock_sum['LowLarge'] >= min_block)]
    bothSmall = nblock_sum[(nblock_sum['HighSmall'] >= min_block) & (nblock_sum['LowSmall'] >= min_block)]

    #add summary to table
    nsub_sum.at[i, 'all4food'] = len(all4foods)
    nsub_sum.at[i, 'atleast1food'] = len(atleast1food)
    nsub_sum.at[i, 'bothHighED'] = len(bothHigh)
    nsub_sum.at[i, 'bothLowED'] = len(bothLow)
    nsub_sum.at[i, 'bothLarge'] = len(bothLarge)
    nsub_sum.at[i, 'bothSmall'] = len(bothSmall)

# export dataframe
nsub_sum.to_csv(str(Path(bids_fmriprep_path).joinpath('task-foodcue_motion-summary_byblock.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
