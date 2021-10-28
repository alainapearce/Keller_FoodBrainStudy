Node: summaryData (utility)
===========================


 Hierarchy : GNG.summaryData
 Exec ID : summaryData


Original Inputs
---------------


* GNG_file : ['/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-026/ses-1/beh/sub-026_ses-1_task-gng_events.tsv', '/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-028/ses-1/beh/sub-028_ses-1_task-gng_events.tsv', '/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-030/ses-1/beh/sub-030_ses-1_task-gng_events.tsv']
* function_str : def summaryGNG(GNG_file):
    import numpy as np
    import pandas as pd
    from scipy.stats import norm

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

        # Accuracy
        nAcc = GNG_data[GNG_data.trial_acc == '1'].shape[0]
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

        ####  Compute signal detection theory metrics ####
        #get z-score for hit and false alarm rates
        #add adjustments for extreme values because norm.ppf of 0/1 is -inf/inf
        z_Hit = norm.ppf(pGo_Hit)
        z_FA = norm.ppf(pNoGo_FA)

        #do Macmillian adjustments for extreme values: if hit rate = 1, new hit
        #rate = (nGo - 0.5)/nGo; if false alarm rate = 0, new false alarm rate
        #= 0.5/nNoGo. If no extreme value, then just save standard calculation
        #for z in that place

        if pGo_Hit == 1:
            pHit_mm = (nGo - 0.5)/nGo
            z_Hit_mm = norm.ppf(pHit_mm)
        else:
            pHit_mm = pGo_Hit
            z_Hit_mm = norm.ppf(pHit_mm)

        if pNoGo_FA == 0:
            pFA_mm = 0.5/nNoGo
            z_FA_mm = norm.ppf(pFA_mm)
        else:
            pFA_mm = pNoGo_FA
            z_FA_mm = norm.ppf(pFA_mm)

        #do loglinear adjustments: add 0.5 to NUMBER of hits and FA and add 1
        #to number of Go and NoGo trials. Then caluculate z off of new hit and
        #FA rates
        nHit_ll = nGo_Hit + 0.5
        nGo_ll = nGo + 1
        nFA_ll = nNoGo_FA + 0.5
        nNoGo_ll = nNoGo + 1
        pHit_ll = nHit_ll/nGo_ll
        pFA_ll = nFA_ll/nNoGo_ll
        z_Hit_ll = norm.ppf(pHit_ll)
        z_FA_ll = norm.ppf(pFA_ll)

        #calculate sensory sensitivity d'
        d_prime_mm = z_Hit_mm - z_FA_mm
        d_prime_ll = z_Hit_ll - z_FA_ll

        #calculate nonparametric sensory sensitivity A':
        #0.5+[sign(H-FA)*((H-FA)^2 + |H-FA|)/(4*max(H, FA) - 4*H*FA))
        A_prime_mm = 0.5 + np.sign(pHit_mm-pFA_mm)*(((pHit_mm-pFA_mm)**2+abs(pHit_mm - pFA_mm))/(4*max(pHit_mm, pFA_mm) - 4*pHit_mm*pFA_mm))
        A_prime_ll = 0.5 + np.sign(pHit_ll-pFA_ll)*(((pHit_ll-pFA_ll)**2+abs(pHit_ll - pFA_ll))/(4*max(pHit_ll, pFA_ll) - 4*pHit_ll*pFA_ll))

        #calculate c (criterion)
        c_mm = (norm.ppf(pHit_mm) + norm.ppf(pFA_mm))/2
        c_ll = (norm.ppf(pHit_ll) + norm.ppf(pFA_ll))/2

        #calculate Grier's Beta--beta", a nonparametric response bias
        Grier_beta_mm = np.sign(pHit_mm-pFA_mm)*((pHit_mm*(1-pHit_mm)-pFA_mm*(1-pFA_mm))/(pHit_mm*(1-pHit_mm)+pFA_mm*(1-pFA_mm)))
        Grier_beta_ll = np.sign(pHit_ll-pFA_ll)*((pHit_ll*(1-pHit_ll)-pFA_ll*(1-pFA_ll))/(pHit_ll*(1-pHit_ll)+pFA_ll*(1-pFA_ll)))

        #combine into array    
        summary_results = [nGo, nNoGo, nAcc, pAcc, nGo_Hit, nGo_Miss, nNoGo_Corr, nNoGo_FA, pGo_Hit, 
                           pGo_Miss, pNoGo_Corr, pNoGo_FA, RTmeanGo_Hit, RTmeanNoGo_FA, RTmedGo_Hit, RTmedNoGo_FA,
                           z_Hit, z_FA, z_Hit_mm, z_FA_mm, z_Hit_ll, z_FA_ll, d_prime_mm, d_prime_ll, A_prime_mm,
                           A_prime_ll, c_mm, c_ll, Grier_beta_mm, Grier_beta_ll]

        return(summary_results)

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
                        'RTmeanNoGo_FA', 'RTmedGo_Hit', 'RTmedNoGo_FA',
                        'z_Hit', 'z_FA', 'z_Hit_mm', 'z_FA_mm', 'z_Hit_ll', 'z_FA_ll', 'd_prime_mm', 
                        'd_prime_ll','A_prime_mm', 'A_prime_ll', 'c_mm', 'c_ll', 'Grier_beta_mm', 'Grier_beta_ll']

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


