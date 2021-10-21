Node: summaryData (utility)
===========================


 Hierarchy : GNG.summaryData
 Exec ID : summaryData


Original Inputs
---------------


* GNG_file : ['/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-031/ses-1/beh/sub-031_ses-1_task-gng_events.tsv', '/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-033/ses-1/beh/sub-033_ses-1_task-gng_events.tsv', '/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-034/ses-1/beh/sub-034_ses-1_task-gng_events.tsv', '/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-035/ses-1/beh/sub-035_ses-1_task-gng_events.tsv', '/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-036/ses-1/beh/sub-036_ses-1_task-gng_events.tsv']
* function_str : def summaryGNG(GNG_file):
    import numpy as np
    import pandas as pd

    ###################################################################
    ####                   Sub-function script                     ####

    #need to write sub-functions (e.g., getGNGtrialAcc) WITHIN the function that is called by the node (e.g., summaryGNG)
    #just like you need to re-import libraries

    def getGNGtrialAcc(GNG_data):
        #Make 2 new variables:
        #trial_resp: indicate if response made during trial (stim or response screen)
        #trial_rt: indicate reaction time from onset of stim screen (add 750 ms to respond_rt if response occured during response screen)

        #initialize empty columns for trial_resp and trial_rt
        GNG_data["trial_resp"] = np.nan
        GNG_data["trial_rt"] = np.nan

        #Assign values to trial_resp and trial_rt
        GNG_data.loc[GNG_data.stim_resp == '{SPACE}', 'trial_resp'] = '{SPACE}'
        GNG_data.loc[GNG_data.respond_resp == '{SPACE}', 'trial_resp'] = '{SPACE}'
        GNG_data.loc[GNG_data.stim_resp == '{SPACE}', 'trial_rt'] = GNG_data.stim_rt
        GNG_data.loc[GNG_data.respond_resp == '{SPACE}', 'trial_rt'] = GNG_data.respond_rt + 750

        ##Create new accuracy variable "Acc_Resp" that indicates a 1 when the columns 'CorrectResp' and 'RESP' match
        #initialize empty columns for accuracy variable
        GNG_data["trial_acc"] = np.nan

        # Change nan to none because pandas/NumPy uses the fact that np.nan != np.nan
        GNG_data[['ca', 'trial_resp']] = GNG_data[['ca', 'trial_resp']].fillna(value='None')

        # Set accuracy equal to 1 when trial_acc = trial_resp
        GNG_data['trial_acc'] = np.where(GNG_data['trial_resp'] == GNG_data['ca'], '1', '0')

        return(GNG_data)

    def summary_stats(GNG_data):

        # Create 2 dataframes, one with Go trials and one with No Go trials
        Go_data = GNG_data.loc[GNG_data['compatibility'] == 'Go']
        NoGo_data = GNG_data.loc[GNG_data['compatibility'] == 'NoGo']

        # count trials
        nGo = len(Go_data)
        nNoGo = len(NoGo_data)

        # Accuracy - here *check par 51
        if 1 in GNG_data.trial_acc:
            nAcc = GNG_data['trial_acc'].value_counts()["1"]
        else: 
            nAcc = 0

        pAcc = nAcc/len(GNG_data)

        # Go Hits/Misses
        nGo_Hit = (Go_data.trial_acc == '1').sum()
        pGo_Hit = nGo_Hit/len(Go_data)

        nGo_Miss = (Go_data.trial_acc == '0').sum()
        pGo_Miss = nGo_Miss/len(Go_data)

        #NoGo Commissions (False Alarms) and Correct no responses  
        nNoGo_Corr = (NoGo_data.trial_acc == '1').sum()
        pNoGo_Corr = nNoGo_Corr/len(NoGo_data)

        nNoGo_FA = (NoGo_data.trial_acc == '0').sum()
        pNoGo_FA = nNoGo_FA/len(NoGo_data)

        # Mean and median RT
        RTmeanGo_Hit = Go_data.loc[(Go_data['trial_acc']=="1"), 'trial_rt'].mean()
        RTmedGo_Hit = Go_data.loc[(Go_data['trial_acc']=="1"), 'trial_rt'].median()

        RTmeanNoGo_FA = NoGo_data.loc[(NoGo_data['trial_acc']=="0"), 'trial_rt'].mean()
        RTmedNoGo_FA = NoGo_data.loc[(NoGo_data['trial_acc']=="0"), 'trial_rt'].median()

        #combine into array    
        summary_results = [nGo, nNoGo, nAcc, pAcc, nGo_Hit, nGo_Miss, nNoGo_Corr, nNoGo_FA, pGo_Hit, 
                           pGo_Miss, pNoGo_Corr, pNoGo_FA, RTmeanGo_Hit, RTmeanNoGo_FA, RTmedGo_Hit, RTmedNoGo_FA]

        return(summary_results)

    ## DDM
    #RT data at different quantils # this is a separate database thats output.
    # Can always skip this for now, and make note to make DDM function
    # SDT = signal detection theory. google norminv, it gives z-score. should be able to ask for norminv in python

    ###################################################################
    ####                Primary function script                    ####

    if isinstance(GNG_file, str):
        if '.tsv' in GNG_file:
            #if only 1 file, will be string and we want an array
            GNG_file = [GNG_file]
        else:
            GNG_file = []

    if len(GNG_file) > 0:

        #loop counter
        count = 0

        for file in GNG_file:

            #load data - loop throgh participant blockfiles
            GNG_data = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python') 

            #check for incomplete blocks
            block_counts = GNG_data['block_list_sample'].value_counts()
            to_remove = block_counts[block_counts < 40].index

            if len(to_remove) > 0:
                GNG_data = GNG_data[~GNG_data.block_list_sample.isin(to_remove)]

            # Compute GNG trial accuracy and rt
            GNG_data = getGNGtrialAcc(GNG_data)

            # Set column names
            colnames = ['sub', 'block', 'nGo', 'nNoGo', 'nAcc', 'pAcc', 'nGo_Hit', 'nGo_Miss', 'nNoGo_Corr', 
                        'nNoGo_FA', 'pGo_Hit', 'pGo_Miss', 'pNoGo_Corr', 'pNoGo_FA', 'RTmeanGo_Hit',
                        'RTmeanNoGo_FA', 'RTmedGo_Hit', 'RTmedNoGo_FA']

            #summary stats - across all blocks
            all_trials_stat = summary_stats(GNG_data)
            all_trials_stat.insert(0, GNG_data.loc[0, 'sub'])
            all_trials_stat.insert(1, 'all')

            if count == 0:
                #make dataset
                overall_summary_data = pd.DataFrame(all_trials_stat).T
                overall_summary_data.columns = colnames
            else:
                overall_summary_data.loc[len(overall_summary_data)] = all_trials_stat

            #summary stats by block

            #get all non-duplicate blocks in dataset
            blocks = GNG_data['block_list_sample'].unique()

            #loop through blocks
            for b in blocks:

                #subset block data from GNG_data
                b_data = GNG_data[GNG_data['block_list_sample'] == b]

                #ensure block_cond column is string
                b_data = b_data.convert_dtypes()

                #set block variable name
                b_var = ("b" + str(int(b)))

                # Get summary stats for block
                block_summary = summary_stats(b_data)
                block_summary.insert(0, GNG_data.loc[0, 'sub'])
                block_summary.insert(1, b_var)

                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = block_summary

            #update count for files loop
            count = 1

    else:
         overall_summary_data = 'no files'

    return overall_summary_data



