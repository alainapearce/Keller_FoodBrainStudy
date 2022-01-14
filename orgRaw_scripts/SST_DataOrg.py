#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The purpose of this script is to organize the source data for the Stop Signal 
Task into BIDS rawdata format. Written Summer 2021.

@author: Alaina Pearce
"""

import pandas as pd
import os
import shutil
from shutil import copy2
# import pathlib so can detect if Windows or not
from pathlib import Path

##############################################################################
####                                                                      ####
####                  Subfunctions called within script                   ####
####                                                                      ####
##############################################################################


# function to rename SST raw data
def bidsformat_sst_raw(raw_filepath, subname):

    #load data
    sst_raw_data = pd.read_csv(raw_filepath, sep = '\t') 

    #add sub to data
    sst_raw_data.insert(0, 'sub', subname)

    # rename variables in BIDS format
    sst_raw_data.columns = ['sub', 'block', 'block_cond', 'food_cond', 'portion_cond', 'stimuli',	'stop_signal', 'req_ssd',
    'correct',	'resp_1', 'resp_2',	'rt_1', 'rt_2',	'true_ssd',	'stimuli_name']
    
    # return pandas dataset
    return(sst_raw_data)

##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################

# get script location
script_path = Path(__file__).parent.resolve()

# change directory to base directory and get path
os.chdir(script_path)
os.chdir('..')
base_directory = Path(os.getcwd())

#set specific paths
bids_source_path = Path(base_directory).joinpath('BIDSdat/sourcedata')
bids_raw_path = Path(base_directory).joinpath('BIDSdat/raw_data')
sst_raw_path = Path(base_directory).joinpath('untouchedRaw/SST_Raw')

#get list of raw SST files
sst_raw_files = list(Path(sst_raw_path).rglob('stop-*.txt'))

#error count
n_error = 0

# loop through files in raw SST directory
for filepath in sst_raw_files:

    # get filename
    filename = os.path.basename(filepath)

    # extract subject from filename
    if len(filename) < 12 or len(filename) > 14:
        raw_name_error = 'naming does not follow known naming convention: ' + filename
        print(raw_name_error)
        
        #check errors - if no errors, start error .txt output
        if n_error == 0:
                        
            #open .txt file
            with open(Path(script_path).joinpath('SST_DataOrg_error.txt'), "w+") as error_file:
                error_file.write(raw_name_error)
                        
                #update error
                n_error = n_error + 1
            
        #if already had error, add to error .txt output
        else:
            with open(Path(script_path).joinpath('SST_DataOrg_error.txt'), "a") as error_file:
                error_file.write(raw_name_error)
        
        #skip rest of loop/go to next file
        continue
    
    #single digit number    
    elif len(filename) == 12:
        subnum = filename[5:6]
    #double digit number
    elif len(filename) == 13:
        subnum = filename[5:7]
    #tripple digit number
    elif len(filename) == 14:
        subnum = filename[5:8] 
        
    # pad subnum with zeros
    subname = str(subnum).zfill(3)
    
    # make BIDS source directory structure if needed
    beh_source_bids_path = Path(bids_source_path).joinpath('sub-' + subname + '/ses-1/beh')
    Path(beh_source_bids_path).mkdir(parents=True, exist_ok=True) 

    #copy source .txt outputs into sourcedata
    copy2(filepath, Path(beh_source_bids_path))
    
    #copy source json file into sourcedata
    json_template_path = Path(base_directory).joinpath('orgRaw_scripts/templates_json/task-sst_source_template.json')
    json_dest_filename = Path(beh_source_bids_path).joinpath('stop-' + subnum + '-1.json')
    shutil.copy(json_template_path, json_dest_filename)

    #check if practice files exist and copy source data with json files
    sst_prac_filename = Path(sst_raw_path).joinpath('stop_prac-' + subnum + '-1.txt')
    
    if not sst_prac_filename.exists():
        
        #check with zeros in sub number
        sst_prac_filename = Path(sst_raw_path).joinpath('stop_prac-' + subname + '-1.txt')
        
        if not sst_prac_filename.exists():
            
            # write out if no eprime file
            prac_err = 'sub-' + subname + '_ses-1 has no practice .txt file in SST_Raw'
            print(prac_err)
                    
            #check errors - if no errors, start error .txt output
            if n_error == 0:
                        
                #open .txt file
                with open(Path(script_path).joinpath('SST_DataOrg_error.txt'), "w+") as error_file:
                    error_file.write(prac_err)
                        
                    #update error
                    n_error = n_error + 1
            
            #if already had error, add to error .txt output
            else:
                with open(Path(script_path).joinpath('SST_DataOrg_error.txt'), "a") as error_file:
                    error_file.write(prac_err)
                        
        else:
           # copy practice .txt file
            copy2(sst_prac_filename, Path(beh_source_bids_path))
            
            # copy practice source json file into sourcedata
            json_prac_dest_filename = Path(beh_source_bids_path).joinpath('stop_prac-' + subnum + '-1.json')
            shutil.copy(json_template_path, json_prac_dest_filename)
            
    else:
        # copy practice .txt file
        copy2(sst_prac_filename, Path(beh_source_bids_path))
        
        # copy practice source json file into sourcedata
        json_prac_dest_filename = Path(beh_source_bids_path).joinpath('stop_prac-' + subnum + '-1.json')
        shutil.copy(json_template_path, json_prac_dest_filename)


    # make BIDS raw directory structure if needed
    beh_raw_bids_path = Path(bids_raw_path).joinpath('sub-' + subname + '/ses-1/beh')
    Path(beh_raw_bids_path).mkdir(parents=True, exist_ok=True) 

    # set bids file name to check if file exists
    bids_filename = Path(beh_raw_bids_path).joinpath('sub-' + subname + '_ses-1_task-sst_events.tsv') 
    
    # if file has not been moved, edit column names and save
    if not bids_filename.exists():

        # run funtion to rename columns
        bids_sst_data = bidsformat_sst_raw(filepath, subname) 
        
        # write to tsv file
        bids_sst_data.to_csv(bids_filename, sep="\t", encoding='utf-8-sig', index = False)
        
    else:
        # write out participants already processed
        print('sub-' + subname + '_ses-1_task-sst_events.tsv exists')
        
