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
import p4a_gen_byrun_onsets

####################
##### Fixtures #####
####################

@pytest.fixture
def onset_dict_fixture():

    HL = {0: [4.0, '*', '*', 4.0, '*'], 1: ['*', '*', '*', '*', '*']}
    HighLarge = pd.DataFrame(data=HL)

    HS = {0: [30.0, '*', '*', 30.0, '*'], 1: ['*', '*', '*', '*', '*']}
    HighSmall = pd.DataFrame(data=HS)

    LL = {0: [56.0, '*', '*', 56.0, '*'], 1: ['*', '*', '*', '*', '*']}
    LowLarge = pd.DataFrame(data=LL)

    LS = {0: [82.0, '*', '*', 82.0, '*'], 1: ['*', '*', '*', '*', '*']}
    LowSmall = pd.DataFrame(data=LS)

    OL = {0: [108.0, '*', '*', 108.0, '*'], 1: ['*', '*', '*', '*', '*']}
    OfficeLarge = pd.DataFrame(data=OL)

    OS = {0: [134.0, '*', '*', 134.0, '*'], 1: ['*', '*', '*', '*', '*']}
    OfficeSmall = pd.DataFrame(data=OS)

    onset_dict_fd1_b20 = {'HighLarge': HighLarge,
                            'HighSmall': HighSmall,
                            'LowLarge': LowLarge,
                            'LowSmall': LowSmall,
                            'OfficeLarge': OfficeLarge,
                            'OfficeSmall': OfficeSmall}

    return onset_dict_fd1_b20


#################
##### Tests #####
#################
def test_p4a(onset_dict_fixture):
    
    # set path to fixtures/preprocessed directory -- will be input to function
    preproc_path = str('/Users/baf44/Keller_FoodBrainStudy/BIDSdat/code/foodcue_proc/fixtures/preprocessed')

    # run function
    onset_dict = p4a_gen_byrun_onsets.gen_byrun_onsets(par_id = 999, 
                                                        censorsum_file = 'fixture_task-foodcue_censorsummary_fd-1.0.tsv', 
                                                        p_thresh_run = False, 
                                                        p_thresh_block=20,
                                                        preproc_path=preproc_path)

    assert_frame_equal(onset_dict_fixture['HighLarge'], onset_dict['HighLarge'])
    assert_frame_equal(onset_dict_fixture['HighSmall'], onset_dict['HighSmall'])
    assert_frame_equal(onset_dict_fixture['LowLarge'], onset_dict['LowLarge'])
    assert_frame_equal(onset_dict_fixture['LowSmall'], onset_dict['LowSmall'])
    assert_frame_equal(onset_dict_fixture['OfficeLarge'], onset_dict['OfficeLarge'])
    assert_frame_equal(onset_dict_fixture['OfficeSmall'], onset_dict['OfficeSmall'])

