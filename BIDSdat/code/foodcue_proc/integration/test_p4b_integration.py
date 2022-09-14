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
import p4b_gen_byblock_onsets

####################
##### Fixtures #####
####################

@pytest.fixture
def onset_dict_byblock_fixture():

    HL = {0: [4.0, '*', 4.0, 4.0, '*'], 1: ['*', '*', '*', '*', '*']}
    HighLarge = pd.DataFrame(data=HL)

    HS = {0: [30.0, '*', 30.0, 30.0, '*'], 1: ['*', '*', '*', '*', '*']}
    HighSmall = pd.DataFrame(data=HS)

    LL = {0: [56.0, 56.0, '*', 56.0, '*'], 1: ['*', '*', '*', '*', '*']}
    LowLarge = pd.DataFrame(data=LL)

    LS = {0: [82.0, 82.0, '*', 82.0, '*'], 1: ['*', '*', '*', '*', '*']}
    LowSmall = pd.DataFrame(data=LS)

    OL = {0: [108.0, 108.0, '*', 108.0, '*'], 1: ['*', '*', '*', '*', '*']}
    OfficeLarge = pd.DataFrame(data=OL)

    OS = {0: [134.0, 134.0, '*', 134.0, '*'], 1: ['*', '*', '*', '*', '*']}
    OfficeSmall = pd.DataFrame(data=OS)

    onset_dict_fd1_byblock7 = {'HighLarge': HighLarge,
                            'HighSmall': HighSmall,
                            'LowLarge': LowLarge,
                            'LowSmall': LowSmall,
                            'OfficeLarge': OfficeLarge,
                            'OfficeSmall': OfficeSmall}

    return onset_dict_fd1_byblock7


#################
##### Tests #####
#################
def test_p4b(onset_dict_byblock_fixture):
    
    # set path to fixtures/preprocessed directory -- will be input to function
    preproc_path = str('/Users/baf44/Keller_FoodBrainStudy/BIDSdat/code/foodcue_proc/fixtures/preprocessed')

    # run function
    onset_dict = p4b_gen_byblock_onsets.gen_byblock_onsets(par_id = 999, 
                                                        censorsum_file = 'fixture_task-foodcue_bycond-censorsummary_fd-1.0.tsv', 
                                                        minblockTR = 7, 
                                                        preproc_path=preproc_path)

    assert_frame_equal(onset_dict_byblock_fixture['HighLarge'], onset_dict['HighLarge'])
    assert_frame_equal(onset_dict_byblock_fixture['HighSmall'], onset_dict['HighSmall'])
    assert_frame_equal(onset_dict_byblock_fixture['LowLarge'], onset_dict['LowLarge'])
    assert_frame_equal(onset_dict_byblock_fixture['LowSmall'], onset_dict['LowSmall'])
    assert_frame_equal(onset_dict_byblock_fixture['OfficeLarge'], onset_dict['OfficeLarge'])
    assert_frame_equal(onset_dict_byblock_fixture['OfficeSmall'], onset_dict['OfficeSmall'])