* GNG_file : ['/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-026/ses-1/beh/sub-026_ses-1_task-gng_events.tsv', '/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-028/ses-1/beh/sub-028_ses-1_task-gng_events.tsv', '/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-030/ses-1/beh/sub-030_ses-1_task-gng_events.tsv']
* function_str : def summaryGNG(GNG_file):
    import numpy as np
    import pandas as pd
    from scipy.stats import norm

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

        # Accuracy
        nAcc = GNG_data[GNG_data.trial_acc == '1'].shape[0]
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

        ####  Compute signal detection theory metrics ####
        #get z-score for hit and false alarm rates
        #add adjustments for extreme values because norm.ppf of 0/1 is -inf/inf
        z_Hit = norm.ppf(pGo_Hit)
        z_FA = norm.ppf(pNoGo_FA)

        #do Macmillian adjustments for extreme values: if hit rate = 1, new hit
        #rate = (nGo - 0.5)/nGo; if false alarm rate = 0, new false alarm rate
        #= 0.5/nNoGo. If no extreme value, then just save standard calculation
        #for z in that place

        if pGo_Hit == 1:
            pHit_mm = (nGo - 0.5)/nGo
            z_Hit_mm = norm.ppf(pHit_mm)
        else:
            pHit_mm = pGo_Hit
            z_Hit_mm = norm.ppf(pHit_mm)

        if pNoGo_FA == 0:
            pFA_mm = 0.5/nNoGo
            z_FA_mm = norm.ppf(pFA_mm)
        else:
            pFA_mm = pNoGo_FA
            z_FA_mm = norm.ppf(pFA_mm)

        #do loglinear adjustments: add 0.5 to NUMBER of hits and FA and add 1
        #to number of Go and NoGo trials. Then caluculate z off of new hit and
        #FA rates
        nHit_ll = nGo_Hit + 0.5
        nGo_ll = nGo + 1
        nFA_ll = nNoGo_FA + 0.5
        nNoGo_ll = nNoGo + 1
        pHit_ll = nHit_ll/nGo_ll
        pFA_ll = nFA_ll/nNoGo_ll
        z_Hit_ll = norm.ppf(pHit_ll)
        z_FA_ll = norm.ppf(pFA_ll)

        #calculate sensory sensitivity d'
        d_prime_mm = z_Hit_mm - z_FA_mm
        d_prime_ll = z_Hit_ll - z_FA_ll

        #calculate nonparametric sensory sensitivity A':
        #0.5+[sign(H-FA)*((H-FA)^2 + |H-FA|)/(4*max(H, FA) - 4*H*FA))
        A_prime_mm = 0.5 + np.sign(pHit_mm-pFA_mm)*(((pHit_mm-pFA_mm)**2+abs(pHit_mm - pFA_mm))/(4*max(pHit_mm, pFA_mm) - 4*pHit_mm*pFA_mm))
        A_prime_ll = 0.5 + np.sign(pHit_ll-pFA_ll)*(((pHit_ll-pFA_ll)**2+abs(pHit_ll - pFA_ll))/(4*max(pHit_ll, pFA_ll) - 4*pHit_ll*pFA_ll))

        #calculate c (criterion)
        c_mm = (norm.ppf(pHit_mm) + norm.ppf(pFA_mm))/2
        c_ll = (norm.ppf(pHit_ll) + norm.ppf(pFA_ll))/2

        #calculate Grier's Beta--beta", a nonparametric response bias
        Grier_beta_mm = np.sign(pHit_mm-pFA_mm)*((pHit_mm*(1-pHit_mm)-pFA_mm*(1-pFA_mm))/(pHit_mm*(1-pHit_mm)+pFA_mm*(1-pFA_mm)))
        Grier_beta_ll = np.sign(pHit_ll-pFA_ll)*((pHit_ll*(1-pHit_ll)-pFA_ll*(1-pFA_ll))/(pHit_ll*(1-pHit_ll)+pFA_ll*(1-pFA_ll)))

        #combine into array    
        summary_results = [nGo, nNoGo, nAcc, pAcc, nGo_Hit, nGo_Miss, nNoGo_Corr, nNoGo_FA, pGo_Hit, 
                           pGo_Miss, pNoGo_Corr, pNoGo_FA, RTmeanGo_Hit, RTmeanNoGo_FA, RTmedGo_Hit, RTmedNoGo_FA,
                           z_Hit, z_FA, z_Hit_mm, z_FA_mm, z_Hit_ll, z_FA_ll, d_prime_mm, d_prime_ll, A_prime_mm,
                           A_prime_ll, c_mm, c_ll, Grier_beta_mm, Grier_beta_ll]

        return(summary_results)

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
                        'RTmeanNoGo_FA', 'RTmedGo_Hit', 'RTmedNoGo_FA',
                        'z_Hit', 'z_FA', 'z_Hit_mm', 'z_FA_mm', 'z_Hit_ll', 'z_FA_ll', 'd_prime_mm', 
                        'd_prime_ll','A_prime_mm', 'A_prime_ll', 'c_mm', 'c_ll', 'Grier_beta_mm', 'Grier_beta_ll']

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


