Node: concatBlocksLong (utility)
================================


 Hierarchy : Nback.concatBlocksLong
 Exec ID : concatBlocksLong.a1


Original Inputs
---------------


* bids_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* block_sumDat : [array([['28', '2', 'b0', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '506.0', '488.0'],
       ['28', '2', 'b1', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '549.5', '534.5'],
       ['28', '2', 'b2', '16', '44', '60', '58', '96.66666666666667',
        '14', '87.5', '2', '12.5', '44', '100.0', '0', '0.0', '93.75',
        '673.6428571428571', '689.5']], dtype='<U32'), array([['22', '2', 'b0', '16', '44', '60', '59', '98.33333333333333',
        '15', '93.75', '1', '6.25', '44', '100.0', '0', '0.0', '96.875',
        '717.6666666666666', '673.0'],
       ['22', '2', 'b1', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '817.3125',
        '824.0'],
       ['22', '2', 'b2', '16', '44', '60', '53', '88.33333333333333',
        '11', '68.75', '5', '31.25', '42', '95.45454545454545', '2',
        '4.545454545454546', '82.10227272727272', '837.2727272727273',
        '699.0']], dtype='<U32'), array([['7', '2', 'b0', '16', '44', '60', '59', '98.33333333333333',
        '16', '100.0', '0', '0.0', '43', '97.72727272727273', '1',
        '2.272727272727273', '98.86363636363637', '737.875', '690.5'],
       ['7', '2', 'b1', '16', '44', '60', '58', '96.66666666666667',
        '15', '93.75', '1', '6.25', '43', '97.72727272727273', '1',
        '2.272727272727273', '95.73863636363637', '670.0666666666667',
        '631.0'],
       ['7', '2', 'b2', '16', '44', '60', '50', '83.33333333333334',
        '15', '93.75', '1', '6.25', '35', '79.54545454545455', '9',
        '20.454545454545457', '86.64772727272728', '1145.2', '1001.0']],
      dtype='<U32'), array([['26', '2', 'b0', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '733.25',
        '748.0'],
       ['26', '2', 'b1', '16', '44', '60', '58', '96.66666666666667',
        '15', '93.75', '1', '6.25', '43', '97.72727272727273', '1',
        '2.272727272727273', '95.73863636363637', '828.3333333333334',
        '769.0'],
       ['26', '2', 'b2', '16', '44', '60', '55', '91.66666666666666',
        '12', '75.0', '4', '25.0', '43', '97.72727272727273', '1',
        '2.272727272727273', '86.36363636363637', '933.4166666666666',
        '1009.0']], dtype='<U32'), array([['6', '2', 'b0', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '490.375',
        '461.0'],
       ['6', '2', 'b1', '16', '44', '60', '59', '98.33333333333333',
        '16', '100.0', '0', '0.0', '43', '97.72727272727273', '1',
        '2.272727272727273', '98.86363636363637', '655.1875', '648.0']],
      dtype='<U32'), array([['5', '2', 'b0', '16', '44', '60', '59', '98.33333333333333',
        '16', '100.0', '0', '0.0', '43', '97.72727272727273', '1',
        '2.272727272727273', '98.86363636363637', '554.4375', '562.0'],
       ['5', '2', 'b1', '16', '44', '60', '58', '96.66666666666667',
        '16', '100.0', '0', '0.0', '42', '95.45454545454545', '2',
        '4.545454545454546', '97.72727272727272', '782.25', '754.5'],
       ['5', '2', 'b2', '16', '44', '60', '58', '96.66666666666667',
        '15', '93.75', '1', '6.25', '43', '97.72727272727273', '1',
        '2.272727272727273', '95.73863636363637', '1008.8', '974.0']],
      dtype='<U32'), array([['2', '2', 'b0', '16', '44', '60', '59', '98.33333333333333',
        '15', '93.75', '1', '6.25', '44', '100.0', '0', '0.0', '96.875',
        '642.2', '620.0'],
       ['2', '2', 'b1', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '690.125',
        '768.0'],
       ['2', '2', 'b2', '16', '44', '60', '51', '85.0', '10', '62.5',
        '6', '37.5', '41', '93.18181818181817', '3',
        '6.8181818181818175', '77.8409090909091', '829.2', '676.0']],
      dtype='<U32'), array([['23', '2', 'b0', '16', '44', '60', '59', '98.33333333333333',
        '15', '93.75', '1', '6.25', '44', '100.0', '0', '0.0', '96.875',
        '1002.0', '981.0'],
       ['23', '2', 'b1', '16', '44', '60', '58', '96.66666666666667',
        '14', '87.5', '2', '12.5', '44', '100.0', '0', '0.0', '93.75',
        '831.2857142857143', '858.0'],
       ['23', '2', 'b2', '16', '44', '60', '52', '86.66666666666667',
        '14', '87.5', '2', '12.5', '38', '86.36363636363636', '6',
        '13.636363636363635', '86.93181818181819', '1001.9285714285714',
        '968.5']], dtype='<U32'), array([['37', '2', 'b0', '16', '44', '60', '58', '96.66666666666667',
        '16', '100.0', '0', '0.0', '42', '95.45454545454545', '2',
        '4.545454545454546', '97.72727272727272', '725.1875', '722.5'],
       ['37', '2', 'b1', '16', '44', '60', '59', '98.33333333333333',
        '15', '93.75', '1', '6.25', '44', '100.0', '0', '0.0', '96.875',
        '810.0', '756.0'],
       ['37', '2', 'b2', '16', '44', '60', '44', '73.33333333333333',
        '11', '68.75', '5', '31.25', '33', '75.0', '11', '25.0',
        '71.875', '822.0909090909091', '863.0']], dtype='<U32'), array([['18', '2', 'b0', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '589.0625',
        '573.0'],
       ['18', '2', 'b1', '16', '44', '60', '57', '95.0', '15', '93.75',
        '1', '6.25', '42', '95.45454545454545', '2', '4.545454545454546',
        '94.60227272727272', '614.6666666666666', '568.0'],
       ['18', '2', 'b2', '16', '44', '60', '59', '98.33333333333333',
        '15', '93.75', '1', '6.25', '44', '100.0', '0', '0.0', '96.875',
        '619.7333333333333', '547.0']], dtype='<U32'), array([['3', '2', 'b0', '16', '44', '60', '59', '98.33333333333333',
        '16', '100.0', '0', '0.0', '43', '97.72727272727273', '1',
        '2.272727272727273', '98.86363636363637', '582.6875', '586.5'],
       ['3', '2', 'b1', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '625.9375',
        '570.5'],
       ['3', '2', 'b2', '16', '44', '60', '56', '93.33333333333333',
        '15', '93.75', '1', '6.25', '41', '93.18181818181817', '3',
        '6.8181818181818175', '93.4659090909091', '812.0', '798.0']],
      dtype='<U32'), array([['40', '2', 'b0', '16', '44', '60', '58', '96.66666666666667',
        '16', '100.0', '0', '0.0', '42', '95.45454545454545', '2',
        '4.545454545454546', '97.72727272727272', '535.375', '510.0'],
       ['40', '2', 'b1', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '543.3125',
        '535.0'],
       ['40', '2', 'b2', '16', '44', '60', '56', '93.33333333333333',
        '12', '75.0', '4', '25.0', '44', '100.0', '0', '0.0', '87.5',
        '621.6666666666666', '546.0']], dtype='<U32'), array([['35', '2', 'b0', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '656.375',
        '638.0'],
       ['35', '2', 'b1', '16', '44', '60', '57', '95.0', '13', '81.25',
        '3', '18.75', '44', '100.0', '0', '0.0', '90.625',
        '888.3076923076923', '875.0'],
       ['35', '2', 'b2', '16', '44', '60', '54', '90.0', '10', '62.5',
        '6', '37.5', '44', '100.0', '0', '0.0', '81.25', '968.6',
        '934.5']], dtype='<U32'), array([['11', '2', 'b0', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '462.875',
        '446.5'],
       ['11', '2', 'b1', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '545.875',
        '493.0'],
       ['11', '2', 'b2', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '541.0625',
        '559.0']], dtype='<U32')]
