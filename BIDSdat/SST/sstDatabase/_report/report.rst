Node: sstDatabase (utility)
===========================


 Hierarchy : SST.sstDatabase
 Exec ID : sstDatabase


Original Inputs
---------------


* SST_summary_dat : [   sub   block  condition racehorse_check  ...    us_rt      ssd ssrt_mean ssrt_int
0  114     all        all               1  ...  439.594  223.188   326.456  319.312
1  114    h_ed       h_ed               1  ...  465.312  223.969    290.75  266.531
2  114    l_ed       l_ed               1  ...  413.875  222.406   362.531  367.094
3  114  l_port     l_port               1  ...  486.357    224.5   303.906      268
4  114  s_port     s_port               1  ...  403.222  221.875    349.23  375.438
5  114       1  hED_lPort               1  ...  498.286  179.188   309.792  277.938
6  114       2  hED_sPort               1  ...  439.667   268.75   271.708  274.125
7  114       3  lED_sPort               1  ...  366.778      175   427.404  461.688
8  114       4  lED_lPort               1  ...  474.429  269.812   298.021      251

[9 rows x 17 columns]]
* bids_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* function_str : def updateDatabase_save(SST_summary_dat, overwrite_flag, bids_dir):
    import pandas as pd
    import numpy as np
    from pathlib import Path
    from nipype.interfaces.base import Bunch

    #get a Bunch object if more than 1 participant 
    if isinstance(SST_summary_dat, Bunch):        
        #get output data from node
        SST_summary_datlist = SST_summary_dat.summarySST_dat

        #combine datasets 
        SST_summary_dat = pd.concat(SST_summary_datlist)

    #if only 1 participant/dataset then it is a list    
    elif isinstance(SST_summary_dat, list):
        if len(SST_summary_dat) == 1:
            SST_summary_dat = SST_summary_dat[0]
        else:
            SST_summary_dat = pd.concat(SST_summary_dat)

    #if a pandas dataframe
    if isinstance(SST_summary_dat, pd.DataFrame):

        #get column names
        columnnames = SST_summary_dat.columns

        #get condition subset
        SST_summary_conds = SST_summary_dat[SST_summary_dat.block.isin(['all', 'h_ed', 'l_ed', 'l_port', 's_port'])]

        #make wide data set 
        SST_summary_wide = SST_summary_conds.pivot(columns='condition', index='sub', values=columnnames[3:17])        
        SST_summary_wide.columns = ['_'.join(col) for col in SST_summary_wide.columns.reorder_levels(order=[1, 0])]

        #make the sub index into a dataset column
        SST_summary_wide = SST_summary_wide.reset_index(level = 0)

        #re-order columns
        columnnames_reorder = ['sub', 'all_racehorse_check', 
                               'all_n_stop_trials', 'all_n_go_trials', 'all_go_rt', 
                               'all_n_go_cor', 'all_go_cor_rt', 'all_n_go_error',  
                               'all_go_error_rt', 'all_n_go_miss', 'all_stop_prob_resp',
                               'all_us_rt', 'all_ssd', 'all_ssrt_mean', 'all_ssrt_int', 
                               'h_ed_racehorse_check', 'h_ed_n_stop_trials',
                               'h_ed_n_go_trials', 'h_ed_go_rt', 'h_ed_n_go_cor', 
                               'h_ed_go_cor_rt', 'h_ed_n_go_error',
                               'h_ed_go_error_rt', 'h_ed_n_go_miss', 'h_ed_stop_prob_resp', 
                               'h_ed_us_rt', 'h_ed_ssd', 'h_ed_ssrt_mean', 'h_ed_ssrt_int',
                               'l_ed_racehorse_check', 'l_ed_n_stop_trials', 'l_ed_n_go_trials', 
                               'l_ed_go_rt', 'l_ed_n_go_cor', 'l_ed_go_cor_rt', 
                               'l_ed_n_go_error', 'l_ed_go_error_rt', 'l_ed_n_go_miss', 
                               'l_ed_stop_prob_resp', 'l_ed_us_rt', 'l_ed_ssd',
                               'l_ed_ssrt_mean', 'l_ed_ssrt_int', 'l_port_racehorse_check', 
                               'l_port_n_stop_trials', 'l_port_n_go_trials', 'l_port_go_rt', 
                               'l_port_n_go_cor', 'l_port_go_cor_rt', 'l_port_n_go_error',
                               'l_port_go_error_rt', 'l_port_n_go_miss', 'l_port_stop_prob_resp', 
                               'l_port_us_rt', 'l_port_ssd', 'l_port_ssrt_mean', 'l_port_ssrt_int',
                               's_port_racehorse_check', 's_port_n_stop_trials',
                               's_port_n_go_trials', 's_port_go_rt', 's_port_n_go_cor', 
                               's_port_go_cor_rt', 's_port_n_go_error',
                               's_port_go_error_rt', 's_port_n_go_miss', 's_port_stop_prob_resp', 
                               's_port_us_rt', 's_port_ssd', 's_port_ssrt_mean', 's_port_ssrt_int']

        SST_summary_wide = SST_summary_wide.reindex(columns=columnnames_reorder)

        #get blocks subset
        SST_summary_blocks = SST_summary_dat[SST_summary_dat.condition.isin(['hED_lPort', 'hED_sPort', 'lED_lPort', 'lED_sPort'])] 

        ## load databases
        #derivative data path
        derivative_data_path = Path(bids_dir).joinpath('derivatives/preprocessed/beh')

        #load databases
        SST_database_cond = pd.read_csv(str(Path(derivative_data_path).joinpath('task-sst_summary_condwide.tsv')), sep = '\t') 
        SST_database_blocks = pd.read_csv(str(Path(derivative_data_path).joinpath('task-sst_summary_blockslong.tsv')), sep = '\t')

        #if overwriting participants
        if overwrite_flag == True:
            #function to drop rows based on values
            def filter_rows_by_values(df, col, values):
                return df[df[col].isin(values) == False]

            #get list of subs to filter in wide and long data
            wide_sub_list = list(SST_summary_wide['sub'].unique())
            block_sub_list = list(SST_summary_blocks['sub'].unique())

            #filter out/remove exisiting subs to overwrite
            SST_database_cond = filter_rows_by_values(SST_database_cond, 'sub', wide_sub_list)
            SST_database_blocks = filter_rows_by_values(SST_database_blocks, 'sub', block_sub_list)

        #add newly processed data
        SST_database_cond = SST_database_cond.append(SST_summary_wide)
        SST_database_blocks = SST_database_blocks.append(SST_summary_blocks)

        #sort to ensure in sub order
        SST_database_cond = SST_database_cond.sort_values(by = 'sub')
        SST_database_blocks = SST_database_blocks.sort_values(by = ['sub', 'block'])

        #round to 3 decimal points
        SST_database_cond = SST_database_cond.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)
        SST_database_blocks = SST_database_blocks.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)

        #write databases
        SST_database_cond.to_csv(str(Path(derivative_data_path).joinpath('task-sst_summary_condwide.tsv')), sep = '\t', encoding='utf-8-sig', index = False) 
        SST_database_blocks.to_csv(str(Path(derivative_data_path).joinpath('task-sst_summary_blockslong.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

    else:
        print('No raw data files that need to be processed')
        SST_database_cond = np.nan
        SST_database_blocks = np.nan

    return SST_database_cond, SST_database_blocks

* overwrite_flag : False


Execution Inputs
----------------


* SST_summary_dat : [   sub   block  condition racehorse_check  ...    us_rt      ssd ssrt_mean ssrt_int
0  114     all        all               1  ...  439.594  223.188   326.456  319.312
1  114    h_ed       h_ed               1  ...  465.312  223.969    290.75  266.531
2  114    l_ed       l_ed               1  ...  413.875  222.406   362.531  367.094
3  114  l_port     l_port               1  ...  486.357    224.5   303.906      268
4  114  s_port     s_port               1  ...  403.222  221.875    349.23  375.438
5  114       1  hED_lPort               1  ...  498.286  179.188   309.792  277.938
6  114       2  hED_sPort               1  ...  439.667   268.75   271.708  274.125
7  114       3  lED_sPort               1  ...  366.778      175   427.404  461.688
8  114       4  lED_lPort               1  ...  474.429  269.812   298.021      251

[9 rows x 17 columns]]
* bids_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* function_str : def updateDatabase_save(SST_summary_dat, overwrite_flag, bids_dir):
    import pandas as pd
    import numpy as np
    from pathlib import Path
    from nipype.interfaces.base import Bunch

    #get a Bunch object if more than 1 participant 
    if isinstance(SST_summary_dat, Bunch):        
        #get output data from node
        SST_summary_datlist = SST_summary_dat.summarySST_dat

        #combine datasets 
        SST_summary_dat = pd.concat(SST_summary_datlist)

    #if only 1 participant/dataset then it is a list    
    elif isinstance(SST_summary_dat, list):
        if len(SST_summary_dat) == 1:
            SST_summary_dat = SST_summary_dat[0]
        else:
            SST_summary_dat = pd.concat(SST_summary_dat)

    #if a pandas dataframe
    if isinstance(SST_summary_dat, pd.DataFrame):

        #get column names
        columnnames = SST_summary_dat.columns

        #get condition subset
        SST_summary_conds = SST_summary_dat[SST_summary_dat.block.isin(['all', 'h_ed', 'l_ed', 'l_port', 's_port'])]

        #make wide data set 
        SST_summary_wide = SST_summary_conds.pivot(columns='condition', index='sub', values=columnnames[3:17])        
        SST_summary_wide.columns = ['_'.join(col) for col in SST_summary_wide.columns.reorder_levels(order=[1, 0])]

        #make the sub index into a dataset column
        SST_summary_wide = SST_summary_wide.reset_index(level = 0)

        #re-order columns
        columnnames_reorder = ['sub', 'all_racehorse_check', 
                               'all_n_stop_trials', 'all_n_go_trials', 'all_go_rt', 
                               'all_n_go_cor', 'all_go_cor_rt', 'all_n_go_error',  
                               'all_go_error_rt', 'all_n_go_miss', 'all_stop_prob_resp',
                               'all_us_rt', 'all_ssd', 'all_ssrt_mean', 'all_ssrt_int', 
                               'h_ed_racehorse_check', 'h_ed_n_stop_trials',
                               'h_ed_n_go_trials', 'h_ed_go_rt', 'h_ed_n_go_cor', 
                               'h_ed_go_cor_rt', 'h_ed_n_go_error',
                               'h_ed_go_error_rt', 'h_ed_n_go_miss', 'h_ed_stop_prob_resp', 
                               'h_ed_us_rt', 'h_ed_ssd', 'h_ed_ssrt_mean', 'h_ed_ssrt_int',
                               'l_ed_racehorse_check', 'l_ed_n_stop_trials', 'l_ed_n_go_trials', 
                               'l_ed_go_rt', 'l_ed_n_go_cor', 'l_ed_go_cor_rt', 
                               'l_ed_n_go_error', 'l_ed_go_error_rt', 'l_ed_n_go_miss', 
                               'l_ed_stop_prob_resp', 'l_ed_us_rt', 'l_ed_ssd',
                               'l_ed_ssrt_mean', 'l_ed_ssrt_int', 'l_port_racehorse_check', 
                               'l_port_n_stop_trials', 'l_port_n_go_trials', 'l_port_go_rt', 
                               'l_port_n_go_cor', 'l_port_go_cor_rt', 'l_port_n_go_error',
                               'l_port_go_error_rt', 'l_port_n_go_miss', 'l_port_stop_prob_resp', 
                               'l_port_us_rt', 'l_port_ssd', 'l_port_ssrt_mean', 'l_port_ssrt_int',
                               's_port_racehorse_check', 's_port_n_stop_trials',
                               's_port_n_go_trials', 's_port_go_rt', 's_port_n_go_cor', 
                               's_port_go_cor_rt', 's_port_n_go_error',
                               's_port_go_error_rt', 's_port_n_go_miss', 's_port_stop_prob_resp', 
                               's_port_us_rt', 's_port_ssd', 's_port_ssrt_mean', 's_port_ssrt_int']

        SST_summary_wide = SST_summary_wide.reindex(columns=columnnames_reorder)

        #get blocks subset
        SST_summary_blocks = SST_summary_dat[SST_summary_dat.condition.isin(['hED_lPort', 'hED_sPort', 'lED_lPort', 'lED_sPort'])] 

        ## load databases
        #derivative data path
        derivative_data_path = Path(bids_dir).joinpath('derivatives/preprocessed/beh')

        #load databases
        SST_database_cond = pd.read_csv(str(Path(derivative_data_path).joinpath('task-sst_summary_condwide.tsv')), sep = '\t') 
        SST_database_blocks = pd.read_csv(str(Path(derivative_data_path).joinpath('task-sst_summary_blockslong.tsv')), sep = '\t')

        #if overwriting participants
        if overwrite_flag == True:
            #function to drop rows based on values
            def filter_rows_by_values(df, col, values):
                return df[df[col].isin(values) == False]

            #get list of subs to filter in wide and long data
            wide_sub_list = list(SST_summary_wide['sub'].unique())
            block_sub_list = list(SST_summary_blocks['sub'].unique())

            #filter out/remove exisiting subs to overwrite
            SST_database_cond = filter_rows_by_values(SST_database_cond, 'sub', wide_sub_list)
            SST_database_blocks = filter_rows_by_values(SST_database_blocks, 'sub', block_sub_list)

        #add newly processed data
        SST_database_cond = SST_database_cond.append(SST_summary_wide)
        SST_database_blocks = SST_database_blocks.append(SST_summary_blocks)

        #sort to ensure in sub order
        SST_database_cond = SST_database_cond.sort_values(by = 'sub')
        SST_database_blocks = SST_database_blocks.sort_values(by = ['sub', 'block'])

        #round to 3 decimal points
        SST_database_cond = SST_database_cond.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)
        SST_database_blocks = SST_database_blocks.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)

        #write databases
        SST_database_cond.to_csv(str(Path(derivative_data_path).joinpath('task-sst_summary_condwide.tsv')), sep = '\t', encoding='utf-8-sig', index = False) 
        SST_database_blocks.to_csv(str(Path(derivative_data_path).joinpath('task-sst_summary_blockslong.tsv')), sep = '\t', encoding='utf-8-sig', index = False)

    else:
        print('No raw data files that need to be processed')
        SST_database_cond = np.nan
        SST_database_blocks = np.nan

    return SST_database_cond, SST_database_blocks

* overwrite_flag : False


Execution Outputs
-----------------


* SST_database_blocks :      sub  block  condition  racehorse_check  ...    us_rt      ssd  ssrt_mean  ssrt_int
0      1      1  lED_lPort                1  ...  702.600  435.500    432.604   310.062
1      1      2  lED_sPort                1  ...  635.167  406.250    439.054   407.250
2      1      3  hED_sPort                1  ...  505.625  433.312    358.879   346.688
3      1      4  hED_lPort                1  ...  573.500  312.375    476.042   347.375
4      4      1  hED_lPort                1  ...  568.286  305.125    439.750   326.438
..   ...    ...        ...              ...  ...      ...      ...        ...       ...
270  123      4  hED_sPort                1  ...  512.375  275.000    260.250   238.000
271  124      1  lED_sPort                1  ...  612.167  376.062    357.807   231.688
272  124      2  lED_lPort                1  ...  710.400  468.750    356.606   218.312
273  124      3  hED_lPort                1  ...  593.833  307.312    456.915   380.938
274  124      4  hED_sPort                1  ...  574.857  345.875    363.755   301.375

[279 rows x 17 columns]
* SST_database_cond :     sub  all_racehorse_check  ...  s_port_ssrt_mean  s_port_ssrt_int
0     1                    1  ...           398.681          364.031
1     4                    1  ...           490.856          406.938
2     5                    1  ...           431.271          397.281
3     6                    0  ...               NaN              NaN
4     7                    1  ...               NaN              NaN
..  ...                  ...  ...               ...              ...
67  120                    0  ...           379.387          338.375
68  121                    1  ...           404.375          357.500
69  122                    1  ...           410.740          276.031
70  123                    1  ...           293.156          253.031
71  124                    1  ...           360.781          278.812

[73 rows x 71 columns]


Runtime info
------------


* duration : 0.102611
* hostname : nut-azp271-10239
* prev_wd : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* working_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/SST/sstDatabase


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

