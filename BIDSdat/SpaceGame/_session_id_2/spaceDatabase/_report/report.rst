Node: spaceDatabase (utility)
=============================


 Hierarchy : SpaceGame.spaceDatabase
 Exec ID : spaceDatabase.a1


Original Inputs
---------------


* Space_group_trialdat : ['no files']
* Space_summary_dat : ['no files']
* bids_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* function_str : def updateDatabase_save(Space_summary_dat, Space_group_trialdat, overwrite_flag, bids_dir):
    import pandas as pd
    import numpy as np
    from pathlib import Path
    from nipype.interfaces.base import Bunch

    #derivative data path
    derivative_data_path = Path(bids_dir).joinpath('derivatives/preprocessed/beh')

    #function to drop rows based on values
    def filter_rows_by_values(df, sub_values, sesnum):
        #filter based on sub and ses
        return df[(df['sub'].isin(sub_values) == False) & (df['ses'] == sesnum)]

    #### Summary Data ####
    #check to see if it is filepath str or 'no files' message
    if isinstance(Space_summary_dat[0], str):

        print('******** No new data to be processed ********')

        Space_database_wide = 'no new data files'
        Space_database_blocks = 'no new data files'

    else:
        #get a Bunch object if more than 1 participant
        if isinstance(Space_summary_dat, Bunch):
            #get output data from node
            Space_summary_datlist = Space_summary_dat.summarySpace_dat

            #combine datasets
            Space_summary_dat = pd.concat(Space_summary_datlist)

        #if only 1 participant/dataset then it is a list
        elif isinstance(Space_summary_dat, list):
            if len(Space_summary_dat) == 1:
                Space_summary_dat = Space_summary_dat[0]
            else:
                Space_summary_dat = pd.concat(Space_summary_dat)

        #if a pandas dataframe
        if isinstance(Space_summary_dat, pd.DataFrame):

            #get column names
            columnnames = Space_summary_dat.columns

            #get session subsets
            db_sessions = Space_summary_dat.ses.unique()

            if len(db_sessions) > 1:
                Space_sum_ses1_dat = Space_summary_dat.groupby('ses').get_group(1)
                Space_sum_ses2_dat = Space_summary_dat.groupby('ses').get_group(2)

                #make wide data set
                Space_sum_ses1_wide = Space_sum_ses1_dat.pivot(columns='block', index='sub', values=columnnames[3:16])
                Space_sum_ses1_wide.columns = ['_'.join(col) for col in Space_sum_ses1_wide.columns.reorder_levels(order=[1, 0])]

                Space_sum_ses2_wide = Space_sum_ses2_dat.pivot(columns='block', index='sub', values=columnnames[3:16])
                Space_sum_ses2_wide.columns = ['_'.join(col) for col in Space_sum_ses2_wide.columns.reorder_levels(order=[1, 0])]

                #make the sub index into a dataset column
                Space_sum_ses1_wide = Space_sum_ses1_wide.reset_index(level = 0)
                Space_sum_ses2_wide = Space_sum_ses2_wide.reset_index(level = 0)

                #add session
                Space_sum_ses1_wide.insert(1, 'ses', 1)
                Space_sum_ses2_wide.insert(1, 'ses', 2)

                #concatonate databases
                Space_summary_wide = pd.concat([Space_sum_ses1_wide,Space_sum_ses2_wide],ignore_index=True)

            else:
                #make wide data set
                Space_summary_wide = Space_summary_dat.pivot(columns='block', index='sub', values=columnnames[3:16])
                Space_summary_wide.columns = ['_'.join(col) for col in Space_summary_wide.columns.reorder_levels(order=[1, 0])]

                #make the sub index into a dataset column
                Space_summary_wide = Space_summary_wide.reset_index(level = 0)

                #add session
                Space_summary_wide.insert(1, 'ses', db_sessions[0])

            #re-order columns
            columnnames_reorder = ['sub', 'ses', 'all_earth_rt_mean', 'all_earth_rt_median', 'all_earth_n_miss', 'all_earth_p_miss', 'all_planet_rt_mean', 'all_planet_rt_median', 'all_planet_n_miss',  'all_planet_p_miss', 'all_reward_rate', 'all_avg_reward', 'all_reward_rate_corrected',  'all_prob_sameplanet_earthsame', 'all_prob_sameplanet_earthdif', 'b1_earth_rt_mean', 'b1_earth_rt_median', 'b1_earth_n_miss', 'b1_earth_p_miss', 'b1_planet_rt_mean', 'b1_planet_rt_median', 'b1_planet_n_miss', 'b1_planet_p_miss', 'b1_reward_rate', 'b1_avg_reward', 'b1_reward_rate_corrected', 'b1_prob_sameplanet_earthsame','b1_prob_sameplanet_earthdif', 'b2_earth_rt_mean', 'b2_earth_rt_median', 'b2_earth_n_miss', 'b2_earth_p_miss', 'b2_planet_rt_mean', 'b2_planet_rt_median', 'b2_planet_n_miss', 'b2_planet_p_miss', 'b2_reward_rate', 'b2_avg_reward', 'b2_reward_rate_corrected', 'b2_prob_sameplanet_earthsame', 'b2_prob_sameplanet_earthdif', 'b3_earth_rt_mean', 'b3_earth_rt_median', 'b3_earth_n_miss', 'b3_earth_p_miss', 'b3_planet_rt_mean','b3_planet_rt_median', 'b3_planet_n_miss', 'b3_planet_p_miss', 'b3_reward_rate', 'b3_avg_reward', 'b3_reward_rate_corrected', 'b3_prob_sameplanet_earthsame', 'b3_prob_sameplanet_earthdif', 'b4_earth_rt_mean', 'b4_earth_rt_median', 'b4_earth_n_miss', 'b4_earth_p_miss',  'b4_planet_rt_mean', 'b4_planet_rt_median', 'b4_planet_n_miss', 'b4_planet_p_miss',   'b4_reward_rate', 'b4_avg_reward', 'b4_reward_rate_corrected', 'b4_prob_sameplanet_earthsame', 'b4_prob_sameplanet_earthdif']

            Space_summary_wide = Space_summary_wide.reindex(columns=columnnames_reorder)

            #get blocks subset
            Space_summary_blocks = Space_summary_dat[Space_summary_dat.block.isin(['b1', 'b2', 'b3', 'b4'])]

            #load databases
            Space_database_wide = pd.read_csv(str(Path(derivative_data_path).joinpath('task-space_summary.tsv')), sep = '\t')
            Space_database_blocks = pd.read_csv(str(Path(derivative_data_path).joinpath('task-space_summary_long.tsv')), sep = '\t')

            #if overwriting participants
            if overwrite_flag == True:
                #filter out/remove exisiting subs to overwrit~
                if len(db_sessions) > 1:
                    #get list of subs by ses to filter in wide and long data
                    wide_sub_list = Space_summary_wide.groupby('ses')['sub'].unique()
                    long_sub_list = Space_summary_blocks.groupby('ses')['sub'].unique()

                    Space_database_ses1 = filter_rows_by_values(Space_database_wide, wide_sub_list[0], 1)
                    Space_database_ses2 = filter_rows_by_values(Space_database_wide, wide_sub_list[1], 2)

                    Space_database_ses1_long = filter_rows_by_values(Space_database_blocks, long_sub_list[0], 1)
                    Space_database_ses2_long = filter_rows_by_values(Space_database_blocks, long_sub_list[1], 2)

                    #concatonate databases
                    Space_database_wide = pd.concat([Space_database_ses1, Space_database_ses2],ignore_index=True)
                    Space_database_blocks = pd.concat([Space_database_ses1_long, Space_database_ses2_long],ignore_index=True)

                else:
                    wide_sub_list = list(Space_summary_wide['sub'].unique())
                    long_sub_list = list(Space_summary_blocks['sub'].unique())

                    #filter by ses and sub
                    Space_database_ses = filter_rows_by_values(Space_database_wide, wide_sub_list, db_sessions[0])
                    Space_database_long_ses = filter_rows_by_values(Space_database_blocks, long_sub_list, db_sessions[0])

                    #concatonate with other session in full database
                    Space_database_wide = pd.concat([Space_database_wide[Space_database_wide['ses'] != db_sessions[0]], Space_database_ses],ignore_index=True)
                    Space_database_blocks = pd.concat([Space_database_blocks[Space_database_blocks['ses'] != db_sessions[0]], Space_database_long_ses],ignore_index=True)


            #add newly processed data
            Space_database_wide = Space_database_wide.append(Space_summary_wide)
            Space_database_blocks = Space_database_blocks.append(Space_summary_blocks)

            #sort to ensure in sub order
            Space_database_wide = Space_database_wide.sort_values(by = ['ses', 'sub'])
            Space_database_blocks = Space_database_blocks.sort_values(by = ['ses', 'sub', 'block'])

            #round to 3 decimal points
            Space_database_wide = Space_database_wide.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)
            Space_database_blocks = Space_database_blocks.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)

            #write databases
            Space_database_wide.to_csv(str(Path(derivative_data_path).joinpath('task-space_summary.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
            Space_database_blocks.to_csv(str(Path(derivative_data_path).joinpath('task-space_summary_long.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

        else:
            print('No raw data files that need to be processed')
            Space_database_wide = np.nan
            Space_database_blocks = np.nan

    #### Group trial data ####
    if isinstance(Space_group_trialdat[0], str):

        print('******** No new data to be processed ********')

        Space_groupdat = 'no new data files'

    else:
        #get a Bunch object if more than 1 participant
        if isinstance(Space_group_trialdat, Bunch):
            #get output data from node
            Space_group_trialdatlist = Space_group_trialdat.group_trialdat

            #combine datasets
            Space_groupdat = pd.concat(Space_group_trialdatlist)

        #if only 1 participant/dataset then it is a list
        elif isinstance(Space_group_trialdat, list):
            if len(Space_group_trialdat) == 1:
                Space_groupdat = Space_group_trialdat[0]
            else:
                Space_groupdat = pd.concat(Space_group_trialdat)

        #if a pandas dataframe
        if isinstance(Space_groupdat, pd.DataFrame):

            #get session subsets
            db_group_sessions = Space_groupdat.ses.unique()

            #load databases
            Space_groupdat_database = pd.read_csv(str(Path(derivative_data_path).joinpath('task-space_groupdata.tsv')), sep = '\t')

            #if overwriting participants
            if overwrite_flag == True:
                #filter out/remove exisiting subs to overwrit~
                if len(db_group_sessions) > 1:
                    #get list of subs by ses to filter in wide and long data
                    dat_sub_list = Space_groupdat.groupby('ses')['sub'].unique()

                    Space_groupdat_ses1 = filter_rows_by_values(Space_groupdat_database, dat_sub_list[0], 1)
                    Space_groupdat_ses2 = filter_rows_by_values(Space_groupdat_database, dat_sub_list[1], 2)

                    #concatonate databases
                    Space_groupdat_database = pd.concat([Space_groupdat_ses1, Space_groupdat_ses2],ignore_index=True)

                else:
                    dat_sub_list = list(Space_groupdat['sub'].unique())

                    #filter by ses and sub
                    Space_groupdat_ses = filter_rows_by_values(Space_groupdat_database, dat_sub_list, db_group_sessions[0])

                    #concatonate with other session in full database
                    Space_groupdat_database = pd.concat([Space_groupdat_database[Space_groupdat_database['ses'] != db_group_sessions[0]], Space_groupdat_ses],ignore_index=True)

            #add newly processed data
            Space_groupdat_database = Space_groupdat_database.append(Space_groupdat)

            #sort to ensure in sub order
            Space_groupdat_database = Space_groupdat_database.sort_values(by = ['sub', 'ses'])

            #round to 3 decimal points
            Space_groupdat_database = Space_groupdat_database.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)

            #write databases
            Space_groupdat_database.to_csv(str(Path(derivative_data_path).joinpath('task-space_groupdata.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

        else:
            print('No raw trial data files that need to be processed')
            Space_groupdat = np.nan

    return Space_database_wide, Space_database_blocks, Space_groupdat

* overwrite_flag : False


Execution Inputs
----------------


* Space_group_trialdat : ['no files']
* Space_summary_dat : ['no files']
* bids_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* function_str : def updateDatabase_save(Space_summary_dat, Space_group_trialdat, overwrite_flag, bids_dir):
    import pandas as pd
    import numpy as np
    from pathlib import Path
    from nipype.interfaces.base import Bunch

    #derivative data path
    derivative_data_path = Path(bids_dir).joinpath('derivatives/preprocessed/beh')

    #function to drop rows based on values
    def filter_rows_by_values(df, sub_values, sesnum):
        #filter based on sub and ses
        return df[(df['sub'].isin(sub_values) == False) & (df['ses'] == sesnum)]

    #### Summary Data ####
    #check to see if it is filepath str or 'no files' message
    if isinstance(Space_summary_dat[0], str):

        print('******** No new data to be processed ********')

        Space_database_wide = 'no new data files'
        Space_database_blocks = 'no new data files'

    else:
        #get a Bunch object if more than 1 participant
        if isinstance(Space_summary_dat, Bunch):
            #get output data from node
            Space_summary_datlist = Space_summary_dat.summarySpace_dat

            #combine datasets
            Space_summary_dat = pd.concat(Space_summary_datlist)

        #if only 1 participant/dataset then it is a list
        elif isinstance(Space_summary_dat, list):
            if len(Space_summary_dat) == 1:
                Space_summary_dat = Space_summary_dat[0]
            else:
                Space_summary_dat = pd.concat(Space_summary_dat)

        #if a pandas dataframe
        if isinstance(Space_summary_dat, pd.DataFrame):

            #get column names
            columnnames = Space_summary_dat.columns

            #get session subsets
            db_sessions = Space_summary_dat.ses.unique()

            if len(db_sessions) > 1:
                Space_sum_ses1_dat = Space_summary_dat.groupby('ses').get_group(1)
                Space_sum_ses2_dat = Space_summary_dat.groupby('ses').get_group(2)

                #make wide data set
                Space_sum_ses1_wide = Space_sum_ses1_dat.pivot(columns='block', index='sub', values=columnnames[3:16])
                Space_sum_ses1_wide.columns = ['_'.join(col) for col in Space_sum_ses1_wide.columns.reorder_levels(order=[1, 0])]

                Space_sum_ses2_wide = Space_sum_ses2_dat.pivot(columns='block', index='sub', values=columnnames[3:16])
                Space_sum_ses2_wide.columns = ['_'.join(col) for col in Space_sum_ses2_wide.columns.reorder_levels(order=[1, 0])]

                #make the sub index into a dataset column
                Space_sum_ses1_wide = Space_sum_ses1_wide.reset_index(level = 0)
                Space_sum_ses2_wide = Space_sum_ses2_wide.reset_index(level = 0)

                #add session
                Space_sum_ses1_wide.insert(1, 'ses', 1)
                Space_sum_ses2_wide.insert(1, 'ses', 2)

                #concatonate databases
                Space_summary_wide = pd.concat([Space_sum_ses1_wide,Space_sum_ses2_wide],ignore_index=True)

            else:
                #make wide data set
                Space_summary_wide = Space_summary_dat.pivot(columns='block', index='sub', values=columnnames[3:16])
                Space_summary_wide.columns = ['_'.join(col) for col in Space_summary_wide.columns.reorder_levels(order=[1, 0])]

                #make the sub index into a dataset column
                Space_summary_wide = Space_summary_wide.reset_index(level = 0)

                #add session
                Space_summary_wide.insert(1, 'ses', db_sessions[0])

            #re-order columns
            columnnames_reorder = ['sub', 'ses', 'all_earth_rt_mean', 'all_earth_rt_median', 'all_earth_n_miss', 'all_earth_p_miss', 'all_planet_rt_mean', 'all_planet_rt_median', 'all_planet_n_miss',  'all_planet_p_miss', 'all_reward_rate', 'all_avg_reward', 'all_reward_rate_corrected',  'all_prob_sameplanet_earthsame', 'all_prob_sameplanet_earthdif', 'b1_earth_rt_mean', 'b1_earth_rt_median', 'b1_earth_n_miss', 'b1_earth_p_miss', 'b1_planet_rt_mean', 'b1_planet_rt_median', 'b1_planet_n_miss', 'b1_planet_p_miss', 'b1_reward_rate', 'b1_avg_reward', 'b1_reward_rate_corrected', 'b1_prob_sameplanet_earthsame','b1_prob_sameplanet_earthdif', 'b2_earth_rt_mean', 'b2_earth_rt_median', 'b2_earth_n_miss', 'b2_earth_p_miss', 'b2_planet_rt_mean', 'b2_planet_rt_median', 'b2_planet_n_miss', 'b2_planet_p_miss', 'b2_reward_rate', 'b2_avg_reward', 'b2_reward_rate_corrected', 'b2_prob_sameplanet_earthsame', 'b2_prob_sameplanet_earthdif', 'b3_earth_rt_mean', 'b3_earth_rt_median', 'b3_earth_n_miss', 'b3_earth_p_miss', 'b3_planet_rt_mean','b3_planet_rt_median', 'b3_planet_n_miss', 'b3_planet_p_miss', 'b3_reward_rate', 'b3_avg_reward', 'b3_reward_rate_corrected', 'b3_prob_sameplanet_earthsame', 'b3_prob_sameplanet_earthdif', 'b4_earth_rt_mean', 'b4_earth_rt_median', 'b4_earth_n_miss', 'b4_earth_p_miss',  'b4_planet_rt_mean', 'b4_planet_rt_median', 'b4_planet_n_miss', 'b4_planet_p_miss',   'b4_reward_rate', 'b4_avg_reward', 'b4_reward_rate_corrected', 'b4_prob_sameplanet_earthsame', 'b4_prob_sameplanet_earthdif']

            Space_summary_wide = Space_summary_wide.reindex(columns=columnnames_reorder)

            #get blocks subset
            Space_summary_blocks = Space_summary_dat[Space_summary_dat.block.isin(['b1', 'b2', 'b3', 'b4'])]

            #load databases
            Space_database_wide = pd.read_csv(str(Path(derivative_data_path).joinpath('task-space_summary.tsv')), sep = '\t')
            Space_database_blocks = pd.read_csv(str(Path(derivative_data_path).joinpath('task-space_summary_long.tsv')), sep = '\t')

            #if overwriting participants
            if overwrite_flag == True:
                #filter out/remove exisiting subs to overwrit~
                if len(db_sessions) > 1:
                    #get list of subs by ses to filter in wide and long data
                    wide_sub_list = Space_summary_wide.groupby('ses')['sub'].unique()
                    long_sub_list = Space_summary_blocks.groupby('ses')['sub'].unique()

                    Space_database_ses1 = filter_rows_by_values(Space_database_wide, wide_sub_list[0], 1)
                    Space_database_ses2 = filter_rows_by_values(Space_database_wide, wide_sub_list[1], 2)

                    Space_database_ses1_long = filter_rows_by_values(Space_database_blocks, long_sub_list[0], 1)
                    Space_database_ses2_long = filter_rows_by_values(Space_database_blocks, long_sub_list[1], 2)

                    #concatonate databases
                    Space_database_wide = pd.concat([Space_database_ses1, Space_database_ses2],ignore_index=True)
                    Space_database_blocks = pd.concat([Space_database_ses1_long, Space_database_ses2_long],ignore_index=True)

                else:
                    wide_sub_list = list(Space_summary_wide['sub'].unique())
                    long_sub_list = list(Space_summary_blocks['sub'].unique())

                    #filter by ses and sub
                    Space_database_ses = filter_rows_by_values(Space_database_wide, wide_sub_list, db_sessions[0])
                    Space_database_long_ses = filter_rows_by_values(Space_database_blocks, long_sub_list, db_sessions[0])

                    #concatonate with other session in full database
                    Space_database_wide = pd.concat([Space_database_wide[Space_database_wide['ses'] != db_sessions[0]], Space_database_ses],ignore_index=True)
                    Space_database_blocks = pd.concat([Space_database_blocks[Space_database_blocks['ses'] != db_sessions[0]], Space_database_long_ses],ignore_index=True)


            #add newly processed data
            Space_database_wide = Space_database_wide.append(Space_summary_wide)
            Space_database_blocks = Space_database_blocks.append(Space_summary_blocks)

            #sort to ensure in sub order
            Space_database_wide = Space_database_wide.sort_values(by = ['ses', 'sub'])
            Space_database_blocks = Space_database_blocks.sort_values(by = ['ses', 'sub', 'block'])

            #round to 3 decimal points
            Space_database_wide = Space_database_wide.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)
            Space_database_blocks = Space_database_blocks.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)

            #write databases
            Space_database_wide.to_csv(str(Path(derivative_data_path).joinpath('task-space_summary.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
            Space_database_blocks.to_csv(str(Path(derivative_data_path).joinpath('task-space_summary_long.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

        else:
            print('No raw data files that need to be processed')
            Space_database_wide = np.nan
            Space_database_blocks = np.nan

    #### Group trial data ####
    if isinstance(Space_group_trialdat[0], str):

        print('******** No new data to be processed ********')

        Space_groupdat = 'no new data files'

    else:
        #get a Bunch object if more than 1 participant
        if isinstance(Space_group_trialdat, Bunch):
            #get output data from node
            Space_group_trialdatlist = Space_group_trialdat.group_trialdat

            #combine datasets
            Space_groupdat = pd.concat(Space_group_trialdatlist)

        #if only 1 participant/dataset then it is a list
        elif isinstance(Space_group_trialdat, list):
            if len(Space_group_trialdat) == 1:
                Space_groupdat = Space_group_trialdat[0]
            else:
                Space_groupdat = pd.concat(Space_group_trialdat)

        #if a pandas dataframe
        if isinstance(Space_groupdat, pd.DataFrame):

            #get session subsets
            db_group_sessions = Space_groupdat.ses.unique()

            #load databases
            Space_groupdat_database = pd.read_csv(str(Path(derivative_data_path).joinpath('task-space_groupdata.tsv')), sep = '\t')

            #if overwriting participants
            if overwrite_flag == True:
                #filter out/remove exisiting subs to overwrit~
                if len(db_group_sessions) > 1:
                    #get list of subs by ses to filter in wide and long data
                    dat_sub_list = Space_groupdat.groupby('ses')['sub'].unique()

                    Space_groupdat_ses1 = filter_rows_by_values(Space_groupdat_database, dat_sub_list[0], 1)
                    Space_groupdat_ses2 = filter_rows_by_values(Space_groupdat_database, dat_sub_list[1], 2)

                    #concatonate databases
                    Space_groupdat_database = pd.concat([Space_groupdat_ses1, Space_groupdat_ses2],ignore_index=True)

                else:
                    dat_sub_list = list(Space_groupdat['sub'].unique())

                    #filter by ses and sub
                    Space_groupdat_ses = filter_rows_by_values(Space_groupdat_database, dat_sub_list, db_group_sessions[0])

                    #concatonate with other session in full database
                    Space_groupdat_database = pd.concat([Space_groupdat_database[Space_groupdat_database['ses'] != db_group_sessions[0]], Space_groupdat_ses],ignore_index=True)

            #add newly processed data
            Space_groupdat_database = Space_groupdat_database.append(Space_groupdat)

            #sort to ensure in sub order
            Space_groupdat_database = Space_groupdat_database.sort_values(by = ['sub', 'ses'])

            #round to 3 decimal points
            Space_groupdat_database = Space_groupdat_database.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)

            #write databases
            Space_groupdat_database.to_csv(str(Path(derivative_data_path).joinpath('task-space_groupdata.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

        else:
            print('No raw trial data files that need to be processed')
            Space_groupdat = np.nan

    return Space_database_wide, Space_database_blocks, Space_groupdat

* overwrite_flag : False


Execution Outputs
-----------------


* Space_database_blocks : no new data files
* Space_database_cond : no new data files
* Space_grouptrial_database : no new data files


Runtime info
------------


* duration : 0.008872
* hostname : nut-azp271-10239
* prev_wd : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* working_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/SpaceGame/_session_id_2/spaceDatabase


Environment
~~~~~~~~~~~


* CLICOLOR : 1
* CONDA_DEFAULT_ENV : base
* CONDA_EXE : /Users/azp271/opt/anaconda3/bin/conda
* CONDA_PREFIX : /Users/azp271/opt/anaconda3
* CONDA_PROMPT_MODIFIER : (base) 
* CONDA_PYTHON_EXE : /Users/azp271/opt/anaconda3/bin/python
* CONDA_SHLVL : 1
* DISPLAY : /private/tmp/com.apple.launchd.1mdV9E7QdF/org.xquartz:0
* DYLD_LIBRARY_PATH : /Applications/freesurfer/lib/gcc/lib::/opt/X11/lib/flat_namespace
* FIX_VERTEX_AREA : 
* FMRI_ANALYSIS_DIR : /Applications/freesurfer/fsfast
* FREESURFER_HOME : /Applications/freesurfer
* FSFAST_HOME : /Applications/freesurfer/fsfast
* FSF_OUTPUT_FORMAT : nii.gz
* FSLDIR : /usr/local/fsl
* FSLGECUDAQ : cuda.q
* FSLLOCKDIR : 
* FSLMACHINELIST : 
* FSLMULTIFILEQUIT : TRUE
* FSLOUTPUTTYPE : NIFTI_GZ
* FSLREMOTECALL : 
* FSLTCLSH : /usr/local/fsl/bin/fsltclsh
* FSLWISH : /usr/local/fsl/bin/fslwish
* FSL_BIN : /usr/local/fsl/bin
* FSL_DIR : /usr/local/fsl
* FS_OVERRIDE : 0
* FUNCTIONALS_DIR : /Applications/freesurfer/sessions
* HOME : /Users/azp271
* LANG : en_US.UTF-8
* LOCAL_DIR : /Applications/freesurfer/local
* LOGNAME : azp271
* LSCOLORS : ExFxBxDxCxegedabagacad
* MINC_BIN_DIR : /Applications/freesurfer/mni/bin
* MINC_LIB_DIR : /Applications/freesurfer/mni/lib
* MNI_DATAPATH : /Applications/freesurfer/mni/data
* MNI_DIR : /Applications/freesurfer/mni
* MNI_PERL5LIB : /Applications/freesurfer/mni/lib/../Library/Perl/Updates/5.12.3
* OLDPWD : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/orgRaw_scripts
* OS : Darwin
* PATH : /Users/azp271/opt/anaconda3/bin:/Users/azp271/opt/anaconda3/condabin:/Applications/freesurfer/bin:/Applications/freesurfer/fsfast/bin:/Applications/freesurfer/tktools:/usr/local/fsl/bin:/Applications/freesurfer/mni/bin:/usr/local/fsl/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/TeX/texbin:/opt/X11/bin:/Library/Apple/usr/bin:/Users/azp271/abin:/Applications/CMake.app/Contents/bin/:/Users/azp271/dcm2niix/build/bin/:/Users/azp271/.local/bin:/Users/azp271/pigz-2.6/
* PERL5LIB : /Applications/freesurfer/mni/lib/../Library/Perl/Updates/5.12.3
* PS1 : (base) \[\033[36m\]\u\[\033[m\]@\[\033[32m\]\h:\[\033[33;1m\]\w\[\033[m\]$ 
* PWD : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code
* SHELL : /bin/bash
* SHLVL : 1
* SSH_AUTH_SOCK : /private/tmp/com.apple.launchd.Eua71eiyFT/Listeners
* SUBJECTS_DIR : /Applications/freesurfer/subjects
* TERM : xterm-256color
* TERM_PROGRAM : Apple_Terminal
* TERM_PROGRAM_VERSION : 433
* TERM_SESSION_ID : 5D558CB1-2FBB-498C-9075-455C5F6CB8AA
* TMPDIR : /var/folders/3c/pvrbw1ld5290z020487lf9340000gp/T/
* USER : azp271
* XPC_FLAGS : 0x0
* XPC_SERVICE_NAME : 0
* _ : /Users/azp271/opt/anaconda3/bin/python3
* _CE_CONDA : 
* _CE_M : 

