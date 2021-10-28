Node: gngDatabase (utility)
===========================


 Hierarchy : GNG.gngDatabase
 Exec ID : gngDatabase


Original Inputs
---------------


* GNG_summary_dat : [  sub block  nGo nNoGo nAcc   pAcc nGo_Hit nGo_Miss nNoGo_Corr  ...   z_FA_ll d_prime_mm d_prime_ll A_prime_mm A_prime_ll      c_mm      c_ll Grier_beta_mm Grier_beta_ll
0   2   all  150    50  189  0.945     149        1         40  ... -0.820792   3.316361   3.149632   0.947581   0.944886  0.816559  0.754024     -0.920512     -0.886516
1   2    b1   30    10   37  0.925      30        0          7  ... -0.472789   2.652446   2.613987   0.917776   0.913237  0.801822  0.834204     -0.855215     -0.863676
2   2    b2   30    10   40    1.0      30        0         10  ... -1.690622   3.772899    3.83182   0.982902   0.984226  0.241596  0.225288     -0.486957     -0.464408
3   2    b3   30    10   36    0.9      29        1          7  ... -0.472789   2.358315   2.133487   0.910509   0.898668  0.654757  0.593954     -0.733945     -0.649826
4   2    b4   30    10   39  0.975      30        0          9  ... -1.096804   3.409597   3.238002   0.969947   0.960681  0.423247  0.522197     -0.691906     -0.762508
5   2    b5   30    10   37  0.925      30        0          7  ... -0.472789   2.652446   2.613987   0.917776   0.913237  0.801822  0.834204     -0.855215     -0.863676

[6 rows x 32 columns]]
* bids_dir : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* function_str : def updateDatabase_save(GNG_summary_dat, overwrite_flag, bids_dir):
    import pandas as pd
    import numpy as np
    from pathlib import Path
    from nipype.interfaces.base import Bunch

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

        #get condition subset (overall and each block)
        #GNG_summary_dat['block'] = GNG_summary_dat['block'].astype(str)
        GNG_summary_conditions = GNG_summary_dat[GNG_summary_dat.block.isin(['all', 'b1', 'b2', 'b3', 'b4', 'b5'])]

        #make wide data set (for every variable, a column for overall and each block)
        GNG_summary_wide = GNG_summary_conditions.pivot(columns='block', index='sub', values=columnnames[2:])        
        GNG_summary_wide.columns = ['_'.join(col) for col in GNG_summary_wide.columns.reorder_levels(order=[1, 0])]

        #remove SDT variables by block from wide dataset
        block_sdt_vars =    ['b1_z_Hit', 'b1_z_FA', 'b1_z_Hit_mm', 'b1_z_FA_mm', 'b1_z_Hit_ll', 'b1_z_FA_ll', 'b1_d_prime_mm', 
                            'b1_d_prime_ll', 'b1_A_prime_mm', 'b1_A_prime_ll', 'b1_c_mm', 'b1_c_ll', 'b1_Grier_beta_mm', 'b1_Grier_beta_ll',

                            'b2_z_Hit', 'b2_z_FA', 'b2_z_Hit_mm', 'b2_z_FA_mm', 'b2_z_Hit_ll', 'b2_z_FA_ll', 'b2_d_prime_mm', 
                            'b2_d_prime_ll', 'b2_A_prime_mm', 'b2_A_prime_ll', 'b2_c_mm', 'b2_c_ll', 'b2_Grier_beta_mm', 'b2_Grier_beta_ll',

                            'b3_z_Hit', 'b3_z_FA', 'b3_z_Hit_mm', 'b3_z_FA_mm', 'b3_z_Hit_ll', 'b3_z_FA_ll', 'b3_d_prime_mm', 
                            'b3_d_prime_ll', 'b3_A_prime_mm', 'b3_A_prime_ll', 'b3_c_mm', 'b3_c_ll', 'b3_Grier_beta_mm', 'b3_Grier_beta_ll',

                            'b4_z_Hit', 'b4_z_FA', 'b4_z_Hit_mm', 'b4_z_FA_mm', 'b4_z_Hit_ll', 'b4_z_FA_ll', 'b4_d_prime_mm', 
                            'b4_d_prime_ll', 'b4_A_prime_mm', 'b4_A_prime_ll', 'b4_c_mm', 'b4_c_ll', 'b4_Grier_beta_mm', 'b4_Grier_beta_ll',

                            'b5_z_Hit', 'b5_z_FA', 'b5_z_Hit_mm', 'b5_z_FA_mm', 'b5_z_Hit_ll', 'b5_z_FA_ll', 'b5_d_prime_mm', 
                            'b5_d_prime_ll', 'b5_A_prime_mm', 'b5_A_prime_ll', 'b5_c_mm', 'b5_c_ll', 'b5_Grier_beta_mm', 'b5_Grier_beta_ll']

        GNG_summary_wide = GNG_summary_wide.drop(columns=block_sdt_vars)

        #make the sub index into a dataset column
        GNG_summary_wide = GNG_summary_wide.reset_index(level = 0)

        #re-order columns
        columnnames_reorder = ['sub', 'all_nGo', 'all_nNoGo', 'all_nAcc', 'all_pAcc', 'all_nGo_Hit', 'all_nGo_Miss', 'all_nNoGo_Corr', 
                              'all_nNoGo_FA', 'all_pGo_Hit', 'all_pGo_Miss', 'all_pNoGo_Corr', 'all_pNoGo_FA', 'all_RTmeanGo_Hit', 
                              'all_RTmeanNoGo_FA', 'all_RTmedGo_Hit', 'all_RTmedNoGo_FA',

                              'all_z_Hit', 'all_z_FA', 'all_z_Hit_mm', 'all_z_FA_mm', 'all_z_Hit_ll', 'all_z_FA_ll', 'all_d_prime_mm', 
                              'all_d_prime_ll', 'all_A_prime_mm', 'all_A_prime_ll', 'all_c_mm', 'all_c_ll', 'all_Grier_beta_mm', 'all_Grier_beta_ll',

                              'b1_nGo', 'b1_nNoGo', 'b1_nAcc', 'b1_pAcc', 'b1_nGo_Hit', 'b1_nGo_Miss', 'b1_nNoGo_Corr', 
                              'b1_nNoGo_FA', 'b1_pGo_Hit', 'b1_pGo_Miss', 'b1_pNoGo_Corr', 'b1_pNoGo_FA', 'b1_RTmeanGo_Hit', 
                              'b1_RTmeanNoGo_FA', 'b1_RTmedGo_Hit', 'b1_RTmedNoGo_FA',

                              'b2_nGo', 'b2_nNoGo', 'b2_nAcc', 'b2_pAcc', 'b2_nGo_Hit', 'b2_nGo_Miss', 'b2_nNoGo_Corr', 
                              'b2_nNoGo_FA', 'b2_pGo_Hit', 'b2_pGo_Miss', 'b2_pNoGo_Corr', 'b2_pNoGo_FA', 'b2_RTmeanGo_Hit', 
                              'b2_RTmeanNoGo_FA', 'b2_RTmedGo_Hit', 'b2_RTmedNoGo_FA',

                              'b3_nGo', 'b3_nNoGo', 'b3_nAcc', 'b3_pAcc', 'b3_nGo_Hit', 'b3_nGo_Miss', 'b3_nNoGo_Corr', 
                              'b3_nNoGo_FA', 'b3_pGo_Hit', 'b3_pGo_Miss', 'b3_pNoGo_Corr', 'b3_pNoGo_FA', 'b3_RTmeanGo_Hit', 
                              'b3_RTmeanNoGo_FA', 'b3_RTmedGo_Hit', 'b3_RTmedNoGo_FA',

                              'b4_nGo', 'b4_nNoGo', 'b4_nAcc', 'b4_pAcc', 'b4_nGo_Hit', 'b4_nGo_Miss', 'b4_nNoGo_Corr', 
                              'b4_nNoGo_FA', 'b4_pGo_Hit', 'b4_pGo_Miss', 'b4_pNoGo_Corr', 'b4_pNoGo_FA', 'b4_RTmeanGo_Hit', 
                              'b4_RTmeanNoGo_FA', 'b4_RTmedGo_Hit', 'b4_RTmedNoGo_FA',

                              'b5_nGo', 'b5_nNoGo', 'b5_nAcc', 'b5_pAcc', 'b5_nGo_Hit', 'b5_nGo_Miss', 'b5_nNoGo_Corr', 
                              'b5_nNoGo_FA', 'b5_pGo_Hit', 'b5_pGo_Miss', 'b5_pNoGo_Corr', 'b5_pNoGo_FA', 'b5_RTmeanGo_Hit', 
                              'b5_RTmeanNoGo_FA', 'b5_RTmedGo_Hit', 'b5_RTmedNoGo_FA']

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
        print('No raw data files that need to be processed')
        GNG_database = np.nan
        GNG_database_long = np.nan

    return GNG_database, GNG_database_long

