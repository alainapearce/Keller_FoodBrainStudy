#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The purpose of this script is to organize the source data for the foodcue fMRI task
into BIDS rawdata format. Written Spring 2022.

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

# function to reformat column names
def bidsformat_foodcue_raw(raw_filepath):

    #load data
    foodcue_raw_data = pd.read_csv(raw_filepath, sep = '\t') 

    # rename variables in BIDS format

    ## rename to lowercase
    foodcue_raw_data.columns= foodcue_raw_data.columns.str.lower()

    ## replace "." and "[" with "_"; remove "]"
    foodcue_raw_data.columns = foodcue_raw_data.columns.str.replace(".", "_", regex=False)
    foodcue_raw_data.columns = foodcue_raw_data.columns.str.replace("[", "_", regex=False)
    foodcue_raw_data.columns = foodcue_raw_data.columns.str.replace("]", "", regex=False)


    ## manually change eprime variable names to match variable names of other tasks  (e.g., go no go)
    foodcue_raw_data = foodcue_raw_data.rename(columns={'experimentname': 'experiment_name', 
                                                        'subject': 'sub',
                                                        'session': 'ses',
                                                        'data_filebasename': 'data_file_basename',
                                                        'experimentversion': 'experiment_version',
                                                        'runtimecapabilities': 'runtime_capabilities',
                                                        'runtimeversion': 'runtime_version',
                                                        'runtime_version_expected': 'runtime_version_expected',
                                                        'sessiondate': 'session_date',
                                                        'sessionstartdatetimeutc': 'session_start_date_time_utc',
                                                        'sessiontime': 'session_time',
                                                        'studioversion': 'studio_version'})    

    # return pandas dataset
    return(foodcue_raw_data)

# function to add columns that are required for functional task event files
def bidsformat_foodcue_func(foodcue_raw_data):

    
    # make new variable: "onset" (in seconds) of the event, measured from the beginning of the acquisition of the
    # first data point stored in the corresponding task data file. Runs started with a 4s fixation, so the onset time of first stimulus (['stimslide_onsettime'].iloc[0])
    # should be equal to 4
    stim1_onset = foodcue_raw_data['stimslide_onsettime'].iloc[0]
    foodcue_raw_data['onset_unrounded'] = ((foodcue_raw_data['stimslide_onsettime'] - stim1_onset)/1000) + 4
    foodcue_raw_data['onset'] = foodcue_raw_data.onset_unrounded.map(lambda x:round(x))

    # make new variable: "duration" of the event (measured from onset) in seconds
    foodcue_raw_data['duration'] = foodcue_raw_data['stimslide_duration']/1000

    # return pandas dataset
    return(foodcue_raw_data)    

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
fmri_raw_path = Path(base_directory).joinpath('untouchedRaw/fMRITask_Raw')

#get list of raw fMRITask files
#Note: these are text files exported from the corresponding edat file
fmri_raw_files = list(Path(fmri_raw_path).rglob('fMRI*Raw*.txt'))

#Create error file. Overwrite existing error file if it exists
error_file = open(Path(script_path).joinpath('foodcue_DataOrg_error.txt'), "w+")

