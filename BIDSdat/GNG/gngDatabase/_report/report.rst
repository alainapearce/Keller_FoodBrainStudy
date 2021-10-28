Node: gngDatabase (utility)
===========================


 Hierarchy : GNG.gngDatabase
 Exec ID : gngDatabase


Original Inputs
---------------


* GNG_summary_dat : [  sub block  nGo nNoGo nAcc   pAcc nGo_Hit nGo_Miss nNoGo_Corr nNoGo_FA pGo_Hit pGo_Miss  ...  z_Hit_mm   z_FA_mm  z_Hit_ll   z_FA_ll d_prime_mm d_prime_ll A_prime_mm A_prime_ll      c_mm      c_ll Grier_beta_mm Grier_beta_ll
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

* overwrite_flag : False


Execution Inputs
----------------


* GNG_summary_dat : [  sub block  nGo nNoGo nAcc   pAcc nGo_Hit nGo_Miss nNoGo_Corr nNoGo_FA pGo_Hit pGo_Miss  ...  z_Hit_mm   z_FA_mm  z_Hit_ll   z_FA_ll d_prime_mm d_prime_ll A_prime_mm A_prime_ll      c_mm      c_ll Grier_beta_mm Grier_beta_ll
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

* overwrite_flag : False


Execution Outputs
-----------------


* GNG_database :     sub  all_nGo  all_nNoGo  all_nAcc  all_pAcc  all_nGo_Hit  all_nGo_Miss  all_nNoGo_Corr  ...  b5_pGo_Hit  b5_pGo_Miss  b5_pNoGo_Corr  b5_pNoGo_FA  b5_RTmeanGo_Hit  b5_RTmeanNoGo_FA  b5_RTmedGo_Hit  b5_RTmedNoGo_FA
0     2      150         50       189     0.945          149             1              40  ...       1.000        0.000            0.7          0.3          525.833           405.667           541.5            399.0
1     3      150         50       183     0.915          140            10              43  ...       1.000        0.000            0.6          0.4          574.367           409.250           564.5            456.0
2    51      150         50         2     0.010            2           148               0  ...       0.033        0.967            0.0          1.0          468.000           610.900           468.0            634.5
3     1      150         50       180     0.900          148             2              32  ...       1.000        0.000            0.6          0.4          472.733           397.500           473.0            382.0
4     4      150         50       171     0.855          143             7              28  ...       0.967        0.033            0.5          0.5          559.172           461.000           501.0            461.0
5     5      150         50       187     0.935          150             0              37  ...       1.000        0.000            0.6          0.4          538.633           425.500           554.5            405.5
6     6      150         50       182     0.910          147             3              35  ...       0.967        0.033            0.7          0.3          622.690           432.667           601.0            469.0
7     7      150         50       180     0.900          150             0              30  ...       1.000        0.000            0.7          0.3          525.467           428.333           528.5            447.0
8     9      150         50       157     0.785          138            12              19  ...       0.867        0.133            0.3          0.7          386.538           371.714           381.5            394.0
9    11      150         50       190     0.950          148             2              42  ...       0.967        0.033            0.9          0.1          476.345           315.000           482.0            315.0
10   17      150         50       173     0.865          148             2              25  ...       1.000        0.000            0.5          0.5          550.500           554.800           541.0            463.0
11   18      150         50       184     0.920          150             0              34  ...       1.000        0.000            0.7          0.3          507.633           510.667           525.5            488.0
12   19      150         50       176     0.880          145             5              31  ...       1.000        0.000            0.4          0.6          557.900           412.500           511.0            397.0
13   20      150         50       174     0.870          143             7              31  ...       0.833        0.167            0.7          0.3          643.240           421.000           627.0            411.0
14   21      150         50       185     0.925          148             2              37  ...       0.967        0.033            0.8          0.2          594.724           381.000           588.0            381.0
15   22      150         50       180     0.900          144             6              36  ...       0.933        0.067            0.6          0.4          618.857           507.500           591.0            510.5
16   23      150         50       171     0.855          138            12              33  ...       1.000        0.000            0.8          0.2          528.733           552.000           542.0            552.0
0    26      150         50       191     0.955          150             0              41  ...       1.000        0.000            0.7          0.3          552.600           433.667           554.5            446.0
1    28      150         50       177     0.885          147             3              30  ...       0.967        0.033            0.4          0.6          462.103           435.333           443.0            391.5
2    30      150         50       183     0.915          144             6              39  ...       1.000        0.000            0.8          0.2          588.167           456.000           587.5            456.0

[20 rows x 111 columns]
* GNG_database_wide :     sub block  nGo  nNoGo  nAcc   pAcc  nGo_Hit  nGo_Miss  nNoGo_Corr  nNoGo_FA  pGo_Hit  ...  z_FA_mm  z_Hit_ll  z_FA_ll  d_prime_mm d_prime_ll  A_prime_mm A_prime_ll   c_mm   c_ll  Grier_beta_mm  Grier_beta_ll
0     2    b1   30     10    37  0.925       30         0           7         3    1.000  ...   -0.524     2.141   -0.473       2.652      2.614       0.918      0.913  0.802  0.834         -0.855         -0.864
1     2    b2   30     10    40  1.000       30         0          10         0    1.000  ...   -1.645     2.141   -1.691       3.773      3.832       0.983      0.984  0.242  0.225         -0.487         -0.464
2     2    b3   30     10    36  0.900       29         1           7         3    0.967  ...   -0.524     1.661   -0.473       2.358      2.133       0.911      0.899  0.655  0.594         -0.734         -0.650
3     2    b4   30     10    39  0.975       30         0           9         1    1.000  ...   -1.282     2.141   -1.097       3.410      3.238       0.970      0.961  0.423  0.522         -0.692         -0.763
4     2    b5   30     10    37  0.925       30         0           7         3    1.000  ...   -0.524     2.141   -0.473       2.652      2.614       0.918      0.913  0.802  0.834         -0.855         -0.864
..  ...   ...  ...    ...   ...    ...      ...       ...         ...       ...      ...  ...      ...       ...      ...         ...        ...         ...        ...    ...    ...            ...            ...
1    30    b1   30     10    37  0.925       30         0           7         3    1.000  ...   -0.524     2.141   -0.473       2.652      2.614       0.918      0.913  0.802  0.834         -0.855         -0.864
2    30    b2   30     10    38  0.950       28         2          10         0    0.933  ...   -1.645     1.401   -1.691       3.146      3.091       0.969      0.967 -0.072 -0.145          0.134          0.262
3    30    b3   30     10    37  0.925       28         2           9         1    0.933  ...   -1.282     1.401   -1.097       2.783      2.498       0.955      0.940  0.110  0.152         -0.182         -0.227
4    30    b4   30     10    33  0.825       28         2           5         5    0.933  ...    0.000     1.401    0.000       1.501      1.401       0.833      0.824  0.751  0.700         -0.601         -0.543
5    30    b5   30     10    38  0.950       30         0           8         2    1.000  ...   -0.842     2.141   -0.748       2.970      2.889       0.944      0.937  0.643  0.697         -0.814         -0.834

[100 rows x 32 columns]


Runtime info
------------


* duration : 0.041417
* hostname : H8-NTR-GCH12202
* prev_wd : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* working_dir : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/GNG/gngDatabase


Environment
~~~~~~~~~~~


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
* MANPATH : /opt/homebrew/share/man:
* MINC_BIN_DIR : /Users/baf44/freesurfer/mni/bin
* MINC_LIB_DIR : /Users/baf44/freesurfer/mni/lib
* MNI_DATAPATH : /Users/baf44/freesurfer/mni/data
* MNI_DIR : /Users/baf44/freesurfer/mni
* MNI_PERL5LIB : /Users/baf44/freesurfer/mni/lib/../Library/Perl/Updates/5.12.3
* OLDPWD : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data
* OS : Darwin
* PATH : /Users/baf44/opt/anaconda3/bin:/Users/baf44/opt/anaconda3/condabin:/opt/homebrew/bin:/opt/homebrew/sbin:/Users/baf44/freesurfer/bin:/Users/baf44/freesurfer/fsfast/bin:/Users/baf44/freesurfer/mni/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Users/baf44/abin
* PERL5LIB : /Users/baf44/freesurfer/mni/lib/../Library/Perl/Updates/5.12.3
* PWD : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code
* SECURITYSESSIONID : 186a5
* SHELL : /bin/bash
* SHLVL : 1
* SSH_AUTH_SOCK : /private/tmp/com.apple.launchd.K6iD4B8TJB/Listeners
* SUBJECTS_DIR : /Users/baf44/freesurfer/subjects
* TERM : xterm-256color
* TERM_PROGRAM : Apple_Terminal
* TERM_PROGRAM_VERSION : 440
* TERM_SESSION_ID : DEB3169F-06AD-466E-9DE9-29C66603AEC1
* TMPDIR : /var/folders/73/mkrc96td4nv8hyspvjhndxt40000gp/T/
* USER : baf44
* XPC_FLAGS : 0x0
* XPC_SERVICE_NAME : 0
* _ : ./GNG_WF.py
* _CE_CONDA : 
* _CE_M : 
* __CFBundleIdentifier : com.apple.Terminal

