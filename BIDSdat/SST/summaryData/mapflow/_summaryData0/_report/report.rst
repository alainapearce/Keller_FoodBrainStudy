Node: utility
=============


 Hierarchy : _summaryData0
 Exec ID : _summaryData0


Original Inputs
---------------


* SST_file : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-114/ses-1/beh/sub-114_ses-1_task-sst_events.tsv
* function_str : def summarySST(SST_file):
    import numpy as np
    import pandas as pd

    ###################################################################
    ####                   Sub-function script                     ####

    #need to sub-functions within the function that is called by the node just 
    #like you need to re-import libraries
    def summary_stats(SST_data):

        ## ANALYSIS NOTE: 
        ## the original version of ANALYZE_IT and recommendations were to remove
        ## the first trial of each block. However, this is not reccomended in the
        ## concensus article Verbruggen et al., 2019 or in the new ANALYZE-IT-Tscope.R
        ## code on Open Science Foundation (https://osf.io/dw4ke/). 

        ## to remove first trial of each block, uncomment below code:

        #drop first row of each block
        #if 1 in SST_data['block']:
        #    block1 = SST_data.loc[SST_data['block'] == 1].index.values
        #    SST_data = SST_data.drop(block1[0])
        #    
        #if 2 in SST_data['block']:
        #    block2 = SST_data.loc[SST_data['block'] == 2].index.values
        #    SST_data = SST_data.drop(block2[0])
        #    
        #if 3 in SST_data['block']:
        #    block3 = SST_data.loc[SST_data['block'] == 3].index.values
        #    SST_data = SST_data.drop(block3[0])
        # 
        #if 4 in SST_data['block']:
        #    block4 = SST_data.loc[SST_data['block'] == 4].index.values
        #    SST_data = SST_data.drop(block4[0])

        #trial counts
        SST_target = SST_data.groupby('stop_signal').get_group(0)
        SST_stop = SST_data.groupby('stop_signal').get_group(1)

        #trial counts
        sst_n_targets = SST_target.shape[0]
        sst_n_stop = SST_stop.shape[0]
        sst_go_correct = SST_target[SST_target['correct'] == 4].shape[0]
        sst_go_error = SST_target[SST_target['correct'] == 2].shape[0]
        sst_go_miss = SST_target[SST_target['correct'] == 1].shape[0]

        #rt 
        go_rt = SST_target.loc[SST_target['rt_1'] > 0, 'rt_1'].mean(axis = 0)    
        go_rt_correct = SST_target.loc[(SST_target['correct'] == 4) & (SST_target['rt_1'] > 0), 'rt_1'].mean(axis = 0)
        go_rt_error = SST_target.loc[(SST_target['correct'] == 2) & (SST_target['rt_1'] > 0), 'rt_1'].mean(axis = 0)

        us_rt = SST_stop.loc[(SST_stop['correct'] == 3) & (SST_stop['rt_1'] > 0), 'rt_1'].mean(axis = 0)

        #probability of responding on signal  -- p(resp|signal)
        signal_presp = SST_stop.loc[(SST_stop['correct'] == 3)].shape[0]/sst_n_stop

        #SSD
        ssd = SST_stop['true_ssd'].mean(axis = 0)

        #racehorse check
        if go_rt > us_rt:
            racehorse = 1
        else:
            racehorse = 0

        if racehorse == 1:

            #SSRT Mean methods
            ssrt_mean = SST_target.loc[SST_target['correct'] != 1, 'rt_1'].mean(axis = 0) - ssd

            #SSRT Integration method
            #replace omissions with max RT if there are omissions
            if sst_go_miss > 0:
                #get max rt
                max_rt = max(SST_target.loc[SST_target['correct'] != 1, 'rt_1'])

                #make new dataset
                SST_target_replace = SST_target

                #supress warning
                pd.options.mode.chained_assignment = None

                #replace ommitted rt values
                SST_target_replace.loc[SST_target_replace['correct'] == 1, 'rt_1'] = max_rt

                #get rt at signal_presp percentile
                nth_rt = np.percentile(SST_target_replace['rt_1'], 100*signal_presp)

            else:
                #get rt at signal_presp percentile
                nth_rt = np.percentile(SST_target['rt_1'], 100*signal_presp)


            #caluclate ssrt
            ssrt_int = nth_rt - ssd

        else:
            ssrt_mean = np.nan
            ssrt_int = np.nan


        #combine into array    
        summary_results = [racehorse, sst_n_stop, sst_n_targets, go_rt, sst_go_correct, go_rt_correct, 
                         sst_go_error, go_rt_error, sst_go_miss, signal_presp, us_rt,
                         ssd, ssrt_mean, ssrt_int]

        return(summary_results)

    ###################################################################
    ####                Primary function script                    ####

    if isinstance(SST_file, str):
        #check to see if it is filepath str or 'No subfiles' message
        if '.tsv' in SST_file:
            #if only 1 file, will be string and we want an array
            SST_file = [SST_file]
        else:
            SST_file = []

    if len(SST_file) > 0:

        #loop counter
        count = 0

        for file in SST_file:

            #load data - loop throgh participant blockfiles
            SST_ProcData = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python') 

            #check for incomplete blocks
            block_counts = SST_ProcData['block'].value_counts()
            to_remove = block_counts[block_counts < 64].index

            if len(to_remove) > 0:
                SST_ProcData = SST_ProcData[~SST_ProcData.block.isin(to_remove)]

            #check for duplicate conditions - coding error in initial task randomization
            cond_list = SST_ProcData.groupby('block')['block_cond'].unique()

            #convert to strings
            cond_list = [str(item[0]) for item in cond_list]
            unique_cond = np.unique(cond_list)

            #if there are duplicate blocks, re-label second instance
            if len(unique_cond) < len(cond_list):
                for cond in unique_cond:
                    cond_group = SST_ProcData.groupby('block_cond').get_group(cond)

                    #number of blocks with condition 'cond'
                    nblocks = len(cond_group['block'].unique())

                    if nblocks > 1:
                        #get block number for second instance of cond
                        dup_block = max(cond_group['block'])

                        #for rows where column 'block' = dup_block, replace column 'block_cond'
                        #values
                        SST_ProcData.loc[SST_ProcData['block'] == dup_block, 'block_cond'] = SST_ProcData[SST_ProcData['block'] == dup_block]['block_cond'].replace(cond, 'dup_' + cond)

            #remove duplicate blocks
            SST_nodup_blocks = SST_ProcData[SST_ProcData['block_cond'].str.contains('dup')==False]

            colnames = ['sub', 'block', 'condition', 'racehorse_check', 'n_stop_trials', 'n_go_trials', 'go_rt', 'n_go_cor', 'go_cor_rt', 'n_go_error',
                'go_error_rt', 'n_go_miss', 'stop_prob_resp', 'us_rt', 'ssd', 'ssrt_mean', 'ssrt_int']

            #summary stats - across all blocks
            all_trials_stat = summary_stats(SST_nodup_blocks)
            all_trials_stat.insert(0, SST_ProcData.loc[0, 'sub'])
            all_trials_stat.insert(1, 'all')
            all_trials_stat.insert(2, 'all')

            if count == 0:
                #make dataset
                overall_summary_data = pd.DataFrame(all_trials_stat).T
                overall_summary_data.columns = colnames
            else:
                overall_summary_data.loc[len(overall_summary_data)] = all_trials_stat

            # summary stats - by block conditions

            #check is there are 2 high ED blocks and 2 low ED blocks
            hed_blocks = [item for item in unique_cond if 'hED' in item]
            led_blocks = [item for item in unique_cond if 'lED' in item]

            #ensure block_cond column is string
            SST_nodup_blocks = SST_nodup_blocks.convert_dtypes()

            if len(hed_blocks) == 2 and len(led_blocks) == 2:
                #high ED data
                SST_hed_blocks = SST_nodup_blocks[SST_nodup_blocks['block_cond'].str.contains('hED')]

                hed_trials_stat = summary_stats(SST_hed_blocks)
                hed_trials_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                hed_trials_stat.insert(1, 'h_ed')
                hed_trials_stat.insert(2, 'h_ed')

                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = hed_trials_stat

                #low ED data
                SST_led_blocks = SST_nodup_blocks[SST_nodup_blocks['block_cond'].str.contains('lED')]

                led_trials_stat = summary_stats(SST_led_blocks) 
                led_trials_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                led_trials_stat.insert(1, 'l_ed')
                led_trials_stat.insert(2, 'l_ed')

                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = led_trials_stat

            #check is there are 2 large portion blocks and 2 small portion blocksa
            lport_blocks = [item for item in unique_cond if 'lPort' in item]
            sport_blocks = [item for item in unique_cond if 'sPort' in item]

            if len(lport_blocks) == 2 and len(sport_blocks) == 2:
                #large portion data
                SST_lport_blocks = SST_nodup_blocks[SST_nodup_blocks['block_cond'].str.contains('lPort')]

                lport_trials_stat = summary_stats(SST_lport_blocks)
                lport_trials_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                lport_trials_stat.insert(1, 'l_port')
                lport_trials_stat.insert(2, 'l_port')

                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = lport_trials_stat


                #small portion
                SST_sport_blocks = SST_nodup_blocks[SST_nodup_blocks['block_cond'].str.contains('sPort')]

                sport_trials_stat = summary_stats(SST_sport_blocks)
                sport_trials_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                sport_trials_stat.insert(1, 's_port')
                sport_trials_stat.insert(2, 's_port')

                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = sport_trials_stat

            #summary stats by block

            #get all non-duplicate blocks in dataset
            blocks = SST_nodup_blocks['block'].unique()

            #loop through blocks
            for b in blocks:
                #block data
                b_data = SST_nodup_blocks[SST_nodup_blocks['block'] == b]

                #ensure block_cond column is string
                b_data = b_data.convert_dtypes()

                #high ED, large portion
                if b_data['block_cond'].str.contains('hED_lPort').any():

                    hED_lPort_stat = summary_stats(b_data)
                    hED_lPort_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                    hED_lPort_stat.insert(1, b)
                    hED_lPort_stat.insert(2, 'hED_lPort')   

                    #append new rows
                    overall_summary_data.loc[len(overall_summary_data)] = hED_lPort_stat

                #high ED, small portion        
                elif b_data['block_cond'].str.contains('hED_sPort').any():

                    hED_sPort_stat = summary_stats(b_data)
                    hED_sPort_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                    hED_sPort_stat.insert(1, b)
                    hED_sPort_stat.insert(2, 'hED_sPort')  

                    #append new rows
                    overall_summary_data.loc[len(overall_summary_data)] = hED_sPort_stat

                #low ED, large portion
                elif b_data['block_cond'].str.contains('lED_lPort').any():

                    lED_lPort_stat = summary_stats(b_data)
                    lED_lPort_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                    lED_lPort_stat.insert(1, b)
                    lED_lPort_stat.insert(2, 'lED_lPort') 

                    #append new rows
                    overall_summary_data.loc[len(overall_summary_data)] = lED_lPort_stat


                #low ED, small portion
                elif b_data['block_cond'].str.contains('lED_sPort').any():

                    lED_sPort_stat = summary_stats(b_data)
                    lED_sPort_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                    lED_sPort_stat.insert(1, b)
                    lED_sPort_stat.insert(2, 'lED_sPort')

                    #append new rows
                    overall_summary_data.loc[len(overall_summary_data)] = lED_sPort_stat

            #update count for files loop
            count = 1

    else:
         overall_summary_data = 'no files'


    return overall_summary_data

