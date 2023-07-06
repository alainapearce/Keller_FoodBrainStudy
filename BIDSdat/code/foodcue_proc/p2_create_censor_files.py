#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

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
import numpy as np
import pandas as pd
import os
from pathlib import Path
import re

#########################################################
####                                                 ####
####                  Subfunctions                   ####
####                                                 ####
#########################################################

def _get_summary_files(bids_fmriprep_path, censor_str, sub, overwrite):
    """Function to import or generate task-foodcue_censorsummary_* and task-foodcue_byblock-censorsummary_* files. 
        Files will be imported if censorsummary file with specified CensorStr exists, otherwise they will be generated. 
        If subject is already in censorsummary database and Overwrite = False, exception will be raised. 
        If subject is already in censorsummary database and Overwrite != False, subject will be removed from summary database.

    Inputs:
        fMRIpreppath (list) - path to import file from
        censor_str (str) - string that defines TR censor criteria 
        sub (str) - subject ID
        overwrite (bool) - True or False for overwriting subject data in censor summary files
        
    Outputs:
        RegressPardat (pandas dataframe) - will contain 1 column per regressor variable and (number confound files * length of 1 confound file) rows
    """

    ########################################
    ### Manage byrun-censorsummary file ###
    ########################################

    # Set paths to summary file
    censor_summary_byrun_path = Path(bids_fmriprep_path).joinpath('task-foodcue_byrun-censorsummary_' + str(censor_str) + '.tsv')

    ### Manage censor_summary_path ###
    if censor_summary_byrun_path.is_file(): # if database exists

        # import database --- converting 'sub' to string will maintain leading zeros
        CenSum_allPar = pd.read_csv(str(censor_summary_byrun_path), sep = '\t', converters={'sub': lambda x: str(x)})

        # check to see if subject already in database
        if (sub in set(CenSum_allPar['sub'])):
            if overwrite is False:
                print("sub_" + sub + " already in foodcue_byrun-censorsummary file. Use overwrite = True to rerun")
                raise Exception()
            else: #overwrite is true
                # remove subject rows from censor_summary_byrun_path
                CenSum_allPar = CenSum_allPar[CenSum_allPar['sub'] != sub]

    # if database does not exist
    else:
        # create new dataframe 
        CenSum_allPar = pd.DataFrame(np.zeros((0, 8)))
        CenSum_allPar.columns = ['sub','run', 'n_vol', 'n_censor', 'p_censor', 'n_vol_interest', 'n_censor_interest', 'p_censor_interest']

    ########################################
    ### Manage byblock-censorsummary file ###
    ########################################

    # Set paths to summary file
    censor_summary_byblock_path = Path(bids_fmriprep_path).joinpath('task-foodcue_byblock-censorsummary_' + str(censor_str) + '.tsv')

    if censor_summary_byblock_path.is_file(): # if database exists

        # import database --- converting 'sub' to string will maintain leading zeros
        CenSum_byBlock_allPar = pd.read_csv(str(censor_summary_byblock_path), sep = '\t', converters={'sub': lambda x: str(x)})

        # check to see if subject already in database
        if (sub in set(CenSum_byBlock_allPar['sub'])):
            if overwrite is False:
                print("sub_" + sub + " already in foodcue_byblock-censorsummary file. Use overwrite = True to rerun")
                raise Exception()
            else: #overwrite is true
                # remove subject rows from censor_summary_path
                CenSum_byBlock_allPar = CenSum_byBlock_allPar[CenSum_byBlock_allPar['sub'] != sub]

    # if database does not exist
    else:
        # create new dataframe 
        CenSum_byBlock_allPar = pd.DataFrame(np.zeros((0, 8)))
        CenSum_byBlock_allPar.columns = ['sub','run', 'HighLarge', 'HighSmall', 'LowLarge', 'LowSmall', 'OfficeLarge','OfficeSmall']

    return(CenSum_allPar, CenSum_byBlock_allPar)

def _get_censorstr(framewise_displacement, std_vars, cen_prev_tr):
    """Function to generate string to identify censor criteria 

    Inputs:
        framewise_displacement (float)
        std_vars (float or False)
        cen_prev_tr (bool)

    Outputs:
        censor_str (str)

    """
    if std_vars is False:
        if cen_prev_tr is False: 
            censor_str = 'fd-' + str(framewise_displacement)
        else:
            censor_str = 'fd-' + str(framewise_displacement) + '_cpt'
    else:
        if cen_prev_tr is False:
            censor_str = 'fd-' + str(framewise_displacement) + '_stddvar-' + str(std_vars)
        else:
            censor_str = 'fd-' + str(framewise_displacement) + '_stddvar-' + str(std_vars) + '_cpt'
    return(censor_str)

