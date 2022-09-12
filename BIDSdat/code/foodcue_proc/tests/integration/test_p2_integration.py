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

# get script location
script_path = Path(__file__).parent.resolve()

# change directory to base directory (BIDSdat) and get path
os.chdir(script_path)
os.chdir('../..')
base_directory = Path(os.getcwd())
bids_origonset_path = Path(base_directory).joinpath('derivatives/preprocessed/foodcue_onsetfiles/orig')

####################
##### Fixtures #####
####################
@pytest.fixture
def censordata_allruns_df_fixture():

    censor_sum_Pardat = pd.DataFrame(np.zeros((0, 8)))
    censor_sum_Pardat.columns = ['sub','run', 'n_vol', 'n_censor', 'p_censor','n_vol_interest', 'n_censor_interest', 'p_censor_interest']


@pytest.fixture
def censor_sum_bycond_Pardat_fixture():

    censor_sum_bycond_fd1 = {'sub': [999, 999, 999, 999, 999],
                            'run': [1.0, 2.0, 3.0, 4.0, 5.0],
                            'HighLarge': [],
                            'HighSmall': [],
                            'LowLarge': [],
                            'LowSmall': [],
                            'OfficeLarge': [],
                            'OfficeSmall': []
                            }

    censor_sum_bycond_fd1 = pd.DataFrame(data=censor_sum_bycond_fd1)

    censor_sum_bycond_fd1_stddvar = {'sub': [999, 999, 999, 999, 999],
                            'run': [1.0, 2.0, 3.0, 4.0, 5.0],
                            'HighLarge': [],
                            'HighSmall': [],
                            'LowLarge': [],
                            'LowSmall': [],
                            'OfficeLarge': [],
                            'OfficeSmall': []
                            }

    censor_sum_bycond_fd1_stddvar = pd.DataFrame(data=censor_sum_bycond_fd1_stddvar)

#################
##### Tests #####
#################
def p2_test(censordata_allruns_df_fixture, censor_sum_bycond_Pardat_fixture):
    
    censordata_allruns_df, censor_sum_bycond_Pardat = p2_create_censor_files.p2_create_censor_files(par_id = 999, framewise_displacement = 1, std_vars = False, cen_prev_tr=False, overwrite=True)

    assert censordata_allruns_df == censordata_allruns_df_fixture

    assert censor_sum_bycond_Pardat == censor_sum_bycond_Pardat_fixture