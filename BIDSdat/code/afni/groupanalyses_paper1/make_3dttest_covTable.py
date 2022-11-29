#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to generate a dataframe with covariates for group-level analyses in AFNI. 

Written by Bari Fuchs in Fall 2022

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
import pandas as pd
import os
from pathlib import Path

##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################
def gen_dataframe():
    """Function to generate covariate dataframe with 1 row per subject and 1 column per covariate.
    
    Note, rows in COVAR_FILE whose first column don't match a dataset label (in analysis script) are ignored (silently). 
        Thus, all subjects can be included in the covariate dataframe, even if they will not be included in analyses

        TO DO: add body fat %, and maternal weight 
    """

    # get script location
    script_path = Path(__file__).parent.resolve()

    # change directory to base directory (BIDSdat) and get path
    os.chdir(script_path)
    os.chdir('../../../../')
    pardata_directory = Path(os.getcwd())
    #bids_directory = Path(os.getcwd())

    #set specific paths
    bids_path = Path(pardata_directory).joinpath('BIDSdat')
    fmriprep_path = Path(pardata_directory).joinpath('BIDSdat/derivatives/preprocessed/fmriprep')
    database_path = Path(pardata_directory).joinpath('Databases')

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
    v6_df = pd.read_spss(Path(database_path).joinpath('visit6_data.sav')) # import motion database
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

    # Add variables from anthro database to covar_df (risk, body fat %)
    covar_df = pd.merge(covar_df,anthro_df[['id', 'sex']],on='id', how='left')

    # Add variable from motion database to covar_df
    covar_df = pd.merge(covar_df,mot_df[['id','fd_avg_allruns']],on='id', how='left')

    # Add fullness variables from v6 database to covar_df
    covar_df = pd.merge(covar_df,v6_df[['id','ff_premri_snack','ff_postmri_snack', 'ff_postmri_snack2']],on='id', how='left')

    ############################
    #### Clean up covariates ###
    ############################

    # encode sex as -1 for male and 1 for female so that the main effect will be the average between males and females
    covar_df = covar_df.replace({'sex':{'Male':1, 'Female':-1}})

    # make function to determine  fulless_preMRI based on other ff variables
    def get_preMRI_ff(row):
        # if post-snack2 is not null, use post-snack2 rating
        if pd.isnull(row['ff_postmri_snack2']) is False:
            ff_premri = row['ff_postmri_snack2']
        # else, if post-snack is not null, use post-snack rating
        elif pd.isnull(row['ff_postmri_snack']) is False:
            ff_premri = row['ff_postmri_snack']
        # else, use pre-snack rating
        else:
            ff_premri = row['ff_premri_snack']
        return ff_premri

    # apply get_preMRI_ff()
    covar_df['ff_premri'] = covar_df.apply(get_preMRI_ff, axis=1)

    # remove variables that are not covariates in analyses
    covar_df.drop(['ff_premri_snack', 'ff_postmri_snack', 'ff_postmri_snack2'], axis = 1, inplace = True)

    # rename id column to Subj
    covar_df = covar_df.rename(columns={'id': 'Subj'})

    #########################
    #### Export dataframe ###
    #########################

    # write dataframe with covariates
    covar_df.to_csv(str(Path(bids_path).joinpath('derivatives/analyses/foodcue-paper1/level2/ttest-covariates.txt')), sep = '\t', encoding='ascii', index = False)