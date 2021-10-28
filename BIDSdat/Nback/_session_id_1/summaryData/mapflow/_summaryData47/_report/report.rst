Node: utility
=============


 Hierarchy : _summaryData47
 Exec ID : _summaryData47


Original Inputs
---------------


* Nback_file : ['/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-106/ses-1/beh/sub-106_ses-1_task-nback0_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-106/ses-1/beh/sub-106_ses-1_task-nback1_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-106/ses-1/beh/sub-106_ses-1_task-nback2_events.tsv']
* function_str : def summaryNback(Nback_file):
    import numpy as np
    import pandas as pd
    from collections.abc import Iterable

    #check if str
    if isinstance(Nback_file, str):

        #check to see if it is filepath str or 'No subfiles' message
        if '.tsv' in Nback_file:
            #if only 1 file, will be string and we want an array
            Nback_file = [Nback_file]
        else:
            Nback_file = []

    if len(Nback_file) > 0:

        #loop counter
        count = 1

        for file in Nback_file:

            #load data - loop throgh participant blockfiles
            Nback_ProcData = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python') 

            #make Acc_Resp column
            Nback_ProcData.fillna('', inplace=True)

            Nback_ProcData.columns = Nback_ProcData.columns.str.replace('b0_', '')
            Nback_ProcData.columns = Nback_ProcData.columns.str.replace('b1_', '')
            Nback_ProcData.columns = Nback_ProcData.columns.str.replace('b2_', '')

            Nback_ProcData['acc_resp'] = np.where(Nback_ProcData['correct'] == Nback_ProcData['stim_resp'], 1, 0)

            Nback_ProcData['procedure_block'] = Nback_ProcData['procedure_block'].replace(['B0BlockProc','B0Block2Proc'],'b0')
            Nback_ProcData['procedure_block'] = Nback_ProcData['procedure_block'].replace(['B1BlockProc','B1Block2Proc'],'b1')
            Nback_ProcData['procedure_block'] = Nback_ProcData['procedure_block'].replace(['B2BlockProc','B2Block2Proc'],'b2')

            #get target and fill datasets
            Nback_Target = Nback_ProcData.groupby('condition').get_group('Target')
            Nback_Fill = Nback_ProcData.groupby('condition').get_group('Fill')

            #trial counts
            nTarget = Nback_Target.shape[0]
            nFill = Nback_Fill.shape[0]
            nTrials = nTarget + nFill

            #Accuracy
            nAcc = Nback_Target['acc_resp'].sum(axis = 0) + Nback_Fill['acc_resp'].sum(axis = 0)
            pAcc = (nAcc/nTrials)*100

            #Go Hits/Misses 
            nTarget_Hit = Nback_Target['acc_resp'].sum(axis = 0)
            pTarget_Hit = (nTarget_Hit/nTarget)*100

            nTarget_Miss = nTarget - nTarget_Hit
            pTarget_Miss = (nTarget_Miss/nTarget)*100

            #NoGo Commissions (False Alarms)
            nFill_Corr = Nback_Fill['acc_resp'].sum(axis = 0)
            pFill_Corr = (nFill_Corr/nFill)*100

            nFill_FA = nFill - nFill_Corr
            pFill_FA = (nFill_FA/nFill)*100

            #Ballanced Acc
            pTarget_BA = (pTarget_Hit + pFill_Corr)/2

            #mean and median RT
            Nback_Target_correct = Nback_Target.groupby('acc_resp').get_group(1)

            RTmeanTarget_Hit = Nback_Target_correct['stim_rt'].mean(axis = 0)
            RTmedTarget_Hit = Nback_Target_correct['stim_rt'].median(axis = 0)

            summaryNback_dat = [Nback_ProcData['sub'][0], Nback_ProcData['ses'][0], Nback_ProcData['procedure_block'][0], nTarget, nFill, nTrials, nAcc, pAcc, nTarget_Hit, pTarget_Hit, nTarget_Miss, pTarget_Miss, nFill_Corr, pFill_Corr, nFill_FA, pFill_FA, pTarget_BA, RTmeanTarget_Hit, RTmedTarget_Hit]

            if count == 1:
                summaryNback_list = summaryNback_dat
                count = count + 1
            else:
                summaryNback_list = np.row_stack((summaryNback_list, summaryNback_dat))
                count = count + 1

    else:
        summaryNback_list = 'no files'

    return summaryNback_list



Execution Inputs
----------------


