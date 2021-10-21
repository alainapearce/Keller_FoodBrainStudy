Node: utility
=============


 Hierarchy : _summaryData0
 Exec ID : _summaryData0


Original Inputs
---------------


* GNG_file : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-051/ses-1/beh/sub-051_ses-1_task-gng_events.tsv
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


* GNG_file : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-051/ses-1/beh/sub-051_ses-1_task-gng_events.tsv
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


* summaryGNG_dat :   sub block  nGo nNoGo nAcc   pAcc nGo_Hit nGo_Miss nNoGo_Corr nNoGo_FA   pGo_Hit  pGo_Miss pNoGo_Corr pNoGo_FA RTmeanGo_Hit RTmeanNoGo_FA RTmedGo_Hit RTmedNoGo_FA
0  51   all  150    50    2   0.01       2      148          0       50  0.013333  0.986667        0.0      1.0        708.0         624.7       708.0        587.0
1  51    b1   30    10    1  0.025       1       29          0       10  0.033333  0.966667        0.0      1.0        948.0         633.1       948.0        626.0
2  51    b2   30    10    0    0.0       0       30          0       10       0.0       1.0        0.0      1.0         <NA>         630.9        <NA>        576.0
3  51    b3   30    10    0    0.0       0       30          0       10       0.0       1.0        0.0      1.0         <NA>         668.6        <NA>        618.5
4  51    b4   30    10    0    0.0       0       30          0       10       0.0       1.0        0.0      1.0         <NA>         580.0        <NA>        537.5
5  51    b5   30    10    0    0.0       1       29          0       10  0.033333  0.966667        0.0      1.0        468.0         610.9       468.0        634.5


Runtime info
------------


* duration : 0.387609
* hostname : H8-NTR-GCH12202
* prev_wd : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code
* working_dir : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code/GNG/summaryData/mapflow/_summaryData0


Environment
~~~~~~~~~~~


* APPLICATION_INSIGHTS_NO_DIAGNOSTIC_CHANNEL : true
* COLORTERM : truecolor
* COMMAND_MODE : unix2003
* CONDA_DEFAULT_ENV : base
* CONDA_EXE : /Users/baf44/opt/anaconda3/bin/conda
* CONDA_PREFIX : /Users/baf44/opt/anaconda3
* CONDA_PROMPT_MODIFIER : (base) 
* CONDA_PYTHON_EXE : /Users/baf44/opt/anaconda3/bin/python
* CONDA_SHLVL : 1
* DISPLAY : /private/tmp/com.apple.launchd.HNyHFHddaJ/org.xquartz:0
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
* MANPATH : /usr/share/man:/usr/local/share/man:/opt/X11/share/man:/opt/homebrew/share/man
* MINC_BIN_DIR : /Users/baf44/freesurfer/mni/bin
* MINC_LIB_DIR : /Users/baf44/freesurfer/mni/lib
* MNI_DATAPATH : /Users/baf44/freesurfer/mni/data
* MNI_DIR : /Users/baf44/freesurfer/mni
* MNI_PERL5LIB : /Users/baf44/freesurfer/mni/lib/../Library/Perl/Updates/5.12.3
* OLDPWD : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code
* ORIGINAL_XDG_CURRENT_DESKTOP : undefined
* OS : Darwin
* PATH : /Users/baf44/freesurfer/bin:/Users/baf44/freesurfer/fsfast/bin:/Users/baf44/freesurfer/mni/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/Users/baf44/freesurfer/bin:/Users/baf44/freesurfer/fsfast/bin:/Users/baf44/freesurfer/mni/bin:/Users/baf44/opt/anaconda3/bin:/Users/baf44/opt/anaconda3/condabin:/Users/baf44/abin:/Users/baf44/abin
* PERL5LIB : /Users/baf44/freesurfer/mni/lib/../Library/Perl/Updates/5.12.3
* PWD : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code
* PYDEVD_USE_FRAME_EVAL : NO
* PYTHONIOENCODING : UTF-8
* PYTHONUNBUFFERED : 1
* SHELL : /bin/zsh
* SHLVL : 3
* SQLITE_EXEMPT_PATH_FROM_VNODE_GUARDS : /Users/baf44/Library/WebKit/Databases
* SSH_AUTH_SOCK : /private/tmp/com.apple.launchd.IGHDFDpBhr/Listeners
* SUBJECTS_DIR : /Users/baf44/freesurfer/subjects
* TERM : xterm-256color
* TERM_PROGRAM : vscode
* TERM_PROGRAM_VERSION : 1.61.1
* TMPDIR : /var/folders/73/mkrc96td4nv8hyspvjhndxt40000gp/T/
* USER : baf44
* VSCODE_GIT_ASKPASS_MAIN : /Applications/Visual Studio Code.app/Contents/Resources/app/extensions/git/dist/askpass-main.js
* VSCODE_GIT_ASKPASS_NODE : /Applications/Visual Studio Code.app/Contents/Frameworks/Code Helper (Renderer).app/Contents/MacOS/Code Helper (Renderer)
* VSCODE_GIT_IPC_HANDLE : /var/folders/73/mkrc96td4nv8hyspvjhndxt40000gp/T/vscode-git-0ab1e11d68.sock
* XPC_FLAGS : 0x0
* XPC_SERVICE_NAME : 0
* _ : /usr/bin/env
* _CE_CONDA : 
* _CE_M : 
* __CFBundleIdentifier : com.microsoft.VSCode
* __CF_USER_TEXT_ENCODING : 0x1F6:0x0:0x0

