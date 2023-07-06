#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to process -desc-confounds_timeseries.tsv files (output from fmriprep) for resting state analyses. 
The following steps will occur:
    (1) determine which TRs need to be censored from each run
    (2) output a censor file that indicates which TRs to censor across all runs -- will be used by AFNI in first-level analyses
    (3) output a regressor file containing regressor information for all runs -- will be used by AFNI in first-level analyses
    (4) make new onsetfiles that exclude runs with >threshold % TRs censored -- will be used by AFNI in first-level analyses
    (5) output summary data that indicates % of TRs censored per run

Copyright (C) 2023 Bari Fuchs

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
parser.add_argument('--framewisedisplacement', '-fd', help='threshold for censoring TRs based on framewise displacement. default is .5', default=0.5, type=float)
parser.add_argument('--stdvars', '-sdv', help='threshold for censoring TRs based on std_dvars. default is 1.5', default=1.5, type=float)
args=parser.parse_args()

##############################################################################
####                                                                      ####
####                  Subfunctions called within script                   ####
####                                                                      ####
##############################################################################

def get_censor_info(Confound_Data, FD_thresh, std_dvars_thresh):
    """Function to determine what TRs (i.e., volumes) need to be censored in first-level analyses based on framewise displacement and std_dvars thresholds
    Inputs:
        Confound_Data (dataframe) - data from a -desc-confounds_timeseries.tsv file
        FD_thresh (integer) - framewise displacement threshold
        std_dvars_thresh (integer) - std_dvars threshold
    Outputs:
        censor_info (list) - length equal to number of TRs in input dataset; 
            0 = TR is to be censored, 1 = TR is to be included in analyses
        nvol (integer) - number of TRs/volumes in the dataset (Confound_Data)
        n_censored (integer) - number of TRs/volumes to be censored 
        p_censored (integer) - percentage of TRs/volumes to be censored
    """

    # get number of volumes
    nvol = len(Confound_Data)

    Confound_Data = Confound_Data.reset_index()  # make sure indexes pair with number of rows

    censor_info = []

    # censor if: 
    #   (1) std_dvars > std_dvars_thresh; 
    #   (2) framewise_displacement > FD_thresh
    #   (3) TR was detected by fmriprep as a steady state outlier

    for index, row in Confound_Data.iterrows():
        if (row['std_dvars'] > std_dvars_thresh) or (row['framewise_displacement'] > FD_thresh) or (row['non_steady_state_outlier00'] == 1):
            censor_info.append(0)
        else:
            censor_info.append(1)

    censor_info_df = pd.DataFrame(censor_info)

    # count number of censored TRs
    n_censored = (censor_info_df[0] == 0).sum()

    # get percent of censored TRs
    p_censored = (n_censored/nvol)*100

    return(censor_info, nvol, n_censored, p_censored)


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

        #confound_files = list(Path(bids_fmriprep_path).rglob('sub-' + str(sub) + '/ses-1/func/*rest*confounds_timeseries.tsv'))
        confound_file = Path(bids_fmriprep_path).joinpath('sub-' + str(sub) + '/ses-1/func/sub-' + str(sub) +'_ses-1_task-rest_desc-confounds_timeseries.tsv')


        # check if file exists
        if confound_file.is_file():
            print('File found for sub-' + str(sub))
        else:
            print('No files found for sub-' + str(sub))
            subject_list.remove(sub)
        
    #check if any files to process
    if subject_list is None:
        sys.exit('No files found for participants' + args.parIDs)   

# if there are no parID arguments entered
else:
    #find all rest*events.tsv files
    confound_files = list(Path(bids_fmriprep_path).rglob('sub-*/ses-1/func/*rest*confounds_timeseries.tsv'))

    # get unique ids from confound_files
    ##pathlib library -- .relative_to give all the path that follows raw_data_path
    ##                  .parts[0] extracts the first directory in remaining path to get
    ##                       list of subjects
    fmriprep_subs = [item.relative_to(bids_fmriprep_path).parts[0] for item in confound_files]

    ##set is finding only unique values
    subject_list = list(set([item[4:7] for item in fmriprep_subs]))   

# set framewise displacement and std_dvar threshold variables
FD_threshold = args.framewisedisplacement
std_dvars_threshold = args.stdvars

# Import or create a database to write censor summary data to
censor_summary_path = Path(bids_fmriprep_path).joinpath('task-rest_censorsummary_fd-' + str(FD_threshold) + '_stddvar-' + str(std_dvars_threshold) + '.tsv')
# if database exists
if censor_summary_path.is_file():
    # import database
    censor_summary_allPar = pd.read_csv(str(Path(bids_fmriprep_path).joinpath('task-rest_censorsummary_fd-' + str(FD_threshold) + '_stddvar-' + str(std_dvars_threshold) + '.tsv')), sep = '\t')