* summaryGNG_dat : [  sub block  nGo nNoGo nAcc   pAcc nGo_Hit nGo_Miss nNoGo_Corr nNoGo_FA pGo_Hit pGo_Miss  ...  z_Hit_mm   z_FA_mm  z_Hit_ll   z_FA_ll d_prime_mm d_prime_ll A_prime_mm A_prime_ll      c_mm      c_ll Grier_beta_mm Grier_beta_ll
0  26   all  150    50  191  0.955     150        0         41        9     1.0      0.0  ...  2.713052 -0.915365  2.715253 -0.891709   3.628417   3.606962   0.953833   0.952259  0.898843  0.911772     -0.955974     -0.957382
1  26    b1   30    10   38   0.95      30        0          8        2     1.0      0.0  ...  2.128045 -0.841621  2.141198 -0.747859   2.969666   2.889057   0.943944   0.937032  0.643212   0.69667     -0.814173     -0.834258
2  26    b2   30    10   38   0.95      30        0          8        2     1.0      0.0  ...  2.128045 -0.841621  2.141198 -0.747859   2.969666   2.889057   0.943944   0.937032  0.643212   0.69667     -0.814173     -0.834258
3  26    b3   30    10   40    1.0      30        0         10        0     1.0      0.0  ...  2.128045 -1.644854  2.141198 -1.690622   3.772899    3.83182   0.982902   0.984226  0.241596  0.225288     -0.486957     -0.464408
4  26    b4   30    10   38   0.95      30        0          8        2     1.0      0.0  ...  2.128045 -0.841621  2.141198 -0.747859   2.969666   2.889057   0.943944   0.937032  0.643212   0.69667     -0.814173     -0.834258
5  26    b5   30    10   37  0.925      30        0          7        3     1.0      0.0  ...  2.128045 -0.524401  2.141198 -0.472789   2.652446   2.613987   0.917776   0.913237  0.801822  0.834204     -0.855215     -0.863676

[6 rows x 32 columns],   sub block  nGo nNoGo nAcc   pAcc nGo_Hit nGo_Miss nNoGo_Corr nNoGo_FA   pGo_Hit  ...   z_FA_mm  z_Hit_ll   z_FA_ll d_prime_mm d_prime_ll A_prime_mm A_prime_ll      c_mm      c_ll Grier_beta_mm Grier_beta_ll
0  28   all  150    50  177  0.885     147        3         30       20      0.98  ... -0.253347  1.992123 -0.248275   2.307096   2.240398   0.889626   0.887436  0.900201  0.871924     -0.848998      -0.82784
1  28    b1   30    10   35  0.875      30        0          5        5       1.0  ...       0.0  2.141198       0.0   2.128045   2.141198   0.864548   0.864886  1.064023  1.070599     -0.876955     -0.880626
2  28    b2   30    10   36    0.9      29        1          7        3  0.966667  ... -0.524401  1.660698 -0.472789   2.358315   2.133487   0.910509   0.898668  0.654757  0.593954     -0.733945     -0.649826
3  28    b3   30    10   38   0.95      30        0          8        2       1.0  ... -0.841621  2.141198 -0.747859   2.969666   2.889057   0.943944   0.937032  0.643212   0.69667     -0.814173     -0.834258
4  28    b4   30    10   35  0.875      29        1          6        4  0.966667  ... -0.253347  1.660698 -0.229884   2.087262   1.890582   0.882663   0.872056  0.790284  0.715407     -0.763265     -0.679995
5  28    b5   30    10   33  0.825      29        1          4        6  0.966667  ...  0.253347  1.660698  0.229884   1.580568   1.430813   0.823994   0.815191  1.043631  0.945291     -0.763265     -0.679995

[6 rows x 32 columns],   sub block  nGo nNoGo nAcc   pAcc nGo_Hit nGo_Miss nNoGo_Corr nNoGo_FA   pGo_Hit  ...   z_FA_mm  z_Hit_ll   z_FA_ll d_prime_mm d_prime_ll A_prime_mm A_prime_ll      c_mm      c_ll Grier_beta_mm Grier_beta_ll
0  30   all  150    50  183  0.915     144        6         39       11      0.96  ... -0.772193  1.716379 -0.753782   2.522879    2.47016   0.929888   0.927197  0.489246  0.481299     -0.634286     -0.618293
1  30    b1   30    10   37  0.925      30        0          7        3       1.0  ... -0.524401  2.141198 -0.472789   2.652446   2.613987   0.917776   0.913237  0.801822  0.834204     -0.855215     -0.863676
2  30    b2   30    10   38   0.95      28        2         10        0  0.933333  ... -1.644854  1.400745 -1.690622    3.14594   3.091367   0.969063   0.966518 -0.071884 -0.144938      0.134177      0.261662
3  30    b3   30    10   37  0.925      28        2          9        1  0.933333  ... -1.281552  1.400745 -1.096804   2.782638   2.497549   0.954696   0.939574  0.109767  0.151971     -0.182482     -0.227331
4  30    b4   30    10   33  0.825      28        2          5        5  0.933333  ...       0.0  1.400745       0.0   1.501086   1.400745   0.832738   0.823713  0.750543  0.700373     -0.601423     -0.542536
5  30    b5   30    10   38   0.95      30        0          8        2       1.0  ... -0.841621  2.141198 -0.747859   2.969666   2.889057   0.943944   0.937032  0.643212   0.69667     -0.814173     -0.834258

[6 rows x 32 columns]]


Subnode reports
---------------


 subnode 0 : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/GNG/summaryData/mapflow/_summaryData0/_report/report.rst
 subnode 1 : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/GNG/summaryData/mapflow/_summaryData1/_report/report.rst
 subnode 2 : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/GNG/summaryData/mapflow/_summaryData2/_report/report.rst

