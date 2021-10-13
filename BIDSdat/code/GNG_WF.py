#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to process Go No Go Task data in Summer 2021 by 
Bari Fuchs. Modeled off of SST_WF.py writted by Alaina Pearce.

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

## GNG summary data function
def summaryGNG(GNG_file):
    import numpy as np
    import pandas as pd
    
    ###################################################################
    ####                   Sub-function script                     ####
    
    #need to write sub-functions (e.g., getGNGtrialAcc) WITHIN the function that is called by the node (e.g., summaryGNG)
    #just like you need to re-import libraries
    def getGNGtrialAcc(GNG_data):
        #Make 2 new variables:
        #trial_resp: indicate if response made during trial (stim or response screen)
        #trial_rt: indicate reaction time from onset of stim screen (add 750 ms to respond_rt if response occured during response screen)
        
        #initialize empty columns for trial_resp and trial_rt
        GNG_data["trial_resp"] = np.nan
        GNG_data["trial_rt"] = np.nan
        
        #Assign values to trial_resp and trial_rt
        GNG_data.loc[GNG_data.stim_resp == '{SPACE}', 'trial_resp'] = '{SPACE}'
        GNG_data.loc[GNG_data.respond_resp == '{SPACE}', 'trial_resp'] = '{SPACE}'
        GNG_data.loc[GNG_data.stim_resp == '{SPACE}', 'trial_rt'] = GNG_data.stim_rt
        GNG_data.loc[GNG_data.respond_resp == '{SPACE}', 'trial_rt'] = GNG_data.respond_rt + 750

        ##Create new accuracy variable "Acc_Resp" that indicates a 1 when the columns 'CorrectResp' and 'RESP' match
        #initialize empty columns for accuracy variable
        GNG_data["trial_acc"] = np.nan
        
        # Change nan to none because pandas/NumPy uses the fact that np.nan != np.nan
        GNG_data[['ca', 'trial_resp']] = GNG_data[['ca', 'trial_resp']].fillna(value='None')
        
        # Set accuracy equal to 1 when trial_acc = trial_resp
        GNG_data['trial_acc'] = np.where(GNG_data['trial_resp'] == GNG_data['ca'], '1', '0')
        
        return(GNG_data)
    
    def summary_stats(GNG_data):
        
        # Create 2 dataframes, one with Go trials and one with No Go trials
        Go_data = GNG_data.loc[GNG_data['compatibility'] == 'Go']
        NoGo_data = GNG_data.loc[GNG_data['compatibility'] == 'NoGo']
        
        # count trials
        nGo = len(Go_data)
        nNoGo = len(NoGo_data)
        
        # Accuracy
        nAcc = GNG_data['trial_acc'].value_counts()["1"]
        pAcc = nAcc/len(GNG_data)

        # Go Hits/Misses
        nGo_Hit = (Go_data.trial_acc == '1').sum()
        pGo_Hit = nGo_Hit/len(Go_data)

        nGo_Miss = (Go_data.trial_acc == '0').sum()
        pGo_Miss = nGo_Miss/len(Go_data)

        #NoGo Commissions (False Alarms) and Correct no responses  
        nNoGo_Corr = (NoGo_data.trial_acc == '1').sum()
        pNoGo_Corr = nNoGo_Corr/len(NoGo_data)

        nNoGo_FA = (NoGo_data.trial_acc == '0').sum()
        pNoGo_FA = nNoGo_FA/len(NoGo_data)

        # Mean and median RT
        RTmeanGo_Hit = Go_data.loc[(Go_data['trial_acc']=="1"), 'trial_rt'].mean()
        RTmedGo_Hit = Go_data.loc[(Go_data['trial_acc']=="1"), 'trial_rt'].median()

        RTmeanNoGo_FA = NoGo_data.loc[(NoGo_data['trial_acc']=="0"), 'trial_rt'].mean()
        RTmedNoGo_FA = NoGo_data.loc[(NoGo_data['trial_acc']=="0"), 'trial_rt'].median()

        #combine into array    
        summary_results = [nGo, nNoGo, nAcc, pAcc, nGo_Hit, nGo_Miss, nNoGo_Corr, nNoGo_FA, pGo_Hit, 
                           pGo_Miss, pNoGo_Corr, pNoGo_FA, RTmeanGo_Hit, RTmeanNoGo_FA, RTmedGo_Hit, RTmedNoGo_FA]

        return(summary_results)

    ## DDM
    #RT data at different quantils # this is a separate database thats output.
    # Can always skip this for now, and make note to make DDM function
    # SDT = signal detection theory. google norminv, it gives z-score. should be able to ask for norminv in python

    ###################################################################
    ####                Primary function script                    ####
    
    if isinstance(GNG_file, str):
        #if only 1 file, will be string and we want an array
        GNG_file = [GNG_file]
        
    if len(GNG_file) > 0:
    
        #loop counter
        count = 0

        for file in GNG_file:

            #load data - loop throgh participant blockfiles
            GNG_data = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python') 

            #check for incomplete blocks
            block_counts = GNG_data['block_list_sample'].value_counts()
            to_remove = block_counts[block_counts < 40].index
            
            if len(to_remove) > 0:
                GNG_data = GNG_data[~GNG_data.block_list_sample.isin(to_remove)]

            # Compute GNG trial accuracy and rt
            GNG_data = getGNGtrialAcc(GNG_data)
            
            # Set column names
            colnames = ['sub', 'block', 'nGo', 'nNoGo', 'nAcc', 'pAcc', 'nGo_Hit', 'nGo_Miss', 'nNoGo_Corr', 
                        'nNoGo_FA', 'pGo_Hit', 'pGo_Miss', 'pNoGo_Corr', 'pNoGo_FA', 'RTmeanGo_Hit',
                        'RTmeanNoGo_FA', 'RTmedGo_Hit', 'RTmedNoGo_FA']
            
            #summary stats - across all blocks
            all_trials_stat = summary_stats(GNG_data)
            all_trials_stat.insert(0, GNG_data.loc[0, 'sub'])
            all_trials_stat.insert(1, 'all')
            
            if count == 0:
                #make dataset
                overall_summary_data = pd.DataFrame(all_trials_stat).T
                overall_summary_data.columns = colnames
            else:
                overall_summary_data.loc[len(overall_summary_data)] = all_trials_stat
            
            #summary stats by block
              
            #get all non-duplicate blocks in dataset
            blocks = GNG_data['block_list_sample'].unique()
            
            #loop through blocks
            for b in blocks:

                #subset block data from GNG_data
                b_data = GNG_data[GNG_data['block_list_sample'] == b]
                
                #ensure block_cond column is string
                b_data = b_data.convert_dtypes()
                
                #set block variable name
                b_var = ("b" + str(int(b)))
                
                # Get summary stats for block
                block_summary = summary_stats(b_data)
                block_summary.insert(0, GNG_data.loc[0, 'sub'])
                block_summary.insert(1, b_var)
                
                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = block_summary
                
            #update count for files loop
            count = 1

    else:
         overall_summary_data = 'no files'
            
    return overall_summary_data