* overwrite_flag : True


Execution Inputs
----------------


* GNG_summary_dat : [  sub block  nGo nNoGo nAcc   pAcc nGo_Hit nGo_Miss nNoGo_Corr  ...   z_FA_ll d_prime_mm d_prime_ll A_prime_mm A_prime_ll      c_mm      c_ll Grier_beta_mm Grier_beta_ll
0   2   all  150    50  189  0.945     149        1         40  ... -0.820792   3.316361   3.149632   0.947581   0.944886  0.816559  0.754024     -0.920512     -0.886516
1   2    b1   30    10   37  0.925      30        0          7  ... -0.472789   2.652446   2.613987   0.917776   0.913237  0.801822  0.834204     -0.855215     -0.863676
2   2    b2   30    10   40    1.0      30        0         10  ... -1.690622   3.772899    3.83182   0.982902   0.984226  0.241596  0.225288     -0.486957     -0.464408
3   2    b3   30    10   36    0.9      29        1          7  ... -0.472789   2.358315   2.133487   0.910509   0.898668  0.654757  0.593954     -0.733945     -0.649826
4   2    b4   30    10   39  0.975      30        0          9  ... -1.096804   3.409597   3.238002   0.969947   0.960681  0.423247  0.522197     -0.691906     -0.762508
5   2    b5   30    10   37  0.925      30        0          7  ... -0.472789   2.652446   2.613987   0.917776   0.913237  0.801822  0.834204     -0.855215     -0.863676

[6 rows x 32 columns]]
* bids_dir : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* function_str : def updateDatabase_save(GNG_summary_dat, overwrite_flag, bids_dir):
    import pandas as pd
    import numpy as np
    from pathlib import Path
    from nipype.interfaces.base import Bunch

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

        #get condition subset (overall and each block)
        #GNG_summary_dat['block'] = GNG_summary_dat['block'].astype(str)
        GNG_summary_conditions = GNG_summary_dat[GNG_summary_dat.block.isin(['all', 'b1', 'b2', 'b3', 'b4', 'b5'])]

        #make wide data set (for every variable, a column for overall and each block)
        GNG_summary_wide = GNG_summary_conditions.pivot(columns='block', index='sub', values=columnnames[2:])        
        GNG_summary_wide.columns = ['_'.join(col) for col in GNG_summary_wide.columns.reorder_levels(order=[1, 0])]

        #remove SDT variables by block from wide dataset
        block_sdt_vars =    ['b1_z_Hit', 'b1_z_FA', 'b1_z_Hit_mm', 'b1_z_FA_mm', 'b1_z_Hit_ll', 'b1_z_FA_ll', 'b1_d_prime_mm', 
                            'b1_d_prime_ll', 'b1_A_prime_mm', 'b1_A_prime_ll', 'b1_c_mm', 'b1_c_ll', 'b1_Grier_beta_mm', 'b1_Grier_beta_ll',

                            'b2_z_Hit', 'b2_z_FA', 'b2_z_Hit_mm', 'b2_z_FA_mm', 'b2_z_Hit_ll', 'b2_z_FA_ll', 'b2_d_prime_mm', 
                            'b2_d_prime_ll', 'b2_A_prime_mm', 'b2_A_prime_ll', 'b2_c_mm', 'b2_c_ll', 'b2_Grier_beta_mm', 'b2_Grier_beta_ll',

                            'b3_z_Hit', 'b3_z_FA', 'b3_z_Hit_mm', 'b3_z_FA_mm', 'b3_z_Hit_ll', 'b3_z_FA_ll', 'b3_d_prime_mm', 
                            'b3_d_prime_ll', 'b3_A_prime_mm', 'b3_A_prime_ll', 'b3_c_mm', 'b3_c_ll', 'b3_Grier_beta_mm', 'b3_Grier_beta_ll',

                            'b4_z_Hit', 'b4_z_FA', 'b4_z_Hit_mm', 'b4_z_FA_mm', 'b4_z_Hit_ll', 'b4_z_FA_ll', 'b4_d_prime_mm', 
                            'b4_d_prime_ll', 'b4_A_prime_mm', 'b4_A_prime_ll', 'b4_c_mm', 'b4_c_ll', 'b4_Grier_beta_mm', 'b4_Grier_beta_ll',

                            'b5_z_Hit', 'b5_z_FA', 'b5_z_Hit_mm', 'b5_z_FA_mm', 'b5_z_Hit_ll', 'b5_z_FA_ll', 'b5_d_prime_mm', 
                            'b5_d_prime_ll', 'b5_A_prime_mm', 'b5_A_prime_ll', 'b5_c_mm', 'b5_c_ll', 'b5_Grier_beta_mm', 'b5_Grier_beta_ll']

        GNG_summary_wide = GNG_summary_wide.drop(columns=block_sdt_vars)

        #make the sub index into a dataset column
        GNG_summary_wide = GNG_summary_wide.reset_index(level = 0)

        #re-order columns
        columnnames_reorder = ['sub', 'all_nGo', 'all_nNoGo', 'all_nAcc', 'all_pAcc', 'all_nGo_Hit', 'all_nGo_Miss', 'all_nNoGo_Corr', 
                              'all_nNoGo_FA', 'all_pGo_Hit', 'all_pGo_Miss', 'all_pNoGo_Corr', 'all_pNoGo_FA', 'all_RTmeanGo_Hit', 
                              'all_RTmeanNoGo_FA', 'all_RTmedGo_Hit', 'all_RTmedNoGo_FA',

                              'all_z_Hit', 'all_z_FA', 'all_z_Hit_mm', 'all_z_FA_mm', 'all_z_Hit_ll', 'all_z_FA_ll', 'all_d_prime_mm', 
                              'all_d_prime_ll', 'all_A_prime_mm', 'all_A_prime_ll', 'all_c_mm', 'all_c_ll', 'all_Grier_beta_mm', 'all_Grier_beta_ll',

                              'b1_nGo', 'b1_nNoGo', 'b1_nAcc', 'b1_pAcc', 'b1_nGo_Hit', 'b1_nGo_Miss', 'b1_nNoGo_Corr', 
                              'b1_nNoGo_FA', 'b1_pGo_Hit', 'b1_pGo_Miss', 'b1_pNoGo_Corr', 'b1_pNoGo_FA', 'b1_RTmeanGo_Hit', 
                              'b1_RTmeanNoGo_FA', 'b1_RTmedGo_Hit', 'b1_RTmedNoGo_FA',

                              'b2_nGo', 'b2_nNoGo', 'b2_nAcc', 'b2_pAcc', 'b2_nGo_Hit', 'b2_nGo_Miss', 'b2_nNoGo_Corr', 
                              'b2_nNoGo_FA', 'b2_pGo_Hit', 'b2_pGo_Miss', 'b2_pNoGo_Corr', 'b2_pNoGo_FA', 'b2_RTmeanGo_Hit', 
                              'b2_RTmeanNoGo_FA', 'b2_RTmedGo_Hit', 'b2_RTmedNoGo_FA',

                              'b3_nGo', 'b3_nNoGo', 'b3_nAcc', 'b3_pAcc', 'b3_nGo_Hit', 'b3_nGo_Miss', 'b3_nNoGo_Corr', 
                              'b3_nNoGo_FA', 'b3_pGo_Hit', 'b3_pGo_Miss', 'b3_pNoGo_Corr', 'b3_pNoGo_FA', 'b3_RTmeanGo_Hit', 
                              'b3_RTmeanNoGo_FA', 'b3_RTmedGo_Hit', 'b3_RTmedNoGo_FA',

                              'b4_nGo', 'b4_nNoGo', 'b4_nAcc', 'b4_pAcc', 'b4_nGo_Hit', 'b4_nGo_Miss', 'b4_nNoGo_Corr', 
                              'b4_nNoGo_FA', 'b4_pGo_Hit', 'b4_pGo_Miss', 'b4_pNoGo_Corr', 'b4_pNoGo_FA', 'b4_RTmeanGo_Hit', 
                              'b4_RTmeanNoGo_FA', 'b4_RTmedGo_Hit', 'b4_RTmedNoGo_FA',

                              'b5_nGo', 'b5_nNoGo', 'b5_nAcc', 'b5_pAcc', 'b5_nGo_Hit', 'b5_nGo_Miss', 'b5_nNoGo_Corr', 
                              'b5_nNoGo_FA', 'b5_pGo_Hit', 'b5_pGo_Miss', 'b5_pNoGo_Corr', 'b5_pNoGo_FA', 'b5_RTmeanGo_Hit', 
                              'b5_RTmeanNoGo_FA', 'b5_RTmedGo_Hit', 'b5_RTmedNoGo_FA']

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
        print('No raw data files that need to be processed')
        GNG_database = np.nan
        GNG_database_long = np.nan

    return GNG_database, GNG_database_long

