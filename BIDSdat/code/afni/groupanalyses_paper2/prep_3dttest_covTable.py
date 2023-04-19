#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to generate a dataframe with covariates for group-level analyses in AFNI. 

Written by Bari Fuchs in Fall 2022

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
import pandas as pd
import os
from pathlib import Path
import numpy as np

##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################
def gen_dataframe():
    """Function to generate covariate dataframe with 1 row per subject and 1 column per covariate.
    
    Note, rows in COVAR_FILE whose first column don't match a dataset label (in analysis script) are ignored (silently). 
        Thus, all subjects can be included in the covariate dataframe, even if they will not be included in analyses

    Covariates include control variables (sex, body fat, motion, pre-mri fullness, pre-mri CAMS) and FEIS intake variables 
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
    risk_path = Path(bids_path).joinpath('derivatives/preprocessed/risk_scores')
    v6covar_path = Path(bids_path).joinpath('derivatives/preprocessed/V6_covariates')
    database_path = Path(proj_path).joinpath('Databases')
    intake_path = Path(bids_path).joinpath('derivatives/analyses/intake_feis')

    #########################################
    #### Import databases with covariates ###
    #########################################

    # import anthro database and format 'id' column for merging 
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

    # import intake database
    intake_df = pd.read_csv(Path(intake_path).joinpath('intake_feis.csv')) # import intake database
    intake_df.rename(columns = {'sub':'id'}, inplace = True) # change 'sub' column name to 'id'
    intake_df['id'] = intake_df['id'].astype(str) # convert to string -- needed for zfill
    intake_df['id'] = intake_df['id'].str.zfill(3) # add leading zeros

    # import riskscores database
    riskscore_df = pd.read_csv(Path(risk_path).joinpath('risk_scores_updated.csv')) # import intake database
    riskscore_df['id'] = riskscore_df['id'].astype(str) # convert to string -- needed for zfill
    riskscore_df['id'] = riskscore_df['id'].str.zfill(3) # add leading zeros

    ###########################################
    #### Combine covariates into 1 database ###
    ###########################################

    # get list of subjects based on id column in mot_df
    subs_list = list(mot_df['id']) # get list of subjects based on id column in mot_df

    # create empty dataframe to append covariates to
    covar_df = pd.DataFrame() #create empty dataframe
    covar_df['id'] = subs_list #add subjects to column sub

    # Add variables from anthro database to covar_df (body fat %)
    covar_df = pd.merge(covar_df,anthro_df[['id', 'sex', 'dxa_total_body_perc_fat' ]],on='id', how='left')

    # Add variable from motion database to covar_df
    covar_df = pd.merge(covar_df,mot_df[['id','fd_avg_allruns']],on='id', how='left')

    # Add fullness and pre-mri cams variables from v6 database to covar_df
    covar_df = pd.merge(covar_df,v6_df[['id','imp_med','imp_max', 'imp_min', 'cams_pre_mri']],on='id', how='left')

    # Add variable from intake database to covar_df
    covar_df = pd.merge(covar_df,intake_df[['id','grams_int', 'grams_ps_lin', 'grams_ps_quad', 'kcal_int', 'kcal_ps_lin','led_grams_int', 'led_grams_ps_lin',
                                            'led_kcal_int', 'led_kcal_ps_lin', 'hed_grams_int', 'hed_grams_ps_lin',
                                            'hed_kcal_int', 'hed_kcal_ps_lin']],on='id', how='left')

    # Add risk score to covar_df
    covar_df = pd.merge(covar_df,riskscore_df[['id','Risk2', 'Risk_imputed', 'eating_rate']],on='id', how='left')

    ############################
    #### Clean up covariates ###
    ############################

    # encode sex as -1 for male and 1 for female so that the main effect will be the average between males and females
    covar_df = covar_df.replace({'sex':{'Male':-1, 'Female':1}})

    # rename id column to Subj
    covar_df = covar_df.rename(columns={'id': 'Subj'})

    # rename pre-mri FF columns
    covar_df.rename(columns={'imp_med': 'ff_medimp', 'imp_max': 'ff_maximp', 'imp_min': 'ff_minimp'}, inplace=True)

    # replace missing values with -999 -- otherwise columns will shift due to missing data in AFNI
    covar_df.replace(np.nan, -999, inplace=True)

    # set column order so that the base covariates come first
    covar_df = covar_df[['Subj','sex','fd_avg_allruns','ff_medimp', 'ff_maximp', 'ff_minimp', 'dxa_total_body_perc_fat', 'cams_pre_mri', 
                                            'Risk2', 'Risk_imputed', 'eating_rate',
                                            'led_grams_int', 'led_grams_ps_lin','led_kcal_int', 'led_kcal_ps_lin', 
                                            'hed_grams_int', 'hed_grams_ps_lin','hed_kcal_int', 'hed_kcal_ps_lin',
                                            'kcal_int', 'kcal_ps_lin', 'grams_int', 'grams_ps_lin', 'grams_ps_quad']]

    #########################
    #### Export dataframe ###
    #########################

    # write dataframe with covariates
    covar_df.to_csv(str(Path(bids_path).joinpath('derivatives/analyses/foodcue-paper2/level2/ttest-covariates.txt')), sep = '\t', encoding='ascii', index = False)