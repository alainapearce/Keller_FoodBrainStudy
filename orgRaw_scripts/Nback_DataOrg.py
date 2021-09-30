#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The purpose of this script is to organize the source data for the the Nback task
into BIDS rawdata format. Written by Alaina L Pearce and Bari Fuchs in Summer 2021.

@author: azp271@psu.edu, baf44@psu.edu
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

# function to get experiment name
def get_task_info(raw_filepath):

    #load data
    nback_raw_data = pd.read_csv(raw_filepath, sep = '\t') 
    
    #Extract experiment name
    exp_subname = nback_raw_data.loc[2,"Subject"]

    #Extract number of columns
    ncol = len(nback_raw_data.columns)

    # return pandas dataset
    return(exp_subname, ncol)

# function to append error message to error_file
def log_error(error_str: str):
    with open(Path(script_path).joinpath('Nback_DataOrg_error.txt'), "a") as error_file:
        error_file.write(error_str + "\n")

# function to rename Nback E-Prime raw data and copy/rename json template file
def bidsformat_nback_raw(raw_filepath, block, base_directory):

    #load data
    nback_raw_data = pd.read_csv(raw_filepath, sep = '\t') 

    #number of columns
    ncols = len(nback_raw_data.columns)

    # remove 'DEVICE' columns from datafiles with more than 44 columns
    if len(nback_raw_data.columns) != 44:
        nback_raw_data = nback_raw_data.loc[:, ~nback_raw_data.columns.str.contains('DEVICE')]
    
    #column rename
    if ncols == 42:
        nback_raw_data.columns = ['experiment_name', 'sub', 'ses', 'data_file_basename', 
            'display_refresh_rate', 'group', 'random_seed', 'session_date', 'session_start_date_time_utc', 
            'session_time', 'block','list1', 'list1_cycle', 'list1_sample',	'procedure_block', 'running_block',	'trial', 'b' + block + '_list1', 
            'b' + block + '_list1_cycle',  'b' + block + '_list1_sample',  'b' + block + '_list2',  'b' + block + '_list2_cycle',	
            'b' + block + '_list2_sample', 'b' + block + '_stim', 'b' + block + '_stim_acc', 'b' + block + '_stim_cresp', 
            'b' + block + '_stim_duration_error', 'b' + block + '_stim_onset_delay', 'b' + block + '_stim_onset_time', 
            'b' + block + '_stim_onset_to_onset_time', 'b' + block + '_stim_resp', 'b' + block + '_stim_rt', 'b' + block + '_stim_rt_time', 
            'condition', 'correct', 'font', 'procedure_trial', 'running_trial']
    elif ncols == 36:
        nback_raw_data.columns = ['experiment_name', 'sub', 'ses', 'data_file_basename', 
            'display_refresh_rate', 'group', 'random_seed', 'session_date', 'session_start_date_time_utc', 
            'session_time', 'block', 'procedure_block', 'running_block', 'trial', 'b' + block + '_list1', 
            'b' + block + '_list1_cycle',  'b' + block + '_list1_sample',  'b' + block + '_list2',  'b' + block + '_list2_cycle',	
            'b' + block + '_list2_sample', 'b' + block + '_stim', 'b' + block + '_stim_acc', 'b' + block + '_stim_cresp', 
            'b' + block + '_stim_duration_error', 'b' + block + '_stim_onset_delay', 'b' + block + '_stim_onset_time', 
            'b' + block + '_stim_onset_to_onset_time', 'b' + block + '_stim_resp', 'b' + block + '_stim_rt', 'b' + block + '_stim_rt_time', 
            'condition', 'correct', 'font', 'procedure_trial', 'running_trial']
    else:
        nback_raw_data.columns = ['experiment_name', 'sub', 'ses', 'clock_information', 'data_file_basename', 
            'display_refresh_rate', 'experiment_version', 'group', 'random_seed', 'runtime_capabilities', 'runtime_version', 
            'runtime_version_expected', 'session_date', 'session_start_date_time_utc', 'session_time', 'studio_version', 
            'block','list1', 'list1_cycle', 'list1_sample',	'procedure_block', 'running_block',	'trial', 'b' + block + '_list1', 
            'b' + block + '_list1_cycle',  'b' + block + '_list1_sample',  'b' + block + '_list2',  'b' + block + '_list2_cycle',	
            'b' + block + '_list2_sample', 'b' + block + '_stim', 'b' + block + '_stim_acc', 'b' + block + '_stim_cresp', 
            'b' + block + '_stim_duration_error', 'b' + block + '_stim_onset_delay', 'b' + block + '_stim_onset_time', 
            'b' + block + '_stim_onset_to_onset_time', 'b' + block + '_stim_resp', 'b' + block + '_stim_rt', 'b' + block + '_stim_rt_time', 
            'condition', 'correct', 'font', 'procedure_trial', 'running_trial']
    
    # replace black with n/a
    nback_raw_data.fillna('n/a', inplace=True)

    # return pandas dataset
    return(nback_raw_data)

