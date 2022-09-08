#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#set up packages
import pytest

# import functions to test
from p2_create_censor_files import _gen_concatenated_regressor_file
from p2_create_censor_files import _gen_run_int_list
from p2_create_censor_files import _get_run_censor_info
from p2_create_censor_files import _get_censorsum_bycond


# def test_gen_concatenated_regressor_file(confound_files_fixture, regress_pardat_fixture):

#     # run function
#     regress_Pardat = _gen_concatenated_regressor_file(confound_files_fixture)
    
#     # check function output
#     assert regress_Pardat == regress_pardat_fixture, "error"

#def test_gen_run_int_list(confound_dat_fixture, r_int_list_fixture, block_onsets_TR_dict_fixture):
#    # # run function
#    r_int_list, block_onsets_TR_dict = _gen_run_int_list(bids_origonset_path, sub = 999, confound_dat_fixture, runnum)

#     # check function output
#    assert r_int_list == r_int_list_fixture, "r_int_list error"
#    assert block_onsets_TR_dict == block_onsets_TR_dict_fixture, "block_onsets_TR_dict error"

def test_get_run_censor_info(confound_dat_fixture, r_int_list_fixture, censor_info_fixture):

    # run function
    res = _get_run_censor_info(confound_dat_fixture, 
                                FD_thresh = 1.0, 
                                std_dvars_thresh = 1.0, 
                                r_int_info = r_int_list_fixture, 
                                cen_prev_TR_flag=True)

    # check function output
    assert censor_info_fixture == res[0], "censor info error"

    # # run function
    # res2 = _get_run_censor_info(confound_dat_fixture, 
    #                             FD_thresh = 1.0, 
    #                             std_dvars_thresh = False, 
    #                             r_int_info = r_int_list_fixture, 
    #                             cen_prev_TR_flag=False)

    # # check function output
    # assert censor_info_fixture == res2[0], "censor info error"

    # # run function
    # res3 = _get_run_censor_info(confound_dat_fixture, 
    #                             FD_thresh = 1.0, 
    #                             std_dvars_thresh = 1.0, 
    #                             r_int_info = r_int_list_fixture, 
    #                             cen_prev_TR_flag=False)

    # # check function output
    # assert censor_info_fixture == res3[0], "censor info error"



#def test_get_censorsum_bycond():
    #bycond_run_row = _get_censorsum_bycond(block_onsets_TR_dict, run_censordata, sub = 999, runnum) 