def _gen_concatenated_regressor_file(confound_files):
    """Function to generate 1 regressor file 
    Inputs:
        confound_files (list) - list of counfound files from fmriprep. 1 confound file per run
        
    Outputs:
        RegressPardat (pandas dataframe) - will contain 1 column per regressor variable and (number confound files * length of 1 confound file) rows
    """
    # Make list of variables to regress in Level 1 analyses
    RegressLev1=['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z', 'csf', 'white_matter', 'global_signal', 'trans_x_derivative1', 'trans_y_derivative1', 'trans_z_derivative1', 'rot_x_derivative1', 'rot_y_derivative1', 'rot_z_derivative1']
    
    # create overall regressor dataframe for participant
    RegressPardat = pd.DataFrame(np.zeros((0, len(RegressLev1))))
    RegressPardat.columns = RegressLev1

    confound_files.sort()
    for file in confound_files: #loop through runs (each run has its own confoundfile)

        #load data
        confound_dat_all = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python')

        # add counfound file (i.e., run-specific) regressor data to overall regressor file
        RegressRun = confound_dat_all[RegressLev1].copy()
        RegressPardat = pd.concat([RegressPardat, RegressRun ])

    # for first row [0] of motion derivative variables in regress_Pardat, replace NA with 0. This will allow deriv variables to be entered into AFNI's 3ddeconvolve
    deriv_vars = ['trans_x_derivative1', 'trans_y_derivative1', 'trans_z_derivative1', 'rot_x_derivative1', 'rot_y_derivative1', 'rot_z_derivative1']
    RegressPardat.loc[0, deriv_vars] = RegressPardat.loc[0, deriv_vars].fillna(value=0)

    return(RegressPardat)

def _gen_run_int_list(orig_onsetfiles, confound_dat, runnum):
    """Function to generate r_int_list and block_onsets_TR_dict based on original onset files
    Inputs:
        orig_onsetfiles (list) - list of PosixPaths to onset files
        confound_dat (dataframe) - dataframe for a run with 1 row per TR
        runnum (int) - run number 
        
    Outputs:
        r_int_list (list) - a list of 1s and 0s equal to the length of a run -- 0 = TR is of non-interest, 1 = TR of interest
        block_onsets_TR_dict (dictionary)
    """

    ### Identify TRs in food blocks ###
    # get onset files (note: there is 1 onset file per condition)

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

    return(r_int_list, block_onsets_TR_dict)