* overwrite_flag : True


Execution Outputs
-----------------


* GNG_database :    sub  all_nGo  all_nNoGo  all_nAcc  all_pAcc  all_nGo_Hit  ...  b5_pNoGo_FA  b5_RTmeanGo_Hit  b5_RTmeanNoGo_FA  b5_RTmedGo_Hit  b5_RTmedNoGo_FA  all_Grier_beta_mm
1    3      150         50       183     0.915          140  ...          0.4          574.367           409.250           564.5            456.0              0.776
0    2      150         50       189     0.945          149  ...          0.3          525.833           405.667           541.5            399.0             -0.921

[2 rows x 112 columns]
* GNG_database_wide :    sub block  nGo  nNoGo  nAcc   pAcc  nGo_Hit  nGo_Miss  nNoGo_Corr  ...  z_FA_ll  d_prime_mm  d_prime_ll  A_prime_mm  A_prime_ll   c_mm   c_ll  Grier_beta_mm Grier_beta_ll
1    2    b1   30     10    37  0.925       30         0           7  ...   -0.473       2.652       2.614       0.918       0.913  0.802  0.834         -0.855        -0.864
2    2    b2   30     10    40  1.000       30         0          10  ...   -1.691       3.773       3.832       0.983       0.984  0.242  0.225         -0.487        -0.464
3    2    b3   30     10    36  0.900       29         1           7  ...   -0.473       2.358       2.133       0.911       0.899  0.655  0.594         -0.734        -0.650
4    2    b4   30     10    39  0.975       30         0           9  ...   -1.097       3.410       3.238       0.970       0.961  0.423  0.522         -0.692        -0.763
5    2    b5   30     10    37  0.925       30         0           7  ...   -0.473       2.652       2.614       0.918       0.913  0.802  0.834         -0.855        -0.864

[5 rows x 32 columns]


Runtime info
------------


* duration : 0.143349
* hostname : H8-NTR-GCH12202
* prev_wd : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code
* working_dir : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code/GNG/gngDatabase


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

