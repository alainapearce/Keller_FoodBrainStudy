Node: gngDatabase (utility)
===========================


 Hierarchy : GNG.gngDatabase
 Exec ID : gngDatabase


Original Inputs
---------------


* GNG_summary_dat : [   sub block  nGo nNoGo nAcc  ... A_prime_ll     c_mm     c_ll Grier_beta_mm Grier_beta_ll
0  113   all  150    50  166  ...   0.827762  1.59038  1.58655     -0.969924     -0.970289
1  113    b1   30    10   33  ...   0.814078  1.32622  1.30699     -0.855215     -0.863676
2  113    b2   30    10   32  ...   0.785909  1.48483  1.44453     -0.814173     -0.834258
3  113    b3   30    10   35  ...   0.864886  1.06402   1.0706     -0.876955     -0.880626
4  113    b4   30    10   33  ...   0.814078  1.32622  1.30699     -0.855215     -0.863676
5  113    b5   30    10   33  ...   0.814078  1.32622  1.30699     -0.855215     -0.863676

[6 rows x 32 columns]]
* bids_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* function_str : def updateDatabase_save(GNG_summary_dat, overwrite_flag, bids_dir):
    import pandas as pd
    import numpy as np
    from pathlib import Path
    from nipype.interfaces.base import Bunch

    #check to see if it is filepath str or 'no files' message
    if isinstance(GNG_summary_dat[0], str):

        print('******** No new data to be processed ********')

        GNG_database = 'no new data files'
        GNG_database_long = 'no new data files'

    else:
        #get a Bunch object if more than 1 participant
        if isinstance(GNG_summary_dat, Bunch):
            #get output data from node
            GNG_summary_datlist = GNG_summary_dat.summaryGNG_dat

            #combine datasets
            GNG_summary_dat = pd.concat(GNG_summary_datlist)

        #if only 1 participant/dataset then it is a list
        elif isinstance(GNG_summary_dat, list):
            if len(GNG_summary_dat) == 1:
                GNG_summary_dat = GNG_summary_dat[0]
            else:
                GNG_summary_dat = pd.concat(GNG_summary_dat)

        #if a pandas dataframe
        if isinstance(GNG_summary_dat, pd.DataFrame):

            #get column names
            columnnames = GNG_summary_dat.columns

            print(GNG_summary_dat.sub)

            #get condition subset (overall and each block)
            #GNG_summary_dat['block'] = GNG_summary_dat['block'].astype(str)
            GNG_summary_conditions = GNG_summary_dat[GNG_summary_dat.block.isin(['all', 'b1', 'b2', 'b3', 'b4', 'b5'])]

            #make wide data set (for every variable, a column for overall and each block)
            GNG_summary_wide = GNG_summary_conditions.pivot(columns='block', index='sub', values=columnnames[2:])
            GNG_summary_wide.columns = ['_'.join(col) for col in GNG_summary_wide.columns.reorder_levels(order=[1, 0])]

            #remove SDT variables by block from wide dataset
            block_sdt_vars =    ['b1_z_Hit', 'b1_z_FA', 'b1_z_Hit_mm', 'b1_z_FA_mm', 'b1_z_Hit_ll', 'b1_z_FA_ll', 'b1_d_prime_mm',  'b1_d_prime_ll', 'b1_A_prime_mm', 'b1_A_prime_ll', 'b1_c_mm', 'b1_c_ll', 'b1_Grier_beta_mm', 'b1_Grier_beta_ll', 'b2_z_Hit', 'b2_z_FA', 'b2_z_Hit_mm', 'b2_z_FA_mm', 'b2_z_Hit_ll', 'b2_z_FA_ll', 'b2_d_prime_mm',  'b2_d_prime_ll', 'b2_A_prime_mm', 'b2_A_prime_ll', 'b2_c_mm', 'b2_c_ll', 'b2_Grier_beta_mm', 'b2_Grier_beta_ll', 'b3_z_Hit', 'b3_z_FA', 'b3_z_Hit_mm', 'b3_z_FA_mm', 'b3_z_Hit_ll', 'b3_z_FA_ll', 'b3_d_prime_mm',  'b3_d_prime_ll', 'b3_A_prime_mm', 'b3_A_prime_ll', 'b3_c_mm', 'b3_c_ll', 'b3_Grier_beta_mm', 'b3_Grier_beta_ll', 'b4_z_Hit', 'b4_z_FA', 'b4_z_Hit_mm', 'b4_z_FA_mm', 'b4_z_Hit_ll', 'b4_z_FA_ll', 'b4_d_prime_mm',  'b4_d_prime_ll', 'b4_A_prime_mm', 'b4_A_prime_ll', 'b4_c_mm', 'b4_c_ll', 'b4_Grier_beta_mm', 'b4_Grier_beta_ll', 'b5_z_Hit', 'b5_z_FA', 'b5_z_Hit_mm', 'b5_z_FA_mm', 'b5_z_Hit_ll', 'b5_z_FA_ll', 'b5_d_prime_mm',  'b5_d_prime_ll', 'b5_A_prime_mm', 'b5_A_prime_ll', 'b5_c_mm', 'b5_c_ll', 'b5_Grier_beta_mm', 'b5_Grier_beta_ll']

            GNG_summary_wide = GNG_summary_wide.drop(columns=block_sdt_vars)

            #make the sub index into a dataset column
            GNG_summary_wide = GNG_summary_wide.reset_index(level = 0)

            #re-order columns
            columnnames_reorder = ['sub', 'all_nGo', 'all_nNoGo', 'all_nAcc', 'all_pAcc', 'all_nGo_Hit', 'all_nGo_Miss', 'all_nNoGo_Corr',  'all_nNoGo_FA', 'all_pGo_Hit', 'all_pGo_Miss', 'all_pNoGo_Corr', 'all_pNoGo_FA', 'all_RTmeanGo_Hit',  'all_RTmeanNoGo_FA', 'all_RTmedGo_Hit', 'all_RTmedNoGo_FA', 'all_z_Hit', 'all_z_FA', 'all_z_Hit_mm', 'all_z_FA_mm', 'all_z_Hit_ll', 'all_z_FA_ll', 'all_d_prime_mm',  'all_d_prime_ll', 'all_A_prime_mm', 'all_A_prime_ll', 'all_c_mm', 'all_c_ll', 'all_Grier_beta_mm', 'all_Grier_beta_ll', 'b1_nGo', 'b1_nNoGo', 'b1_nAcc', 'b1_pAcc', 'b1_nGo_Hit', 'b1_nGo_Miss', 'b1_nNoGo_Corr',  'b1_nNoGo_FA', 'b1_pGo_Hit', 'b1_pGo_Miss', 'b1_pNoGo_Corr', 'b1_pNoGo_FA', 'b1_RTmeanGo_Hit',  'b1_RTmeanNoGo_FA', 'b1_RTmedGo_Hit', 'b1_RTmedNoGo_FA', 'b2_nGo', 'b2_nNoGo', 'b2_nAcc', 'b2_pAcc', 'b2_nGo_Hit', 'b2_nGo_Miss', 'b2_nNoGo_Corr',  'b2_nNoGo_FA', 'b2_pGo_Hit', 'b2_pGo_Miss', 'b2_pNoGo_Corr', 'b2_pNoGo_FA', 'b2_RTmeanGo_Hit',  'b2_RTmeanNoGo_FA', 'b2_RTmedGo_Hit', 'b2_RTmedNoGo_FA', 'b3_nGo', 'b3_nNoGo', 'b3_nAcc', 'b3_pAcc', 'b3_nGo_Hit', 'b3_nGo_Miss', 'b3_nNoGo_Corr',  'b3_nNoGo_FA', 'b3_pGo_Hit', 'b3_pGo_Miss', 'b3_pNoGo_Corr', 'b3_pNoGo_FA', 'b3_RTmeanGo_Hit',  'b3_RTmeanNoGo_FA', 'b3_RTmedGo_Hit', 'b3_RTmedNoGo_FA', 'b4_nGo', 'b4_nNoGo', 'b4_nAcc', 'b4_pAcc', 'b4_nGo_Hit', 'b4_nGo_Miss', 'b4_nNoGo_Corr',  'b4_nNoGo_FA', 'b4_pGo_Hit', 'b4_pGo_Miss', 'b4_pNoGo_Corr', 'b4_pNoGo_FA', 'b4_RTmeanGo_Hit',  'b4_RTmeanNoGo_FA', 'b4_RTmedGo_Hit', 'b4_RTmedNoGo_FA', 'b5_nGo', 'b5_nNoGo', 'b5_nAcc', 'b5_pAcc', 'b5_nGo_Hit', 'b5_nGo_Miss', 'b5_nNoGo_Corr',  'b5_nNoGo_FA', 'b5_pGo_Hit', 'b5_pGo_Miss', 'b5_pNoGo_Corr', 'b5_pNoGo_FA', 'b5_RTmeanGo_Hit',  'b5_RTmeanNoGo_FA', 'b5_RTmedGo_Hit', 'b5_RTmedNoGo_FA']

            GNG_summary_wide = GNG_summary_wide.reindex(columns=columnnames_reorder)

            #get indiviudal blocks subset
            GNG_summary_blocks = GNG_summary_dat[GNG_summary_dat.block.isin(['b1', 'b2', 'b3', 'b4', 'b5'])]

            ## load databases
            #derivative data path
            derivative_data_path = Path(bids_dir).joinpath('derivatives/preprocessed/beh')

            #load databases
            GNG_database = pd.read_csv(str(Path(derivative_data_path).joinpath('task-gng_summary.tsv')), sep = '\t')
            GNG_database_long = pd.read_csv(str(Path(derivative_data_path).joinpath('task-gng_summary_long.tsv')), sep = '\t')

            #if overwriting participants
            if overwrite_flag == True:
                #function to drop rows based on values
                def filter_rows_by_values(df, col, values):
                    return df[df[col].isin(values) == False]

                #get list of subs to filter in wide and long data
                wide_sub_list = list(GNG_summary_wide['sub'].unique())
                long_sub_list = list(GNG_summary_blocks['sub'].unique())

                #filter out/remove exisiting subs to overwrite
                GNG_database = filter_rows_by_values(GNG_database, 'sub', wide_sub_list)
                GNG_database_long = filter_rows_by_values(GNG_database_long, 'sub', long_sub_list)

            #add newly processed data
            GNG_database = GNG_database.append(GNG_summary_wide)
            GNG_database_long = GNG_database_long.append(GNG_summary_blocks)

            #round to 3 decimal points
            GNG_database = GNG_database.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)
            GNG_database_long = GNG_database_long.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)

            #write databases
            GNG_database.to_csv(str(Path(derivative_data_path).joinpath('task-gng_summary.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
            GNG_database_long.to_csv(str(Path(derivative_data_path).joinpath('task-gng_summary_long.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

        else:
            print('******** No new data to be processed ********')
            GNG_database = 'no new data files'
            GNG_database_long = 'no new data files'

    return GNG_database, GNG_database_long

* overwrite_flag : False


Execution Inputs
----------------


* GNG_summary_dat : [   sub block  nGo nNoGo nAcc  ... A_prime_ll     c_mm     c_ll Grier_beta_mm Grier_beta_ll
0  113   all  150    50  166  ...   0.827762  1.59038  1.58655     -0.969924     -0.970289
1  113    b1   30    10   33  ...   0.814078  1.32622  1.30699     -0.855215     -0.863676
2  113    b2   30    10   32  ...   0.785909  1.48483  1.44453     -0.814173     -0.834258
3  113    b3   30    10   35  ...   0.864886  1.06402   1.0706     -0.876955     -0.880626
4  113    b4   30    10   33  ...   0.814078  1.32622  1.30699     -0.855215     -0.863676
5  113    b5   30    10   33  ...   0.814078  1.32622  1.30699     -0.855215     -0.863676

[6 rows x 32 columns]]
* bids_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* function_str : def updateDatabase_save(GNG_summary_dat, overwrite_flag, bids_dir):
    import pandas as pd
    import numpy as np
    from pathlib import Path
    from nipype.interfaces.base import Bunch

    #check to see if it is filepath str or 'no files' message
    if isinstance(GNG_summary_dat[0], str):

        print('******** No new data to be processed ********')

        GNG_database = 'no new data files'
        GNG_database_long = 'no new data files'

    else:
        #get a Bunch object if more than 1 participant
        if isinstance(GNG_summary_dat, Bunch):
            #get output data from node
            GNG_summary_datlist = GNG_summary_dat.summaryGNG_dat

            #combine datasets
            GNG_summary_dat = pd.concat(GNG_summary_datlist)

        #if only 1 participant/dataset then it is a list
        elif isinstance(GNG_summary_dat, list):
            if len(GNG_summary_dat) == 1:
                GNG_summary_dat = GNG_summary_dat[0]
            else:
                GNG_summary_dat = pd.concat(GNG_summary_dat)

        #if a pandas dataframe
        if isinstance(GNG_summary_dat, pd.DataFrame):

            #get column names
            columnnames = GNG_summary_dat.columns

            print(GNG_summary_dat.sub)

            #get condition subset (overall and each block)
            #GNG_summary_dat['block'] = GNG_summary_dat['block'].astype(str)
            GNG_summary_conditions = GNG_summary_dat[GNG_summary_dat.block.isin(['all', 'b1', 'b2', 'b3', 'b4', 'b5'])]

            #make wide data set (for every variable, a column for overall and each block)
            GNG_summary_wide = GNG_summary_conditions.pivot(columns='block', index='sub', values=columnnames[2:])
            GNG_summary_wide.columns = ['_'.join(col) for col in GNG_summary_wide.columns.reorder_levels(order=[1, 0])]

            #remove SDT variables by block from wide dataset
            block_sdt_vars =    ['b1_z_Hit', 'b1_z_FA', 'b1_z_Hit_mm', 'b1_z_FA_mm', 'b1_z_Hit_ll', 'b1_z_FA_ll', 'b1_d_prime_mm',  'b1_d_prime_ll', 'b1_A_prime_mm', 'b1_A_prime_ll', 'b1_c_mm', 'b1_c_ll', 'b1_Grier_beta_mm', 'b1_Grier_beta_ll', 'b2_z_Hit', 'b2_z_FA', 'b2_z_Hit_mm', 'b2_z_FA_mm', 'b2_z_Hit_ll', 'b2_z_FA_ll', 'b2_d_prime_mm',  'b2_d_prime_ll', 'b2_A_prime_mm', 'b2_A_prime_ll', 'b2_c_mm', 'b2_c_ll', 'b2_Grier_beta_mm', 'b2_Grier_beta_ll', 'b3_z_Hit', 'b3_z_FA', 'b3_z_Hit_mm', 'b3_z_FA_mm', 'b3_z_Hit_ll', 'b3_z_FA_ll', 'b3_d_prime_mm',  'b3_d_prime_ll', 'b3_A_prime_mm', 'b3_A_prime_ll', 'b3_c_mm', 'b3_c_ll', 'b3_Grier_beta_mm', 'b3_Grier_beta_ll', 'b4_z_Hit', 'b4_z_FA', 'b4_z_Hit_mm', 'b4_z_FA_mm', 'b4_z_Hit_ll', 'b4_z_FA_ll', 'b4_d_prime_mm',  'b4_d_prime_ll', 'b4_A_prime_mm', 'b4_A_prime_ll', 'b4_c_mm', 'b4_c_ll', 'b4_Grier_beta_mm', 'b4_Grier_beta_ll', 'b5_z_Hit', 'b5_z_FA', 'b5_z_Hit_mm', 'b5_z_FA_mm', 'b5_z_Hit_ll', 'b5_z_FA_ll', 'b5_d_prime_mm',  'b5_d_prime_ll', 'b5_A_prime_mm', 'b5_A_prime_ll', 'b5_c_mm', 'b5_c_ll', 'b5_Grier_beta_mm', 'b5_Grier_beta_ll']

            GNG_summary_wide = GNG_summary_wide.drop(columns=block_sdt_vars)

            #make the sub index into a dataset column
            GNG_summary_wide = GNG_summary_wide.reset_index(level = 0)

            #re-order columns
            columnnames_reorder = ['sub', 'all_nGo', 'all_nNoGo', 'all_nAcc', 'all_pAcc', 'all_nGo_Hit', 'all_nGo_Miss', 'all_nNoGo_Corr',  'all_nNoGo_FA', 'all_pGo_Hit', 'all_pGo_Miss', 'all_pNoGo_Corr', 'all_pNoGo_FA', 'all_RTmeanGo_Hit',  'all_RTmeanNoGo_FA', 'all_RTmedGo_Hit', 'all_RTmedNoGo_FA', 'all_z_Hit', 'all_z_FA', 'all_z_Hit_mm', 'all_z_FA_mm', 'all_z_Hit_ll', 'all_z_FA_ll', 'all_d_prime_mm',  'all_d_prime_ll', 'all_A_prime_mm', 'all_A_prime_ll', 'all_c_mm', 'all_c_ll', 'all_Grier_beta_mm', 'all_Grier_beta_ll', 'b1_nGo', 'b1_nNoGo', 'b1_nAcc', 'b1_pAcc', 'b1_nGo_Hit', 'b1_nGo_Miss', 'b1_nNoGo_Corr',  'b1_nNoGo_FA', 'b1_pGo_Hit', 'b1_pGo_Miss', 'b1_pNoGo_Corr', 'b1_pNoGo_FA', 'b1_RTmeanGo_Hit',  'b1_RTmeanNoGo_FA', 'b1_RTmedGo_Hit', 'b1_RTmedNoGo_FA', 'b2_nGo', 'b2_nNoGo', 'b2_nAcc', 'b2_pAcc', 'b2_nGo_Hit', 'b2_nGo_Miss', 'b2_nNoGo_Corr',  'b2_nNoGo_FA', 'b2_pGo_Hit', 'b2_pGo_Miss', 'b2_pNoGo_Corr', 'b2_pNoGo_FA', 'b2_RTmeanGo_Hit',  'b2_RTmeanNoGo_FA', 'b2_RTmedGo_Hit', 'b2_RTmedNoGo_FA', 'b3_nGo', 'b3_nNoGo', 'b3_nAcc', 'b3_pAcc', 'b3_nGo_Hit', 'b3_nGo_Miss', 'b3_nNoGo_Corr',  'b3_nNoGo_FA', 'b3_pGo_Hit', 'b3_pGo_Miss', 'b3_pNoGo_Corr', 'b3_pNoGo_FA', 'b3_RTmeanGo_Hit',  'b3_RTmeanNoGo_FA', 'b3_RTmedGo_Hit', 'b3_RTmedNoGo_FA', 'b4_nGo', 'b4_nNoGo', 'b4_nAcc', 'b4_pAcc', 'b4_nGo_Hit', 'b4_nGo_Miss', 'b4_nNoGo_Corr',  'b4_nNoGo_FA', 'b4_pGo_Hit', 'b4_pGo_Miss', 'b4_pNoGo_Corr', 'b4_pNoGo_FA', 'b4_RTmeanGo_Hit',  'b4_RTmeanNoGo_FA', 'b4_RTmedGo_Hit', 'b4_RTmedNoGo_FA', 'b5_nGo', 'b5_nNoGo', 'b5_nAcc', 'b5_pAcc', 'b5_nGo_Hit', 'b5_nGo_Miss', 'b5_nNoGo_Corr',  'b5_nNoGo_FA', 'b5_pGo_Hit', 'b5_pGo_Miss', 'b5_pNoGo_Corr', 'b5_pNoGo_FA', 'b5_RTmeanGo_Hit',  'b5_RTmeanNoGo_FA', 'b5_RTmedGo_Hit', 'b5_RTmedNoGo_FA']

            GNG_summary_wide = GNG_summary_wide.reindex(columns=columnnames_reorder)

            #get indiviudal blocks subset
            GNG_summary_blocks = GNG_summary_dat[GNG_summary_dat.block.isin(['b1', 'b2', 'b3', 'b4', 'b5'])]

            ## load databases
            #derivative data path
            derivative_data_path = Path(bids_dir).joinpath('derivatives/preprocessed/beh')

            #load databases
            GNG_database = pd.read_csv(str(Path(derivative_data_path).joinpath('task-gng_summary.tsv')), sep = '\t')
            GNG_database_long = pd.read_csv(str(Path(derivative_data_path).joinpath('task-gng_summary_long.tsv')), sep = '\t')

            #if overwriting participants
            if overwrite_flag == True:
                #function to drop rows based on values
                def filter_rows_by_values(df, col, values):
                    return df[df[col].isin(values) == False]

                #get list of subs to filter in wide and long data
                wide_sub_list = list(GNG_summary_wide['sub'].unique())
                long_sub_list = list(GNG_summary_blocks['sub'].unique())

                #filter out/remove exisiting subs to overwrite
                GNG_database = filter_rows_by_values(GNG_database, 'sub', wide_sub_list)
                GNG_database_long = filter_rows_by_values(GNG_database_long, 'sub', long_sub_list)

            #add newly processed data
            GNG_database = GNG_database.append(GNG_summary_wide)
            GNG_database_long = GNG_database_long.append(GNG_summary_blocks)

            #round to 3 decimal points
            GNG_database = GNG_database.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)
            GNG_database_long = GNG_database_long.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)

            #write databases
            GNG_database.to_csv(str(Path(derivative_data_path).joinpath('task-gng_summary.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
            GNG_database_long.to_csv(str(Path(derivative_data_path).joinpath('task-gng_summary_long.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

        else:
            print('******** No new data to be processed ********')
            GNG_database = 'no new data files'
            GNG_database_long = 'no new data files'

    return GNG_database, GNG_database_long

* overwrite_flag : False


Execution Outputs
-----------------


* GNG_database :     sub  all_nGo  all_nNoGo  ...  b5_RTmeanNoGo_FA  b5_RTmedGo_Hit  b5_RTmedNoGo_FA
0     1      150         50  ...           397.500           473.0            382.0
1     2      150         50  ...           405.667           541.5            399.0
2     3      150         50  ...           409.250           564.5            456.0
3     4      150         50  ...           461.000           501.0            461.0
4     5      150         50  ...           425.500           554.5            405.5
..  ...      ...        ...  ...               ...             ...              ...
87  126      150         50  ...           539.000           695.0            547.0
88  127      150         50  ...           400.000           452.0            330.0
89  128      150         50  ...           489.500           643.0            492.0
90  129      150         50  ...           440.571           540.0            436.0
0   113      150         50  ...           375.857           445.0            361.0

[92 rows x 111 columns]
* GNG_database_wide :     sub block  nGo  nNoGo  nAcc  ...  A_prime_ll   c_mm   c_ll  Grier_beta_mm  Grier_beta_ll
0   103    b1   30     10    36  ...       0.899  0.655  0.594         -0.734         -0.650
1   103    b2   30     10    36  ...       0.912  0.330  0.326         -0.440         -0.406
2   103    b3   30     10    36  ...       0.899  0.655  0.594         -0.734         -0.650
3   103    b4   30     10    38  ...       0.950  0.276  0.282         -0.473         -0.438
4   103    b5   30     10    33  ...       0.815  1.044  0.945         -0.763         -0.680
..  ...   ...  ...    ...   ...  ...         ...    ...    ...            ...            ...
1   113    b1   30     10    33  ...       0.814  1.326  1.307         -0.855         -0.864
2   113    b2   30     10    32  ...       0.786  1.485  1.445         -0.814         -0.834
3   113    b3   30     10    35  ...       0.865  1.064  1.071         -0.877         -0.881
4   113    b4   30     10    33  ...       0.814  1.326  1.307         -0.855         -0.864
5   113    b5   30     10    33  ...       0.814  1.326  1.307         -0.855         -0.864

[1120 rows x 32 columns]


Runtime info
------------


* duration : 0.294874
* hostname : nut-azp271-10239
* prev_wd : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* working_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/GNG/gngDatabase


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

