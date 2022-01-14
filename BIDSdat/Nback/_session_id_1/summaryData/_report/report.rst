Node: summaryData (utility)
===========================


 Hierarchy : Nback.summaryData
 Exec ID : summaryData.a0


Original Inputs
---------------


* Nback_file : ['No subfiles']
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


* Nback_file : ['No subfiles']
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


* summaryNback_dat : ['no files']


Subnode reports
---------------


 subnode 0 : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/Nback/_session_id_1/summaryData/mapflow/_summaryData0/_report/report.rst

