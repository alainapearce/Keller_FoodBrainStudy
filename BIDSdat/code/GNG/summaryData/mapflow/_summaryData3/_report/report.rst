Node: utility
=============


 Hierarchy : _summaryData3
 Exec ID : _summaryData3


Original Inputs
---------------


* GNG_file : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-030/ses-1/beh/sub-030_ses-1_task-gng_events.tsv
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

        # Set accuracy equal to 1 when ca = trial_resp
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
            colnames = ['sub', 'block', 'nGo', 'nNoGo', 'nAcc', 'pAcc', 'nGo_Hit', 'nGo_Miss', 'nNoGo_Corr',  'nNoGo_FA', 'pGo_Hit', 'pGo_Miss', 'pNoGo_Corr', 'pNoGo_FA', 'RTmeanGo_Hit', 'RTmeanNoGo_FA', 'RTmedGo_Hit', 'RTmedNoGo_FA', 'z_Hit', 'z_FA', 'z_Hit_mm', 'z_FA_mm', 'z_Hit_ll', 'z_FA_ll', 'd_prime_mm',  'd_prime_ll','A_prime_mm', 'A_prime_ll', 'c_mm', 'c_ll', 'Grier_beta_mm', 'Grier_beta_ll']

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


* GNG_file : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-030/ses-1/beh/sub-030_ses-1_task-gng_events.tsv
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

        # Set accuracy equal to 1 when ca = trial_resp
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
            colnames = ['sub', 'block', 'nGo', 'nNoGo', 'nAcc', 'pAcc', 'nGo_Hit', 'nGo_Miss', 'nNoGo_Corr',  'nNoGo_FA', 'pGo_Hit', 'pGo_Miss', 'pNoGo_Corr', 'pNoGo_FA', 'RTmeanGo_Hit', 'RTmeanNoGo_FA', 'RTmedGo_Hit', 'RTmedNoGo_FA', 'z_Hit', 'z_FA', 'z_Hit_mm', 'z_FA_mm', 'z_Hit_ll', 'z_FA_ll', 'd_prime_mm',  'd_prime_ll','A_prime_mm', 'A_prime_ll', 'c_mm', 'c_ll', 'Grier_beta_mm', 'Grier_beta_ll']

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


* summaryGNG_dat :   sub block  nGo nNoGo nAcc   pAcc nGo_Hit  ... d_prime_ll A_prime_mm A_prime_ll       c_mm      c_ll Grier_beta_mm Grier_beta_ll
0  30   all  150    50  183  0.915     144  ...    2.47016   0.929888   0.927197   0.489246  0.481299     -0.634286     -0.618293
1  30    b1   30    10   37  0.925      30  ...    2.61399   0.917776   0.913237   0.801822  0.834204     -0.855215     -0.863676
2  30    b2   30    10   38   0.95      28  ...    3.09137   0.969063   0.966518 -0.0718838 -0.144938      0.134177      0.261662
3  30    b3   30    10   37  0.925      28  ...    2.49755   0.954696   0.939574   0.109767  0.151971     -0.182482     -0.227331
4  30    b4   30    10   33  0.825      28  ...    1.40075   0.832738   0.823713   0.750543  0.700373     -0.601423     -0.542536
5  30    b5   30    10   38   0.95      30  ...    2.88906   0.943944   0.937032   0.643212   0.69667     -0.814173     -0.834258

[6 rows x 32 columns]


Runtime info
------------


* duration : 3.376283
* hostname : nut-azp271-10239
* prev_wd : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code
* working_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code/GNG/summaryData/mapflow/_summaryData3


Environment
~~~~~~~~~~~


* CLICOLOR : 1
* COLORTERM : truecolor
* CONDA_DEFAULT_ENV : base
* CONDA_EXE : /Users/azp271/opt/anaconda3/bin/conda
* CONDA_PREFIX : /Users/azp271/opt/anaconda3
* CONDA_PROMPT_MODIFIER : (base) 
* CONDA_PYTHON_EXE : /Users/azp271/opt/anaconda3/bin/python
* CONDA_SHLVL : 1
* DISPLAY : /private/tmp/com.apple.launchd.1mdV9E7QdF/org.xquartz:0
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
* GIT_ASKPASS : /Applications/Visual Studio Code.app/Contents/Resources/app/extensions/git/dist/askpass.sh
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
* OLDPWD : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code
* ORIGINAL_XDG_CURRENT_DESKTOP : undefined
* OS : Darwin
* PATH : /Applications/freesurfer/bin:/Applications/freesurfer/fsfast/bin:/Applications/freesurfer/tktools:/usr/local/fsl/bin:/Applications/freesurfer/mni/bin:/usr/local/fsl/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/TeX/texbin:/opt/X11/bin:/Library/Apple/usr/bin:/Users/azp271/opt/anaconda3/bin:/Users/azp271/opt/anaconda3/condabin:/Applications/freesurfer/bin:/Applications/freesurfer/fsfast/bin:/Applications/freesurfer/tktools:/usr/local/fsl/bin:/Applications/freesurfer/mni/bin:/Users/azp271/abin:/Applications/CMake.app/Contents/bin:/Users/azp271/dcm2niix/build/bin:/Users/azp271/.local/bin:/Users/azp271/pigz-2.6:/Users/azp271/abin:/Applications/CMake.app/Contents/bin:/Users/azp271/dcm2niix/build/bin:/Users/azp271/.local/bin:/Users/azp271/pigz-2.6
* PERL5LIB : /Applications/freesurfer/mni/lib/../Library/Perl/Updates/5.12.3
* PS1 : (base) \[\033[36m\]\u\[\033[m\]@\[\033[32m\]\h:\[\033[33;1m\]\w\[\033[m\]$ 
* PWD : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code
* PYDEVD_USE_FRAME_EVAL : NO
* PYTHONIOENCODING : UTF-8
* PYTHONUNBUFFERED : 1
* SHELL : /bin/bash
* SHLVL : 2
* SSH_AUTH_SOCK : /private/tmp/com.apple.launchd.Eua71eiyFT/Listeners
* SUBJECTS_DIR : /Applications/freesurfer/subjects
* TERM : xterm-256color
* TERM_PROGRAM : vscode
* TERM_PROGRAM_VERSION : 1.63.2
* TMPDIR : /var/folders/3c/pvrbw1ld5290z020487lf9340000gp/T/
* USER : azp271
* VSCODE_GIT_ASKPASS_EXTRA_ARGS : --ms-enable-electron-run-as-node
* VSCODE_GIT_ASKPASS_MAIN : /Applications/Visual Studio Code.app/Contents/Resources/app/extensions/git/dist/askpass-main.js
* VSCODE_GIT_ASKPASS_NODE : /Applications/Visual Studio Code.app/Contents/MacOS/Electron
* VSCODE_GIT_IPC_HANDLE : /var/folders/3c/pvrbw1ld5290z020487lf9340000gp/T/vscode-git-13de00805e.sock
* XPC_FLAGS : 0x0
* XPC_SERVICE_NAME : 0
* _ : /usr/bin/env
* _CE_CONDA : 
* _CE_M : 
* __CF_USER_TEXT_ENCODING : 0x1F6:0x0:0x0