# if database does not exist
else:
    # create new dataframe 
    censor_summary_allPar = pd.DataFrame(np.zeros((0, 5)))
    censor_summary_allPar.columns = ['sub','run', 'n_vol', 'n_censor', 'p_censor']

## Loop through subject_list and create onset files ##
subs = list(subject_list)
for sub in subs:

    # get resting state confound file 
    confound_file = Path(bids_fmriprep_path).joinpath('sub-' + str(sub) + '/ses-1/func/sub-' + str(sub) +'_ses-1_task-rest_desc-confounds_timeseries.tsv')

    # create censor data summary per participant
    censor_sum_Pardat = pd.DataFrame(np.zeros((0, 5)))
    censor_sum_Pardat.columns = ['sub','run', 'n_vol', 'n_censor', 'p_censor']

    # create overall regressor dataframe participant
    #regress_lev1=['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z', 'trans_x_derivative1', 'trans_y_derivative1', 'trans_z_derivative1', 'rot_x_derivative1', 'rot_y_derivative1', 'rot_z_derivative1']
    regress_lev1=['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z', 'csf', 'white_matter', 'global_signal', 'trans_x_derivative1', 'trans_y_derivative1', 'trans_z_derivative1', 'rot_x_derivative1', 'rot_y_derivative1', 'rot_z_derivative1']
    regress_Pardat = pd.DataFrame(np.zeros((0, len(regress_lev1))))
    regress_Pardat.columns = regress_lev1

    # create empty list for censor data
    censordata_allruns = []

    # extract censor information from confoundfile

    #load data
    confound_dat_all = pd.read_csv(str(confound_file), sep = '\t', encoding = 'utf-8-sig', engine='python')

    # select variables for processing data
    confound_dat = confound_dat_all[['framewise_displacement', 'std_dvars', 'dvars' ,'trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z',
                                    'trans_x_derivative1', 'trans_y_derivative1', 'trans_z_derivative1', 'rot_x_derivative1', 
                                    'rot_y_derivative1', 'rot_z_derivative1', 'csf', 'white_matter', 'global_signal']].copy()

    # add non-steady-state outlier column (only exists in confound.tsv files with non-steady-state outliers)
    if 'non_steady_state_outlier00' in confound_dat_all:
        confound_dat['non_steady_state_outlier00'] = confound_dat_all['non_steady_state_outlier00']
    else: 
        confound_dat['non_steady_state_outlier00'] = 0

    # run function to get censor information
    res = get_censor_info(confound_dat, FD_thresh = FD_threshold, std_dvars_thresh = std_dvars_threshold)

    #export participant censor file
    censordata = res[0]
    censor_data_df = pd.DataFrame(censordata)
    censor_data_df.columns = ['header']
    #censor_data_df.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'sub-' + sub + '_rest_censor_fd-' + str(FD_threshold) + '_stddvar-' + str(std_dvars_threshold) + '.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

    # add regressor data to overall regressor file
    regress_run = confound_dat[regress_lev1].copy()
    regress_Pardat = regress_Pardat.append(regress_run)

    # for first row [0] of motion derivative variables in regress_Pardat, replace NA with 0. This will allow deriv variables to be entered into AFNI's 3ddeconvolve
    deriv_vars = ['trans_x_derivative1', 'trans_y_derivative1', 'trans_z_derivative1', 'rot_x_derivative1', 'rot_y_derivative1', 'rot_z_derivative1']
    regress_Pardat.loc[0, deriv_vars] = regress_Pardat.loc[0, deriv_vars].fillna(value=0)

    # add run summary information to participant summary dataframe 
    # res[1] = number of TRs; res[2] = number of TRs censored, res[3] = % of TRs censored
    df_len = len(censor_sum_Pardat)
    runsum = [sub, 'rest', res[1], res[2], res[3]]
    censor_sum_Pardat.loc[df_len] = runsum

    # Export participant regressor file with and without columns names
    #regress_Pardat.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'sub-' + sub + '_rest_confounds-noheader.tsv')), sep = '\t', encoding='utf-8-sig', index = False, header=False)
    #regress_Pardat.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'sub-' + sub + '_rest_confounds-header.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

    ## Add participant summary dataframe to overall summary database ##

    # if subject data already in censor_summary_allPar, remove existing rows
    if sub in censor_summary_allPar['sub']:
        censor_summary_allPar = censor_summary_allPar[censor_summary_allPar.sub != sub]
    
    # Add participant summary dataframe to overall summary database
    censor_summary_allPar = censor_summary_allPar.append(censor_sum_Pardat)

#write summary database
#print(censor_summary_allPar)
censor_summary_allPar.to_csv(str(Path(bids_fmriprep_path).joinpath('task-rest_censorsummary_fd-' + str(FD_threshold) + '_stddvar-' + str(std_dvars_threshold) + '.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
