#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to generate a dataframe with covariates for group-level analyses in AFNI. 

Copyright (C) 2022 Bari Fuchs

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
import pandas as pd
import os
from pathlib import Path

##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################
def gen_dataframe():
    """Function to generate txt file with 1 row per subject and 1 column per covariate for use with 3dttest++ in AFNI. 
        Covariates to include in analyses can be specified via AFNI using column indexing.
    
    Rows in COVAR_FILE whose first column don't match a dataset label (e.g., in AFNI's gen_group_command.py for 3dttest++) are ignored (silently). 
        Thus, all subjects can be included in the covariate dataframe, even if they will not be included in analyses
    """

    # get script location
    script_path = Path(__file__).parent.resolve()

    # change directory to bids and get path
    os.chdir(script_path)
    os.chdir('../../../')
    bids_path = Path(os.getcwd())

    # change directory project directory
    os.chdir('../')
    proj_path = Path(os.getcwd())

    #set specific paths
    fmriprep_path = Path(bids_path).joinpath('derivatives/preprocessed/fmriprep')
    v6covar_path = Path(bids_path).joinpath('derivatives/preprocessed/V6_covariates')
    database_path = Path(proj_path).joinpath('Databases')

    #########################################
    #### Import databases with covariates ###
    #########################################

    # import anthro database and format 'id' column for merging ``
    anthro_df = pd.read_spss(Path(database_path).joinpath('anthro_data.sav')) # import anthro database
    anthro_df['id'] = anthro_df['id'].astype(int) # get rid of decimal place
    anthro_df['id'] = anthro_df['id'].astype(str) # convert to string -- needed for zfill
    anthro_df['id'] = anthro_df['id'].str.zfill(3) # add leading zeros

    # import motion database and format 'id' column for merging 
    mot_df = pd.read_csv(Path(fmriprep_path).joinpath('task-foodcue_avg-fd.tsv'), sep='\t') # import motion database
    mot_df['id'] = mot_df['id'].astype(int) # get rid of decimal place
    mot_df['id'] = mot_df['id'].astype(str) # convert to string -- needed for zfill
    mot_df['id'] = mot_df['id'].str.zfill(3) # add leading zeros

    # import v6 database and format 'id' column for merging 
    v6_df = pd.read_csv(Path(v6covar_path).joinpath('V6_covariates.csv')) # import v6 database
    v6_df['id'] = v6_df['id'].astype(int) # get rid of decimal place
    v6_df['id'] = v6_df['id'].astype(str) # convert to string -- needed for zfill
    v6_df['id'] = v6_df['id'].str.zfill(3) # add leading zeros

    ###########################################
    #### Combine covariates into 1 database ###
    ###########################################

    # get list of subjects based on id column in mot_df
    subs_list = list(mot_df['id']) # get list of subjects based on id column in mot_df

    # create empty dataframe to append covariates to
    covar_df = pd.DataFrame() #create empty dataframe
    covar_df['id'] = subs_list #add subjects to column sub

    # Add variables from anthro database to covar_df (sex, risk)
    covar_df = pd.merge(covar_df,anthro_df[['id', 'sex', 'risk_status_mom', 'dxa_total_fat_mass', 'height_avg']],on='id', how='left')

    # Add variable from motion database to covar_df
    covar_df = pd.merge(covar_df,mot_df[['id','fd_avg_allruns']],on='id', how='left')

    # Add fullness and pre-mri cams variables from v6 database to covar_df
    covar_df = pd.merge(covar_df,v6_df[['id','imp_med','imp_max', 'imp_min', 'cams_pre_mri']],on='id', how='left')

    ############################
    #### Clean up covariates ###
    ############################

    # encode sex as -1 for male and 1 for female so that the main effect will be the average between males and females
    covar_df = covar_df.replace({'sex':{'Male':-1, 'Female':1}})

    # encode risk as -1 for low and 1 for high so that the main effect will be the average between males and females
    covar_df = covar_df.replace({'risk_status_mom':{'Low Risk':-1, 'High Risk':1}})

    # rename id column to Subj
    covar_df = covar_df.rename(columns={'id': 'Subj'})

    # rename pre-mri FF columns
    covar_df.rename(columns={'imp_med': 'ff_medimp', 'imp_max': 'ff_maximp', 'imp_min': 'ff_minimp'}, inplace=True)

    # compute fat mass index
    covar_df['dxa_total_fat_mass'] = covar_df['dxa_total_fat_mass'].astype(str).astype(float) #convert to string, then float
    covar_df['height_avg'] = covar_df['height_avg'].astype(str).astype(float) #convert to string, then float
    covar_df['fmi'] = (covar_df['dxa_total_fat_mass'].div(1000)) / ((covar_df["height_avg"] * .01)**2)

    # set column order so that the base covariates come first
    covar_df = covar_df[['Subj','sex','fd_avg_allruns','ff_medimp', 'ff_maximp', 'ff_minimp', 'cams_pre_mri', 'risk_status_mom', 'fmi']]

    #########################
    #### Export dataframe ###
    #########################

    # write dataframe with covariates
    covar_df.to_csv(str(Path(bids_path).joinpath('derivatives/analyses/foodcue-paper1/level2/ttest-covariates.txt')), sep = '\t', encoding='ascii', index = False)