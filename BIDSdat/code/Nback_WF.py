#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to process the N-Back Task data in Summer 2021 by 
Alaina Pearce and Bari Fuchs.

Copyright (C) 2021 Alaina L Pearce and Bari Fuchs

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

@author: azp271@psu.edu, baf44@psu.edu
"""

#set up packages    
import numpy as np
import pandas as pd
import os
import sys, argparse

# to enter multiple subject arguments in terminal format like:
#-p 2 3 -s 2

#input arguments setup
parser=argparse.ArgumentParser()

parser.add_argument('--session', '-s', help='Session number')
parser.add_argument('--parIDs', '-p', help='participant list', type=float, nargs="+")
parser.add_argument('--overwrite', '-f', help='force overwrite of existing data')

args=parser.parse_args()

# Hardcode session and sub

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

    #load data 
    database = Path(database_path).joinpath('task-nback_summary.tsv')
    Nback_database = pd.read_csv(str(database), sep = '\t', encoding = 'utf-8-sig', header = 0, engine='python')

    #check for existing data
    if dat_overwrite is False:
        #load data 
        database = Path(database_path).joinpath('task-nback_summary.tsv')
        Nback_database = pd.read_csv(str(database), sep = '\t', encoding = 'utf-8-sig', header = 0, engine='python')

        #check session in database
        db_sessions = Nback_database.session.unique()

        #if session number is in database
        if session_num in db_sessions:

            Nback_database_ses = Nback_database.groupby('session').get_group(session_num)

            subs = list(subject_list_use)

            for sub in subs:

                #check if in database
                if len(Nback_database_ses[Nback_database_ses['sub']==int(sub)].index.tolist()) > 0:
                    subject_list_use.remove(sub)
    
    if len(subject_list_use) > 0:
        template_path = Path('sub-%s/ses-%s/beh/*task-nback*.tsv')
        selectfiles = Node(DataGrabber(infields=['subject_ids', 'session_id'],
                      outfields=['blockFiles'],
                      base_directory = str(raw_data_path), 
                      template = str(template_path),
                      sort_filelist = True),
          name='selectfiles')
        selectfiles.inputs.session_id = session_id
        selectfiles.inputs.subject_ids = subject_list_use
        
        sub_files = selectfiles.run().outputs.blockFiles
        
    else:
        sub_files = 'No subfiles'

    return sub_files


## summary data function
def summaryNback(Nback_file):
    import numpy as np
    import pandas as pd
    from collections.abc import Iterable
    
    #check if str
    if isinstance(Nback_file, str):

        #check to see if it is filepath str or 'No subfiles' message
        if '.tsv' in Nback_file:
            #if only 1 file, will be string and we want an array
            Nback_file = [Nback_file]
        else:
            Nback_file = []
        
    if len(Nback_file) > 0:
    
        #loop counter
        count = 1

        for file in Nback_file:

            #load data - loop throgh participant blockfiles
            Nback_ProcData = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python') 

            #make Acc_Resp column
            Nback_ProcData.fillna('', inplace=True)

            Nback_ProcData.columns = Nback_ProcData.columns.str.replace('b0_', '')
            Nback_ProcData.columns = Nback_ProcData.columns.str.replace('b1_', '')
            Nback_ProcData.columns = Nback_ProcData.columns.str.replace('b2_', '')

            Nback_ProcData['acc_resp'] = np.where(Nback_ProcData['correct'] == Nback_ProcData['stim_resp'], 1, 0)

            Nback_ProcData['procedure_block'] = Nback_ProcData['procedure_block'].replace(['B0BlockProc','B0Block2Proc'],'b0')
            Nback_ProcData['procedure_block'] = Nback_ProcData['procedure_block'].replace(['B1BlockProc','B1Block2Proc'],'b1')
            Nback_ProcData['procedure_block'] = Nback_ProcData['procedure_block'].replace(['B2BlockProc','B2Block2Proc'],'b2')

            #get target and fill datasets
            Nback_Target = Nback_ProcData.groupby('condition').get_group('Target')
            Nback_Fill = Nback_ProcData.groupby('condition').get_group('Fill')

            #trial counts
            nTarget = Nback_Target.shape[0]
            nFill = Nback_Fill.shape[0]
            nTrials = nTarget + nFill

            #Accuracy
            nAcc = Nback_Target['acc_resp'].sum(axis = 0) + Nback_Fill['acc_resp'].sum(axis = 0)
            pAcc = (nAcc/nTrials)*100

            #Go Hits/Misses 
            nTarget_Hit = Nback_Target['acc_resp'].sum(axis = 0)
            pTarget_Hit = (nTarget_Hit/nTarget)*100

            nTarget_Miss = nTarget - nTarget_Hit
            pTarget_Miss = (nTarget_Miss/nTarget)*100

            #NoGo Commissions (False Alarms)
            nFill_Corr = Nback_Fill['acc_resp'].sum(axis = 0)
            pFill_Corr = (nFill_Corr/nFill)*100

            nFill_FA = nFill - nFill_Corr
            pFill_FA = (nFill_FA/nFill)*100

            #Ballanced Acc
            pTarget_BA = (pTarget_Hit + pFill_Corr)/2

            #mean and median RT
            Nback_Target_correct = Nback_Target.groupby('acc_resp').get_group(1)

            RTmeanTarget_Hit = Nback_Target_correct['stim_rt'].mean(axis = 0)
            RTmedTarget_Hit = Nback_Target_correct['stim_rt'].median(axis = 0)
    
            summaryNback_dat = [Nback_ProcData['sub'][0], Nback_ProcData['ses'][0], Nback_ProcData['procedure_block'][0], nTarget, nFill, nTrials, nAcc, pAcc, nTarget_Hit, pTarget_Hit, nTarget_Miss, pTarget_Miss, nFill_Corr, pFill_Corr, nFill_FA, pFill_FA, pTarget_BA, RTmeanTarget_Hit, RTmedTarget_Hit]
        
            if count == 1:
                summaryNback_list = summaryNback_dat
                count = count + 1
            else:
                summaryNback_list = np.row_stack((summaryNback_list, summaryNback_dat))
                count = count + 1
            
    else:
        summaryNback_list = 'no files'

    return summaryNback_list

## summary data function
def updateDatabase_save(block_sumDat, overwrite_flag, bids_dir):
    import numpy as np
    import pandas as pd
    from pathlib import Path
    from nipype.interfaces.base import Bunch
    
    #get a Bunch object if more than 1 participant 
    if isinstance(block_sumDat, Bunch):        
        #get output data from node
        np_allBlockDat = block_sumDat.summaryNback_dat
        
    #if only 1 participant/dataset then it is a list    
    elif isinstance(block_sumDat, list):
        if len(block_sumDat) == 1:
            np_allBlockDat = block_sumDat[0]
        else:
            np_allBlockDat = block_sumDat
    
    #convert np subarrays to pandas
    def np2pds(t):
        return [pd.DataFrame(sublist) for sublist in t]
        
    pandas_allBlockDat = np2pds(np_allBlockDat)

    #combine datasets 
    allBlockDat = pd.concat(pandas_allBlockDat)
    
    #if a pandas dataframe
    if isinstance(allBlockDat, pd.DataFrame):
        col_names = ['sub', 'ses', 'block','n_targets', 'n_fill', 'n_trials', 'n_acc', 'p_acc', 'n_target_hit', 'p_target_hit', 'n_target_miss', 'p_target_miss', 'n_fill_corr', 'p_fill_corr', 'n_fill_fa', 'p_fill_fa', 'p_target_ba', 'rt_mean_target_hit', 'rt_med_target_hit']
        allBlockDat.columns = col_names
        allBlockDat = pd.DataFrame(allBlockDat).convert_dtypes()
        allBlockDat = allBlockDat.reset_index(drop = True)    

        #set numeric columns to dtype numeric
        num_cols = allBlockDat.loc[:, allBlockDat.columns != 'block'].apply(pd.to_numeric).round(3)

        #replace in orig dataset
        allBlockDat.loc[:, num_cols.columns] = num_cols
    
        #get session subsets
        db_sessions = allBlockDat.ses.unique()

        #make wide data set 
        if len(db_sessions) > 1:
            allBlockDat_ses1_dat = allBlockDat.groupby('ses').get_group(1)
            allBlockDat_ses2_dat = allBlockDat.groupby('ses').get_group(2)
            
            #make wide data set 
            allBlockDat_ses1_wide = allBlockDat_ses1_dat.pivot(columns='block', index='sub', values=col_names[3:19])
            allBlockDat_ses1_wide.columns = ['_'.join(col) for col in allBlockDat_ses1_wide.columns.reorder_levels(order=[1, 0])]

            allBlockDat_ses2_wide = allBlockDat_ses2_dat.pivot(columns='block', index='sub', values=col_names[3:19])
            allBlockDat_ses2_wide.columns = ['_'.join(col) for col in allBlockDat_ses2_wide.columns.reorder_levels(order=[1, 0])]

            #make the sub index into a dataset column
            allBlockDat_ses1_wide = allBlockDat_ses1_wide.reset_index(level = 0)
            allBlockDat_ses2_wide = allBlockDat_ses2_wide.reset_index(level = 0)

            #add session
            allBlockDat_ses1_wide.insert(1, 'ses', 1)
            allBlockDat_ses1_wide.insert(1, 'ses', 2)


            #concatonate databases
            allBlockDat_wide = pd.concat([allBlockDat_ses1_wide, allBlockDat_ses2_wide],ignore_index=True)

        else:
            #make wide data set 
            allBlockDat_wide = allBlockDat.pivot(columns='block', index='sub', values = col_names[3:19])        
            allBlockDat_wide.columns = ['_'.join(col) for col in allBlockDat_wide.columns.reorder_levels(order=[1, 0])]
        
            #make the sub index into a dataset column
            allBlockDat_wide = allBlockDat_wide.reset_index(level = 0)

            #add session
            allBlockDat_wide.insert(1, 'ses', db_sessions[0])

        #re-order columns
        columnnames_reorder = ['sub', 'ses', 
         'b0_n_targets', 'b0_n_fill', 'b0_n_trials', 'b0_n_acc','b0_p_acc',
         'b0_n_target_hit','b0_p_target_hit', 'b0_n_target_miss',
         'b0_p_target_miss','b0_n_fill_corr','b0_p_fill_corr',
         'b0_n_fill_fa', 'b0_p_fill_fa','b0_p_target_ba',
         'b0_rt_mean_target_hit','b0_rt_med_target_hit',
         'b1_n_targets', 'b1_n_fill', 'b1_n_trials', 'b1_n_acc','b1_p_acc',
         'b1_n_target_hit','b1_p_target_hit','b1_n_target_miss',
         'b1_p_target_miss', 'b1_n_fill_corr','b1_p_fill_corr',
         'b1_n_fill_fa','b1_p_fill_fa','b1_p_target_ba',
         'b1_rt_mean_target_hit','b1_rt_med_target_hit',
         'b2_n_targets', 'b2_n_fill', 'b2_n_trials', 'b2_n_acc','b2_p_acc',
         'b2_n_target_hit','b2_p_target_hit', 'b2_n_target_miss',
         'b2_p_target_miss','b2_n_fill_corr','b2_p_fill_corr',
         'b2_n_fill_fa','b2_p_fill_fa','b2_p_target_ba',
         'b2_rt_mean_target_hit','b2_rt_med_target_hit']
           
        allBlockDat_wide = allBlockDat_wide.reindex(columns=columnnames_reorder)

        ## load databases
        #derivative data path
        derivative_data_path = Path(bids_dir).joinpath('derivatives/preprocessed/beh')

        #load databases
        Nback_database = pd.read_csv(str(Path(derivative_data_path).joinpath('task-nback_summary.tsv')), sep = '\t') 
        Nback_database_long = pd.read_csv(str(Path(derivative_data_path).joinpath('task-nback_summary_long.tsv')), sep = '\t')

        #if overwriting participants
        if overwrite_flag == True:
            #function to drop rows based on values
            def filter_rows_by_values(df, sub_values, sesnum):
                #fileter based on sub and ses
                return df[(df['sub'].isin(sub_values) == False) & (df['ses'] == sesnum)]

            #filter out/remove exisiting subs to overwrit~
            if len(db_sessions) > 1:
                #get list of subs by ses to filter in wide and long data
                wide_sub_list = allBlockDat_wide.groupby('ses')['sub'].unique()
                long_sub_list = allBlockDat.groupby('ses')['sub'].unique()

                Nback_database_ses1 = filter_rows_by_values(Nback_database, wide_sub_list[0], 1)
                Nback_database_ses2 = filter_rows_by_values(Nback_database, wide_sub_list[1], 2)

                Nback_database_ses1_long = filter_rows_by_values(Nback_database_long, long_sub_list[0], 1)
                Nback_database_ses2_long = filter_rows_by_values(Nback_database_long, long_sub_list[1], 2)

                #concatonate databases
                Nback_database = pd.concat([Nback_database_ses1, Nback_database_ses2],ignore_index=True)
                Nback_database_long = pd.concat([Nback_database_ses1_long, Nback_database_ses2_long],ignore_index=True)

            else:
                wide_sub_list = list(allBlockDat_wide['sub'].unique())
                long_sub_list = list(allBlockDat['sub'].unique())

                #filter by ses and sub
                Nback_database_ses = filter_rows_by_values(Nback_database, wide_sub_list, db_sessions[0])
                Nback_database_long_ses = filter_rows_by_values(Nback_database_long, long_sub_list, db_sessions[0])

                #concatonate with other session in full database
                Nback_database = pd.concat([Nback_database[Nback_database['ses'] != db_sessions[0]], Nback_database_ses],ignore_index=True)
                Nback_database_long = pd.concat([Nback_database_long[Nback_database_long['ses'] != db_sessions[0]], Nback_database_long_ses],ignore_index=True)

        #add newly processed data
        Nback_database = Nback_database.append(allBlockDat_wide)
        Nback_database_long = Nback_database_long.append(allBlockDat)

        #sort to ensure in sub order
        Nback_database = Nback_database.sort_values(by = ['ses', 'sub'])
        Nback_database_long = Nback_database_long.sort_values(by = ['ses', 'sub', 'block'])

        #write databases
        Nback_database.to_csv(str(Path(derivative_data_path).joinpath('task-nback_summary.tsv')), sep = '\t', encoding='utf-8-sig', index = False) 
        Nback_database_long.to_csv(str(Path(derivative_data_path).joinpath('task-nback_summary_long.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

        return Nback_database, Nback_database_long

#################### Primary Workflow Script ########################

#Set up workflow
from nipype import Workflow, Node, Function, DataGrabber, MapNode, IdentityInterface
from pathlib import Path
from shutil import copy2

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
    
    if args.parIDs is not None and len(args.parIDs) >= 1:

        #make sure have integers
        subject_ids = list(map(int, args.parIDs))


        #get leading zeros
        subject_list = [str(item).zfill(3) for item in subject_ids]
        
        #check for raw data
        subs = list(subject_list)

        for sub in subs:

            raw_file = list(Path(raw_data_path).rglob('sub-' + str(sub) + '/ses-' + str(session) + '/beh/*nback*.tsv'))

            if len(raw_file) < 1:
                #participants but no session entered
                print('No Files found for sub-' + str(sub) + ' and session ' + str(session))
                subject_list.remove(sub)
        
        #check if any files to process
        if subject_list is None:
            sys.exit('No Files found for participants' + args.parIDs + ' for session ' + str(session))      
    else:
        #no participants entered - find all files for session
        nback_raw_files = list(Path(raw_data_path).rglob('sub-*/ses-' + str(session) + '/beh/*nback*.tsv'))

        #pathlib library -- .relative_to give all the path that follows raw_data_path
        #                   .parts[0] extracts the first directory in remaining path to get
        #                       list of subjects
        nback_raw_subs = [item.relative_to(raw_data_path).parts[0] for item in nback_raw_files]

        #set is finding only unique values
        subject_list = list(set([item[4:7] for item in nback_raw_subs]))   
else:   
    #no session argument entered     

    if args.parIDs is not None and len(args.parIDs) >= 1:
        #participants but no session entered
        sys.exit('If participant numbers are passed, need to specify a session')
    else:
        #no participants entered - find all files
        nback_raw_files_s1 = list(Path(raw_data_path).rglob('sub-*/ses-1/beh/*nback*.tsv'))
        nback_raw_files_s2 = list(Path(raw_data_path).rglob('sub-*/ses-2/beh/*nback*.tsv'))

        #pathlib library -- .relative_to give all the path that follows raw_data_path
        #                   .parts[0] extracts the first directory in remaining path to get
        #                       list of subjects
        nback_raw_subs_s1 = [item.relative_to(raw_data_path).parts[0] for item in nback_raw_files_s1]
        nback_raw_subs_s2 = [item.relative_to(raw_data_path).parts[0] for item in nback_raw_files_s2]

        #set is finding only unique values
        subject_list_s1 = list(set([item[4:7] for item in nback_raw_subs_s1]))
        subject_list_s2 = list(set([item[4:7] for item in nback_raw_subs_s2]))

        subject_list = [[subject_list_s1], [subject_list_s2]]

# move back to script directory
os.chdir(script_path)

#build workflow
Nback_WF = Workflow('Nback')

#summary data - define earlier than use so can connect to workflow based
#on user input arguments
sumResults = MapNode(Function(input_names = ['Nback_file'],
                           output_names = ['summaryNback_dat'],
                           function = summaryNback),
                     iterfield = ['Nback_file'],
                     name = 'summaryData')

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
    Nback_WF.connect(sessNode, "session_id", selectIDNode, "session_id")
        
    #Connect select node and sesseion to summary results node
    Nback_WF.connect(selectIDNode, "sub_files", sumResults, "Nback_file")

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

    #connect session itterable AND selectID node to sumResults node
    Nback_WF.connect(selectIDNode, "sub_files", sumResults, "Nback_file")

concat_saveDat = Node(Function(input_names = ['block_sumDat', 'overwrite_flag', 'bids_dir'],
                           output_names = ['allBlocks_longDat'],
                           function = updateDatabase_save),
                     name = 'concatBlocksLong')
concat_saveDat.inputs.overwrite_flag = dat_overwrite
concat_saveDat.inputs.bids_dir = str(base_directory)

Nback_WF.connect(sumResults, "summaryNback_dat", concat_saveDat, "block_sumDat")

res = Nback_WF.run()
