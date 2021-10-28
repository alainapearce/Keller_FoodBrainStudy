Node: utility
=============


 Hierarchy : _summaryData0
 Exec ID : _summaryData0


Original Inputs
---------------


* GNG_file : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-002/ses-1/beh/sub-002_ses-1_task-gng_events.tsv
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


* GNG_file : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-002/ses-1/beh/sub-002_ses-1_task-gng_events.tsv
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


* summaryGNG_dat :   sub block  nGo nNoGo nAcc   pAcc nGo_Hit nGo_Miss nNoGo_Corr  ...   z_FA_ll d_prime_mm d_prime_ll A_prime_mm A_prime_ll      c_mm      c_ll Grier_beta_mm Grier_beta_ll
0   2   all  150    50  189  0.945     149        1         40  ... -0.820792   3.316361   3.149632   0.947581   0.944886  0.816559  0.754024     -0.920512     -0.886516
1   2    b1   30    10   37  0.925      30        0          7  ... -0.472789   2.652446   2.613987   0.917776   0.913237  0.801822  0.834204     -0.855215     -0.863676
2   2    b2   30    10   40    1.0      30        0         10  ... -1.690622   3.772899    3.83182   0.982902   0.984226  0.241596  0.225288     -0.486957     -0.464408
3   2    b3   30    10   36    0.9      29        1          7  ... -0.472789   2.358315   2.133487   0.910509   0.898668  0.654757  0.593954     -0.733945     -0.649826
4   2    b4   30    10   39  0.975      30        0          9  ... -1.096804   3.409597   3.238002   0.969947   0.960681  0.423247  0.522197     -0.691906     -0.762508
5   2    b5   30    10   37  0.925      30        0          7  ... -0.472789   2.652446   2.613987   0.917776   0.913237  0.801822  0.834204     -0.855215     -0.863676

[6 rows x 32 columns]


Runtime info
------------


* duration : 0.519617
* hostname : H8-NTR-GCH12202
* prev_wd : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code
* working_dir : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code/GNG/summaryData/mapflow/_summaryData0


Environment
~~~~~~~~~~~


* COLORTERM : truecolor
* COMMAND_MODE : unix2003
* CONDA_DEFAULT_ENV : base
* CONDA_EXE : /Users/baf44/opt/anaconda3/bin/conda
* CONDA_PREFIX : /Users/baf44/opt/anaconda3
* CONDA_PROMPT_MODIFIER : (base) 
* CONDA_PYTHON_EXE : /Users/baf44/opt/anaconda3/bin/python
* CONDA_SHLVL : 1
* DISPLAY : /private/tmp/com.apple.launchd.cocWWLGA0Z/org.xquartz:0
* FIX_VERTEX_AREA : 
* FMRI_ANALYSIS_DIR : /Users/baf44/freesurfer/fsfast
* FREESURFER : /Users/baf44/freesurfer
* FREESURFER_HOME : /Users/baf44/freesurfer
* FSFAST_HOME : /Users/baf44/freesurfer/fsfast
* FSF_OUTPUT_FORMAT : nii.gz
* FS_OVERRIDE : 0
* FUNCTIONALS_DIR : /Users/baf44/freesurfer/sessions
* GIT_ASKPASS : /Applications/Visual Studio Code.app/Contents/Resources/app/extensions/git/dist/askpass.sh
* HOME : /Users/baf44
* HOMEBREW_CELLAR : /opt/homebrew/Cellar
* HOMEBREW_PREFIX : /opt/homebrew
* HOMEBREW_REPOSITORY : /opt/homebrew
* HOMEBREW_SHELLENV_PREFIX : /opt/homebrew
* INFOPATH : /opt/homebrew/share/info:
* LANG : en_US.UTF-8
* LOCAL_DIR : /Users/baf44/freesurfer/local
* LOGNAME : baf44
* LaunchInstanceID : DF683324-4730-42C2-BFF3-FE6A6C2C2D9E
* MANPATH : /usr/share/man:/usr/local/share/man:/opt/X11/share/man:/opt/homebrew/share/man
* MINC_BIN_DIR : /Users/baf44/freesurfer/mni/bin
* MINC_LIB_DIR : /Users/baf44/freesurfer/mni/lib
* MNI_DATAPATH : /Users/baf44/freesurfer/mni/data
* MNI_DIR : /Users/baf44/freesurfer/mni
* MNI_PERL5LIB : /Users/baf44/freesurfer/mni/lib/../Library/Perl/Updates/5.12.3
* OLDPWD : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* ORIGINAL_XDG_CURRENT_DESKTOP : undefined
* OS : Darwin
* PATH : /Users/baf44/freesurfer/bin:/Users/baf44/freesurfer/fsfast/bin:/Users/baf44/freesurfer/mni/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Users/baf44/opt/anaconda3/bin:/Users/baf44/opt/anaconda3/condabin:/opt/homebrew/bin:/opt/homebrew/sbin:/Users/baf44/freesurfer/bin:/Users/baf44/freesurfer/fsfast/bin:/Users/baf44/freesurfer/mni/bin:/Users/baf44/abin:/Users/baf44/abin
* PERL5LIB : /Users/baf44/freesurfer/mni/lib/../Library/Perl/Updates/5.12.3
* PWD : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* PYDEVD_USE_FRAME_EVAL : NO
* PYTHONIOENCODING : UTF-8
* PYTHONUNBUFFERED : 1
* SECURITYSESSIONID : 186a5
* SHELL : /bin/bash
* SHLVL : 2
* SSH_AUTH_SOCK : /private/tmp/com.apple.launchd.K6iD4B8TJB/Listeners
* SUBJECTS_DIR : /Users/baf44/freesurfer/subjects
* TERM : xterm-256color
* TERM_PROGRAM : vscode
* TERM_PROGRAM_VERSION : 1.61.1
* TMPDIR : /var/folders/73/mkrc96td4nv8hyspvjhndxt40000gp/T/
* USER : baf44
* VSCODE_GIT_ASKPASS_MAIN : /Applications/Visual Studio Code.app/Contents/Resources/app/extensions/git/dist/askpass-main.js
* VSCODE_GIT_ASKPASS_NODE : /Applications/Visual Studio Code.app/Contents/Frameworks/Code Helper (Renderer).app/Contents/MacOS/Code Helper (Renderer)
* VSCODE_GIT_IPC_HANDLE : /var/folders/73/mkrc96td4nv8hyspvjhndxt40000gp/T/vscode-git-ff1f1ca801.sock
* XPC_FLAGS : 0x0
* XPC_SERVICE_NAME : 0
* _ : /usr/bin/env
* _CE_CONDA : 
* _CE_M : 
* __CFBundleIdentifier : com.microsoft.VSCode
* __CF_USER_TEXT_ENCODING : 0x1F6:0x0:0x0

