#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#set up packages
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import os
from pandas.testing import assert_frame_equal

# import functions to test
import p2_create_censor_files

####################
##### Fixtures #####
####################
@pytest.fixture
def censordata_allruns_df_fixture():

    censordata_allruns_fd1 = pd.DataFrame(np.zeros((400, 1)))
    censordata_allruns_fd1.columns = ['header']
    censordata_allruns_fd1.at[np.r_[2:80, 91:95, 104:160, 162:171, 175:184, 193:197, 242:251, 255:264, 268:277, 281:290, 294:303, 307:316],["header"]] = 1

    # change column to integer datatype
    censordata_allruns_fd1 = censordata_allruns_fd1.astype({'header':'int'})

    return censordata_allruns_fd1

@pytest.fixture
def censor_sum_Pardat_fixture():

    censor_sum_Pardat_fd1 = {'sub': ['999', '999', '999', '999', '999'],
                            'run': [1.0, 2.0, 3.0, 4.0, 5.0],
                            'n_vol': [78.0, 78.0, 78.0, 78.0, 78.0],
                            'n_censor': [0.0, 18.0, 56.0, 24.0, 78.0],
                            'p_censor': [0.0, 23.1, 71.8, 30.8, 100],
                            'n_vol_interest': [54.0, 54.0, 54.0, 54.0, 54.0],
                            'n_censor_interest': [0.0, 18.0, 32.0, 0.0, 54.0],
                            'p_censor_interest': [0.0, 33.3, 59.3, 0.0, 100]}

    censor_sum_Pardat_fd1 = pd.DataFrame(data=censor_sum_Pardat_fd1)
    return censor_sum_Pardat_fd1
 

@pytest.fixture
def censor_sum_bycond_Pardat_fixture():

    censor_sum_bycond_fd1 = {'sub': ['999', '999', '999', '999', '999'],
                            'run': [1.0, 2.0, 3.0, 4.0, 5.0],
                            'HighLarge': [9.0, 0.0, 9.0, 9.0, 0.0],
                            'HighSmall': [9.0, 0.0, 9.0, 9.0, 0.0],
                            'LowLarge': [9.0, 9.0, 4.0, 9.0, 0.0],
                            'LowSmall': [9.0, 9.0, 0.0, 9.0, 0.0],
                            'OfficeLarge': [9.0, 9.0, 0.0, 9.0, 0.0],
                            'OfficeSmall': [9.0, 9.0, 0.0, 9.0, 0.0]}

    censor_sum_bycond_fd1 = pd.DataFrame(data=censor_sum_bycond_fd1)

    return censor_sum_bycond_fd1

#################
##### Tests #####
#################
def test_p2(censordata_allruns_df_fixture, censor_sum_Pardat_fixture, censor_sum_bycond_Pardat_fixture):
    
    # set path to fixtures/preprocessed directory -- will be input to function
    preproc_path = str('/Users/baf44/Keller_FoodBrainStudy/BIDSdat/code/foodcue_proc/fixtures/preprocessed')

    # run function
    censordata_allruns_df, censor_sum_Pardat, censor_sum_bycond_Pardat = p2_create_censor_files.create_censor_files(par_id = 999, 
                                                                                                                        framewise_displacement = 1, 
                                                                                                                        std_vars = False, 
                                                                                                                        cen_prev_tr=False, 
                                                                                                                        overwrite=True, 
                                                                                                                        preproc_path=preproc_path)

    assert_frame_equal(censordata_allruns_df, censordata_allruns_df_fixture)
    assert_frame_equal(censor_sum_Pardat, censor_sum_Pardat_fixture)
    assert_frame_equal(censor_sum_bycond_Pardat.reset_index(drop=True), censor_sum_bycond_Pardat_fixture.reset_index(drop=True)) #drop index since we dont care about that being equal