* function_str : def updateDatabase_save(block_sumDat, overwrite_flag, bids_dir):
    import numpy as np
    import pandas as pd
    from pathlib import Path
    from nipype.interfaces.base import Bunch

    #get a Bunch object if more than 1 participant 
    if isinstance(block_sumDat, Bunch):        
        #get output data from node
        np_allBlockDat = block_sumDat.summaryNback_dat

    #if only 1 participant/dataset then it is a list    
    elif isinstance(block_sumDat, list):
        if len(block_sumDat) == 1:
            np_allBlockDat = block_sumDat[0]
        else:
            np_allBlockDat = block_sumDat

    #convert np subarrays to pandas
    def np2pds(t):
        return [pd.DataFrame(sublist) for sublist in t]

    pandas_allBlockDat = np2pds(np_allBlockDat)

    #combine datasets 
    allBlockDat = pd.concat(pandas_allBlockDat)

    #if a pandas dataframe
    if isinstance(allBlockDat, pd.DataFrame):
        col_names = ['sub', 'ses', 'block','n_targets', 'n_fill', 'n_trials', 'n_acc', 'p_acc', 'n_target_hit', 'p_target_hit', 'n_target_miss', 'p_target_miss', 'n_fill_corr', 'p_fill_corr', 'n_fill_fa', 'p_fill_fa', 'p_target_ba', 'rt_mean_target_hit', 'rt_med_target_hit']
        allBlockDat.columns = col_names
        allBlockDat = pd.DataFrame(allBlockDat).convert_dtypes()
        allBlockDat = allBlockDat.reset_index(drop = True)    

        #set numeric columns to dtype numeric
        num_cols = allBlockDat.loc[:, allBlockDat.columns != 'block'].apply(pd.to_numeric).round(3)

        #replace in orig dataset
        allBlockDat.loc[:, num_cols.columns] = num_cols

        #get session subsets
        db_sessions = allBlockDat.ses.unique()

        #make wide data set 
        if len(db_sessions) > 1:
            allBlockDat_ses1_dat = allBlockDat.groupby('ses').get_group(1)
            allBlockDat_ses2_dat = allBlockDat.groupby('ses').get_group(2)

            #make wide data set 
            allBlockDat_ses1_wide = allBlockDat_ses1_dat.pivot(columns='block', index='sub', values=col_names[3:19])
            allBlockDat_ses1_wide.columns = ['_'.join(col) for col in allBlockDat_ses1_wide.columns.reorder_levels(order=[1, 0])]

            allBlockDat_ses2_wide = allBlockDat_ses2_dat.pivot(columns='block', index='sub', values=col_names[3:19])
            allBlockDat_ses2_wide.columns = ['_'.join(col) for col in allBlockDat_ses2_wide.columns.reorder_levels(order=[1, 0])]

            #make the sub index into a dataset column
            allBlockDat_ses1_wide = allBlockDat_ses1_wide.reset_index(level = 0)
            allBlockDat_ses2_wide = allBlockDat_ses2_wide.reset_index(level = 0)

            #add session
            allBlockDat_ses1_wide.insert(1, 'ses', 1)
            allBlockDat_ses1_wide.insert(1, 'ses', 2)


            #concatonate databases
            allBlockDat_wide = pd.concat([allBlockDat_ses1_wide, allBlockDat_ses2_wide],ignore_index=True)

        else:
            #make wide data set 
            allBlockDat_wide = allBlockDat.pivot(columns='block', index='sub', values = col_names[3:19])        
            allBlockDat_wide.columns = ['_'.join(col) for col in allBlockDat_wide.columns.reorder_levels(order=[1, 0])]

            #make the sub index into a dataset column
            allBlockDat_wide = allBlockDat_wide.reset_index(level = 0)

            #add session
            allBlockDat_wide.insert(1, 'ses', db_sessions[0])

        #re-order columns
        columnnames_reorder = ['sub', 'ses', 
         'b0_n_targets', 'b0_n_fill', 'b0_n_trials', 'b0_n_acc','b0_p_acc',
         'b0_n_target_hit','b0_p_target_hit', 'b0_n_target_miss',
         'b0_p_target_miss','b0_n_fill_corr','b0_p_fill_corr',
         'b0_n_fill_fa', 'b0_p_fill_fa','b0_p_target_ba',
         'b0_rt_mean_target_hit','b0_rt_med_target_hit',
         'b1_n_targets', 'b1_n_fill', 'b1_n_trials', 'b1_n_acc','b1_p_acc',
         'b1_n_target_hit','b1_p_target_hit','b1_n_target_miss',
         'b1_p_target_miss', 'b1_n_fill_corr','b1_p_fill_corr',
         'b1_n_fill_fa','b1_p_fill_fa','b1_p_target_ba',
         'b1_rt_mean_target_hit','b1_rt_med_target_hit',
         'b2_n_targets', 'b2_n_fill', 'b2_n_trials', 'b2_n_acc','b2_p_acc',
         'b2_n_target_hit','b2_p_target_hit', 'b2_n_target_miss',
         'b2_p_target_miss','b2_n_fill_corr','b2_p_fill_corr',
         'b2_n_fill_fa','b2_p_fill_fa','b2_p_target_ba',
         'b2_rt_mean_target_hit','b2_rt_med_target_hit']

        allBlockDat_wide = allBlockDat_wide.reindex(columns=columnnames_reorder)

        ## load databases
        #derivative data path
        derivative_data_path = Path(bids_dir).joinpath('derivatives/preprocessed/beh')

        #load databases
        Nback_database = pd.read_csv(str(Path(derivative_data_path).joinpath('task-nback_summary.tsv')), sep = '\t') 
        Nback_database_long = pd.read_csv(str(Path(derivative_data_path).joinpath('task-nback_summary_long.tsv')), sep = '\t')

        #if overwriting participants
        if overwrite_flag == True:
            #function to drop rows based on values
            def filter_rows_by_values(df, sub_values, sesnum):
                #fileter based on sub and ses
                return df[(df['sub'].isin(sub_values) == False) & (df['ses'] == sesnum)]

            #filter out/remove exisiting subs to overwrit~
            if len(db_sessions) > 1:
                #get list of subs by ses to filter in wide and long data
                wide_sub_list = allBlockDat_wide.groupby('ses')['sub'].unique()
                long_sub_list = allBlockDat.groupby('ses')['sub'].unique()

                Nback_database_ses1 = filter_rows_by_values(Nback_database, wide_sub_list[0], 1)
                Nback_database_ses2 = filter_rows_by_values(Nback_database, wide_sub_list[1], 2)

                Nback_database_ses1_long = filter_rows_by_values(Nback_database_long, long_sub_list[0], 1)
                Nback_database_ses2_long = filter_rows_by_values(Nback_database_long, long_sub_list[1], 2)

                #concatonate databases
                Nback_database = pd.concat([Nback_database_ses1, Nback_database_ses2],ignore_index=True)
                Nback_database_long = pd.concat([Nback_database_ses1_long, Nback_database_ses2_long],ignore_index=True)

            else:
                wide_sub_list = list(allBlockDat_wide['sub'].unique())
                long_sub_list = list(allBlockDat['sub'].unique())

                #filter by ses and sub
                Nback_database_ses = filter_rows_by_values(Nback_database, wide_sub_list, db_sessions[0])
                Nback_database_long_ses = filter_rows_by_values(Nback_database_long, long_sub_list, db_sessions[0])

                #concatonate with other session in full database
                Nback_database = pd.concat([Nback_database[Nback_database['ses'] != db_sessions[0]], Nback_database_ses],ignore_index=True)
                Nback_database_long = pd.concat([Nback_database_long[Nback_database_long['ses'] != db_sessions[0]], Nback_database_long_ses],ignore_index=True)

        #add newly processed data
        Nback_database = Nback_database.append(allBlockDat_wide)
        Nback_database_long = Nback_database_long.append(allBlockDat)

        #sort to ensure in sub order
        Nback_database = Nback_database.sort_values(by = ['ses', 'sub'])
        Nback_database_long = Nback_database_long.sort_values(by = ['ses', 'sub', 'block'])

        #round to 3 decimal points
        Nback_database = Nback_database.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)
        Nback_database_long = Nback_database_long.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)

        #write databases
        Nback_database.to_csv(str(Path(derivative_data_path).joinpath('task-nback_summary.tsv')), sep = '\t', encoding='utf-8-sig', index = False) 
        Nback_database_long.to_csv(str(Path(derivative_data_path).joinpath('task-nback_summary_long.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

        return Nback_database, Nback_database_long

* overwrite_flag : True


Execution Inputs
----------------


* bids_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* block_sumDat : [array([['28', '2', 'b0', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '506.0', '488.0'],
       ['28', '2', 'b1', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '549.5', '534.5'],
       ['28', '2', 'b2', '16', '44', '60', '58', '96.66666666666667',
        '14', '87.5', '2', '12.5', '44', '100.0', '0', '0.0', '93.75',
        '673.6428571428571', '689.5']], dtype='<U32'), array([['22', '2', 'b0', '16', '44', '60', '59', '98.33333333333333',
        '15', '93.75', '1', '6.25', '44', '100.0', '0', '0.0', '96.875',
        '717.6666666666666', '673.0'],
       ['22', '2', 'b1', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '817.3125',
        '824.0'],
       ['22', '2', 'b2', '16', '44', '60', '53', '88.33333333333333',
        '11', '68.75', '5', '31.25', '42', '95.45454545454545', '2',
        '4.545454545454546', '82.10227272727272', '837.2727272727273',
        '699.0']], dtype='<U32'), array([['7', '2', 'b0', '16', '44', '60', '59', '98.33333333333333',
        '16', '100.0', '0', '0.0', '43', '97.72727272727273', '1',
        '2.272727272727273', '98.86363636363637', '737.875', '690.5'],
       ['7', '2', 'b1', '16', '44', '60', '58', '96.66666666666667',
        '15', '93.75', '1', '6.25', '43', '97.72727272727273', '1',
        '2.272727272727273', '95.73863636363637', '670.0666666666667',
        '631.0'],
       ['7', '2', 'b2', '16', '44', '60', '50', '83.33333333333334',
        '15', '93.75', '1', '6.25', '35', '79.54545454545455', '9',
        '20.454545454545457', '86.64772727272728', '1145.2', '1001.0']],
      dtype='<U32'), array([['26', '2', 'b0', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '733.25',
        '748.0'],
       ['26', '2', 'b1', '16', '44', '60', '58', '96.66666666666667',
        '15', '93.75', '1', '6.25', '43', '97.72727272727273', '1',
        '2.272727272727273', '95.73863636363637', '828.3333333333334',
        '769.0'],
       ['26', '2', 'b2', '16', '44', '60', '55', '91.66666666666666',
        '12', '75.0', '4', '25.0', '43', '97.72727272727273', '1',
        '2.272727272727273', '86.36363636363637', '933.4166666666666',
        '1009.0']], dtype='<U32'), array([['6', '2', 'b0', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '490.375',
        '461.0'],
       ['6', '2', 'b1', '16', '44', '60', '59', '98.33333333333333',
        '16', '100.0', '0', '0.0', '43', '97.72727272727273', '1',
        '2.272727272727273', '98.86363636363637', '655.1875', '648.0']],
      dtype='<U32'), array([['5', '2', 'b0', '16', '44', '60', '59', '98.33333333333333',
        '16', '100.0', '0', '0.0', '43', '97.72727272727273', '1',
        '2.272727272727273', '98.86363636363637', '554.4375', '562.0'],
       ['5', '2', 'b1', '16', '44', '60', '58', '96.66666666666667',
        '16', '100.0', '0', '0.0', '42', '95.45454545454545', '2',
        '4.545454545454546', '97.72727272727272', '782.25', '754.5'],
       ['5', '2', 'b2', '16', '44', '60', '58', '96.66666666666667',
        '15', '93.75', '1', '6.25', '43', '97.72727272727273', '1',
        '2.272727272727273', '95.73863636363637', '1008.8', '974.0']],
      dtype='<U32'), array([['2', '2', 'b0', '16', '44', '60', '59', '98.33333333333333',
        '15', '93.75', '1', '6.25', '44', '100.0', '0', '0.0', '96.875',
        '642.2', '620.0'],
       ['2', '2', 'b1', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '690.125',
        '768.0'],
       ['2', '2', 'b2', '16', '44', '60', '51', '85.0', '10', '62.5',
        '6', '37.5', '41', '93.18181818181817', '3',
        '6.8181818181818175', '77.8409090909091', '829.2', '676.0']],
      dtype='<U32'), array([['23', '2', 'b0', '16', '44', '60', '59', '98.33333333333333',
        '15', '93.75', '1', '6.25', '44', '100.0', '0', '0.0', '96.875',
        '1002.0', '981.0'],
       ['23', '2', 'b1', '16', '44', '60', '58', '96.66666666666667',
        '14', '87.5', '2', '12.5', '44', '100.0', '0', '0.0', '93.75',
        '831.2857142857143', '858.0'],
       ['23', '2', 'b2', '16', '44', '60', '52', '86.66666666666667',
        '14', '87.5', '2', '12.5', '38', '86.36363636363636', '6',
        '13.636363636363635', '86.93181818181819', '1001.9285714285714',
        '968.5']], dtype='<U32'), array([['37', '2', 'b0', '16', '44', '60', '58', '96.66666666666667',
        '16', '100.0', '0', '0.0', '42', '95.45454545454545', '2',
        '4.545454545454546', '97.72727272727272', '725.1875', '722.5'],
       ['37', '2', 'b1', '16', '44', '60', '59', '98.33333333333333',
        '15', '93.75', '1', '6.25', '44', '100.0', '0', '0.0', '96.875',
        '810.0', '756.0'],
       ['37', '2', 'b2', '16', '44', '60', '44', '73.33333333333333',
        '11', '68.75', '5', '31.25', '33', '75.0', '11', '25.0',
        '71.875', '822.0909090909091', '863.0']], dtype='<U32'), array([['18', '2', 'b0', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '589.0625',
        '573.0'],
       ['18', '2', 'b1', '16', '44', '60', '57', '95.0', '15', '93.75',
        '1', '6.25', '42', '95.45454545454545', '2', '4.545454545454546',
        '94.60227272727272', '614.6666666666666', '568.0'],
       ['18', '2', 'b2', '16', '44', '60', '59', '98.33333333333333',
        '15', '93.75', '1', '6.25', '44', '100.0', '0', '0.0', '96.875',
        '619.7333333333333', '547.0']], dtype='<U32'), array([['3', '2', 'b0', '16', '44', '60', '59', '98.33333333333333',
        '16', '100.0', '0', '0.0', '43', '97.72727272727273', '1',
        '2.272727272727273', '98.86363636363637', '582.6875', '586.5'],
       ['3', '2', 'b1', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '625.9375',
        '570.5'],
       ['3', '2', 'b2', '16', '44', '60', '56', '93.33333333333333',
        '15', '93.75', '1', '6.25', '41', '93.18181818181817', '3',
        '6.8181818181818175', '93.4659090909091', '812.0', '798.0']],
      dtype='<U32'), array([['40', '2', 'b0', '16', '44', '60', '58', '96.66666666666667',
        '16', '100.0', '0', '0.0', '42', '95.45454545454545', '2',
        '4.545454545454546', '97.72727272727272', '535.375', '510.0'],
       ['40', '2', 'b1', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '543.3125',
        '535.0'],
       ['40', '2', 'b2', '16', '44', '60', '56', '93.33333333333333',
        '12', '75.0', '4', '25.0', '44', '100.0', '0', '0.0', '87.5',
        '621.6666666666666', '546.0']], dtype='<U32'), array([['35', '2', 'b0', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '656.375',
        '638.0'],
       ['35', '2', 'b1', '16', '44', '60', '57', '95.0', '13', '81.25',
        '3', '18.75', '44', '100.0', '0', '0.0', '90.625',
        '888.3076923076923', '875.0'],
       ['35', '2', 'b2', '16', '44', '60', '54', '90.0', '10', '62.5',
        '6', '37.5', '44', '100.0', '0', '0.0', '81.25', '968.6',
        '934.5']], dtype='<U32'), array([['11', '2', 'b0', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '462.875',
        '446.5'],
       ['11', '2', 'b1', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '545.875',
        '493.0'],
       ['11', '2', 'b2', '16', '44', '60', '60', '100.0', '16', '100.0',
        '0', '0.0', '44', '100.0', '0', '0.0', '100.0', '541.0625',
        '559.0']], dtype='<U32')]
* function_str : def updateDatabase_save(block_sumDat, overwrite_flag, bids_dir):
    import numpy as np
    import pandas as pd
    from pathlib import Path
    from nipype.interfaces.base import Bunch

    #get a Bunch object if more than 1 participant 
    if isinstance(block_sumDat, Bunch):        
        #get output data from node
        np_allBlockDat = block_sumDat.summaryNback_dat

    #if only 1 participant/dataset then it is a list    
    elif isinstance(block_sumDat, list):
        if len(block_sumDat) == 1:
            np_allBlockDat = block_sumDat[0]
        else:
            np_allBlockDat = block_sumDat

    #convert np subarrays to pandas
    def np2pds(t):
        return [pd.DataFrame(sublist) for sublist in t]

    pandas_allBlockDat = np2pds(np_allBlockDat)

    #combine datasets 
    allBlockDat = pd.concat(pandas_allBlockDat)

    #if a pandas dataframe
    if isinstance(allBlockDat, pd.DataFrame):
        col_names = ['sub', 'ses', 'block','n_targets', 'n_fill', 'n_trials', 'n_acc', 'p_acc', 'n_target_hit', 'p_target_hit', 'n_target_miss', 'p_target_miss', 'n_fill_corr', 'p_fill_corr', 'n_fill_fa', 'p_fill_fa', 'p_target_ba', 'rt_mean_target_hit', 'rt_med_target_hit']
        allBlockDat.columns = col_names
        allBlockDat = pd.DataFrame(allBlockDat).convert_dtypes()
        allBlockDat = allBlockDat.reset_index(drop = True)    

        #set numeric columns to dtype numeric
        num_cols = allBlockDat.loc[:, allBlockDat.columns != 'block'].apply(pd.to_numeric).round(3)

        #replace in orig dataset
        allBlockDat.loc[:, num_cols.columns] = num_cols

        #get session subsets
        db_sessions = allBlockDat.ses.unique()

        #make wide data set 
        if len(db_sessions) > 1:
            allBlockDat_ses1_dat = allBlockDat.groupby('ses').get_group(1)
            allBlockDat_ses2_dat = allBlockDat.groupby('ses').get_group(2)

            #make wide data set 
            allBlockDat_ses1_wide = allBlockDat_ses1_dat.pivot(columns='block', index='sub', values=col_names[3:19])
            allBlockDat_ses1_wide.columns = ['_'.join(col) for col in allBlockDat_ses1_wide.columns.reorder_levels(order=[1, 0])]

            allBlockDat_ses2_wide = allBlockDat_ses2_dat.pivot(columns='block', index='sub', values=col_names[3:19])
            allBlockDat_ses2_wide.columns = ['_'.join(col) for col in allBlockDat_ses2_wide.columns.reorder_levels(order=[1, 0])]

            #make the sub index into a dataset column
            allBlockDat_ses1_wide = allBlockDat_ses1_wide.reset_index(level = 0)
            allBlockDat_ses2_wide = allBlockDat_ses2_wide.reset_index(level = 0)

            #add session
            allBlockDat_ses1_wide.insert(1, 'ses', 1)
            allBlockDat_ses1_wide.insert(1, 'ses', 2)


            #concatonate databases
            allBlockDat_wide = pd.concat([allBlockDat_ses1_wide, allBlockDat_ses2_wide],ignore_index=True)

        else:
            #make wide data set 
            allBlockDat_wide = allBlockDat.pivot(columns='block', index='sub', values = col_names[3:19])        
            allBlockDat_wide.columns = ['_'.join(col) for col in allBlockDat_wide.columns.reorder_levels(order=[1, 0])]

            #make the sub index into a dataset column
            allBlockDat_wide = allBlockDat_wide.reset_index(level = 0)

            #add session
            allBlockDat_wide.insert(1, 'ses', db_sessions[0])

        #re-order columns
        columnnames_reorder = ['sub', 'ses', 
         'b0_n_targets', 'b0_n_fill', 'b0_n_trials', 'b0_n_acc','b0_p_acc',
         'b0_n_target_hit','b0_p_target_hit', 'b0_n_target_miss',
         'b0_p_target_miss','b0_n_fill_corr','b0_p_fill_corr',
         'b0_n_fill_fa', 'b0_p_fill_fa','b0_p_target_ba',
         'b0_rt_mean_target_hit','b0_rt_med_target_hit',
         'b1_n_targets', 'b1_n_fill', 'b1_n_trials', 'b1_n_acc','b1_p_acc',
         'b1_n_target_hit','b1_p_target_hit','b1_n_target_miss',
         'b1_p_target_miss', 'b1_n_fill_corr','b1_p_fill_corr',
         'b1_n_fill_fa','b1_p_fill_fa','b1_p_target_ba',
         'b1_rt_mean_target_hit','b1_rt_med_target_hit',
         'b2_n_targets', 'b2_n_fill', 'b2_n_trials', 'b2_n_acc','b2_p_acc',
         'b2_n_target_hit','b2_p_target_hit', 'b2_n_target_miss',
         'b2_p_target_miss','b2_n_fill_corr','b2_p_fill_corr',
         'b2_n_fill_fa','b2_p_fill_fa','b2_p_target_ba',
         'b2_rt_mean_target_hit','b2_rt_med_target_hit']

        allBlockDat_wide = allBlockDat_wide.reindex(columns=columnnames_reorder)

        ## load databases
        #derivative data path
        derivative_data_path = Path(bids_dir).joinpath('derivatives/preprocessed/beh')

        #load databases
        Nback_database = pd.read_csv(str(Path(derivative_data_path).joinpath('task-nback_summary.tsv')), sep = '\t') 
        Nback_database_long = pd.read_csv(str(Path(derivative_data_path).joinpath('task-nback_summary_long.tsv')), sep = '\t')

        #if overwriting participants
        if overwrite_flag == True:
            #function to drop rows based on values
            def filter_rows_by_values(df, sub_values, sesnum):
                #fileter based on sub and ses
                return df[(df['sub'].isin(sub_values) == False) & (df['ses'] == sesnum)]

            #filter out/remove exisiting subs to overwrit~
            if len(db_sessions) > 1:
                #get list of subs by ses to filter in wide and long data
                wide_sub_list = allBlockDat_wide.groupby('ses')['sub'].unique()
                long_sub_list = allBlockDat.groupby('ses')['sub'].unique()

                Nback_database_ses1 = filter_rows_by_values(Nback_database, wide_sub_list[0], 1)
                Nback_database_ses2 = filter_rows_by_values(Nback_database, wide_sub_list[1], 2)

                Nback_database_ses1_long = filter_rows_by_values(Nback_database_long, long_sub_list[0], 1)
                Nback_database_ses2_long = filter_rows_by_values(Nback_database_long, long_sub_list[1], 2)

                #concatonate databases
                Nback_database = pd.concat([Nback_database_ses1, Nback_database_ses2],ignore_index=True)
                Nback_database_long = pd.concat([Nback_database_ses1_long, Nback_database_ses2_long],ignore_index=True)

            else:
                wide_sub_list = list(allBlockDat_wide['sub'].unique())
                long_sub_list = list(allBlockDat['sub'].unique())

                #filter by ses and sub
                Nback_database_ses = filter_rows_by_values(Nback_database, wide_sub_list, db_sessions[0])
                Nback_database_long_ses = filter_rows_by_values(Nback_database_long, long_sub_list, db_sessions[0])

                #concatonate with other session in full database
                Nback_database = pd.concat([Nback_database[Nback_database['ses'] != db_sessions[0]], Nback_database_ses],ignore_index=True)
                Nback_database_long = pd.concat([Nback_database_long[Nback_database_long['ses'] != db_sessions[0]], Nback_database_long_ses],ignore_index=True)

        #add newly processed data
        Nback_database = Nback_database.append(allBlockDat_wide)
        Nback_database_long = Nback_database_long.append(allBlockDat)

        #sort to ensure in sub order
        Nback_database = Nback_database.sort_values(by = ['ses', 'sub'])
        Nback_database_long = Nback_database_long.sort_values(by = ['ses', 'sub', 'block'])

        #round to 3 decimal points
        Nback_database = Nback_database.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)
        Nback_database_long = Nback_database_long.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)

        #write databases
        Nback_database.to_csv(str(Path(derivative_data_path).joinpath('task-nback_summary.tsv')), sep = '\t', encoding='utf-8-sig', index = False) 
        Nback_database_long.to_csv(str(Path(derivative_data_path).joinpath('task-nback_summary_long.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

        return Nback_database, Nback_database_long

* overwrite_flag : True


Execution Outputs
-----------------


* allBlocks_longDat : (    sub  ses  ...  b2_rt_mean_target_hit  b2_rt_med_target_hit
0     5    1  ...                960.067                 878.0
1     6    1  ...               1033.000                 920.5
2     7    1  ...               1108.455                1068.0
3     9    1  ...               1130.636                1107.0
4    11    1  ...                657.700                 656.5
..  ...  ...  ...                    ...                   ...
9    26    2  ...                933.417                1009.0
10   28    2  ...                673.643                 689.5
11   35    2  ...                968.600                 934.5
12   37    2  ...                822.091                 863.0
13   40    2  ...                621.667                 546.0

[68 rows x 50 columns],     sub  ses block  ...  p_target_ba  rt_mean_target_hit  rt_med_target_hit
0     5    1    b0  ...      100.000             582.500              560.5
1     5    1    b1  ...       98.864             675.188              646.5
2     5    1    b2  ...       95.739             960.067              878.0
3     6    1    b0  ...       98.864             658.250              654.5
4     6    1    b1  ...       90.625             774.308              738.0
..  ...  ...   ...  ...          ...                 ...                ...
24   37    2    b1  ...       96.875             810.000              756.0
25   37    2    b2  ...       71.875             822.091              863.0
32   40    2    b0  ...       97.727             535.375              510.0
33   40    2    b1  ...      100.000             543.312              535.0
34   40    2    b2  ...       87.500             621.667              546.0

[202 rows x 19 columns])


Runtime info
------------


* duration : 0.076529
* hostname : ND-NTR-FCH12085
* prev_wd : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* working_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/Nback/_session_id_2/concatBlocksLong


Environment
~~~~~~~~~~~


* CLICOLOR : 1
* CONDA_DEFAULT_ENV : base
* CONDA_EXE : /Users/azp271/opt/anaconda3/bin/conda
* CONDA_PREFIX : /Users/azp271/opt/anaconda3
* CONDA_PROMPT_MODIFIER : (base) 
* CONDA_PYTHON_EXE : /Users/azp271/opt/anaconda3/bin/python
* CONDA_SHLVL : 1
* DISPLAY : /private/tmp/com.apple.launchd.GWJcr5aiMQ/org.xquartz:0
* DYLD_LIBRARY_PATH : /opt/X11/lib/flat_namespace:/opt/X11/lib/flat_namespace
* HOME : /Users/azp271
* LANG : en_US.UTF-8
* LOGNAME : azp271
* LSCOLORS : ExFxBxDxCxegedabagacad
* OLDPWD : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* PATH : /Users/azp271/opt/anaconda3/bin:/Users/azp271/opt/anaconda3/condabin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/TeX/texbin:/opt/X11/bin:/Library/Apple/usr/bin:/Users/azp271/abin
* PS1 : (base) \[\033[36m\]\u\[\033[m\]@\[\033[32m\]\h:\[\033[33;1m\]\w\[\033[m\]$ 
* PWD : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code
* SHELL : /bin/bash
* SHLVL : 2
* SSH_AUTH_SOCK : /private/tmp/com.apple.launchd.7qhvbO6vQS/Listeners
* TERM : xterm-256color
* TERM_PROGRAM : Apple_Terminal
* TERM_PROGRAM_VERSION : 440
* TERM_SESSION_ID : 216F9EAF-B278-47F3-8606-A712F9800D89
* TMPDIR : /var/folders/y5/lybvr3s93wn9ny273pk2fhgr0000gp/T/
* USER : azp271
* XPC_FLAGS : 0x0
* XPC_SERVICE_NAME : 0
* _ : /Users/azp271/opt/anaconda3/bin/python3
* _CE_CONDA : 
* _CE_M : 
* __CFBundleIdentifier : com.apple.Terminal

