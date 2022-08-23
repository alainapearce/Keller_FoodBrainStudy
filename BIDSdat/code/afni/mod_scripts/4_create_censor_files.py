#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to process -desc-confounds_timeseries.tsv files (output from fmriprep) in preparation for first-level analyses in AFNI. 
The following steps will occur:
    (1) determine which TRs need to be censored from each run
    (2) output a censor file that indicates which TRs to censor across all runs -- will be used by AFNI in first-level analyses
    (3) output a regressor file containing regressor information for all runs -- will be used by AFNI in first-level analyses
    (4) output summary data that indicates % of TRs censored per run (total and for blocks of interest)

Written by Bari Fuchs in Spring 2022

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
import numpy as np
import pandas as pd
import os
import sys, argparse
#from scipy.stats import norm
from scipy.stats.morestats import shapiro
from pathlib import Path
import re

from sqlalchemy import false

##############################################################################
####                                                                      ####
####                        Set up script function                        ####
####                                                                      ####
##############################################################################

# to enter multiple subject arguments in terminal format like:
#-p 2 3

# to overwrite onsets of all input IDs, specify in terminal format like:
#-f

#input arguments setup
parser=argparse.ArgumentParser()
parser.add_argument('--parIDs', '-p', help='participant list', type=float, nargs="+")

# input arguments related to censoring TRs
parser.add_argument('--framewisedisplacement', '-fd', help='threshold for censoring TRs based on framewise displacement. default is 1.0', default=1.0, type=float)
parser.add_argument('--stdvars', '-sdv', help='threshold for censoring TRs based on std_dvars', type=float)
parser.add_argument('--cen_prev_tr', '-cpt', help='if argument is present, censor TRs based on FD in the subsequent TR', action='store_true', default=False, required=False)

args=parser.parse_args()

##############################################################################
####                                                                      ####
####                  Subfunctions called within script                   ####
####                                                                      ####
##############################################################################

def get_censor_info(Confound_Data, FD_thresh, std_dvars_thresh, r_int_info, cen_prev_TR):
    """Function to determine what TRs (i.e., volumes) need to be censored in first-level analyses based on framewise displacement and std_dvars thresholds
    Inputs:
        Confound_Data (dataframe) - data from a -desc-confounds_timeseries.tsv file
        FD_thresh (float) - framewise displacement threshold
        std_dvars_thresh ('none' or float) - std_dvars threshold
        r_int_info (list) - length equal to number of TRs in Confound_Data; 
            0 = TR is of non-interest, 1 = TR of interest
        cen_prev_TR (True or False) -- boolean input to indicate whether to censor a TR based on the subquent TR's FD
    Outputs:
        censor_info (list) - length equal to number of TRs in input dataset; 
            0 = TR is to be censored, 1 = TR is to be included in analyses
        nvol (integer) - number of TRs/volumes in the dataset (Confound_Data)
        n_censored (integer) - number of TRs/volumes to be censored 
        p_censored (integer) - percentage of TRs/volumes to be censored
        nvol_int (integer) - number of TRs/volumes of interest in the dataset
        n_censored_int (integer) - number of TRs/volumes of interest to be censored 
        p_censored_int (integer) - percentage of TRs/volumes of interest to be censored
    """

    Confound_Data = Confound_Data.reset_index()  # make sure indexes pair with number of rows

    # censor TR if: 
    #   (1) First or second TR (datapoints 0 and 1)
    #   (2) framewise_displacement > FD_thresh
    #   (3) TR was detected by fmriprep as a steady state outlier
    #   (4) std_dvars > std_dvars_thresh, if a threshold is specified
    #   (5) framewise_displacement on the next TR > FD_thresh, if cen_prev_TR = True
    
    censor_info = []
    for index, row in Confound_Data.iterrows():
        # if first or second TR
        if (index < 2):
            censor_info.append(0)
        # if fd > threshold
        elif (row['framewise_displacement'] > FD_thresh):
            censor_info.append(0) # censor current TR
            if cen_prev_TR is True:
                censor_info[index-1] = 0 # censor previous TR
        # if steady state outlier
        elif (row['non_steady_state_outlier00'] == 1):
            censor_info.append(0)
        # if std_dvars thresold a float (i.e., is specified)
        elif isinstance(std_dvars_threshold, float):
            # if std_dvars is above thresold
            if (row['std_dvars'] > std_dvars_thresh):
                censor_info.append(0)
        else:
            censor_info.append(1)

    censor_info_df = pd.DataFrame(censor_info)

    ## Get censor information for all TRs (excluding dummy scans!) ###

    # remove first 2 rows (dummy volumes) from censor_info_df
    censor_info_df = censor_info_df.iloc[2: , :]

    # count number of volumes (excluding dummy scans)
    nvol = len(censor_info_df)

    # count number of censored TRs
    n_censored = (censor_info_df[0] == 0).sum()

    # get percent of censored TRs, rounded to 2 decimals
    p_censored = round((n_censored/nvol)*100,1)

    ### Get censor information for TRs of interest ###

    # get indices of r_int_info that are non-zero (i.e., TRs of interest)
    interest_ind = np.nonzero(r_int_info)[0]

    # filter censor_info to only include indeces of interest
    censor_info_int = [censor_info[i] for i in interest_ind]
    
    censor_info_int_df = pd.DataFrame(censor_info_int)

    # get number of volumes of interest
    nvol_int = len(censor_info_int)

    # count number of censored TRs of intrest
    n_censored_int = (censor_info_int_df[0] == 0).sum()

    # get percent of censored TRs of interest, rounded to 2 decimals
    p_censored_int = round((n_censored_int/nvol_int)*100,2)

    return(censor_info, nvol, n_censored, p_censored, nvol_int, n_censored_int, p_censored_int)

