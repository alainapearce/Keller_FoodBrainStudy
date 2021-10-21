Node: gngDatabase (utility)
===========================


 Hierarchy : GNG.gngDatabase
 Exec ID : gngDatabase


Original Inputs
---------------


* GNG_summary_dat : [  sub block  nGo nNoGo nAcc   pAcc nGo_Hit nGo_Miss nNoGo_Corr nNoGo_FA   pGo_Hit  pGo_Miss pNoGo_Corr pNoGo_FA RTmeanGo_Hit RTmeanNoGo_FA RTmedGo_Hit RTmedNoGo_FA
0  51   all  150    50    2   0.01       2      148          0       50  0.013333  0.986667        0.0      1.0        708.0         624.7       708.0        587.0
1  51    b1   30    10    1  0.025       1       29          0       10  0.033333  0.966667        0.0      1.0        948.0         633.1       948.0        626.0
2  51    b2   30    10    0    0.0       0       30          0       10       0.0       1.0        0.0      1.0         <NA>         630.9        <NA>        576.0
3  51    b3   30    10    0    0.0       0       30          0       10       0.0       1.0        0.0      1.0         <NA>         668.6        <NA>        618.5
4  51    b4   30    10    0    0.0       0       30          0       10       0.0       1.0        0.0      1.0         <NA>         580.0        <NA>        537.5
5  51    b5   30    10    0    0.0       1       29          0       10  0.033333  0.966667        0.0      1.0        468.0         610.9       468.0        634.5]
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

        #make the sub index into a dataset column
        GNG_summary_wide = GNG_summary_wide.reset_index(level = 0)

        #re-order columns
        columnnames_reorder = ['sub', 'all_nGo', 'all_nNoGo', 'all_nAcc', 'all_pAcc', 'all_nGo_Hit', 'all_nGo_Miss', 'all_nNoGo_Corr', 
                              'all_nNoGo_FA', 'all_pGo_Hit', 'all_pGo_Miss', 'all_pNoGo_Corr', 'all_pNoGo_FA', 'all_RTmeanGo_Hit', 
                              'all_RTmeanNoGo_FA', 'all_RTmedGo_Hit', 'all_RTmedNoGo_FA',

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


* GNG_summary_dat : [  sub block  nGo nNoGo nAcc   pAcc nGo_Hit nGo_Miss nNoGo_Corr nNoGo_FA   pGo_Hit  pGo_Miss pNoGo_Corr pNoGo_FA RTmeanGo_Hit RTmeanNoGo_FA RTmedGo_Hit RTmedNoGo_FA
0  51   all  150    50    2   0.01       2      148          0       50  0.013333  0.986667        0.0      1.0        708.0         624.7       708.0        587.0
1  51    b1   30    10    1  0.025       1       29          0       10  0.033333  0.966667        0.0      1.0        948.0         633.1       948.0        626.0
2  51    b2   30    10    0    0.0       0       30          0       10       0.0       1.0        0.0      1.0         <NA>         630.9        <NA>        576.0
3  51    b3   30    10    0    0.0       0       30          0       10       0.0       1.0        0.0      1.0         <NA>         668.6        <NA>        618.5
4  51    b4   30    10    0    0.0       0       30          0       10       0.0       1.0        0.0      1.0         <NA>         580.0        <NA>        537.5
5  51    b5   30    10    0    0.0       1       29          0       10  0.033333  0.966667        0.0      1.0        468.0         610.9       468.0        634.5]
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

        #make the sub index into a dataset column
        GNG_summary_wide = GNG_summary_wide.reset_index(level = 0)

        #re-order columns
        columnnames_reorder = ['sub', 'all_nGo', 'all_nNoGo', 'all_nAcc', 'all_pAcc', 'all_nGo_Hit', 'all_nGo_Miss', 'all_nNoGo_Corr', 
                              'all_nNoGo_FA', 'all_pGo_Hit', 'all_pGo_Miss', 'all_pNoGo_Corr', 'all_pNoGo_FA', 'all_RTmeanGo_Hit', 
                              'all_RTmeanNoGo_FA', 'all_RTmedGo_Hit', 'all_RTmedNoGo_FA',

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


* GNG_database :     sub  all_nGo  all_nNoGo  all_nAcc  all_pAcc  all_nGo_Hit  ...  b5_pNoGo_Corr  b5_pNoGo_FA  b5_RTmeanGo_Hit  b5_RTmeanNoGo_FA  b5_RTmedGo_Hit  b5_RTmedNoGo_FA
0     7      150         50       180     0.900          150  ...            0.7          0.3          525.467           428.333           528.5            447.0
1     3      150         50       183     0.915          140  ...            0.6          0.4          574.367           409.250           564.5            456.0
2     4      150         50       171     0.855          143  ...            0.5          0.5          559.172           461.000           501.0            461.0
3     5      150         50       187     0.935          150  ...            0.6          0.4          538.633           425.500           554.5            405.5
4     1      150         50       180     0.900          148  ...            0.6          0.4          472.733           397.500           473.0            382.0
5     2      150         50       189     0.945          149  ...            0.7          0.3          525.833           405.667           541.5            399.0
6     4      150         50       171     0.855          143  ...            0.5          0.5          559.172           461.000           501.0            461.0
7     6      150         50       182     0.910          147  ...            0.7          0.3          622.690           432.667           601.0            469.0
8     9      150         50       157     0.785          138  ...            0.3          0.7          386.538           371.714           381.5            394.0
9    11      150         50       190     0.950          148  ...            0.9          0.1          476.345           315.000           482.0            315.0
10   17      150         50       173     0.865          148  ...            0.5          0.5          550.500           554.800           541.0            463.0
11   18      150         50       184     0.920          150  ...            0.7          0.3          507.633           510.667           525.5            488.0
12   19      150         50       176     0.880          145  ...            0.4          0.6          557.900           412.500           511.0            397.0
13   20      150         50       174     0.870          143  ...            0.7          0.3          643.240           421.000           627.0            411.0
14   21      150         50       185     0.925          148  ...            0.8          0.2          594.724           381.000           588.0            381.0
15   22      150         50       180     0.900          144  ...            0.6          0.4          618.857           507.500           591.0            510.5
16   23      150         50       171     0.855          138  ...            0.8          0.2          528.733           552.000           542.0            552.0
17   26      150         50       191     0.955          150  ...            0.7          0.3          552.600           433.667           554.5            446.0
18   28      150         50       177     0.885          147  ...            0.4          0.6          462.103           435.333           443.0            391.5
0    51      150         50         2     0.010            2  ...            0.0          1.0          468.000           610.900           468.0            634.5

[20 rows x 97 columns]
* GNG_database_wide :     sub block  nGo  nNoGo  nAcc   pAcc  nGo_Hit  nGo_Miss  nNoGo_Corr  nNoGo_FA  pGo_Hit  pGo_Miss  pNoGo_Corr  pNoGo_FA RTmeanGo_Hit  RTmeanNoGo_FA RTmedGo_Hit  RTmedNoGo_FA
0     7    b1   30     10    34  0.850       30         0           4         6    1.000     0.000         0.4       0.6      492.533        412.500       453.0         397.5
1     7    b2   30     10    34  0.850       30         0           4         6    1.000     0.000         0.4       0.6        551.3        376.833       529.0         457.0
2     7    b3   30     10    37  0.925       30         0           7         3    1.000     0.000         0.7       0.3      551.033        479.000       535.5         465.0
3     7    b4   30     10    38  0.950       30         0           8         2    1.000     0.000         0.8       0.2        549.2        422.500       561.5         422.5
4     7    b5   30     10    37  0.925       30         0           7         3    1.000     0.000         0.7       0.3      525.467        428.333       528.5         447.0
..  ...   ...  ...    ...   ...    ...      ...       ...         ...       ...      ...       ...         ...       ...          ...            ...         ...           ...
1    51    b1   30     10     1  0.025        1        29           0        10    0.033     0.967         0.0       1.0        948.0        633.100       948.0         626.0
2    51    b2   30     10     0  0.000        0        30           0        10    0.000     1.000         0.0       1.0         <NA>        630.900        <NA>         576.0
3    51    b3   30     10     0  0.000        0        30           0        10    0.000     1.000         0.0       1.0         <NA>        668.600        <NA>         618.5
4    51    b4   30     10     0  0.000        0        30           0        10    0.000     1.000         0.0       1.0         <NA>        580.000        <NA>         537.5
5    51    b5   30     10     0  0.000        1        29           0        10    0.033     0.967         0.0       1.0        468.0        610.900       468.0         634.5

[100 rows x 18 columns]


Runtime info
------------


* duration : 0.038056
* hostname : H8-NTR-GCH12202
* prev_wd : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code
* working_dir : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code/GNG/gngDatabase


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

