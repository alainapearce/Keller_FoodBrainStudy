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

#set up packages    
from email import header
from pickle import TRUE
from aem import con
from scipy.stats.morestats import shapiro
from pathlib import Path

# import data processing functions
import p1_getonsets
import p2_create_censor_files

##############################################################################
####                                                                      ####
####                             Core Script                              ####
####                                                                      ####
##############################################################################

# get list of subs
subs = ['001']

# call functions for each sub
for sub in subs:
     p1_getonsets.p1_getonsets(par_id = sub, overwrite=True)
     p2_create_censor_files.p2_create_censor_files(par_id = sub, framewise_displacement = 1.0, std_vars=False, cen_prev_tr=False)
