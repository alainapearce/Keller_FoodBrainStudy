#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was created to run python functions related to generating onsets and censorfiles 
that will be used for analyses with AFNI. 

Written by Bari Fuchs in August 2022

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

# import data processing functions
import make_index_byrun
import make_index_byblock
import make_3dmvm_dataframe

############################
### generate index files ###
############################

#make_index_byrun.gen_index_byrun(onset_dir = 'fd-0.9_b20', nruns = 3, preproc_path = False)
#make_index_byblock.gen_index_byblock(onset_dir = 'fd-0.9_by-block-7', nblocks = 3, preproc_path = False)

###############################
### generate MVM datatables ###
###############################

make_3dmvm_dataframe.gen_dataframe(template = 'ped', index_file = 'index_all_fd-0.9_by-block-7_3blocks.txt')
make_3dmvm_dataframe.gen_dataframe(template = 'ped', index_file = 'index_all_fd-0.9_b20_3runs.txt')
