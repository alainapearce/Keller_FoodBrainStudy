#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The purpose of this script is to organize the source data for the Go No Go
into BIDS rawdata format. Written Summer 2021.

@author: Bari Fuchs
"""

import pandas as pd
import os
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
    gng_raw_data = pd.read_csv(raw_filepath, sep = '\t') 
    
    #Extract experiment name
    exp_name = gng_raw_data.loc[2,"ExperimentName"]

    #Extract eprime version
    if gng_raw_data.loc[2,"RuntimeVersion"].startswith("2"):
        eprime_ver = "2"
        
    elif gng_raw_data.loc[2,"RuntimeVersion"].startswith("3"):
        eprime_ver = "3"

    #Extract number of columns
    ncol = len(gng_raw_data.columns)
    
    #Set file version
    if exp_name == 'Go No-Go Zoo Task1':
        file_version = "1"
    
    if exp_name == 'Go No-Go Zoo_pseudorand' and ncol == 58:
        file_version = "2"
        
    if exp_name == 'Go No-Go Zoo_pseudorand' and ncol == 76:
        file_version = "3"

    # return pandas dataset
    return(exp_name, eprime_ver, ncol, file_version)

# function to append error message to error_file
def log_error(error_str: str):
    with open(Path(script_path).joinpath('GNG_DataOrg_error.txt'), "a") as error_file:
        error_file.write(error_str + "\n")

# function to remove columns/rows associated with practice trials and rename GNG raw data columns
def bidsformat_gng_raw(raw_filepath):

    #load data
    gng_raw_data = pd.read_csv(raw_filepath, sep = '\t') 

    if gng_raw_data.ExperimentName[1] == 'Go No-Go Zoo Task1':
        
        # Drop rows associated with practice trials (Prac = 1)
        gng_raw_data = gng_raw_data[gng_raw_data.Prac != 1]
        
        # Drop columns associated with practice trials
        drop_cols = ['Prac','Prac.Cycle','Prac.Sample','Practice','Practice.Cycle','Practice.Sample']
        gng_raw_data = gng_raw_data.drop(drop_cols, axis=1)

    # remove 'DEVICE' columns from datafiles with 76 columns
    if len(gng_raw_data.columns) == 76:
        gng_raw_data = gng_raw_data.loc[:, ~gng_raw_data.columns.str.endswith('DEVICE')]
        
    # rename variables in BIDS format
    gng_raw_data.columns = ['experiment_name', 'sub', 'ses', 'clock_information','data_file_basename', 
        'display_refresh_rate', 'experiment_version', 'group', 'random_seed', 'runtime_capabilities', 'runtime_version', 
        'runtime_version_expected', 'session_date', 'session_start_date_time_utc', 'session_time', 'studio_version', 
        'block','block_list','block_list_cycle', 'block_list_sample', 'order','procedure_block','running_block','trial','ca','compatibility',
        'gonogo','image','imagecode','procedure_trial','respond_acc','respond_cresp','respond_resp','respond_rt','respond_rt_time','running_trial',
        's1','stim_acc','stim_cresp','stim_resp','stim_rt','stim_rt_time','target','trial1','trial1_cycle','trial1_sample',
        'trial2','trial2_cycle','trial2_sample','trial3','trial3_cycle','trial3_sample','trial4','trial4_cycle','trial4_sample',
        'trial5','trial5_cycle','trial5_sample']
    
    # return pandas dataset
    return(gng_raw_data)

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
gng_raw_path = Path(base_directory).joinpath('untouchedRaw/GNG_Raw')

#get list of raw GNG files
#Note: these are text files exported from the corresponding edat file
gng_raw_files = list(Path(gng_raw_path).rglob('GNG_Zoo_Raw*.txt'))

#Create error file. Overwrite existing error file if it exists
error_file = open(Path(script_path).joinpath('GNG_DataOrg_error.txt'), "w+")

# loop through files in raw GNG directory
for filepath in gng_raw_files:
    
    # get filename
    filename = os.path.basename(filepath)

    # extract subject from filename
    subname = filename[12:15] 

    #extract experiment name, eprime version, number of columns, taskversion of source dataframe
    task_info = get_task_info(filepath)
    exp_name = task_info[0]
    eprime_ver = task_info[1]
    ncol_source = task_info[2]
    file_version = task_info[3]

    # make BIDS source directory structure if needed
    beh_source_bids_path = Path(bids_source_path).joinpath('sub-' + subname + '/ses-1/beh')
    Path(beh_source_bids_path).mkdir(parents=True, exist_ok=True) 

    # copy raw GNG file into sourcedata
    copy2(filepath, Path(beh_source_bids_path))
    
    # set json file templates for raw GNG and practice file
    json_template_task1_path = Path(base_directory).joinpath('orgRaw_scripts/templates_json/task-gng_task1_source_template.json')
    json_template_pseudo_v2_path = Path(base_directory).joinpath('orgRaw_scripts/templates_json/task-gng_pseudorand_58col_source_template.json')
    json_template_pseudo_v3_path = Path(base_directory).joinpath('orgRaw_scripts/templates_json/task-gng_pseudorand_76col_source_template.json')

    # set raw GNG json file destination names
    json_gng_dest_filename = Path(beh_source_bids_path).joinpath('GNG_Zoo_Raw-' + subname + '-1.json')

    # Copy json file for raw GNG file (based on file verison) into sourcedata
    if file_version == '1':
        copy2(json_template_task1_path, Path(json_gng_dest_filename))
        
    if file_version == '2':
        copy2(json_template_pseudo_v2_path, Path(json_gng_dest_filename))

    if file_version == '3':
        copy2(json_template_pseudo_v3_path, Path(json_gng_dest_filename))

## NOTE: exp_name does not correspond to expected filename for all participants (some files may have been renamed). 
#Thus, to copy eprime file, check for every potential filename for each file

    #copy source eprime outputs into sourcedata
    #copy edat file
    eprime_filename = Path(gng_raw_path).joinpath('Go No-Go Zoo Task1-' + subname.lstrip('0') + '-1.edat' + eprime_ver)
    if not eprime_filename.exists():
        #check with zeros in sub number
        eprime_filename = Path(gng_raw_path).joinpath('Go No-Go Zoo Task1-' + subname + '-1.edat' + eprime_ver)
        if not eprime_filename.exists():
            #check with alternative taskname and no leading zeros in sub number
            eprime_filename = Path(gng_raw_path).joinpath('Go No-Go Zoo_pseudorand-' + subname.lstrip('0') + '-1.edat' + eprime_ver)
            if not eprime_filename.exists():
                #check with alternative taskname and leading zeros in sub number
                eprime_filename = Path(gng_raw_path).joinpath('Go No-Go Zoo_pseudorand-' + subname + '-1.edat' + eprime_ver)   
                if not eprime_filename.exists():
                    # write out if no edat file
                    eprime_err = 'sub-' + subname + ' has no GNG edat file'
                    print(eprime_err)
                    #open error file and append error message
                    log_error(eprime_err)
                else:
                    copy2(eprime_filename, Path(beh_source_bids_path))
            else:
                copy2(eprime_filename, Path(beh_source_bids_path))
        else:
            copy2(eprime_filename, Path(beh_source_bids_path))
    else:
        copy2(eprime_filename, Path(beh_source_bids_path))


    #copy ExperimentAdvisorReport
    eprimeXML_filename = Path(gng_raw_path).joinpath('Go No-Go Zoo Task1-' + subname.lstrip('0') + '-1-ExperimentAdvisorReport.xml')
    if not eprimeXML_filename.exists():
        #check with zeros in sub number
        eprimeXML_filename = Path(gng_raw_path).joinpath('Go No-Go Zoo Task1-' + subname + '-1-ExperimentAdvisorReport.xml')
        if not eprimeXML_filename.exists():
            #check with alternative taskname and no leading zeros in sub number
            eprimeXML_filename = Path(gng_raw_path).joinpath('Go No-Go Zoo_pseudorand-' + subname.lstrip('0') + '-1-ExperimentAdvisorReport.xml')
            if not eprimeXML_filename.exists():
                #check with alternative taskname and leading zeros in sub number
                eprimeXML_filename = Path(gng_raw_path).joinpath('Go No-Go Zoo_pseudorand-' + subname + '-1-ExperimentAdvisorReport.xml')   
                if not eprimeXML_filename.exists():
                    # write out if no edat file
                    eprime_err = 'sub-' + subname + ' has no GNG xml file'
                    print(eprime_err)
                    #open error file and append error message
                    log_error(eprime_err)
                else:
                    copy2(eprimeXML_filename, Path(beh_source_bids_path))
            else:
                copy2(eprimeXML_filename, Path(beh_source_bids_path))
        else:
            copy2(eprimeXML_filename, Path(beh_source_bids_path))
    else:
        copy2(eprimeXML_filename, Path(beh_source_bids_path))

    
    #copy eprime txt file
    eprimeTXT_filename = Path(gng_raw_path).joinpath('Go No-Go Zoo Task1-' + subname.lstrip('0') + '-1.txt')
    if not eprimeTXT_filename.exists():
        #check with zeros in sub number
        eprimeTXT_filename = Path(gng_raw_path).joinpath('Go No-Go Zoo Task1-' + subname + '-1.txt')
        if not eprimeTXT_filename.exists():
            #check with alternative taskname and no leading zeros in sub number
            eprimeTXT_filename = Path(gng_raw_path).joinpath('Go No-Go Zoo_pseudorand-' + subname.lstrip('0') + '-1.txt')
            if not eprimeTXT_filename.exists():
                #check with alternative taskname and leading zeros in sub number
                eprimeTXT_filename = Path(gng_raw_path).joinpath('Go No-Go Zoo_pseudorand-' + subname + '-1.txt')   
                if not eprimeTXT_filename.exists():
                    # write out if no edat file
                    eprime_err = 'sub-' + subname + ' has no GNG txt file'
                    print(eprime_err)
                    #open error file and append error message
                    log_error(eprime_err)
                else:
                    copy2(eprimeTXT_filename, Path(beh_source_bids_path))
            else:
                copy2(eprimeTXT_filename, Path(beh_source_bids_path))
        else:
            copy2(eprimeTXT_filename, Path(beh_source_bids_path))
    else:
        copy2(eprimeTXT_filename, Path(beh_source_bids_path))


    #check if practice files exist and copy into source data

    #get list of practice files that contain subname with or without leading zeros
    pattern1 = 'Go No-Go Zoo Task_practice-' + subname
    pattern2 = 'Go No-Go Zoo Task_practice-' + subname.lstrip('0')
    gng_practice_files = list(Path(gng_raw_path).glob(pattern1 + "*")) + list(Path(gng_raw_path).glob(pattern2 + "-*"))
    
    # if no practice files and experiment did not contain practice trials (i.e., exp_name = Go No-Go Zoo_pseudorand), log error
    if exp_name == 'Go No-Go Zoo_pseudorand' and not gng_practice_files:
        practice_err = 'sub-' + subname + ' has no practice file'
        print(practice_err)
        #open error file and append error message
        log_error(practice_err)
    
    # copy practice files into source data
    else:
        for practicefile in gng_practice_files:
            copy2(practicefile, Path(beh_source_bids_path))

    # make BIDS raw directory structure if needed
    beh_raw_bids_path = Path(bids_raw_path).joinpath('sub-' + subname + '/ses-1/beh')
    Path(beh_raw_bids_path).mkdir(parents=True, exist_ok=True) 

    # set bids file name to check if file exists
    bids_filename = Path(beh_raw_bids_path).joinpath('sub-' + subname + '_ses-1_task-gng_events.tsv') 
    
    # if file has not been moved, edit column names and save
    if not bids_filename.exists():

        # run funtion to rename columns
        bids_gng_data = bidsformat_gng_raw(filepath) 
        
        # write to tsv file
        bids_gng_data.to_csv(bids_filename, sep="\t", encoding='utf-8-sig', index = False)
        
    else:
        # write out participants already processed
        print('sub-' + subname + '_ses-1_task-gng_events.tsv exists')
        
