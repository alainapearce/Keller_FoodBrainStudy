#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to process Stop-Signal Task data in Summer 2021 by 
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

@author: azp271
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
#-p 2 3

#input arguments setup
parser=argparse.ArgumentParser()

parser.add_argument('--parIDs', '-p', help='participant list', type=float, nargs="+")
parser.add_argument('--overwrite', '-f', help='force overwrite of existing data')

args=parser.parse_args()

##############################################################################
####                                                                      ####
####                  Subfunctions called within script                   ####
####                                                                      ####
##############################################################################

## summary data function
def summarySST(SST_file):
    import numpy as np
    import pandas as pd
    
    ###################################################################
    ####                   Sub-function script                     ####
    
    #need to sub-functions within the function that is called by the node just 
    #like you need to re-import libraries
    def summary_stats(SST_data):
    
        ## ANALYSIS NOTE: 
        ## the original version of ANALYZE_IT and recommendations were to remove
        ## the first trial of each block. However, this is not reccomended in the
        ## concensus article Verbruggen et al., 2019 or in the new ANALYZE-IT-Tscope.R
        ## code on Open Science Foundation (https://osf.io/dw4ke/). 
        
        ## to remove first trial of each block, uncomment below code:
        
        #drop first row of each block
        #if 1 in SST_data['block']:
        #    block1 = SST_data.loc[SST_data['block'] == 1].index.values
        #    SST_data = SST_data.drop(block1[0])
        #    
        #if 2 in SST_data['block']:
        #    block2 = SST_data.loc[SST_data['block'] == 2].index.values
        #    SST_data = SST_data.drop(block2[0])
        #    
        #if 3 in SST_data['block']:
        #    block3 = SST_data.loc[SST_data['block'] == 3].index.values
        #    SST_data = SST_data.drop(block3[0])
        # 
        #if 4 in SST_data['block']:
        #    block4 = SST_data.loc[SST_data['block'] == 4].index.values
        #    SST_data = SST_data.drop(block4[0])
                
        #trial counts
        SST_target = SST_data.groupby('stop_signal').get_group(0)
        SST_stop = SST_data.groupby('stop_signal').get_group(1)
                
        #trial counts
        sst_n_targets = SST_target.shape[0]
        sst_n_stop = SST_stop.shape[0]
        sst_go_correct = SST_target[SST_target['correct'] == 4].shape[0]
        sst_go_error = SST_target[SST_target['correct'] == 2].shape[0]
        sst_go_miss = SST_target[SST_target['correct'] == 1].shape[0]
                
        #rt 
        go_rt = SST_target.loc[SST_target['rt_1'] > 0, 'rt_1'].mean(axis = 0)    
        go_rt_correct = SST_target.loc[(SST_target['correct'] == 4) & (SST_target['rt_1'] > 0), 'rt_1'].mean(axis = 0)
        go_rt_error = SST_target.loc[(SST_target['correct'] == 2) & (SST_target['rt_1'] > 0), 'rt_1'].mean(axis = 0)
    
        us_rt = SST_stop.loc[(SST_stop['correct'] == 3) & (SST_stop['rt_1'] > 0), 'rt_1'].mean(axis = 0)
                
        #probability of responding on signal  -- p(resp|signal)
        signal_presp = SST_stop.loc[(SST_stop['correct'] == 3)].shape[0]/sst_n_stop
                
        #SSD
        ssd = SST_stop['true_ssd'].mean(axis = 0)
        
        #racehorse check
        if go_rt > us_rt:
            racehorse = 1
        else:
            racehorse = 0
            
        if racehorse == 1:
                
            #SSRT Mean methods
            ssrt_mean = SST_target.loc[SST_target['correct'] != 1, 'rt_1'].mean(axis = 0) - ssd
        
            #SSRT Integration method
            #replace omissions with max RT if there are omissions
            if sst_go_miss > 0:
                #get max rt
                max_rt = max(SST_target.loc[SST_target['correct'] != 1, 'rt_1'])
            
                #make new dataset
                SST_target_replace = SST_target
            
                #supress warning
                pd.options.mode.chained_assignment = None
            
                #replace ommitted rt values
                SST_target_replace.loc[SST_target_replace['correct'] == 1, 'rt_1'] = max_rt
                    
                #get rt at signal_presp percentile
                nth_rt = np.percentile(SST_target_replace['rt_1'], 100*signal_presp)
                    
            else:
                #get rt at signal_presp percentile
                nth_rt = np.percentile(SST_target['rt_1'], 100*signal_presp)
          
              
            #caluclate ssrt
            ssrt_int = nth_rt - ssd
        
        else:
            ssrt_mean = np.nan
            ssrt_int = np.nan
            
            
        #combine into array    
        summary_results = [racehorse, sst_n_stop, sst_n_targets, go_rt, sst_go_correct, go_rt_correct, 
                         sst_go_error, go_rt_error, sst_go_miss, signal_presp, us_rt,
                         ssd, ssrt_mean, ssrt_int]
        
        return(summary_results)

    ###################################################################
    ####                Primary function script                    ####
    
    if isinstance(SST_file, str):
        #check to see if it is filepath str or 'No subfiles' message
        if '.tsv' in SST_file:
            #if only 1 file, will be string and we want an array
            SST_file = [SST_file]
        else:
            SST_file = []
        
    if len(SST_file) > 0:
    
        #loop counter
        count = 0

        for file in SST_file:

            #load data - loop throgh participant blockfiles
            SST_ProcData = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python') 

            #check for incomplete blocks
            block_counts = SST_ProcData['block'].value_counts()
            to_remove = block_counts[block_counts < 64].index
            
            if len(to_remove) > 0:
                SST_ProcData = SST_ProcData[~SST_ProcData.block.isin(to_remove)]

            #check for duplicate conditions - coding error in initial task randomization
            cond_list = SST_ProcData.groupby('block')['block_cond'].unique()
            
            #convert to strings
            cond_list = [str(item[0]) for item in cond_list]
            unique_cond = np.unique(cond_list)
                
            #if there are duplicate blocks, re-label second instance
            if len(unique_cond) < len(cond_list):
                for cond in unique_cond:
                    cond_group = SST_ProcData.groupby('block_cond').get_group(cond)
                    
                    #number of blocks with condition 'cond'
                    nblocks = len(cond_group['block'].unique())
                    
                    if nblocks > 1:
                        #get block number for second instance of cond
                        dup_block = max(cond_group['block'])
                    
                        #for rows where column 'block' = dup_block, replace column 'block_cond'
                        #values
                        SST_ProcData.loc[SST_ProcData['block'] == dup_block, 'block_cond'] = SST_ProcData[SST_ProcData['block'] == dup_block]['block_cond'].replace(cond, 'dup_' + cond)
            
            #remove duplicate blocks
            SST_nodup_blocks = SST_ProcData[SST_ProcData['block_cond'].str.contains('dup')==False]
            
            colnames = ['sub', 'block', 'condition', 'racehorse_check', 'n_stop_trials', 'n_go_trials', 'go_rt', 'n_go_cor', 'go_cor_rt', 'n_go_error',
                'go_error_rt', 'n_go_miss', 'stop_prob_resp', 'us_rt', 'ssd', 'ssrt_mean', 'ssrt_int']
            
            #summary stats - across all blocks
            all_trials_stat = summary_stats(SST_nodup_blocks)
            all_trials_stat.insert(0, SST_ProcData.loc[0, 'sub'])
            all_trials_stat.insert(1, 'all')
            all_trials_stat.insert(2, 'all')
            
            if count == 0:
                #make dataset
                overall_summary_data = pd.DataFrame(all_trials_stat).T
                overall_summary_data.columns = colnames
            else:
                overall_summary_data.loc[len(overall_summary_data)] = all_trials_stat
            
            # summary stats - by block conditions
           
            #check is there are 2 high ED blocks and 2 low ED blocks
            hed_blocks = [item for item in unique_cond if 'hED' in item]
            led_blocks = [item for item in unique_cond if 'lED' in item]
            
            #ensure block_cond column is string
            SST_nodup_blocks = SST_nodup_blocks.convert_dtypes()

            if len(hed_blocks) == 2 and len(led_blocks) == 2:
                #high ED data
                SST_hed_blocks = SST_nodup_blocks[SST_nodup_blocks['block_cond'].str.contains('hED')]
                
                hed_trials_stat = summary_stats(SST_hed_blocks)
                hed_trials_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                hed_trials_stat.insert(1, 'h_ed')
                hed_trials_stat.insert(2, 'h_ed')
                
                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = hed_trials_stat

                #low ED data
                SST_led_blocks = SST_nodup_blocks[SST_nodup_blocks['block_cond'].str.contains('lED')]
                
                led_trials_stat = summary_stats(SST_led_blocks) 
                led_trials_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                led_trials_stat.insert(1, 'l_ed')
                led_trials_stat.insert(2, 'l_ed')
                
                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = led_trials_stat
            
            #check is there are 2 large portion blocks and 2 small portion blocksa
            lport_blocks = [item for item in unique_cond if 'lPort' in item]
            sport_blocks = [item for item in unique_cond if 'sPort' in item]

            if len(lport_blocks) == 2 and len(sport_blocks) == 2:
                #large portion data
                SST_lport_blocks = SST_nodup_blocks[SST_nodup_blocks['block_cond'].str.contains('lPort')]
                
                lport_trials_stat = summary_stats(SST_lport_blocks)
                lport_trials_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                lport_trials_stat.insert(1, 'l_port')
                lport_trials_stat.insert(2, 'l_port')
                
                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = lport_trials_stat
            
                
                #small portion
                SST_sport_blocks = SST_nodup_blocks[SST_nodup_blocks['block_cond'].str.contains('sPort')]
                
                sport_trials_stat = summary_stats(SST_sport_blocks)
                sport_trials_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                sport_trials_stat.insert(1, 's_port')
                sport_trials_stat.insert(2, 's_port')
                
                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = sport_trials_stat
            
            #summary stats by block
              
            #get all non-duplicate blocks in dataset
            blocks = SST_nodup_blocks['block'].unique()
            
            #loop through blocks
            for b in blocks:
                #block data
                b_data = SST_nodup_blocks[SST_nodup_blocks['block'] == b]
                
                #ensure block_cond column is string
                b_data = b_data.convert_dtypes()
                
                #high ED, large portion
                if b_data['block_cond'].str.contains('hED_lPort').any():
                
                    hED_lPort_stat = summary_stats(b_data)
                    hED_lPort_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                    hED_lPort_stat.insert(1, b)
                    hED_lPort_stat.insert(2, 'hED_lPort')   
                        
                    #append new rows
                    overall_summary_data.loc[len(overall_summary_data)] = hED_lPort_stat
            
                #high ED, small portion        
                elif b_data['block_cond'].str.contains('hED_sPort').any():

                    hED_sPort_stat = summary_stats(b_data)
                    hED_sPort_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                    hED_sPort_stat.insert(1, b)
                    hED_sPort_stat.insert(2, 'hED_sPort')  
                        
                    #append new rows
                    overall_summary_data.loc[len(overall_summary_data)] = hED_sPort_stat
            
                #low ED, large portion
                elif b_data['block_cond'].str.contains('lED_lPort').any():
                
                    lED_lPort_stat = summary_stats(b_data)
                    lED_lPort_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                    lED_lPort_stat.insert(1, b)
                    lED_lPort_stat.insert(2, 'lED_lPort') 
                        
                    #append new rows
                    overall_summary_data.loc[len(overall_summary_data)] = lED_lPort_stat
            
                
                #low ED, small portion
                elif b_data['block_cond'].str.contains('lED_sPort').any():
            
                    lED_sPort_stat = summary_stats(b_data)
                    lED_sPort_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                    lED_sPort_stat.insert(1, b)
                    lED_sPort_stat.insert(2, 'lED_sPort')
                        
                    #append new rows
                    overall_summary_data.loc[len(overall_summary_data)] = lED_sPort_stat

            #update count for files loop
            count = 1

    else:
         overall_summary_data = 'no files'
            

    return overall_summary_data