Execution Inputs
----------------


* GNG_file : ['/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-031/ses-1/beh/sub-031_ses-1_task-gng_events.tsv', '/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-033/ses-1/beh/sub-033_ses-1_task-gng_events.tsv', '/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-034/ses-1/beh/sub-034_ses-1_task-gng_events.tsv', '/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-035/ses-1/beh/sub-035_ses-1_task-gng_events.tsv', '/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-036/ses-1/beh/sub-036_ses-1_task-gng_events.tsv']
* function_str : def summaryGNG(GNG_file):
    import numpy as np
    import pandas as pd

    ###################################################################
    ####                   Sub-function script                     ####

    #need to write sub-functions (e.g., getGNGtrialAcc) WITHIN the function that is called by the node (e.g., summaryGNG)
    #just like you need to re-import libraries

    def getGNGtrialAcc(GNG_data):
        #Make 2 new variables:
        #trial_resp: indicate if response made during trial (stim or response screen)
        #trial_rt: indicate reaction time from onset of stim screen (add 750 ms to respond_rt if response occured during response screen)

        #initialize empty columns for trial_resp and trial_rt
        GNG_data["trial_resp"] = np.nan
        GNG_data["trial_rt"] = np.nan

        #Assign values to trial_resp and trial_rt
        GNG_data.loc[GNG_data.stim_resp == '{SPACE}', 'trial_resp'] = '{SPACE}'
        GNG_data.loc[GNG_data.respond_resp == '{SPACE}', 'trial_resp'] = '{SPACE}'
        GNG_data.loc[GNG_data.stim_resp == '{SPACE}', 'trial_rt'] = GNG_data.stim_rt
        GNG_data.loc[GNG_data.respond_resp == '{SPACE}', 'trial_rt'] = GNG_data.respond_rt + 750

        ##Create new accuracy variable "Acc_Resp" that indicates a 1 when the columns 'CorrectResp' and 'RESP' match
        #initialize empty columns for accuracy variable
        GNG_data["trial_acc"] = np.nan

        # Change nan to none because pandas/NumPy uses the fact that np.nan != np.nan
        GNG_data[['ca', 'trial_resp']] = GNG_data[['ca', 'trial_resp']].fillna(value='None')

        # Set accuracy equal to 1 when trial_acc = trial_resp
        GNG_data['trial_acc'] = np.where(GNG_data['trial_resp'] == GNG_data['ca'], '1', '0')

        return(GNG_data)

    def summary_stats(GNG_data):

        # Create 2 dataframes, one with Go trials and one with No Go trials
        Go_data = GNG_data.loc[GNG_data['compatibility'] == 'Go']
        NoGo_data = GNG_data.loc[GNG_data['compatibility'] == 'NoGo']

        # count trials
        nGo = len(Go_data)
        nNoGo = len(NoGo_data)

        # Accuracy - here *check par 51
        if 1 in GNG_data.trial_acc:
            nAcc = GNG_data['trial_acc'].value_counts()["1"]
        else: 
            nAcc = 0

        pAcc = nAcc/len(GNG_data)

        # Go Hits/Misses
        nGo_Hit = (Go_data.trial_acc == '1').sum()
        pGo_Hit = nGo_Hit/len(Go_data)

        nGo_Miss = (Go_data.trial_acc == '0').sum()
        pGo_Miss = nGo_Miss/len(Go_data)

        #NoGo Commissions (False Alarms) and Correct no responses  
        nNoGo_Corr = (NoGo_data.trial_acc == '1').sum()
        pNoGo_Corr = nNoGo_Corr/len(NoGo_data)

        nNoGo_FA = (NoGo_data.trial_acc == '0').sum()
        pNoGo_FA = nNoGo_FA/len(NoGo_data)

        # Mean and median RT
        RTmeanGo_Hit = Go_data.loc[(Go_data['trial_acc']=="1"), 'trial_rt'].mean()
        RTmedGo_Hit = Go_data.loc[(Go_data['trial_acc']=="1"), 'trial_rt'].median()

        RTmeanNoGo_FA = NoGo_data.loc[(NoGo_data['trial_acc']=="0"), 'trial_rt'].mean()
        RTmedNoGo_FA = NoGo_data.loc[(NoGo_data['trial_acc']=="0"), 'trial_rt'].median()

        #combine into array    
        summary_results = [nGo, nNoGo, nAcc, pAcc, nGo_Hit, nGo_Miss, nNoGo_Corr, nNoGo_FA, pGo_Hit, 
                           pGo_Miss, pNoGo_Corr, pNoGo_FA, RTmeanGo_Hit, RTmeanNoGo_FA, RTmedGo_Hit, RTmedNoGo_FA]

        return(summary_results)

    ## DDM
    #RT data at different quantils # this is a separate database thats output.
    # Can always skip this for now, and make note to make DDM function
    # SDT = signal detection theory. google norminv, it gives z-score. should be able to ask for norminv in python

    ###################################################################
    ####                Primary function script                    ####

    if isinstance(GNG_file, str):
        if '.tsv' in GNG_file:
            #if only 1 file, will be string and we want an array
            GNG_file = [GNG_file]
        else:
            GNG_file = []

    if len(GNG_file) > 0:

        #loop counter
        count = 0

        for file in GNG_file:

            #load data - loop throgh participant blockfiles
            GNG_data = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python') 

            #check for incomplete blocks
            block_counts = GNG_data['block_list_sample'].value_counts()
            to_remove = block_counts[block_counts < 40].index

            if len(to_remove) > 0:
                GNG_data = GNG_data[~GNG_data.block_list_sample.isin(to_remove)]

            # Compute GNG trial accuracy and rt
            GNG_data = getGNGtrialAcc(GNG_data)

            # Set column names
            colnames = ['sub', 'block', 'nGo', 'nNoGo', 'nAcc', 'pAcc', 'nGo_Hit', 'nGo_Miss', 'nNoGo_Corr', 
                        'nNoGo_FA', 'pGo_Hit', 'pGo_Miss', 'pNoGo_Corr', 'pNoGo_FA', 'RTmeanGo_Hit',
                        'RTmeanNoGo_FA', 'RTmedGo_Hit', 'RTmedNoGo_FA']

            #summary stats - across all blocks
            all_trials_stat = summary_stats(GNG_data)
            all_trials_stat.insert(0, GNG_data.loc[0, 'sub'])
            all_trials_stat.insert(1, 'all')

            if count == 0:
                #make dataset
                overall_summary_data = pd.DataFrame(all_trials_stat).T
                overall_summary_data.columns = colnames
            else:
                overall_summary_data.loc[len(overall_summary_data)] = all_trials_stat

            #summary stats by block

            #get all non-duplicate blocks in dataset
            blocks = GNG_data['block_list_sample'].unique()

            #loop through blocks
            for b in blocks:

                #subset block data from GNG_data
                b_data = GNG_data[GNG_data['block_list_sample'] == b]

                #ensure block_cond column is string
                b_data = b_data.convert_dtypes()

                #set block variable name
                b_var = ("b" + str(int(b)))

                # Get summary stats for block
                block_summary = summary_stats(b_data)
                block_summary.insert(0, GNG_data.loc[0, 'sub'])
                block_summary.insert(1, b_var)

                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = block_summary

            #update count for files loop
            count = 1

    else:
         overall_summary_data = 'no files'

    return overall_summary_data