##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################

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

##check for input arguments and get initial list of subject IDs ##

# if there is 1 or more parID argument
if args.parIDs is not None and len(args.parIDs) >= 1:

    #make sure have integers
    subject_ids = list(map(int, args.parIDs))

    #get leading zeros
    subject_list = [str(item).zfill(3) for item in subject_ids]
        
    #check for raw data
    subs = list(subject_list)

    for sub in subs:

        confound_files = list(Path(bids_fmriprep_path).rglob('sub-' + str(sub) + '/ses-1/func/*confounds_timeseries.tsv'))
        orig_onsetfiles = list(Path(bids_origonset_path).rglob('sub-' + str(sub) + '*AFNIonsets.txt'))

        if len(confound_files) < 1:
            print('No confound files found for sub-' + str(sub))
            subject_list.remove(sub)

        if len(orig_onsetfiles) < 1:
            print('No onset files found for sub-' + str(sub))
            subject_list.remove(sub)
        
    #check if any files to process
    if subject_list is None:
        sys.exit('No Files found for participants' + args.parIDs)   

# if there are no parID arguments entered
else:
    #find all foodcue*events.tsv files
    confound_files = list(Path(bids_fmriprep_path).rglob('sub-*/ses-1/func/*confounds_timeseries.tsv'))

    # get unique ids from confound_files
    ##pathlib library -- .relative_to give all the path that follows raw_data_path
    ##                  .parts[0] extracts the first directory in remaining path to get
    ##                       list of subjects
    fmriprep_subs = [item.relative_to(bids_fmriprep_path).parts[0] for item in confound_files]

    ##set is finding only unique values
    subject_list = list(set([item[4:7] for item in fmriprep_subs]))

    for sub in subject_list:        
        orig_onsetfiles = list(Path(bids_origonset_path).rglob('sub-' + str(sub) + '*AFNIonsets.txt'))
        if len(orig_onsetfiles) < 1:
            print('Confound files but no onset files found for sub-' + str(sub))
            subject_list.remove(sub)

# set framewise displacement and std_dvar threshold variables
FD_threshold = args.framewisedisplacement
if args.stdvars is None:
    std_dvars_threshold = 'none'
else:
    std_dvars_threshold = args.stdvars

# set cen_prev_tr flag 
cen_prev_tr_flag = args.cen_prev_tr