* Nback_file : ['/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-106/ses-1/beh/sub-106_ses-1_task-nback0_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-106/ses-1/beh/sub-106_ses-1_task-nback1_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-106/ses-1/beh/sub-106_ses-1_task-nback2_events.tsv']
* function_str : def summaryNback(Nback_file):
    import numpy as np
    import pandas as pd
    from collections.abc import Iterable

    #check if str
    if isinstance(Nback_file, str):

        #check to see if it is filepath str or 'No subfiles' message
        if '.tsv' in Nback_file:
            #if only 1 file, will be string and we want an array
            Nback_file = [Nback_file]
        else:
            Nback_file = []

    if len(Nback_file) > 0:

        #loop counter
        count = 1

        for file in Nback_file:

            #load data - loop throgh participant blockfiles
            Nback_ProcData = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python') 

            #make Acc_Resp column
            Nback_ProcData.fillna('', inplace=True)

            Nback_ProcData.columns = Nback_ProcData.columns.str.replace('b0_', '')
            Nback_ProcData.columns = Nback_ProcData.columns.str.replace('b1_', '')
            Nback_ProcData.columns = Nback_ProcData.columns.str.replace('b2_', '')

            Nback_ProcData['acc_resp'] = np.where(Nback_ProcData['correct'] == Nback_ProcData['stim_resp'], 1, 0)

            Nback_ProcData['procedure_block'] = Nback_ProcData['procedure_block'].replace(['B0BlockProc','B0Block2Proc'],'b0')
            Nback_ProcData['procedure_block'] = Nback_ProcData['procedure_block'].replace(['B1BlockProc','B1Block2Proc'],'b1')
            Nback_ProcData['procedure_block'] = Nback_ProcData['procedure_block'].replace(['B2BlockProc','B2Block2Proc'],'b2')

            #get target and fill datasets
            Nback_Target = Nback_ProcData.groupby('condition').get_group('Target')
            Nback_Fill = Nback_ProcData.groupby('condition').get_group('Fill')

            #trial counts
            nTarget = Nback_Target.shape[0]
            nFill = Nback_Fill.shape[0]
            nTrials = nTarget + nFill

            #Accuracy
            nAcc = Nback_Target['acc_resp'].sum(axis = 0) + Nback_Fill['acc_resp'].sum(axis = 0)
            pAcc = (nAcc/nTrials)*100

            #Go Hits/Misses 
            nTarget_Hit = Nback_Target['acc_resp'].sum(axis = 0)
            pTarget_Hit = (nTarget_Hit/nTarget)*100

            nTarget_Miss = nTarget - nTarget_Hit
            pTarget_Miss = (nTarget_Miss/nTarget)*100

            #NoGo Commissions (False Alarms)
            nFill_Corr = Nback_Fill['acc_resp'].sum(axis = 0)
            pFill_Corr = (nFill_Corr/nFill)*100

            nFill_FA = nFill - nFill_Corr
            pFill_FA = (nFill_FA/nFill)*100

            #Ballanced Acc
            pTarget_BA = (pTarget_Hit + pFill_Corr)/2

            #mean and median RT
            Nback_Target_correct = Nback_Target.groupby('acc_resp').get_group(1)

            RTmeanTarget_Hit = Nback_Target_correct['stim_rt'].mean(axis = 0)
            RTmedTarget_Hit = Nback_Target_correct['stim_rt'].median(axis = 0)

            summaryNback_dat = [Nback_ProcData['sub'][0], Nback_ProcData['ses'][0], Nback_ProcData['procedure_block'][0], nTarget, nFill, nTrials, nAcc, pAcc, nTarget_Hit, pTarget_Hit, nTarget_Miss, pTarget_Miss, nFill_Corr, pFill_Corr, nFill_FA, pFill_FA, pTarget_BA, RTmeanTarget_Hit, RTmedTarget_Hit]

            if count == 1:
                summaryNback_list = summaryNback_dat
                count = count + 1
            else:
                summaryNback_list = np.row_stack((summaryNback_list, summaryNback_dat))
                count = count + 1

    else:
        summaryNback_list = 'no files'

    return summaryNback_list



Execution Outputs
-----------------


* summaryNback_dat : [['106' '1' 'b0' '16' '44' '60' '57' '95.0' '16' '100.0' '0' '0.0' '41'
  '93.18181818181817' '3' '6.8181818181818175' '96.5909090909091' '706.5'
  '663.5']
 ['106' '1' 'b1' '16' '44' '60' '52' '86.66666666666667' '12' '75.0' '4'
  '25.0' '40' '90.9090909090909' '4' '9.090909090909092'
  '82.95454545454545' '1009.5833333333334' '923.5']
 ['106' '1' 'b2' '16' '44' '60' '53' '88.33333333333333' '9' '56.25' '7'
  '43.75' '44' '100.0' '0' '0.0' '78.125' '808.0' '632.0']]


Runtime info
------------


* duration : 0.075475
* hostname : ND-NTR-FCH12085
* prev_wd : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* working_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/Nback/_session_id_1/summaryData/mapflow/_summaryData47


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
* HOME : /Users/azp271
* LANG : en_US.UTF-8
* LOGNAME : azp271
* LSCOLORS : ExFxBxDxCxegedabagacad
* OLDPWD : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/orgRaw_scripts
* PATH : /Users/azp271/opt/anaconda3/bin:/Users/azp271/opt/anaconda3/condabin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/TeX/texbin:/opt/X11/bin:/Library/Apple/usr/bin
* PS1 : (base) \[\033[36m\]\u\[\033[m\]@\[\033[32m\]\h:\[\033[33;1m\]\w\[\033[m\]$ 
* PWD : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code
* SHELL : /bin/bash
* SHLVL : 1
* SSH_AUTH_SOCK : /private/tmp/com.apple.launchd.7qhvbO6vQS/Listeners
* TERM : xterm-256color
* TERM_PROGRAM : Apple_Terminal
* TERM_PROGRAM_VERSION : 440
* TERM_SESSION_ID : A30D2AAF-B645-4A29-9775-89587571A8F8
* TMPDIR : /var/folders/y5/lybvr3s93wn9ny273pk2fhgr0000gp/T/
* USER : azp271
* XPC_FLAGS : 0x0
* XPC_SERVICE_NAME : 0
* _ : /Users/azp271/opt/anaconda3/bin/python3
* _CE_CONDA : 
* _CE_M : 
* __CFBundleIdentifier : com.apple.Terminal