## summary data function
def updateDatabase_save(GNG_summary_dat, overwrite_flag, bids_dir):
    import pandas as pd
    import numpy as np
    from pathlib import Path
    from nipype.interfaces.base import Bunch
    
    #get a Bunch object if more than 1 participant 
    if isinstance(GNG_summary_dat, Bunch):        
        #get output data from node
        GNG_summary_datlist = GNG_summary_dat.summaryGNG_dat
        
        #combine datasets 
        GNG_summary_dat = pd.concat(GNG_summary_datlist)
        
    #if only 1 participant/dataset then it is a list    
    elif isinstance(GNG_summary_dat, list):
        if len(GNG_summary_dat) == 1:
            GNG_summary_dat = GNG_summary_dat[0]
        else:
            GNG_summary_dat = pd.concat(GNG_summary_dat)

    #if a pandas dataframe
    if isinstance(GNG_summary_dat, pd.DataFrame):
        
        #get column names
        columnnames = GNG_summary_dat.columns
       
        #get condition subset (overall and each block)
        #GNG_summary_dat['block'] = GNG_summary_dat['block'].astype(str)
        GNG_summary_conditions = GNG_summary_dat[GNG_summary_dat.block.isin(['all', 'b1', 'b2', 'b3', 'b4', 'b5'])]

        #make wide data set (for every variable, a column for overall and each block)
        GNG_summary_wide = GNG_summary_conditions.pivot(columns='block', index='sub', values=columnnames[2:])        
        GNG_summary_wide.columns = ['_'.join(col) for col in GNG_summary_wide.columns.reorder_levels(order=[1, 0])]
        
        #make the sub index into a dataset column
        GNG_summary_wide = GNG_summary_wide.reset_index(level = 0)
        
        #re-order columns
        columnnames_reorder = ['sub', 'all_nGo', 'all_nNoGo', 'all_nAcc', 'all_pAcc', 'all_nGo_Hit', 'all_nGo_Miss', 'all_nNoGo_Corr', 
                              'all_nNoGo_FA', 'all_pGo_Hit', 'all_pGo_Miss', 'all_pNoGo_Corr', 'all_pNoGo_FA', 'all_RTmeanGo_Hit', 
                              'all_RTmeanNoGo_FA', 'all_RTmedGo_Hit', 'all_RTmedNoGo_FA',
        
                              'b1_nGo', 'b1_nNoGo', 'b1_nAcc', 'b1_pAcc', 'b1_nGo_Hit', 'b1_nGo_Miss', 'b1_nNoGo_Corr', 
                              'b1_nNoGo_FA', 'b1_pGo_Hit', 'b1_pGo_Miss', 'b1_pNoGo_Corr', 'b1_pNoGo_FA', 'b1_RTmeanGo_Hit', 
                              'b1_RTmeanNoGo_FA', 'b1_RTmedGo_Hit', 'b1_RTmedNoGo_FA',

                              'b2_nGo', 'b2_nNoGo', 'b2_nAcc', 'b2_pAcc', 'b2_nGo_Hit', 'b2_nGo_Miss', 'b2_nNoGo_Corr', 
                              'b2_nNoGo_FA', 'b2_pGo_Hit', 'b2_pGo_Miss', 'b2_pNoGo_Corr', 'b2_pNoGo_FA', 'b2_RTmeanGo_Hit', 
                              'b2_RTmeanNoGo_FA', 'b2_RTmedGo_Hit', 'b2_RTmedNoGo_FA',

                              'b3_nGo', 'b3_nNoGo', 'b3_nAcc', 'b3_pAcc', 'b3_nGo_Hit', 'b3_nGo_Miss', 'b3_nNoGo_Corr', 
                              'b3_nNoGo_FA', 'b3_pGo_Hit', 'b3_pGo_Miss', 'b3_pNoGo_Corr', 'b3_pNoGo_FA', 'b3_RTmeanGo_Hit', 
                              'b3_RTmeanNoGo_FA', 'b3_RTmedGo_Hit', 'b3_RTmedNoGo_FA',
        
                              'b4_nGo', 'b4_nNoGo', 'b4_nAcc', 'b4_pAcc', 'b4_nGo_Hit', 'b4_nGo_Miss', 'b4_nNoGo_Corr', 
                              'b4_nNoGo_FA', 'b4_pGo_Hit', 'b4_pGo_Miss', 'b4_pNoGo_Corr', 'b4_pNoGo_FA', 'b4_RTmeanGo_Hit', 
                              'b4_RTmeanNoGo_FA', 'b4_RTmedGo_Hit', 'b4_RTmedNoGo_FA',

                              'b5_nGo', 'b5_nNoGo', 'b5_nAcc', 'b5_pAcc', 'b5_nGo_Hit', 'b5_nGo_Miss', 'b5_nNoGo_Corr', 
                              'b5_nNoGo_FA', 'b5_pGo_Hit', 'b5_pGo_Miss', 'b5_pNoGo_Corr', 'b5_pNoGo_FA', 'b5_RTmeanGo_Hit', 
                              'b5_RTmeanNoGo_FA', 'b5_RTmedGo_Hit', 'b5_RTmedNoGo_FA']
        
        GNG_summary_wide = GNG_summary_wide.reindex(columns=columnnames_reorder)
    
        #get indiviudal blocks subset
        GNG_summary_blocks = GNG_summary_dat[GNG_summary_dat.block.isin(['b1', 'b2', 'b3', 'b4', 'b5'])] 
    
        ## load databases
        #derivative data path
        derivative_data_path = Path(bids_dir).joinpath('derivatives/preprocessed/beh')

        #load databases
        GNG_database = pd.read_csv(str(Path(derivative_data_path).joinpath('task-gng_summary.tsv')), sep = '\t') 
        GNG_database_long = pd.read_csv(str(Path(derivative_data_path).joinpath('task-gng_summary_long.tsv')), sep = '\t')

        #if overwriting participants
        if overwrite_flag == True:
            #function to drop rows based on values
            def filter_rows_by_values(df, col, values):
                return df[df[col].isin(values) == False]

            #get list of subs to filter in wide and long data
            wide_sub_list = list(GNG_summary_wide['sub'].unique())
            long_sub_list = list(GNG_summary_blocks['sub'].unique())

            #filter out/remove exisiting subs to overwrite
            GNG_database = filter_rows_by_values(GNG_database, 'sub', wide_sub_list)
            GNG_database_long = filter_rows_by_values(GNG_database_long, 'sub', long_sub_list)

        #add newly processed data
        GNG_database = GNG_database.append(GNG_summary_wide)
        GNG_database_long = GNG_database_long.append(GNG_summary_blocks)

        #write databases
        GNG_database.to_csv(str(Path(derivative_data_path).joinpath('task-gng_summary.tsv')), sep = '\t', encoding='utf-8-sig', index = False) 
        GNG_database_long.to_csv(str(Path(derivative_data_path).joinpath('task-gng_summary_long.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

    else:
        print('No raw data files that need to be processed')
        GNG_database = np.nan
        GNG_database_long = np.nan
        
    return GNG_database, GNG_database_long

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

        raw_file = list(Path(raw_data_path).rglob('sub-' + str(sub) + '/ses-1/beh/*gng*.tsv'))

        if len(raw_file) < 1:
            print('No Files found for sub-' + str(sub))
            subject_list.remove(sub)
        
    #check if any files to process
    if subject_list is None:
        sys.exit('No Files found for participants' + args.parIDs)   

else:
    #no participants entered - find all files for session
    gng_raw_files = list(Path(raw_data_path).rglob('sub-*/ses-1/beh/*gng*.tsv'))

    #pathlib library -- .relative_to give all the path that follows raw_data_path
    #                   .parts[0] extracts the first directory in remaining path to get
    #                       list of subjects
    gng_raw_subs = [item.relative_to(raw_data_path).parts[0] for item in gng_raw_files]

    #set is finding only unique values
    subject_list = list(set([item[4:7] for item in gng_raw_subs]))   

# move back to script directory
os.chdir(script_path)

#build workflow
GNG_WF = Workflow('GNG')

#summary data - define earlier than use so can connect to workflow based
#on user input arguments
sumResults = MapNode(Function(input_names = ['GNG_file', 'session_id'],
                           output_names = ['summaryGNG_dat'],
                           function = summaryGNG),
                     iterfield = ['GNG_file'],
                     name = 'summaryData')

# get subject ids that need to be procssed
if args.overwrite is None:
        
    #load data 
    database = Path(database_path).joinpath('task-gng_summary.tsv')
    gng_database = pd.read_csv(str(database), sep = '\t', encoding = 'utf-8-sig', header = 0, engine='python')
    
    #get unique ids
    subs_exist = gng_database['sub'].unique()
    
    #make match format of subject_list
    subs_exist_str = [str(item).zfill(3) for item in subs_exist]
    
    #compare subject_list to subs_exist
    for sub in subject_list:
        if sub in subs_exist_str:
            
            #remove sub if in list that exists in database already
            print('Skipping sub-' + str(sub) + ' - Exists in database already.')
            subject_list.remove(sub)
        
    #node to get list of ids to process - selectfiles
    if len(subject_list) > 0:
                
        template_path = Path('sub-%s/ses-1/beh/*task-gng*.tsv')
        selectfiles = Node(DataGrabber(infields=['subject_ids'],
                      outfields=['gngFiles'],
                      base_directory = str(raw_data_path), 
                      template = str(template_path),
                      sort_filelist = True),
          name='selectfiles')
        
        selectfiles.inputs.subject_ids = subject_list
        
        #Connect select node and sesseion to summary results node
        GNG_WF.connect(selectfiles, "gngFiles", sumResults, "GNG_file")
        
    else:
        #exit if no files exist
        sys.exit('No new subjects to add to database')   

#overwrite option specified     
else:
    # select files Node 
    template_path = Path('sub-%s/ses-1/beh/*task-gng*.tsv')
    selectfiles = Node(DataGrabber(infields=['subject_ids'],
                  outfields=['gngFiles'],
                  base_directory = str(raw_data_path), 
                  template = str(template_path),
                  sort_filelist = True),
      name='selectfiles')
        
    #manually set subject list in selectfiles
    selectfiles.inputs.subject_ids = subject_list
        
    #Connect selectfiles to summary results node
    GNG_WF.connect(selectfiles, "gngFiles", sumResults, "GNG_file")

#concatonate blocks and update/save database
if args.overwrite is None:
    dat_overwrite = False
else:
    dat_overwrite = True

database_saveDat = Node(Function(input_names = ['GNG_summary_dat', 'overwrite_flag', 'bids_dir'],
                           output_names = ['GNG_database', 'GNG_database_wide'],
                           function = updateDatabase_save),
                     name = 'gngDatabase')
database_saveDat.inputs.overwrite_flag = dat_overwrite
database_saveDat.inputs.bids_dir = str(base_directory)

GNG_WF.connect(sumResults, "summaryGNG_dat", database_saveDat, "GNG_summary_dat")

res = GNG_WF.run()