Execution Outputs
-----------------


* summaryGNG_dat : [  sub block  nGo nNoGo nAcc   pAcc nGo_Hit nGo_Miss nNoGo_Corr nNoGo_FA   pGo_Hit  pGo_Miss pNoGo_Corr pNoGo_FA RTmeanGo_Hit RTmeanNoGo_FA RTmedGo_Hit RTmedNoGo_FA
0  31   all  150    50  175  0.875     146        4         29       21  0.973333  0.026667       0.58     0.42   483.438356     434.52381       476.5        341.0
1  31    b1   30    10   37  0.925      30        0          7        3       1.0       0.0        0.7      0.3   507.233333    312.666667       498.5        300.0
2  31    b2   30    10    0    0.0      28        2          3        7  0.933333  0.066667        0.3      0.7   488.964286    498.857143       506.5        333.0
3  31    b3   30    10    0    0.0      28        2          6        4  0.933333  0.066667        0.6      0.4   442.678571        374.25       435.5        327.0
4  31    b4   30    10    0    0.0      30        0          5        5       1.0       0.0        0.5      0.5   518.033333         476.6       504.5        382.0
5  31    b5   30    10    0    0.0      30        0          8        2       1.0       0.0        0.8      0.2   457.933333         407.5       449.0        407.5,   sub block  nGo nNoGo nAcc   pAcc nGo_Hit nGo_Miss nNoGo_Corr nNoGo_FA   pGo_Hit  pGo_Miss pNoGo_Corr pNoGo_FA RTmeanGo_Hit RTmeanNoGo_FA RTmedGo_Hit RTmedNoGo_FA
0  33   all  150    50  178   0.89     146        4         32       18  0.973333  0.026667       0.64     0.36   649.671233         481.5       646.5        493.5
1  33    b1   30    10   35  0.875      28        2          7        3  0.933333  0.066667        0.7      0.3   636.178571    513.333333       646.5        518.0
2  33    b2   30    10    0    0.0      30        0          9        1       1.0       0.0        0.9      0.1   686.333333         454.0       676.0        454.0
3  33    b3   30    10    0    0.0      29        1          7        3  0.966667  0.033333        0.7      0.3   648.724138    545.333333       606.0        538.0
4  33    b4   30    10    0    0.0      30        0          4        6       1.0       0.0        0.4      0.6   672.366667    440.833333       660.0        425.0
5  33    b5   30    10    0    0.0      29        1          5        5  0.966667  0.033333        0.5      0.5   602.241379         478.4       577.0        542.0,   sub block  nGo nNoGo nAcc   pAcc nGo_Hit nGo_Miss nNoGo_Corr nNoGo_FA   pGo_Hit  pGo_Miss pNoGo_Corr pNoGo_FA RTmeanGo_Hit RTmeanNoGo_FA RTmedGo_Hit RTmedNoGo_FA
0  34   all  150    50  179  0.895     146        4         33       17  0.973333  0.026667       0.66     0.34   538.780822    462.941176       530.0        457.0
1  34    b1   30    10   34   0.85      29        1          5        5  0.966667  0.033333        0.5      0.5   522.862069         428.0       509.0        414.0
2  34    b2   30    10    0    0.0      29        1          7        3  0.966667  0.033333        0.7      0.3   558.551724    545.666667       549.0        497.0
3  34    b3   30    10    0    0.0      30        0          7        3       1.0       0.0        0.7      0.3   528.433333    381.333333       498.0        370.0
4  34    b4   30    10    0    0.0      29        1          7        3  0.966667  0.033333        0.7      0.3   561.034483    481.666667       549.0        491.0
5  34    b5   30    10    0    0.0      29        1          7        3  0.966667  0.033333        0.7      0.3    523.37931    501.333333       513.0        520.0,   sub block  nGo nNoGo nAcc   pAcc nGo_Hit nGo_Miss nNoGo_Corr nNoGo_FA   pGo_Hit  pGo_Miss pNoGo_Corr pNoGo_FA RTmeanGo_Hit RTmeanNoGo_FA RTmedGo_Hit RTmedNoGo_FA
0  35   all  150    50  179  0.895     143        7         36       14  0.953333  0.046667       0.72     0.28   606.265734    514.642857       581.0        511.5
1  35    b1   30    10   38   0.95      29        1          9        1  0.966667  0.033333        0.9      0.1   578.758621         470.0       580.0        470.0
2  35    b2   30    10    0    0.0      27        3          6        4       0.9       0.1        0.6      0.4   598.777778         511.0       589.0        518.0
3  35    b3   30    10    0    0.0      29        1          7        3  0.966667  0.033333        0.7      0.3   599.034483    555.666667       581.0        510.0
4  35    b4   30    10    0    0.0      28        2          7        3  0.933333  0.066667        0.7      0.3   643.321429    540.666667       630.0        519.0
5  35    b5   30    10    0    0.0      30        0          7        3       1.0       0.0        0.7      0.3        612.0    467.333333       558.5        493.0,   sub block  nGo nNoGo nAcc   pAcc nGo_Hit nGo_Miss nNoGo_Corr nNoGo_FA   pGo_Hit  pGo_Miss pNoGo_Corr pNoGo_FA RTmeanGo_Hit RTmeanNoGo_FA RTmedGo_Hit RTmedNoGo_FA
0  36   all  150    50  175  0.875     147        3         28       22      0.98      0.02       0.56     0.44    447.55102    418.863636       434.0        392.0
1  36    b1   30    10   37  0.925      30        0          7        3       1.0       0.0        0.7      0.3        441.6    335.333333       430.5        317.0
2  36    b2   30    10    0    0.0      30        0          6        4       1.0       0.0        0.6      0.4   459.066667        340.25       420.0        351.0
3  36    b3   30    10    0    0.0      30        0          6        4       1.0       0.0        0.6      0.4   463.133333         486.0       443.5        490.5
4  36    b4   30    10    0    0.0      29        1          5        5  0.966667  0.033333        0.5      0.5   432.517241         351.4       427.0        371.0
5  36    b5   30    10    0    0.0      28        2          4        6  0.933333  0.066667        0.4      0.6   440.464286         524.5       432.0        478.0]


Subnode reports
---------------


 subnode 0 : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/GNG/summaryData/mapflow/_summaryData0/_report/report.rst
 subnode 1 : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/GNG/summaryData/mapflow/_summaryData1/_report/report.rst
 subnode 2 : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/GNG/summaryData/mapflow/_summaryData2/_report/report.rst
 subnode 3 : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/GNG/summaryData/mapflow/_summaryData3/_report/report.rst
 subnode 4 : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/GNG/summaryData/mapflow/_summaryData4/_report/report.rst