def _get_run_censor_info(confound_dat, FD_thresh, std_dvars_thresh, r_int_info, cen_prev_TR_flag):
    """Function to determine what TRs (i.e., volumes) need to be censored in first-level analyses based on framewise displacement and std_dvars thresholds
    Inputs:
        confound_dat (dataframe) - data from a -desc-confounds_timeseries.tsv file
        FD_thresh (float) - framewise displacement threshold
        std_dvars_thresh ('False' or float) - std_dvars threshold
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

    confound_dat = confound_dat.reset_index()  # make sure indexes pair with number of rows

    # censor TR if: 
    #   (1) First or second TR (datapoints 0 and 1)
    #   (2) framewise_displacement > FD_thresh
    #   (3) TR was detected by fmriprep as a steady state outlier
    #   (4) std_dvars > std_dvars_thresh, if a threshold is specified
    #   (5) framewise_displacement on the next TR > FD_thresh, if cen_prev_TR = True
    
    censor_info = []
    for index, row in confound_dat.iterrows():
        # if first or second TR
        if (index < 2):
            censor_info.append(0)
        # if fd > threshold
        elif (row['framewise_displacement'] > FD_thresh):
            censor_info.append(0) # censor current TR
            if cen_prev_TR_flag is True:
                censor_info[index-1] = 0 # censor previous TR
        # if steady state outlier
        elif (row['non_steady_state_outlier00'] == 1):
            censor_info.append(0)
        # if std_dvars thresold a float (i.e., is specified)
        elif isinstance(std_dvars_thresh, float):
            # if std_dvars is above thresold
            if (row['std_dvars'] > std_dvars_thresh):
                censor_info.append(0)
            else:
                censor_info.append(1)
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

    # get percent of censored TRs, rounded to 1 decimals
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

    # get percent of censored TRs of interest, rounded to 1 decimals
    p_censored_int = round((n_censored_int/nvol_int)*100,1)

    return(censor_info, nvol, n_censored, p_censored, nvol_int, n_censored_int, p_censored_int)

def _get_censorsum_byblock(block_onsets_TR_dict, run_censordata, sub, runnum):

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

    # Generate a dataframe row that indicates how many TRs are good per condition (block) in a run
    byblock_run_row = pd.DataFrame([[sub, runnum, block_TRcount_dict['HighLarge'], block_TRcount_dict['HighSmall'], block_TRcount_dict['LowLarge'], block_TRcount_dict['LowSmall'], block_TRcount_dict['OfficeLarge'], block_TRcount_dict['OfficeSmall']]], columns=['sub','run', 'HighLarge', 'HighSmall', 'LowLarge', 'LowSmall', 'OfficeLarge','OfficeSmall'])

    return(byblock_run_row)
    

##############################################################################
####                                                                      ####
####                             Main Function                            ####
####                                                                      ####
##############################################################################

def create_censor_files(par_id, framewise_displacement, std_vars=False, cen_prev_tr=False, overwrite = False, preproc_path = False):
    """
    This function will process -desc-confounds_timeseries.tsv files (output from fmriprep) for 1 participant in preparation for first-level analyses in AFNI. 
    The following steps will occur:
        (1) output a regressor file containing regressor information for all runs -- will be used by AFNI in first-level analyses
        (2) determine which TRs need to be censored from each run based on input criteria
        (3) output a censor file that indicates which TRs to censor across all runs -- will be used by AFNI in first-level analyses
        (4) generate censor summary information by run (e.g, % of TRs censored across run and blocks of interest)
        (5) generate censor summary information by block (e.g, # TRs censored per block per run)
        (6) append participant censor summary info to an overall censor summary dataframe

    Inputs:
        par_id 
        framewise_displacement (int or float)
        std_vars (optional, int or float)
        cen_prev_tr (bool)
        overwrite (bool)
        Path (str) - path to direcory that contains foodcue_onsetfiles/ and fmriprep/ directories.
        
    """

    # set base_directory
    if preproc_path is False:

        # get script location
        script_path = Path(__file__).parent.resolve()

        # change directory to base directory (BIDSdat) and get path
        os.chdir(script_path)
        os.chdir('../..')
        base_directory = Path(os.getcwd())

        #set specific paths
        bids_origonset_path = Path(base_directory).joinpath('derivatives/preprocessed/foodcue_onsetfiles/orig')
        bids_fmriprep_path = Path(base_directory).joinpath('derivatives/preprocessed/fmriprep')


    elif isinstance(preproc_path, str):
        # make input string a path
        preprocessed_directory = Path(preproc_path)

        #set specific paths
        bids_origonset_path = Path(preprocessed_directory).joinpath('foodcue_onsetfiles/orig')
        bids_fmriprep_path = Path(preprocessed_directory).joinpath('fmriprep')

    else: 
        print("preproc_path must be string")
        raise Exception()


    # set sub with leading zeros
    sub = str(par_id).zfill(3)
   
    # get participant confound and onset files
    confound_files = list(Path(bids_fmriprep_path).rglob('sub-' + str(sub) + '/ses-1/func/*task-foodcue_run*confounds_timeseries.tsv'))
    orig_onsetfiles = list(Path(bids_origonset_path).rglob('sub-' + str(sub) + '*AFNIonsets.txt'))

    # exit if no participant confound files or onset files
    if len(confound_files) > 5:
        print("sub-" + str(sub) + " has more than 5 confound files. Should have 1 per run at most")
        raise Exception()

    if len(confound_files) < 1:
        print("No confound files found for sub-" + str(sub) + ". Unable to generate regressor and censor files")
        raise Exception()

    if len(orig_onsetfiles) < 1:
        print("No onset files found for sub-'" + str(sub) + "Run p1_getonsets() before p2_create_censor_files()")
        raise Exception()

    # check framewise_displacement input
    if isinstance(framewise_displacement, int) or isinstance(framewise_displacement, float):
            framewise_displacement = float(framewise_displacement)
    else:
        print("framewise_displacement must be integer or float")
        raise Exception()
    
    # check std_vars input
    if std_vars is not False:
        if isinstance(std_vars, int) or isinstance(std_vars, float):
            std_vars = float(std_vars)
        else:
            print("std_vars must be integer or float if specified")
            raise Exception()

    # set censor string 
    censor_str = _get_censorstr(framewise_displacement, std_vars, cen_prev_tr)

    ###############################################
    ### Import or generate censor summary files ###
    ###############################################

    censor_summary_byrun_allPar, censor_summary_byblock_allPar = _get_summary_files(bids_fmriprep_path, censor_str, sub, overwrite)

    ##############################
    ### Create regressor files ###
    ##############################

    # run function to generate concatenated level-1-regressor dataframe
    regress_Pardat = _gen_concatenated_regressor_file(confound_files)

    # Export participant regressor file with and without columns names
    regress_Pardat.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'sub-' + sub + '_foodcue-allruns_confounds-noheader.tsv')), sep = '\t', encoding='utf-8-sig', index = False, header=False)
    regress_Pardat.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'sub-' + sub + '_foodcue-allruns_confounds-header.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

    ###########################
    ### Create censor files ###
    ###########################

    # create run censor data summary per participant
    censor_sum_byrun_Pardat = pd.DataFrame(np.zeros((0, 8)))
    censor_sum_byrun_Pardat.columns = ['sub','run', 'n_vol', 'n_censor', 'p_censor','n_vol_interest', 'n_censor_interest', 'p_censor_interest']

    censor_sum_byblock_Pardat = pd.DataFrame(np.zeros((0, 8)))
    censor_sum_byblock_Pardat.columns = ['sub','run', 'HighLarge', 'HighSmall', 'LowLarge', 'LowSmall', 'OfficeLarge','OfficeSmall']

    # create empty list for censor data
    censordata_allruns = []

    confound_files.sort()
    for file in confound_files:

        #load data
        confound_dat_all = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python')

        # get run number
        runnum = int(str(file).rsplit('/',1)[-1][31:32])

        # select variables generating censor files
        confound_dat = confound_dat_all[['framewise_displacement', 'std_dvars']].copy()

        # add non-steady-state outlier column (only exists in confound.tsv files with non-steady-state outliers)
        if 'non_steady_state_outlier00' in confound_dat_all:
            confound_dat['non_steady_state_outlier00'] = confound_dat_all['non_steady_state_outlier00']
        else: 
            confound_dat['non_steady_state_outlier00'] = 0

        # get orignal onset files for subject (note: there is 1 onset file per condition)
        orig_onsetfiles = list(Path(bids_origonset_path).rglob('sub-' + str(sub) + '*AFNIonsets.txt'))

        # run function to generate r_int_list and a dictionary of block onset times (block_onsets_TR_dict)
        r_int_list, block_onsets_TR_dict = _gen_run_int_list(orig_onsetfiles, confound_dat, runnum)

        # run function to get censor information by run
        res = _get_run_censor_info(confound_dat, FD_thresh = framewise_displacement, std_dvars_thresh = std_vars, r_int_info = r_int_list, cen_prev_TR_flag=cen_prev_tr)

        # add run-specific censor data to overall censor file
        run_censordata = res[0]
        censordata_allruns.extend(run_censordata)
        
        # add run-specific summary information to participant summary dataframe (censor_sum_byrun_Pardat)
        # res[1] = number of TRs total; res[2] = number of TRs censored total, res[3] = % of TRs censored total
        # res[4] = number of TRs of interest; res[5] = number of TRs of interest censored , res[6] = % of TRs of interest censored
        df_len = len(censor_sum_byrun_Pardat)
        runsum = [sub, runnum, res[1], res[2], res[3], res[4], res[5], res[6]]
        censor_sum_byrun_Pardat.loc[df_len] = runsum

        # get censor information by condition/block
        byblock_run_row = pd.DataFrame(_get_censorsum_byblock(block_onsets_TR_dict, run_censordata, sub, runnum))
        
        # append censor information by condition/block to censor_sum_byblock_Pardat dataframe
        censor_sum_byblock_Pardat = pd.concat([censor_sum_byblock_Pardat, byblock_run_row])

    # Export participant censor file (note: afni expects TSV files to have headers -- so export with header=True)
    censordata_allruns_df = pd.DataFrame(censordata_allruns)
    censordata_allruns_df.columns = ['header']
    censordata_allruns_df.to_csv(str(Path(bids_fmriprep_path).joinpath('sub-' + sub + '/ses-1/func/' + 'sub-' + sub + '_foodcue-allruns_censor_' + str(censor_str) + '.tsv')), sep = '\t', encoding='utf-8-sig', index = False, header=True)

    # Add participant censor summarys to overall censor summary databases
    censor_summary_byrun_allPar = pd.concat([censor_summary_byrun_allPar, censor_sum_byrun_Pardat])
    censor_summary_byblock_allPar = pd.concat([censor_summary_byblock_allPar, censor_sum_byblock_Pardat])

    # Export overall censor summary databases
    censor_summary_byrun_allPar.to_csv(str(Path(bids_fmriprep_path).joinpath('task-foodcue_byrun-censorsummary_' + str(censor_str) + '.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
    censor_summary_byblock_allPar.to_csv(str(Path(bids_fmriprep_path).joinpath('task-foodcue_byblock-censorsummary_' + str(censor_str) + '.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

    # return particpant databases for integration testing
    return censordata_allruns_df, censor_sum_byrun_Pardat, censor_sum_byblock_Pardat

#if __name__ == "__main__":
#    p2_create_censor_files(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