## summary data function
def updateDatabase_save(SST_summary_dat, overwrite_flag, bids_dir):
    import pandas as pd
    import numpy as np
    from pathlib import Path
    from nipype.interfaces.base import Bunch
    
    #get a Bunch object if more than 1 participant 
    if isinstance(SST_summary_dat, Bunch):        
        #get output data from node
        SST_summary_datlist = SST_summary_dat.summarySST_dat
        
        #combine datasets 
        SST_summary_dat = pd.concat(SST_summary_datlist)
        
    #if only 1 participant/dataset then it is a list    
    elif isinstance(SST_summary_dat, list):
        if len(SST_summary_dat) == 1:
            SST_summary_dat = SST_summary_dat[0]
        else:
            SST_summary_dat = pd.concat(SST_summary_dat)

    #if a pandas dataframe
    if isinstance(SST_summary_dat, pd.DataFrame):
        
        #get column names
        columnnames = SST_summary_dat.columns
       
        #get condition subset
        SST_summary_conds = SST_summary_dat[SST_summary_dat.block.isin(['all', 'h_ed', 'l_ed', 'l_port', 's_port'])]

        #make wide data set 
        SST_summary_wide = SST_summary_conds.pivot(columns='condition', index='sub', values=columnnames[3:17])        
        SST_summary_wide.columns = ['_'.join(col) for col in SST_summary_wide.columns.reorder_levels(order=[1, 0])]
        
        #make the sub index into a dataset column
        SST_summary_wide = SST_summary_wide.reset_index(level = 0)
        
        #re-order columns
        columnnames_reorder = ['sub', 'all_racehorse_check', 
                               'all_n_stop_trials', 'all_n_go_trials', 'all_go_rt', 
                               'all_n_go_cor', 'all_go_cor_rt', 'all_n_go_error',  
                               'all_go_error_rt', 'all_n_go_miss', 'all_stop_prob_resp',
                               'all_us_rt', 'all_ssd', 'all_ssrt_mean', 'all_ssrt_int', 
                               'h_ed_racehorse_check', 'h_ed_n_stop_trials',
                               'h_ed_n_go_trials', 'h_ed_go_rt', 'h_ed_n_go_cor', 
                               'h_ed_go_cor_rt', 'h_ed_n_go_error',
                               'h_ed_go_error_rt', 'h_ed_n_go_miss', 'h_ed_stop_prob_resp', 
                               'h_ed_us_rt', 'h_ed_ssd', 'h_ed_ssrt_mean', 'h_ed_ssrt_int',
                               'l_ed_racehorse_check', 'l_ed_n_stop_trials', 'l_ed_n_go_trials', 
                               'l_ed_go_rt', 'l_ed_n_go_cor', 'l_ed_go_cor_rt', 
                               'l_ed_n_go_error', 'l_ed_go_error_rt', 'l_ed_n_go_miss', 
                               'l_ed_stop_prob_resp', 'l_ed_us_rt', 'l_ed_ssd',
                               'l_ed_ssrt_mean', 'l_ed_ssrt_int', 'l_port_racehorse_check', 
                               'l_port_n_stop_trials', 'l_port_n_go_trials', 'l_port_go_rt', 
                               'l_port_n_go_cor', 'l_port_go_cor_rt', 'l_port_n_go_error',
                               'l_port_go_error_rt', 'l_port_n_go_miss', 'l_port_stop_prob_resp', 
                               'l_port_us_rt', 'l_port_ssd', 'l_port_ssrt_mean', 'l_port_ssrt_int',
                               's_port_racehorse_check', 's_port_n_stop_trials',
                               's_port_n_go_trials', 's_port_go_rt', 's_port_n_go_cor', 
                               's_port_go_cor_rt', 's_port_n_go_error',
                               's_port_go_error_rt', 's_port_n_go_miss', 's_port_stop_prob_resp', 
                               's_port_us_rt', 's_port_ssd', 's_port_ssrt_mean', 's_port_ssrt_int']
        
        SST_summary_wide = SST_summary_wide.reindex(columns=columnnames_reorder)
    
        #get blocks subset
        SST_summary_blocks = SST_summary_dat[SST_summary_dat.condition.isin(['hED_lPort', 'hED_sPort', 'lED_lPort', 'lED_sPort'])] 
    
        ## load databases
        #derivative data path
        derivative_data_path = Path(bids_dir).joinpath('derivatives/preprocessed/beh')

        #load databases
        SST_database_cond = pd.read_csv(str(Path(derivative_data_path).joinpath('task-sst_summary_condwide.tsv')), sep = '\t') 
        SST_database_blocks = pd.read_csv(str(Path(derivative_data_path).joinpath('task-sst_summary_blockslong.tsv')), sep = '\t')

        #if overwriting participants
        if overwrite_flag == True:
            #function to drop rows based on values
            def filter_rows_by_values(df, col, values):
                return df[df[col].isin(values) == False]

            #get list of subs to filter in wide and long data
            wide_sub_list = list(SST_summary_wide['sub'].unique())
            block_sub_list = list(SST_summary_blocks['sub'].unique())

            #filter out/remove exisiting subs to overwrite
            SST_database_cond = filter_rows_by_values(SST_database_cond, 'sub', wide_sub_list)
            SST_database_blocks = filter_rows_by_values(SST_database_blocks, 'sub', block_sub_list)
        
        #add newly processed data
        SST_database_cond = SST_database_cond.append(SST_summary_wide)
        SST_database_blocks = SST_database_blocks.append(SST_summary_blocks)

        #sort to ensure in sub order
        SST_database_cond = SST_database_cond.sort_values(by = 'sub')
        SST_database_blocks = SST_database_blocks.sort_values(by = ['sub', 'block'])

        #round to 3 decimal points
        SST_database_cond = SST_database_cond.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)
        SST_database_blocks = SST_database_blocks.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)

        #write databases
        SST_database_cond.to_csv(str(Path(derivative_data_path).joinpath('task-sst_summary_condwide.tsv')), sep = '\t', encoding='utf-8-sig', index = False) 
        SST_database_blocks.to_csv(str(Path(derivative_data_path).joinpath('task-sst_summary_blockslong.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
    
    else:
        print('No raw data files that need to be processed')
        SST_database_cond = np.nan
        SST_database_blocks = np.nan
        
    return SST_database_cond, SST_database_blocks

##############################################################################
####                                                                      ####
####                       Primary Workflow Script                        ####
####                                                                      ####
##############################################################################

#Set up workflow
from nipype import Workflow, Node, Function, DataGrabber, MapNode
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
if args.parIDs is not None and len(args.parIDs) >= 1:

    #make sure have integers
    subject_ids = list(map(int, args.parIDs))

    #get leading zeros
    subject_list = [str(item).zfill(3) for item in subject_ids]
        
    #check for raw data
    subs = list(subject_list)

    for sub in subs:

        raw_file = list(Path(raw_data_path).rglob('sub-' + str(sub) + '/ses-1/beh/*sst*.tsv'))

        if len(raw_file) < 1:
            print('No Files found for sub-' + str(sub))
            subject_list.remove(sub)
        
    #check if any files to process
    if subject_list is None:
        sys.exit('No Files found for participants' + args.parIDs)      
else:
    #no participants entered - find all files for session
    sst_raw_files = list(Path(raw_data_path).rglob('sub-*/ses-1/beh/*sst*.tsv'))

    #pathlib library -- .relative_to give all the path that follows raw_data_path
    #                   .parts[0] extracts the first directory in remaining path to get
    #                       list of subjects
    sst_raw_subs = [item.relative_to(raw_data_path).parts[0] for item in sst_raw_files]

    #set is finding only unique values
    subject_list = list(set([item[4:7] for item in sst_raw_subs]))   

# move back to script directory
os.chdir(str(script_path))

#build workflow
SST_WF = Workflow('SST', base_dir = str(script_path))

#summary data - define earlier than use so can connect to workflow based
#on user input arguments

sumResults = MapNode(Function(input_names = ['SST_file', 'session_id'],
                           output_names = ['summarySST_dat'],
                           function = summarySST),
                     iterfield = ['SST_file'],
                     name = 'summaryData')

# get subject ids that need to be procssed
if args.overwrite is None:
        
    #load data 
    database = Path(database_path).joinpath('task-sst_summary_condwide.tsv')
    SST_database = pd.read_csv(str(database), sep = '\t', encoding = 'utf-8-sig', header = 0, engine='python')
    
    #get unique ids
    subs_exist = SST_database['sub'].unique()
    
    #make match format of subject_list
    subs_exist_str = [str(item).zfill(3) for item in subs_exist]
    
    #compare subject_list to subs_exist
    #get intersection
    match_subs = list(set.intersection(set(subject_list), set(subs_exist_str)))
    
    #report
    for sub in match_subs:
        #remove sub if in list that exists in database already
        print('Skipping sub-' + str(sub) + ' - Exists in database already.')
    
    #get subject_list
    subject_list = list(set(subject_list) -  set(match_subs))
        
    #node to get list of ids to process - selectfiles
    if len(subject_list) > 0:
                
        template_path = Path('sub-%s/ses-1/beh/*task-sst*.tsv')
        selectfiles = Node(DataGrabber(infields=['subject_ids'],
                      outfields=['sstFiles'],
                      base_directory = str(raw_data_path), 
                      template = str(template_path),
                      sort_filelist = True),
          name='selectfiles')
        
        selectfiles.inputs.subject_ids = subject_list
        
        #Connect select node and sesseion to summary results node
        SST_WF.connect(selectfiles, "sstFiles", sumResults, "SST_file")
        
    else:
        #exit if no files exist
        sys.exit('No new subjects to add to database')   

#overwrite option specified     
else:

    # select files Node 
    template_path = Path('sub-%s/ses-1/beh/*task-sst*.tsv')
    selectfiles = Node(DataGrabber(infields=['subject_ids'],
                  outfields=['sstFiles'],
                  base_directory = str(raw_data_path), 
                  template = str(template_path),
                  sort_filelist = True),
      name='selectfiles')
        
    #manually set subject list in selectfiles
    selectfiles.inputs.subject_ids = subject_list
        
    #Connect selectfiles to summary results node
    SST_WF.connect(selectfiles, "sstFiles", sumResults, "SST_file")

#concatonate blocks and update/save database
if args.overwrite is None:
    dat_overwrite = False
else:
    dat_overwrite = True

database_saveDat = Node(Function(input_names = ['SST_summary_dat', 'overwrite_flag', 'bids_dir'],
                           output_names = ['SST_database_cond', 'SST_database_blocks'],
                           function = updateDatabase_save),
                     name = 'sstDatabase')
database_saveDat.inputs.overwrite_flag = dat_overwrite
database_saveDat.inputs.bids_dir = str(base_directory)

SST_WF.connect(sumResults, "summarySST_dat", database_saveDat, "SST_summary_dat")

res = SST_WF.run()