# loop through files in raw fmriTask directory
for filepath in fmri_raw_files:
    
    # get filename
    filename = os.path.basename(filepath)

    # extract subject from filename
    subname = filename[11:14] 

    # extract task version (A or B) from filename
    task_version = filename[5:6] 

    #load data
    foodcue_data = pd.read_csv(filepath, sep = '\t') 
    
    #Get list of experiment name(s)
    exp_names = foodcue_data.ExperimentName.unique()
    exp_list = exp_names.tolist()

    # make BIDS source directory structure if needed
    beh_source_bids_path = Path(bids_source_path).joinpath('sub-' + subname + '/ses-1/beh')
    Path(beh_source_bids_path).mkdir(parents=True, exist_ok=True) 

    # copy raw fMRItask file into sourcedata
    copy2(filepath, Path(beh_source_bids_path))
    
    # set json file templates for raw fMRI task files
    if len(foodcue_data.columns) == 171:
        json_template_path = Path(base_directory).joinpath('orgRaw_scripts/templates_json/task-foodcue_171col_source_template.json')
    if len(foodcue_data.columns) == 144:
        json_template_path = Path(base_directory).joinpath('orgRaw_scripts/templates_json/task-foodcue_144col_source_template.json')
    if len(foodcue_data.columns) == 129:
        json_template_path = Path(base_directory).joinpath('orgRaw_scripts/templates_json/task-foodcue_129col_source_template.json')
    if len(foodcue_data.columns) == 108:
        json_template_path = Path(base_directory).joinpath('orgRaw_scripts/templates_json/task-foodcue_108col_source_template.json')

    # set raw fMRI json file destination names
    json_fmri_dest_filename = Path(beh_source_bids_path).joinpath('fMRI_' + task_version + '_Raw-' + subname + '-1.json')

    # Copy json file for raw foodcue file (based on file verison) into sourcedata
    copy2(json_template_path, Path(json_fmri_dest_filename))

    ## NOTE: Foodcue runs were either presented through 1 eprime experiment (000_R01_V[A or B]_allProc), through run-specific files (e.g., Run5_V[A or B]_R01_R2proc), 
    ## or a combination of _allProc and run-specific experiments. Any experiment used should have an .edat, ExperimentAdvisorReport, and txt file. 
    ## In addition, subjects who used run-specific experiments should have a .emrg file that contains the output of all experiments merged together. 
    ## Thus, to copy eprime files, check for every potential filename for each eprime experiment run

    # If the "_allProc" experiment was used, copy corresponding eprime files
    if any("allProc" in exp_name for exp_name in exp_list):

        #copy edat2 file 
        eprime_filename = Path(fmri_raw_path).joinpath('000_R01_V' + task_version + '_allProc-' + subname.lstrip('0') + '-1.edat2') 
        if not eprime_filename.exists():
            #check with zeros in sub number
            eprime_filename = Path(fmri_raw_path).joinpath('000_R01_V' + task_version + '_allProc-' + subname + '-1.edat2')
            if not eprime_filename.exists():
                #check with edat3
                eprime_filename = Path(fmri_raw_path).joinpath('000_R01_V' + task_version + '_allProc-' + subname.lstrip('0') + '-1.edat3')
                if not eprime_filename.exists():
                    #check with zeros in sub number
                    eprime_filename = Path(fmri_raw_path).joinpath('000_R01_V' + task_version + '_allProc-' + subname.lstrip('0') + '-1.edat3')
                    if not eprime_filename.exists():
                        # write out if no edat file
                        eprime_err = 'sub-' + subname + ' has no fmri allProc edat file'
                        print(eprime_err)
                        #open error file and append error message
                        with open(Path(script_path).joinpath('foodcue_DataOrg_error.txt'), "a") as error_file:
                            error_file.write(eprime_err + "\n")
                    else:
                        copy2(eprime_filename, Path(beh_source_bids_path))
                else:
                    copy2(eprime_filename, Path(beh_source_bids_path))
            else:
                copy2(eprime_filename, Path(beh_source_bids_path))
        else:
            copy2(eprime_filename, Path(beh_source_bids_path))

        #copy ExperimentAdvisorReport
        eprimeXML_filename = Path(fmri_raw_path).joinpath('000_R01_V' + task_version + '_allProc-' + subname.lstrip('0') + '-1-ExperimentAdvisorReport.xml')
        if not eprimeXML_filename.exists():
            #check with zeros in sub number
            eprimeXML_filename = Path(fmri_raw_path).joinpath('000_R01_V' + task_version + '_allProc-' + subname + '-1-ExperimentAdvisorReport.xml')
            if not eprimeXML_filename.exists():
                # write out if no edat file
                eprime_err = 'sub-' + subname + ' has no fmri allProc xml file'
                print(eprime_err)
                #open error file and append error message
                with open(Path(script_path).joinpath('foodcue_DataOrg_error.txt'), "a") as error_file:
                    error_file.write(eprime_err + "\n")
            else:
                copy2(eprimeXML_filename, Path(beh_source_bids_path))
        else:
            copy2(eprimeXML_filename, Path(beh_source_bids_path))


        #copy eprime txt file
        eprimeTXT_filename = Path(fmri_raw_path).joinpath('000_R01_V' + task_version + '_allProc-' + subname.lstrip('0') + '-1.txt')
        if not eprimeTXT_filename.exists():
            #check with zeros in sub number
            eprimeTXT_filename = Path(fmri_raw_path).joinpath('000_R01_V' + task_version + '_allProc-' + subname + '-1.txt')
            if not eprimeTXT_filename.exists():
                # write out if no edat file
                eprime_err = 'sub-' + subname + ' has no fmri allProc txt file'
                print(eprime_err)
                #open error file and append error message
                with open(Path(script_path).joinpath('foodcue_DataOrg_error.txt'), "a") as error_file:
                    error_file.write(eprime_err + "\n")
            else:
                copy2(eprimeTXT_filename, Path(beh_source_bids_path))
        else:
            copy2(eprimeTXT_filename, Path(beh_source_bids_path))

    # If individual run experiment(s) were used, copy merged file and corresponding eprime files
    if any("Run" in exp_name for exp_name in exp_list):

        # copy merged file
        merge_filename = Path(fmri_raw_path).joinpath('000_R01_V' + task_version + '_allProc-' + subname.lstrip('0') + '-1_merge.emrg3') 
        if not merge_filename.exists():
            #check with zeros in sub number
            merge_filename = Path(fmri_raw_path).joinpath('000_R01_V' + task_version + '_allProc-' + subname + '-1_merge.emrg3') 
            if not merge_filename.exists():
                # write out if no edat file
                eprime_err = 'sub-' + subname + ' has single-run experiments but has no fmri merge file'
                print(eprime_err)
                #open error file and append error message
                with open(Path(script_path).joinpath('foodcue_DataOrg_error.txt'), "a") as error_file:
                    error_file.write(eprime_err + "\n")
            else:
                copy2(merge_filename, Path(beh_source_bids_path))
        else:
            copy2(merge_filename, Path(beh_source_bids_path))

        # copy eprime output for each single-run experiment
        single_proc_exps = [x for x in exp_list if x.startswith("Run")]
        for experiment in single_proc_exps:

            #copy edat2 file
            eprime_filename = Path(fmri_raw_path).joinpath(experiment + '-' + subname.lstrip('0') + '-1.edat2') 
            if not eprime_filename.exists():
                #check with zeros in sub number
                eprime_filename = Path(fmri_raw_path).joinpath(experiment + '-' + subname + '-1.edat2')
                if not eprime_filename.exists():
                    #check with edat3
                    eprime_filename = Path(fmri_raw_path).joinpath(experiment + '-' + subname.lstrip('0') + '-1.edat3')
                    if not eprime_filename.exists():
                        #check with zeros in sub number
                        eprime_filename = Path(fmri_raw_path).joinpath(experiment + '-' + subname + '-1.edat3')
                        if not eprime_filename.exists():
                            # write out if no edat file
                            eprime_err = 'sub-' + subname + ' has no fmri edat file for' + experiment
                            print(eprime_err)
                            #open error file and append error message
                            with open(Path(script_path).joinpath('foodcue_DataOrg_error.txt'), "a") as error_file:
                                error_file.write(eprime_err + "\n")
                        else:
                            copy2(eprime_filename, Path(beh_source_bids_path))
                    else:
                        copy2(eprime_filename, Path(beh_source_bids_path))               
                else:
                    copy2(eprime_filename, Path(beh_source_bids_path))
            else:
                copy2(eprime_filename, Path(beh_source_bids_path))

            # copy ExperimentAdvisorReport
            eprimeXML_filename = Path(fmri_raw_path).joinpath(experiment + "-" + subname.lstrip('0') + '-1-ExperimentAdvisorReport.xml')
            if not eprimeXML_filename.exists():
                #check with zeros in sub number
                eprimeXML_filename = Path(fmri_raw_path).joinpath(experiment + '-' + subname + + '-1-ExperimentAdvisorReport.xml')
                if not eprimeXML_filename.exists():
                    # write out if no edat file
                    eprime_err = 'sub-' + subname + ' has no fmri txt file'
                    print(eprime_err)
                    #open error file and append error message
                    with open(Path(script_path).joinpath('foodcue_DataOrg_error.txt'), "a") as error_file:
                        error_file.write(eprime_err + "\n")
                else:
                    copy2(eprimeXML_filename, Path(beh_source_bids_path))
            else:
                copy2(eprimeXML_filename, Path(beh_source_bids_path))

            # copy txt
            eprimeTXT_filename = Path(fmri_raw_path).joinpath(experiment + "-" + subname.lstrip('0') + '-1.txt')
            if not eprimeTXT_filename.exists():
                #check with zeros in sub number
                eprimeXML_filename = Path(fmri_raw_path).joinpath(experiment + '-' + subname + '-1.txt')
                if not eprimeTXT_filename.exists():
                    # write out if no edat file
                    eprime_err = 'sub-' + subname + ' has no fmri txt file'
                    print(eprime_err)
                    #open error file and append error message
                    with open(Path(script_path).joinpath('foodcue_DataOrg_error.txt'), "a") as error_file:
                        error_file.write(eprime_err + "\n")
                else:
                    copy2(eprimeTXT_filename, Path(beh_source_bids_path))
            else:
                copy2(eprimeTXT_filename, Path(beh_source_bids_path))


    # make BIDS raw directory structure if needed
    func_raw_bids_path = Path(bids_raw_path).joinpath('sub-' + subname + '/ses-1/func')
    Path(func_raw_bids_path).mkdir(parents=True, exist_ok=True) 

    # run function to rename columns
    bids_foodcue_data = bidsformat_foodcue_raw(filepath)

    # get number of runs in bids_foodcue_data
    runs = bids_foodcue_data['block'].unique()
    nruns = len(runs)

    # create a separate dataframe for each run
    for run in runs:

            #subset run data from bids_foodcue_data
            run_dat = bids_foodcue_data[bids_foodcue_data['block'] == run].copy()

            if len(run_dat) > 1:
                #set bids filename
                run_str = str(run)
                bids_filename = Path(func_raw_bids_path).joinpath('sub-' + subname + '_task-foodcue_run-0' + run_str + '_bold_events.tsv')

                if not bids_filename.exists():

                    #add required bids columns
                    run_dat = bidsformat_foodcue_func(run_dat)

                    # write to tsv file
                    run_dat.to_csv(bids_filename, sep="\t", encoding='utf-8-sig', index = False)

                else:
                    # write out participants already processed
                    print('sub-' + subname + '_task-foodcue_run-0' + run_str + '_bold_events.tsv')