# Import or create a database to write censor summary data to
censor_summary_path = Path(bids_fmriprep_path).joinpath('task-foodcue_censorsummary_fd-' + str(FD_threshold) + '_stddvar-' + str(std_dvars_threshold) + '.tsv')
# if database exists
if censor_summary_path.is_file():
    # import database
    censor_summary_allPar = pd.read_csv(str(Path(bids_fmriprep_path).joinpath('task-foodcue_censorsummary_fd-' + str(FD_threshold) + '_stddvar-' + str(std_dvars_threshold) + '.tsv')), sep = '\t')
# if database does not exist
else:
    # create new dataframe 
    censor_summary_allPar = pd.DataFrame(np.zeros((0, 8)))
    censor_summary_allPar.columns = ['sub','run', 'n_vol', 'n_censor', 'p_censor', 'n_vol_interest', 'n_censor_interest', 'p_censor_interest']

# create block censor summary dataframe
blockcensor_sum = pd.DataFrame(np.zeros((0, 8)))
blockcensor_sum.columns = ['sub','run', 'HighLarge', 'HighSmall', 'LowLarge', 'LowSmall', 'OfficeLarge','OfficeSmall']

## Loop through subject_list and create onset files ##
subs = list(subject_list)
for sub in subs:

    # get confound files -- Note: each events file corresponds to 1 foodcue run
    confoundfiles = list(Path(bids_fmriprep_path).rglob('sub-' + str(sub) + '/ses-1/func/*foodcue*confounds_timeseries.tsv'))

    # get number of runs -- Note: each confound file corresponds to 1 foodcue run
    nruns = len(confoundfiles)

    # create run censor data summary per participant
    censor_sum_Pardat = pd.DataFrame(np.zeros((0, 8)))
    censor_sum_Pardat.columns = ['sub','run', 'n_vol', 'n_censor', 'p_censor','n_vol_interest', 'n_censor_interest', 'p_censor_interest']

    # create overall regressor dataframe participant
    regress_lev1=['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z', 'csf', 'white_matter', 'global_signal', 'trans_x_derivative1', 'trans_y_derivative1', 'trans_z_derivative1', 'rot_x_derivative1', 'rot_y_derivative1', 'rot_z_derivative1']
    regress_Pardat = pd.DataFrame(np.zeros((0, len(regress_lev1))))
    regress_Pardat.columns = regress_lev1

    # create empty list for censor data
    censordata_allruns = []

    # extract censor information for each run (each confoundfile)
    confoundfiles.sort()
    for file in confoundfiles: #loop through runs (each run has its own confoundfile)

        #load data
        confound_dat_all = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python')

        # get run number
        runnum = int(str(file).rsplit('/',1)[-1][31:32])

        # select variables for processing data
        confound_dat = confound_dat_all[['framewise_displacement', 'std_dvars', 'dvars' ,'trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z',
                                        'trans_x_derivative1', 'trans_y_derivative1', 'trans_z_derivative1', 'rot_x_derivative1', 
                                        'rot_y_derivative1', 'rot_z_derivative1', 'csf', 'white_matter', 'global_signal']].copy()

        # add non-steady-state outlier column (only exists in confound.tsv files with non-steady-state outliers)
        if 'non_steady_state_outlier00' in confound_dat_all:
            confound_dat['non_steady_state_outlier00'] = confound_dat_all['non_steady_state_outlier00']
        else: 
            confound_dat['non_steady_state_outlier00'] = 0
        
        ### Identify TRs in food blocks ###
        # get onset files (note: there is 1 onset file per condition)
        orig_onsetfiles = list(Path(bids_origonset_path).rglob('sub-' + str(sub) + '*AFNIonsets.txt'))

        # make empty list for block onsets
        block_onsets_TR = []

        # make dictionary for block onsets
        block_onsets_TR_dict = {}

        # loop through onset files to get block onset times
        for onsetfile in orig_onsetfiles:
            # get file name
            filename = onsetfile.stem
            # get condition 
            cond = re.split('_|-',filename)[2]

            ## Uncomment this and indent loop if want to only consider food blocks and not office supply blocks
            # if condition contains High or Low string 
            #if ('High' in cond) or ('Low' in cond):

            #load file
            onsetfile_dat = pd.read_csv(str(onsetfile), sep = '\t', encoding = 'utf-8-sig', engine='python', header=None)

            # get block onset time for the given run (indexed by row) -- onset times are in seconds
            onset_time = (onsetfile_dat.iloc[runnum-1, 0])

            # convert onset time to TR
            TR = 2
            onset_TR = int(onset_time / TR)

            # append block onset TR to list
            block_onsets_TR.append(onset_TR)

            # add condition and onset to dictionary
            block_onsets_TR_dict[cond] = onset_TR

        # Make a list of 1s and 0s equal to the length of a run -- 0 = TR is of non-interest, 1 = TR of interest
        r_int_list = [0] * len(confound_dat) # Make a list of 0s equal to the length of confound_dat
        for onset in block_onsets_TR: #loop through onsets
            offset = onset + 9  #Get block offset -- note: this will be the first TR after the block of interest
            r_int_list[onset:offset] = [1, 1, 1, 1, 1, 1, 1, 1, 1]  #At indices onset to offset-1 in r_int_list, set value to 1

        # run function to get censor information by run
        res = get_censor_info(confound_dat, FD_thresh = FD_threshold, std_dvars_thresh = std_dvars_threshold, r_int_info = r_int_list, cen_prev_TR=cen_prev_tr_flag)

        #export run-specific censor file
        run_censordata = res[0]
        run_censor_data_df = pd.DataFrame(run_censordata)
        #run_censor_data_df.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'sub-' + sub + '_foodcue-r' + str(runnum) + '_censor_fd-' + str(FD_threshold) + '_stddvar-' + str(std_dvars_threshold) + '.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

        # add run-specific censor data to overall censor file
        censordata_allruns.extend(run_censordata)
        
        # add run-specific regressor data to overall regressor file
        regress_run = confound_dat[regress_lev1].copy()
        regress_Pardat = regress_Pardat.append(regress_run)

        ##########################
        # get motion BY CONDITION
        ##########################

        # make dictionary for TR count
        block_TRcount_dict = {}

        for condition in block_onsets_TR_dict: #loop through condition keys

            # get condition onset and offset
            onset = block_onsets_TR_dict[condition]
            offset = onset + 9

            # extract censor info for TRs associated with the condition
            cond_censor = run_censordata[onset:offset]

            # count the number of uncensored TRs in the condition
            cond_uncensor_count = sum(cond_censor)

            # add to dictionary
            block_TRcount_dict[condition] = cond_uncensor_count

            # make dataframe
            df = pd.DataFrame([block_TRcount_dict], columns=block_TRcount_dict.keys())

        # Add motion by contion to summary dataframe - this will append 1 row per run, with 1 column per conditon
        to_append = pd.DataFrame([[sub, runnum, block_TRcount_dict['HighLarge'], block_TRcount_dict['HighSmall'], block_TRcount_dict['LowLarge'], block_TRcount_dict['LowSmall'], block_TRcount_dict['OfficeLarge'], block_TRcount_dict['OfficeSmall']]], columns=['sub','run', 'HighLarge', 'HighSmall', 'LowLarge', 'LowSmall', 'OfficeLarge','OfficeSmall'])
        blockcensor_sum = blockcensor_sum.append(to_append)

        # for first row [0] of motion derivative variables in regress_Pardat, replace NA with 0. This will allow deriv variables to be entered into AFNI's 3ddeconvolve
        deriv_vars = ['trans_x_derivative1', 'trans_y_derivative1', 'trans_z_derivative1', 'rot_x_derivative1', 'rot_y_derivative1', 'rot_z_derivative1']
        regress_Pardat.loc[0, deriv_vars] = regress_Pardat.loc[0, deriv_vars].fillna(value=0)

        # add run-specific summary information to participant summary dataframe 
        # res[1] = number of TRs total; res[2] = number of TRs censored total, res[3] = % of TRs censored total
        # res[4] = number of TRs of interest; res[5] = number of TRs of interest censored , res[6] = % of TRs of interest censored
        df_len = len(censor_sum_Pardat)
        runsum = [sub, runnum, res[1], res[2], res[3], res[4], res[5], res[6]]
        censor_sum_Pardat.loc[df_len] = runsum

    # Export participant censor file (note: afni expects TSV files to have headers -- so export with header=True)
    censordata_allruns_df = pd.DataFrame(censordata_allruns)
    censordata_allruns_df.columns = ['header']

    if cen_prev_tr_flag is True:
        if std_dvars_threshold == 'none':
            censordata_allruns_df.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'sub-' + sub + '_foodcue-allruns_censor_fd-' + str(FD_threshold) + '_cpt.tsv')), sep = '\t', encoding='utf-8-sig', index = False, header=True)
        else:
            censordata_allruns_df.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'sub-' + sub + '_foodcue-allruns_censor_fd-' + str(FD_threshold) + '_stddvar-' + str(std_dvars_threshold) + '_cpt.tsv')), sep = '\t', encoding='utf-8-sig', index = False, header=True)
    else: #cen_prev_tr_flag is False
        if std_dvars_threshold == 'none':
            censordata_allruns_df.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'sub-' + sub + '_foodcue-allruns_censor_fd-' + str(FD_threshold) + '.tsv')), sep = '\t', encoding='utf-8-sig', index = False, header=True)
        else:
            censordata_allruns_df.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'sub-' + sub + '_foodcue-allruns_censor_fd-' + str(FD_threshold) + '_stddvar-' + str(std_dvars_threshold) + '.tsv')), sep = '\t', encoding='utf-8-sig', index = False, header=True)
   
    # Export participant regressor file with and without columns names
    regress_Pardat.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'sub-' + sub + '_foodcue-allruns_confounds-noheader.tsv')), sep = '\t', encoding='utf-8-sig', index = False, header=False)
    regress_Pardat.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'sub-' + sub + '_foodcue-allruns_confounds-header.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

    ## Add participant summary dataframe to overall summary database ##

    # if subject data already in censor_summary_allPar, remove existing rows
    if sub in censor_summary_allPar['sub']:
        censor_summary_allPar = censor_summary_allPar[censor_summary_allPar.sub != sub]
    
    # Add participant summary dataframe to overall summary database
    censor_summary_allPar = censor_summary_allPar.append(censor_sum_Pardat)