* session_id : <undefined>


Execution Inputs
----------------


* SST_file : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-114/ses-1/beh/sub-114_ses-1_task-sst_events.tsv
* function_str : def summarySST(SST_file):
    import numpy as np
    import pandas as pd

    ###################################################################
    ####                   Sub-function script                     ####

    #need to sub-functions within the function that is called by the node just 
    #like you need to re-import libraries
    def summary_stats(SST_data):

        ## ANALYSIS NOTE: 
        ## the original version of ANALYZE_IT and recommendations were to remove
        ## the first trial of each block. However, this is not reccomended in the
        ## concensus article Verbruggen et al., 2019 or in the new ANALYZE-IT-Tscope.R
        ## code on Open Science Foundation (https://osf.io/dw4ke/). 

        ## to remove first trial of each block, uncomment below code:

        #drop first row of each block
        #if 1 in SST_data['block']:
        #    block1 = SST_data.loc[SST_data['block'] == 1].index.values
        #    SST_data = SST_data.drop(block1[0])
        #    
        #if 2 in SST_data['block']:
        #    block2 = SST_data.loc[SST_data['block'] == 2].index.values
        #    SST_data = SST_data.drop(block2[0])
        #    
        #if 3 in SST_data['block']:
        #    block3 = SST_data.loc[SST_data['block'] == 3].index.values
        #    SST_data = SST_data.drop(block3[0])
        # 
        #if 4 in SST_data['block']:
        #    block4 = SST_data.loc[SST_data['block'] == 4].index.values
        #    SST_data = SST_data.drop(block4[0])

        #trial counts
        SST_target = SST_data.groupby('stop_signal').get_group(0)
        SST_stop = SST_data.groupby('stop_signal').get_group(1)

        #trial counts
        sst_n_targets = SST_target.shape[0]
        sst_n_stop = SST_stop.shape[0]
        sst_go_correct = SST_target[SST_target['correct'] == 4].shape[0]
        sst_go_error = SST_target[SST_target['correct'] == 2].shape[0]
        sst_go_miss = SST_target[SST_target['correct'] == 1].shape[0]

        #rt 
        go_rt = SST_target.loc[SST_target['rt_1'] > 0, 'rt_1'].mean(axis = 0)    
        go_rt_correct = SST_target.loc[(SST_target['correct'] == 4) & (SST_target['rt_1'] > 0), 'rt_1'].mean(axis = 0)
        go_rt_error = SST_target.loc[(SST_target['correct'] == 2) & (SST_target['rt_1'] > 0), 'rt_1'].mean(axis = 0)

        us_rt = SST_stop.loc[(SST_stop['correct'] == 3) & (SST_stop['rt_1'] > 0), 'rt_1'].mean(axis = 0)

        #probability of responding on signal  -- p(resp|signal)
        signal_presp = SST_stop.loc[(SST_stop['correct'] == 3)].shape[0]/sst_n_stop

        #SSD
        ssd = SST_stop['true_ssd'].mean(axis = 0)

        #racehorse check
        if go_rt > us_rt:
            racehorse = 1
        else:
            racehorse = 0

        if racehorse == 1:

            #SSRT Mean methods
            ssrt_mean = SST_target.loc[SST_target['correct'] != 1, 'rt_1'].mean(axis = 0) - ssd

            #SSRT Integration method
            #replace omissions with max RT if there are omissions
            if sst_go_miss > 0:
                #get max rt
                max_rt = max(SST_target.loc[SST_target['correct'] != 1, 'rt_1'])

                #make new dataset
                SST_target_replace = SST_target

                #supress warning
                pd.options.mode.chained_assignment = None

                #replace ommitted rt values
                SST_target_replace.loc[SST_target_replace['correct'] == 1, 'rt_1'] = max_rt

                #get rt at signal_presp percentile
                nth_rt = np.percentile(SST_target_replace['rt_1'], 100*signal_presp)

            else:
                #get rt at signal_presp percentile
                nth_rt = np.percentile(SST_target['rt_1'], 100*signal_presp)


            #caluclate ssrt
            ssrt_int = nth_rt - ssd

        else:
            ssrt_mean = np.nan
            ssrt_int = np.nan


        #combine into array    
        summary_results = [racehorse, sst_n_stop, sst_n_targets, go_rt, sst_go_correct, go_rt_correct, 
                         sst_go_error, go_rt_error, sst_go_miss, signal_presp, us_rt,
                         ssd, ssrt_mean, ssrt_int]

        return(summary_results)

    ###################################################################
    ####                Primary function script                    ####

    if isinstance(SST_file, str):
        #check to see if it is filepath str or 'No subfiles' message
        if '.tsv' in SST_file:
            #if only 1 file, will be string and we want an array
            SST_file = [SST_file]
        else:
            SST_file = []

    if len(SST_file) > 0:

        #loop counter
        count = 0

        for file in SST_file:

            #load data - loop throgh participant blockfiles
            SST_ProcData = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python') 

            #check for incomplete blocks
            block_counts = SST_ProcData['block'].value_counts()
            to_remove = block_counts[block_counts < 64].index

            if len(to_remove) > 0:
                SST_ProcData = SST_ProcData[~SST_ProcData.block.isin(to_remove)]

            #check for duplicate conditions - coding error in initial task randomization
            cond_list = SST_ProcData.groupby('block')['block_cond'].unique()

            #convert to strings
            cond_list = [str(item[0]) for item in cond_list]
            unique_cond = np.unique(cond_list)

            #if there are duplicate blocks, re-label second instance
            if len(unique_cond) < len(cond_list):
                for cond in unique_cond:
                    cond_group = SST_ProcData.groupby('block_cond').get_group(cond)

                    #number of blocks with condition 'cond'
                    nblocks = len(cond_group['block'].unique())

                    if nblocks > 1:
                        #get block number for second instance of cond
                        dup_block = max(cond_group['block'])

                        #for rows where column 'block' = dup_block, replace column 'block_cond'
                        #values
                        SST_ProcData.loc[SST_ProcData['block'] == dup_block, 'block_cond'] = SST_ProcData[SST_ProcData['block'] == dup_block]['block_cond'].replace(cond, 'dup_' + cond)

            #remove duplicate blocks
            SST_nodup_blocks = SST_ProcData[SST_ProcData['block_cond'].str.contains('dup')==False]

            colnames = ['sub', 'block', 'condition', 'racehorse_check', 'n_stop_trials', 'n_go_trials', 'go_rt', 'n_go_cor', 'go_cor_rt', 'n_go_error',
                'go_error_rt', 'n_go_miss', 'stop_prob_resp', 'us_rt', 'ssd', 'ssrt_mean', 'ssrt_int']

            #summary stats - across all blocks
            all_trials_stat = summary_stats(SST_nodup_blocks)
            all_trials_stat.insert(0, SST_ProcData.loc[0, 'sub'])
            all_trials_stat.insert(1, 'all')
            all_trials_stat.insert(2, 'all')

            if count == 0:
                #make dataset
                overall_summary_data = pd.DataFrame(all_trials_stat).T
                overall_summary_data.columns = colnames
            else:
                overall_summary_data.loc[len(overall_summary_data)] = all_trials_stat

            # summary stats - by block conditions

            #check is there are 2 high ED blocks and 2 low ED blocks
            hed_blocks = [item for item in unique_cond if 'hED' in item]
            led_blocks = [item for item in unique_cond if 'lED' in item]

            #ensure block_cond column is string
            SST_nodup_blocks = SST_nodup_blocks.convert_dtypes()

            if len(hed_blocks) == 2 and len(led_blocks) == 2:
                #high ED data
                SST_hed_blocks = SST_nodup_blocks[SST_nodup_blocks['block_cond'].str.contains('hED')]

                hed_trials_stat = summary_stats(SST_hed_blocks)
                hed_trials_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                hed_trials_stat.insert(1, 'h_ed')
                hed_trials_stat.insert(2, 'h_ed')

                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = hed_trials_stat

                #low ED data
                SST_led_blocks = SST_nodup_blocks[SST_nodup_blocks['block_cond'].str.contains('lED')]

                led_trials_stat = summary_stats(SST_led_blocks) 
                led_trials_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                led_trials_stat.insert(1, 'l_ed')
                led_trials_stat.insert(2, 'l_ed')

                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = led_trials_stat

            #check is there are 2 large portion blocks and 2 small portion blocksa
            lport_blocks = [item for item in unique_cond if 'lPort' in item]
            sport_blocks = [item for item in unique_cond if 'sPort' in item]

            if len(lport_blocks) == 2 and len(sport_blocks) == 2:
                #large portion data
                SST_lport_blocks = SST_nodup_blocks[SST_nodup_blocks['block_cond'].str.contains('lPort')]

                lport_trials_stat = summary_stats(SST_lport_blocks)
                lport_trials_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                lport_trials_stat.insert(1, 'l_port')
                lport_trials_stat.insert(2, 'l_port')

                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = lport_trials_stat


                #small portion
                SST_sport_blocks = SST_nodup_blocks[SST_nodup_blocks['block_cond'].str.contains('sPort')]

                sport_trials_stat = summary_stats(SST_sport_blocks)
                sport_trials_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                sport_trials_stat.insert(1, 's_port')
                sport_trials_stat.insert(2, 's_port')

                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = sport_trials_stat

            #summary stats by block

            #get all non-duplicate blocks in dataset
            blocks = SST_nodup_blocks['block'].unique()

            #loop through blocks
            for b in blocks:
                #block data
                b_data = SST_nodup_blocks[SST_nodup_blocks['block'] == b]

                #ensure block_cond column is string
                b_data = b_data.convert_dtypes()

                #high ED, large portion
                if b_data['block_cond'].str.contains('hED_lPort').any():

                    hED_lPort_stat = summary_stats(b_data)
                    hED_lPort_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                    hED_lPort_stat.insert(1, b)
                    hED_lPort_stat.insert(2, 'hED_lPort')   

                    #append new rows
                    overall_summary_data.loc[len(overall_summary_data)] = hED_lPort_stat

                #high ED, small portion        
                elif b_data['block_cond'].str.contains('hED_sPort').any():

                    hED_sPort_stat = summary_stats(b_data)
                    hED_sPort_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                    hED_sPort_stat.insert(1, b)
                    hED_sPort_stat.insert(2, 'hED_sPort')  

                    #append new rows
                    overall_summary_data.loc[len(overall_summary_data)] = hED_sPort_stat

                #low ED, large portion
                elif b_data['block_cond'].str.contains('lED_lPort').any():

                    lED_lPort_stat = summary_stats(b_data)
                    lED_lPort_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                    lED_lPort_stat.insert(1, b)
                    lED_lPort_stat.insert(2, 'lED_lPort') 

                    #append new rows
                    overall_summary_data.loc[len(overall_summary_data)] = lED_lPort_stat


                #low ED, small portion
                elif b_data['block_cond'].str.contains('lED_sPort').any():

                    lED_sPort_stat = summary_stats(b_data)
                    lED_sPort_stat.insert(0, SST_ProcData.loc[0, 'sub'])
                    lED_sPort_stat.insert(1, b)
                    lED_sPort_stat.insert(2, 'lED_sPort')

                    #append new rows
                    overall_summary_data.loc[len(overall_summary_data)] = lED_sPort_stat

            #update count for files loop
            count = 1

    else:
         overall_summary_data = 'no files'


    return overall_summary_data

* session_id : <undefined>


Execution Outputs
-----------------


* summarySST_dat :    sub   block  condition racehorse_check  ...    us_rt      ssd ssrt_mean ssrt_int
0  114     all        all               1  ...  439.594  223.188   326.456  319.312
1  114    h_ed       h_ed               1  ...  465.312  223.969    290.75  266.531
2  114    l_ed       l_ed               1  ...  413.875  222.406   362.531  367.094
3  114  l_port     l_port               1  ...  486.357    224.5   303.906      268
4  114  s_port     s_port               1  ...  403.222  221.875    349.23  375.438
5  114       1  hED_lPort               1  ...  498.286  179.188   309.792  277.938
6  114       2  hED_sPort               1  ...  439.667   268.75   271.708  274.125
7  114       3  lED_sPort               1  ...  366.778      175   427.404  461.688
8  114       4  lED_lPort               1  ...  474.429  269.812   298.021      251

[9 rows x 17 columns]


Runtime info
------------


* duration : 0.490516
* hostname : nut-azp271-10239
* prev_wd : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* working_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/SST/summaryData/mapflow/_summaryData0


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