##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################

# get script location
script_path = Path(os.path.dirname(__file__))

# change directory to base directory and get path
os.chdir(script_path)
os.chdir('..')
base_directory = Path(os.getcwd())

#set specific paths
bids_source_path = Path(base_directory).joinpath('BIDSdat/sourcedata')
bids_raw_path = Path(base_directory).joinpath('BIDSdat/raw_data')
nback_raw_path = Path(base_directory).joinpath('Nback_Raw')

#get list of raw Nback files
nback_raw_files = list(Path(nback_raw_path).rglob('NBack*.txt'))

#Create error file. Overwrite existing error file if it exists
error_file = open(Path(script_path).joinpath('GNG_DataOrg_error.txt'), "w+")

# loop through files in raw Nback directory
for filepath in nback_raw_files:

    # get filename
    filename = os.path.basename(filepath)

    # extract sub, sess, and block info from filename
    subname = filename[12:15] 
    sesnum =  filename[16]  
    block = filename[6] 

    #extract experiment name, eprime version, number of columns, taskversion of source dataframe
    task_info = get_task_info(filepath)
    exp_subname = task_info[0]
    ncol_source = task_info[1]

    # make BIDS source directory structure if needed
    beh_source_bids_path = Path(bids_source_path).joinpath('sub-' + subname + '/ses-' + sesnum + '/beh')
    Path(beh_source_bids_path).mkdir(parents=True, exist_ok=True) 

    #copy exported .txt file to sourcedata
    copy2(filepath, Path(beh_source_bids_path))

    # set json file templates for raw GNG and practice file
    json_template_path = Path(base_directory).joinpath('orgRaw_scripts/templates_json/task-nback' + block + '_' + str(ncol_source) + 'col_source_template.json')

    # set raw GNG json file destination names
    json_nback_sourcename = Path(beh_source_bids_path).joinpath('NBack_' + block + '_Raw_' + subname + '-' + sesnum + '.json')

    #copy source json file
    copy2(json_template_path, Path(json_nback_sourcename))
    
    #get file paths to start checking
    eprime_filepath = Path(nback_raw_path).joinpath(block + '-back_R01-' + str(exp_subname) + '-' + sesnum + '.edat*') 
    eprimeXML_filepath = Path(nback_raw_path).joinpath(block + '-back_R01-' + str(exp_subname) + '-' + sesnum + '-ExperimentAdvisorReport.xml')    
    eprimeTXT_filepath = Path(nback_raw_path).joinpath(block + '-back_R01-' + str(exp_subname) + '-' + sesnum + '.txt')  
    
    #check if eprime files exist and copy
    if not eprime_filepath.exists():
        
        #check with zeros in sub number
        eprime_filepath = Path(nback_raw_path).joinpath(block + '-back_R01-' + subname + '-' + sesnum + '.edat*')

        if not eprime_filepath.exists():

            # write out if no eprime file
            eprime_err = 'sub-' + subname + '_ses-' + sesnum + ' has no edat file in NbackRaw for block' + block
            print(eprime_err)
                    
            #open error file and append error message
            log_error(eprime_err)
                        
        else:
            # copy eprime file
            copy2(eprime_filepath, Path(beh_source_bids_path))     
    else:
        # copy eprime file
        copy2(eprime_filepath, Path(beh_source_bids_path))

    #check if eprime xml files exist and copy
    if not eprimeXML_filepath.exists():
        
        #check with zeros in sub number
        eprimeXML_filepath = Path(nback_raw_path).joinpath(block + '-back_R01-' + subname + '-' + sesnum + '-ExperimentAdvisorReport.xml')
        
        if not eprimeXML_filepath.exists():
            # write out participant doesn't have file
            xml_error = 'sub-' + subname + '_ses-' + sesnum + ' has no xml file in NbackRaw for block' + block
            print(xml_error)
            
            #open error file and append error message
            log_error(eprime_err)
                    
        else:
            # copy file
            copy2(eprimeXML_filepath, Path(beh_source_bids_path))

    else:
        # copy file
        copy2(eprimeXML_filepath, Path(beh_source_bids_path))
    
    #check if eprime xml files exist and copy
    if not eprimeTXT_filepath.exists():
    
        #check with zeros in sub number
        eprimeTXT_filepath = Path(nback_raw_path).joinpath(block + '-back_R01-' + subname + '-' + sesnum + '.txt')

        if not eprimeTXT_filepath.exists():
            # write out participant doesn't have file
            txt_error = 'sub-' + subname + '_ses-' + sesnum + ' has no .txt file in NbackRaw for block' + block
            print(txt_error)
            
            #open error file and append error message
            log_error(eprime_err)
        
        else:
            # copy file
            copy2(eprimeTXT_filepath, Path(beh_source_bids_path))

    else:
        # copy file
        copy2(eprimeTXT_filepath, Path(beh_source_bids_path))


    #get list of practice files that contain subname with or without leading zeros
    pattern1 = 'R01_practice_' + block + '-back-' + subname + '-' + sesnum
    pattern2 = 'R01_practice_' + block + '-back-' + subname.lstrip('0') + '-' + sesnum
    nback_practice_files = list(Path(nback_raw_path).glob(pattern1 + "*")) + list(Path(nback_raw_path).glob(pattern2 + "-*"))

    # if no practice files and experiment did not contain practice trials (i.e., exp_name = Go No-Go Zoo_pseudorand), log error
    if len(nback_practice_files) == 0:
        practice_err = 'sub-' + subname + ' has no practice files'
        print(practice_err)
        #open error file and append error message
        log_error(practice_err)
    
    else: # copy practice files and corresponding json into source data
        for practicefile in nback_practice_files:
            copy2(practicefile, Path(beh_source_bids_path))

    # make BIDS raw directory structure if needed
    beh_raw_bids_path = Path(bids_raw_path).joinpath('sub-' + subname + '/ses-' + sesnum + '/beh')
    Path(beh_raw_bids_path).mkdir(parents=True, exist_ok=True) 

    # set bids file name to check if file exists
    bids_filename = Path(beh_raw_bids_path).joinpath('sub-' + subname + '_ses-' + sesnum + '_task-nback' + block + '_events.tsv') 
    
    # if file has not been moved, edit column names and save
    if not bids_filename.exists():

        # run funtion to rename columns
        bids_nback_data = bidsformat_nback_raw(filepath, block, base_directory) 
        
        # write to tsv file
        bids_nback_data.to_csv(bids_filename, sep="\t", encoding='utf-8-sig')

    else:
        # write out participants already processed
        print('sub-' + subname + '_ses-' + sesnum + '_task-nback' + block + '_events.tsv exists')
        
