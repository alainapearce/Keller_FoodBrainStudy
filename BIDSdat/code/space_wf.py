#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to process Space Game Task data in Summer 2021 by 
Alaina Pearce.

Copyright (C) 2021 Alaina L Pearce

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

@author: azp271@psu.edu
"""

#set up packages    
import numpy as np
import pandas as pd
import os
import sys, argparse

##############################################################################
####                                                                      ####
####                        Set up script function                        ####
####                                                                      ####
##############################################################################

# to enter multiple subject arguments in terminal format like:
#-p 2 3 -s 1

#input arguments setup
parser=argparse.ArgumentParser()

parser.add_argument('--parIDs', '-p', help='participant list', type=float, nargs="+")
parser.add_argument('--overwrite', '-f', help='force overwrite of existing data')
parser.add_argument('--session', '-s', help='Session number', nargs="+")

args=parser.parse_args()

##############################################################################
####                                                                      ####
####                  Subfunctions called within script                   ####
####                                                                      ####
##############################################################################

## check data function/filter ids
def checkData(subject_list, session_id, base_directory, dat_overwrite):
    import pandas as pd
    from pathlib import Path
    from nipype import Node, DataGrabber
    from collections.abc import Iterable
    
    #raw data
    raw_data_path = Path(base_directory).joinpath('raw_data')

    #database
    database_path = Path(base_directory).joinpath('derivatives/preprocessed/beh/')

    #get session
    #check if session_id is an iterable
    if isinstance(session_id, Iterable) == True:
        session = str(''.join(session_id))
    else:
        session = str(session_id)
        
    session_num = int(session)

    #check if has 1 or 2 session lists
    if isinstance(subject_list[0], str) == True:
        subject_list_use = subject_list
    else:
        session = session_num - 1
        subject_list_use = subject_list[session][0]

    #check for existing data
    if dat_overwrite is False:
        #load data 
        database = Path(database_path).joinpath('task-space_summary.tsv')
        Space_database = pd.read_csv(str(database), sep = '\t', encoding = 'utf-8-sig', header = 0, engine='python')

        #check session in database
        db_sessions = Space_database.ses.unique()

        #if session number is in database
        if session_num in db_sessions:

            Space_database_ses = Space_database.groupby('ses').get_group(session_num)

            subs = list(subject_list_use)

            for sub in subs:

                #check if in database
                if len(Space_database_ses[Space_database_ses['sub']==int(sub)].index.tolist()) > 0:
                    #remove sub if in list that exists in database already
                    print('Skipping sub-' + str(sub) + ' for session' + str(session_num) + ' - Exists in database already.')
                    subject_list_use.remove(sub)
    
    #get file paths
    if len(subject_list_use) > 0:
        template_path = Path('sub-%s/ses-%s/beh/*task-space*.tsv')
        selectfiles = Node(DataGrabber(infields=['subject_ids', 'session_id'],
                      outfields=['sub_files'],
                      base_directory = str(raw_data_path), 
                      template = str(template_path),
                      sort_filelist = True),
          name='selectfiles')
        selectfiles.inputs.session_id = session_id
        selectfiles.inputs.subject_ids = subject_list_use
        
        sub_files = selectfiles.run().outputs.sub_files
        
    else:
        sub_files = 'No subfiles'

    return sub_files

## summary data function
def summarySpace(Space_file, base_directory):
    import numpy as np
    import pandas as pd
    import scipy.io as sio
    from pathlib import Path
    
    ###################################################################
    ####                   Sub-function script                     ####
    
    #need to sub-functions within the function that is called by the node just 
    #like you need to re-import libraries
    def summary_stats(Space_data):
        
        #Earth RT
        earthRT_mean = Space_data.loc[Space_data['rt_earth'] > 0, 'rt_earth'].mean(axis = 0)*1000  
        earthRT_median = Space_data.loc[Space_data['rt_earth'] > 0, 'rt_earth'].median(axis = 0)*1000  

        #Earth missed
        earth_n_miss = Space_data['missed_earth'].sum(axis = 0)
        earth_p_miss = Space_data['missed_earth'].sum(axis = 0)/Space_data['missed_earth'].shape[0]
        
        #Planet RT
        planetRT_mean = Space_data.loc[Space_data['rt_planet'] > 0, 'rt_planet'].mean(axis = 0)*1000  
        planetRT_median = Space_data.loc[Space_data['rt_planet'] > 0, 'rt_planet'].median(axis = 0)*1000  

        #Planet missed
        planet_n_miss = Space_data['missed_planet'].sum(axis = 0)
        planet_p_miss = Space_data['missed_planet'].sum(axis = 0)/Space_data['missed_planet'].shape[0]
        
        #reward rate
        reward_rate = Space_data.loc[(Space_data['missed_earth'] == 0) & (Space_data['missed_planet'] == 0), 'points'].mean(axis = 0)

        #average reward overall across both options
        rewards = Space_data[['rewards1', 'rewards2']].values.tolist()
        rewards_flat = [item for sublist in rewards for item in sublist]
        avg_reward = sum(rewards_flat)/len(rewards_flat)

        #corrected reward rate
        reward_rate_corrected = reward_rate - avg_reward

        #stay probabilities (always won previously as no negatives) for if
        #earth state is same or different
        prob_sameplanet_earthsame = Space_data.loc[(Space_data['same_earth'] == 1) & (Space_data['missed_earth'] == 0) & (Space_data['missed_planet'] == 0), 'same_planet'].mean(axis = 0)
        prob_sameplanet_earthdif = Space_data.loc[(Space_data['same_earth'] == 0) & (Space_data['missed_earth'] == 0) & (Space_data['missed_planet'] == 0), 'same_planet'].mean(axis = 0)

        summary_results = [earthRT_mean, earthRT_median, earth_n_miss, earth_p_miss, planetRT_mean, planetRT_median, 
                            planet_n_miss, planet_p_miss, reward_rate, avg_reward, reward_rate_corrected, 
                            prob_sameplanet_earthsame, prob_sameplanet_earthdif]

        return(summary_results)

    ###################################################################
    ####                Primary function script                    ####
    
    #summary column names
    colnames = ['sub', 'ses', 'block', 'earth_rt_mean', 'earth_rt_median', 'earth_n_miss', 'earth_p_miss', 'planet_rt_mean', 
                'planet_rt_median', 'planet_n_miss', 'planet_p_miss', 'reward_rate', 'avg_reward', 
                'reward_rate_corrected', 'prob_sameplanet_earthsame', 'prob_sameplanet_earthdif']

    #check if str
    if isinstance(Space_file, str):

        #check to see if it is filepath str or 'No subfiles' message
        if '.tsv' in Space_file:
            #if only 1 file, will be string and we want an array
            Space_file = [Space_file]
        else:
            Space_file = []
        
    if len(Space_file) > 0:
    
        #loop counter
        count = 0

        #supress warning
        pd.options.mode.chained_assignment = None

        for file in Space_file:

            #load data 
            Space_ProcData = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python') 

            #add previous trial data
            Space_ProcData['prev_state_earth'] = Space_ProcData['state_earth'].shift(1)
            Space_ProcData['prev_state_earth'] = np.where(np.isnan(Space_ProcData['prev_state_earth']), 0, Space_ProcData['prev_state_earth'])

            Space_ProcData['prev_state_planet'] = Space_ProcData['state_planet'].shift(1)
            Space_ProcData['prev_state_planet'] = np.where(np.isnan(Space_ProcData['prev_state_planet']), 0, Space_ProcData['prev_state_planet'])

            Space_ProcData['same_earth'] = np.where(Space_ProcData['state_earth'] == Space_ProcData['prev_state_earth'], 1, 0)
            Space_ProcData['same_planet'] = np.where(Space_ProcData['state_planet'] == Space_ProcData['prev_state_planet'], 1, 0)

            #summary stats - across all blocks
            all_trials_stat = summary_stats(Space_ProcData)
            all_trials_stat.insert(0, Space_ProcData.loc[0, 'sub'])
            all_trials_stat.insert(1, Space_ProcData.loc[0, 'ses'])
            all_trials_stat.insert(2, 'all')
            
            if count == 0:
                #make summary dataset
                overall_summary_data = pd.DataFrame(all_trials_stat).T
                overall_summary_data.columns = colnames

                #make group_trailsdat dataset
                space_group_trialsdat = Space_ProcData
            else:
                #add to summary dataset
                overall_summary_data.loc[len(overall_summary_data)] = all_trials_stat
            
                #add to group_trailsdat dataset
                space_group_trialsdat = Space_ProcData
                space_group_trialsdat = pd.concat([space_group_trialsdat, Space_ProcData],ignore_index=True)

            # summary stats - by block 
            for b in np.unique(Space_ProcData['block']):
                #get block data
                block_data = Space_ProcData.loc[Space_ProcData['block'] == b]

                #re-do previous trial data base on just current block
                block_data['prev_state_earth'] = block_data['state_earth'].shift(1)
                block_data['prev_state_earth'] = np.where(np.isnan(block_data['prev_state_earth']), 0, block_data['prev_state_earth'])

                block_data['prev_state_planet'] = block_data['state_planet'].shift(1)
                block_data['prev_state_planet'] = np.where(np.isnan(block_data['prev_state_planet']), 0, block_data['prev_state_planet'])

                block_data['same_earth'] = np.where(block_data['state_earth'] == block_data['prev_state_earth'], 1, 0)
                block_data['same_planet'] = np.where(block_data['state_planet'] == block_data['prev_state_planet'], 1, 0)

                #get summary results
                block_trials_stat = summary_stats(block_data)
                block_trials_stat.insert(0, Space_ProcData.loc[0, 'sub'])
                block_trials_stat.insert(1, Space_ProcData.loc[0, 'ses'])

                block_name = 'b' + str(b)
                block_trials_stat.insert(2, block_name)
                
                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = block_trials_stat

            #update count for files loop
            count = 1

    else:
         overall_summary_data = 'no files'
         space_group_trialsdat = 'no files'
            
    return overall_summary_data, space_group_trialsdat

## summary data function
def updateDatabase_save(Space_summary_dat, Space_group_trialdat, overwrite_flag, bids_dir):
    import pandas as pd
    import numpy as np
    from pathlib import Path
    from nipype.interfaces.base import Bunch

    #derivative data path
    derivative_data_path = Path(bids_dir).joinpath('derivatives/preprocessed/beh')

    #function to drop rows based on values
    def filter_rows_by_values(df, sub_values, sesnum):
        #filter based on sub and ses
        return df[(df['sub'].isin(sub_values) == False) & (df['ses'] == sesnum)]

    #### Summary Data ####
    #check to see if it is filepath str or 'no files' message
    if isinstance(Space_summary_dat[0], str):
                
        print('******** No new data to be processed ********')
                
        Space_database_wide = 'no new data files'
        Space_database_blocks = 'no new data files'
    
    else:
        #get a Bunch object if more than 1 participant
        if isinstance(Space_summary_dat, Bunch):
            #get output data from node
            Space_summary_datlist = Space_summary_dat.summarySpace_dat
        
            #combine datasets
            Space_summary_dat = pd.concat(Space_summary_datlist)
        
        #if only 1 participant/dataset then it is a list
        elif isinstance(Space_summary_dat, list):
            if len(Space_summary_dat) == 1:
                Space_summary_dat = Space_summary_dat[0]
            else:
                Space_summary_dat = pd.concat(Space_summary_dat)

        #if a pandas dataframe
        if isinstance(Space_summary_dat, pd.DataFrame):
        
            #get column names
            columnnames = Space_summary_dat.columns
       
            #get session subsets
            db_sessions = Space_summary_dat.ses.unique()
        
            if len(db_sessions) > 1:
                Space_sum_ses1_dat = Space_summary_dat.groupby('ses').get_group(1)
                Space_sum_ses2_dat = Space_summary_dat.groupby('ses').get_group(2)

                #make wide data set
                Space_sum_ses1_wide = Space_sum_ses1_dat.pivot(columns='block', index='sub', values=columnnames[3:16])
                Space_sum_ses1_wide.columns = ['_'.join(col) for col in Space_sum_ses1_wide.columns.reorder_levels(order=[1, 0])]

                Space_sum_ses2_wide = Space_sum_ses2_dat.pivot(columns='block', index='sub', values=columnnames[3:16])
                Space_sum_ses2_wide.columns = ['_'.join(col) for col in Space_sum_ses2_wide.columns.reorder_levels(order=[1, 0])]

                #make the sub index into a dataset column
                Space_sum_ses1_wide = Space_sum_ses1_wide.reset_index(level = 0)
                Space_sum_ses2_wide = Space_sum_ses2_wide.reset_index(level = 0)

                #add session
                Space_sum_ses1_wide.insert(1, 'ses', 1)
                Space_sum_ses2_wide.insert(1, 'ses', 2)

                #concatonate databases
                Space_summary_wide = pd.concat([Space_sum_ses1_wide,Space_sum_ses2_wide],ignore_index=True)
            
            else:
                #make wide data set
                Space_summary_wide = Space_summary_dat.pivot(columns='block', index='sub', values=columnnames[3:16])
                Space_summary_wide.columns = ['_'.join(col) for col in Space_summary_wide.columns.reorder_levels(order=[1, 0])]
        
                #make the sub index into a dataset column
                Space_summary_wide = Space_summary_wide.reset_index(level = 0)

                #add session
                Space_summary_wide.insert(1, 'ses', db_sessions[0])

            #re-order columns
            columnnames_reorder = ['sub', 'ses', 'all_earth_rt_mean', 'all_earth_rt_median', 'all_earth_n_miss', 'all_earth_p_miss', 'all_planet_rt_mean', 'all_planet_rt_median', 'all_planet_n_miss',  'all_planet_p_miss', 'all_reward_rate', 'all_avg_reward', 'all_reward_rate_corrected',  'all_prob_sameplanet_earthsame', 'all_prob_sameplanet_earthdif', 'b1_earth_rt_mean', 'b1_earth_rt_median', 'b1_earth_n_miss', 'b1_earth_p_miss', 'b1_planet_rt_mean', 'b1_planet_rt_median', 'b1_planet_n_miss', 'b1_planet_p_miss', 'b1_reward_rate', 'b1_avg_reward', 'b1_reward_rate_corrected', 'b1_prob_sameplanet_earthsame','b1_prob_sameplanet_earthdif', 'b2_earth_rt_mean', 'b2_earth_rt_median', 'b2_earth_n_miss', 'b2_earth_p_miss', 'b2_planet_rt_mean', 'b2_planet_rt_median', 'b2_planet_n_miss', 'b2_planet_p_miss', 'b2_reward_rate', 'b2_avg_reward', 'b2_reward_rate_corrected', 'b2_prob_sameplanet_earthsame', 'b2_prob_sameplanet_earthdif', 'b3_earth_rt_mean', 'b3_earth_rt_median', 'b3_earth_n_miss', 'b3_earth_p_miss', 'b3_planet_rt_mean','b3_planet_rt_median', 'b3_planet_n_miss', 'b3_planet_p_miss', 'b3_reward_rate', 'b3_avg_reward', 'b3_reward_rate_corrected', 'b3_prob_sameplanet_earthsame', 'b3_prob_sameplanet_earthdif', 'b4_earth_rt_mean', 'b4_earth_rt_median', 'b4_earth_n_miss', 'b4_earth_p_miss',  'b4_planet_rt_mean', 'b4_planet_rt_median', 'b4_planet_n_miss', 'b4_planet_p_miss',   'b4_reward_rate', 'b4_avg_reward', 'b4_reward_rate_corrected', 'b4_prob_sameplanet_earthsame', 'b4_prob_sameplanet_earthdif']
        
            Space_summary_wide = Space_summary_wide.reindex(columns=columnnames_reorder)
    
            #get blocks subset
            Space_summary_blocks = Space_summary_dat[Space_summary_dat.block.isin(['b1', 'b2', 'b3', 'b4'])]
    
            #load databases
            Space_database_wide = pd.read_csv(str(Path(derivative_data_path).joinpath('task-space_summary.tsv')), sep = '\t')
            Space_database_blocks = pd.read_csv(str(Path(derivative_data_path).joinpath('task-space_summary_long.tsv')), sep = '\t')

            #if overwriting participants
            if overwrite_flag == True:
                #filter out/remove exisiting subs to overwrit~
                if len(db_sessions) > 1:
                    #get list of subs by ses to filter in wide and long data
                    wide_sub_list = Space_summary_wide.groupby('ses')['sub'].unique()
                    long_sub_list = Space_summary_blocks.groupby('ses')['sub'].unique()

                    Space_database_ses1 = filter_rows_by_values(Space_database_wide, wide_sub_list[0], 1)
                    Space_database_ses2 = filter_rows_by_values(Space_database_wide, wide_sub_list[1], 2)

                    Space_database_ses1_long = filter_rows_by_values(Space_database_blocks, long_sub_list[0], 1)
                    Space_database_ses2_long = filter_rows_by_values(Space_database_blocks, long_sub_list[1], 2)

                    #concatonate databases
                    Space_database_wide = pd.concat([Space_database_ses1, Space_database_ses2],ignore_index=True)
                    Space_database_blocks = pd.concat([Space_database_ses1_long, Space_database_ses2_long],ignore_index=True)

                else:
                    wide_sub_list = list(Space_summary_wide['sub'].unique())
                    long_sub_list = list(Space_summary_blocks['sub'].unique())

                    #filter by ses and sub
                    Space_database_ses = filter_rows_by_values(Space_database_wide, wide_sub_list, db_sessions[0])
                    Space_database_long_ses = filter_rows_by_values(Space_database_blocks, long_sub_list, db_sessions[0])

                    #concatonate with other session in full database
                    Space_database_wide = pd.concat([Space_database_wide[Space_database_wide['ses'] != db_sessions[0]], Space_database_ses],ignore_index=True)
                    Space_database_blocks = pd.concat([Space_database_blocks[Space_database_blocks['ses'] != db_sessions[0]], Space_database_long_ses],ignore_index=True)

        
            #add newly processed data
            Space_database_wide = Space_database_wide.append(Space_summary_wide)
            Space_database_blocks = Space_database_blocks.append(Space_summary_blocks)

            #sort to ensure in sub order
            Space_database_wide = Space_database_wide.sort_values(by = ['ses', 'sub'])
            Space_database_blocks = Space_database_blocks.sort_values(by = ['ses', 'sub', 'block'])
        
            #round to 3 decimal points
            Space_database_wide = Space_database_wide.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)
            Space_database_blocks = Space_database_blocks.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)
        
            #write databases
            Space_database_wide.to_csv(str(Path(derivative_data_path).joinpath('task-space_summary.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
            Space_database_blocks.to_csv(str(Path(derivative_data_path).joinpath('task-space_summary_long.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
    
        else:
            print('No raw data files that need to be processed')
            Space_database_wide = np.nan
            Space_database_blocks = np.nan

    #### Group trial data ####
    if isinstance(Space_group_trialdat[0], str):
                
        print('******** No new data to be processed ********')
            
        Space_groupdat = 'no new data files'
        
    else:
        #get a Bunch object if more than 1 participant
        if isinstance(Space_group_trialdat, Bunch):
            #get output data from node
            Space_group_trialdatlist = Space_group_trialdat.group_trialdat
        
            #combine datasets
            Space_groupdat = pd.concat(Space_group_trialdatlist)
        
        #if only 1 participant/dataset then it is a list
        elif isinstance(Space_group_trialdat, list):
            if len(Space_group_trialdat) == 1:
                Space_groupdat = Space_group_trialdat[0]
            else:
                Space_groupdat = pd.concat(Space_group_trialdat)

        #if a pandas dataframe
        if isinstance(Space_groupdat, pd.DataFrame):
       
            #get session subsets
            db_group_sessions = Space_groupdat.ses.unique()

            #load databases
            Space_groupdat_database = pd.read_csv(str(Path(derivative_data_path).joinpath('task-space_groupdata.tsv')), sep = '\t')

            #if overwriting participants
            if overwrite_flag == True:
                #filter out/remove exisiting subs to overwrit~
                if len(db_group_sessions) > 1:
                    #get list of subs by ses to filter in wide and long data
                    dat_sub_list = Space_groupdat.groupby('ses')['sub'].unique()

                    Space_groupdat_ses1 = filter_rows_by_values(Space_groupdat_database, dat_sub_list[0], 1)
                    Space_groupdat_ses2 = filter_rows_by_values(Space_groupdat_database, dat_sub_list[1], 2)

                    #concatonate databases
                    Space_groupdat_database = pd.concat([Space_groupdat_ses1, Space_groupdat_ses2],ignore_index=True)

                else:
                    dat_sub_list = list(Space_groupdat['sub'].unique())

                    #filter by ses and sub
                    Space_groupdat_ses = filter_rows_by_values(Space_groupdat_database, dat_sub_list, db_group_sessions[0])

                    #concatonate with other session in full database
                    Space_groupdat_database = pd.concat([Space_groupdat_database[Space_groupdat_database['ses'] != db_group_sessions[0]], Space_groupdat_ses],ignore_index=True)

            #add newly processed data
            Space_groupdat_database = Space_groupdat_database.append(Space_groupdat)

            #sort to ensure in sub order
            Space_groupdat_database = Space_groupdat_database.sort_values(by = ['sub', 'ses'])

            #round to 3 decimal points
            Space_groupdat_database = Space_groupdat_database.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)
        
            #write databases
            Space_groupdat_database.to_csv(str(Path(derivative_data_path).joinpath('task-space_groupdata.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
    
        else:
            print('No raw trial data files that need to be processed')
            Space_groupdat = np.nan
    
    return Space_database_wide, Space_database_blocks, Space_groupdat

##############################################################################
####                                                                      ####
####                       Primary Workflow Script                        ####
####                                                                      ####
##############################################################################

#Set up workflow
from nipype import Workflow, Node, Function, DataGrabber, MapNode, IdentityInterface
from pathlib import Path

# get script location
script_path = Path(os.path.dirname(__file__))

# change directory to base directory and get path
os.chdir(script_path)
os.chdir('..')

#bids
base_directory = Path(os.getcwd())

#raw data
raw_data_path = Path(base_directory).joinpath('raw_data')

#database
database_path = Path(base_directory).joinpath('derivatives/preprocessed/beh/')

#check for input arguments
if args.overwrite is None:
    dat_overwrite = False
else:
    dat_overwrite = True

#session argument entered       
if args.session is not None:

    #make sure have integer
    session = int(args.session)

    #check for input arguments         
    if args.parIDs is not None and len(args.parIDs) >= 1:

        #make sure have integers
        subject_ids = list(map(int, args.parIDs))

        #get leading zeros
        subject_list = [str(item).zfill(3) for item in subject_ids]
        
        #check for raw data
        subs = list(subject_list)

        for sub in subs:

            raw_file = list(Path(raw_data_path).rglob('sub-' + str(sub) + '/ses-' + str(session) + '/beh/*space*.tsv'))

            if len(raw_file) < 1:
                print('No Files found for sub-' + str(sub) + ' and session ' + str(session))
                subject_list.remove(sub)
        
        #check if any files to process
        if subject_list is None:
            sys.exit('No Files found for participants' + args.parIDs + ' for session ' + str(session))      
    else:
        #no participants entered - find all files for session
        space_raw_files = list(Path(raw_data_path).rglob('sub-*/ses-' + str(session) + '/beh/*space*.tsv'))

        #pathlib library -- .relative_to give all the path that follows raw_data_path
        #                   .parts[0] extracts the first directory in remaining path to get
        #                       list of subjects
        space_raw_subs = [item.relative_to(raw_data_path).parts[0] for item in space_raw_files]

        #set is finding only unique values
        subject_list = list(set([item[4:7] for item in space_raw_subs]))   
else:   
    #no session argument entered     

    if args.parIDs is not None and len(args.parIDs) >= 1:
        #participants but no session entered
        sys.exit('If participant numbers are passed, need to specify a session')
    else:
        #no participants entered - find all files
        space_raw_files_s1 = list(Path(raw_data_path).rglob('sub-*/ses-1/beh/*space*.tsv'))
        space_raw_files_s2 = list(Path(raw_data_path).rglob('sub-*/ses-2/beh/*space*.tsv'))

        #pathlib library -- .relative_to give all the path that follows raw_data_path
        #                   .parts[0] extracts the first directory in remaining path to get
        #                       list of subjects
        space_raw_subs_s1 = [item.relative_to(raw_data_path).parts[0] for item in space_raw_files_s1]
        space_raw_subs_s2 = [item.relative_to(raw_data_path).parts[0] for item in space_raw_files_s2]

        #set is finding only unique values
        subject_list_s1 = list(set([item[4:7] for item in space_raw_subs_s1]))
        subject_list_s2 = list(set([item[4:7] for item in space_raw_subs_s2]))

        subject_list = [[subject_list_s1], [subject_list_s2]]
        
# move back to script directory
os.chdir(script_path)

#build workflow
Space_WF = Workflow('SpaceGame', base_dir = str(script_path))

#summary data - define earlier than use so can connect to workflow based
#on user input arguments

sumResults = MapNode(Function(input_names = ['Space_file', 'base_directory'],
                           output_names = ['summarySpace_dat', 'group_trialdat'],
                           function = summarySpace),
                     iterfield = ['Space_file'],
                     name = 'summaryData')
sumResults.inputs.base_directory = base_directory

# get subject ids that need to be procssed
if args.session is None:
    #if no session argument, use iterable in Identity interface to iterate over sessions
    sessNode = Node(IdentityInterface(fields=['session_id']),
                  name="sessinfo")
    sessNode.iterables = [('session_id', ['1', '2'])]
    
    #function node to get list of ids to process - selectfiles runs inside function
    selectIDNode = Node(Function(input_names = ['subject_list', 'session_id', 'base_directory', 'dat_overwrite'],
                           output_names = ['sub_files'],
                           function = checkData),
                     name = 'selectID')
    selectIDNode.inputs.subject_list = subject_list
    selectIDNode.inputs.base_directory = base_directory
    selectIDNode.inputs.dat_overwrite = dat_overwrite

    #connect session itterable to selectID node
    Space_WF.connect(sessNode, "session_id", selectIDNode, "session_id")
        
    #Connect select node and sesseion to summary results node
    Space_WF.connect(selectIDNode, "sub_files", sumResults, "Space_file")

else:
    
    #session argument so use entered sesssion to get subject ids to process
    #function node to get list of ids to process - selectfiles runs inside function
    selectIDNode = Node(Function(input_names = ['subject_list', 'session_id', 'base_directory', 'dat_overwrite'],
                           output_names = ['sub_files'],
                           function = checkData),
                     name = 'selectID')
    selectIDNode.inputs.subject_list = subject_list
    selectIDNode.inputs.base_directory = base_directory
    selectIDNode.inputs.session_id = session
    selectIDNode.inputs.dat_overwrite = dat_overwrite

    #connect session itterable AND selectID node to sumResults
    Space_WF.connect(selectIDNode, "sub_files", sumResults, "Space_file")

#concatonate blocks and update/save database
database_saveDat = Node(Function(input_names = ['Space_summary_dat', 'Space_group_trialdat', 'overwrite_flag', 'bids_dir'],
                           output_names = ['Space_database_cond', 'Space_database_blocks', 'Space_grouptrial_database'],
                           function = updateDatabase_save),
                     name = 'spaceDatabase')
database_saveDat.inputs.overwrite_flag = dat_overwrite
database_saveDat.inputs.bids_dir = str(base_directory)

Space_WF.connect(sumResults, "summarySpace_dat", database_saveDat, "Space_summary_dat")
Space_WF.connect(sumResults, "group_trialdat", database_saveDat, "Space_group_trialdat")


res = Space_WF.run()