#######################################
#### Write censor summary database ####
#######################################

if cen_prev_tr_flag is True:
    if std_dvars_threshold == 'none':
        censor_summary_allPar.to_csv(str(Path(bids_fmriprep_path).joinpath('task-foodcue_censorsummary_fd-' + str(FD_threshold) + '_cpt.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
        blockcensor_sum.to_csv(str(Path(bids_fmriprep_path).joinpath('task-foodcue_bycond-censorsummary_fd-' + str(FD_threshold) + '_cpt.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
    else:
        censor_summary_allPar.to_csv(str(Path(bids_fmriprep_path).joinpath('task-foodcue_censorsummary_fd-' + str(FD_threshold) + '_stddvar-' + str(std_dvars_threshold) + '_cpt.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
        blockcensor_sum.to_csv(str(Path(bids_fmriprep_path).joinpath('task-foodcue_bycond-censorsummary_fd-' + str(FD_threshold) + '_stddvar-' + str(std_dvars_threshold) + '_cpt.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
else: #cen_prev_tr_flag is False
    if std_dvars_threshold == 'none':
        censor_summary_allPar.to_csv(str(Path(bids_fmriprep_path).joinpath('task-foodcue_censorsummary_fd-' + str(FD_threshold) + '.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
        blockcensor_sum.to_csv(str(Path(bids_fmriprep_path).joinpath('task-foodcue_bycond-censorsummary_fd-' + str(FD_threshold) + '.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
    else:
        censor_summary_allPar.to_csv(str(Path(bids_fmriprep_path).joinpath('task-foodcue_censorsummary_fd-' + str(FD_threshold) + '_stddvar-' + str(std_dvars_threshold) + '.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
        blockcensor_sum.to_csv(str(Path(bids_fmriprep_path).joinpath('task-foodcue_bycond-censorsummary_fd-' + str(FD_threshold) + '_stddvar-' + str(std_dvars_threshold) + '.tsv')), sep = '\t', encoding='utf-8-sig', index = False)