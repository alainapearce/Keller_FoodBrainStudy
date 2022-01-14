Node: concatBlocksLong (utility)
================================


 Hierarchy : Nback.concatBlocksLong
 Exec ID : concatBlocksLong.a1


Original Inputs
---------------


* bids_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* block_sumDat : ['no files']
* function_str : def updateDatabase_save(block_sumDat, overwrite_flag, bids_dir):
    import numpy as np
    import pandas as pd
    from pathlib import Path
    from nipype.interfaces.base import Bunch

    #check to see if it is filepath str or 'no files' message
    if isinstance(block_sumDat[0], str):

        print('******** No new data to be processed ********')

        Nback_database = 'no new data files'
        Nback_database_long = 'no new data files'

    else:
        #get a Bunch object if more than 1 participant
        if isinstance(block_sumDat, Bunch):
            #get output data from node
            np_allBlockDat = block_sumDat.summaryNback_dat

        #if only 1 participant/dataset then it is a list
        elif isinstance(block_sumDat, list):
            if len(block_sumDat) == 1:
                np_allBlockDat = block_sumDat[0]
            else:
                np_allBlockDat = block_sumDat

        #convert np subarrays to pandas
        def np2pds(t):
            return [pd.DataFrame(sublist) for sublist in t]

        pandas_allBlockDat = np2pds(np_allBlockDat)

        #combine datasets
        allBlockDat = pd.concat(pandas_allBlockDat)

        #if a pandas dataframe
        if isinstance(allBlockDat, pd.DataFrame):
            col_names = ['sub', 'ses', 'block','n_targets', 'n_fill', 'n_trials', 'n_acc', 'p_acc', 'n_target_hit', 'p_target_hit', 'n_target_miss', 'p_target_miss', 'n_fill_corr', 'p_fill_corr', 'n_fill_fa', 'p_fill_fa', 'p_target_ba', 'rt_mean_target_hit', 'rt_med_target_hit']
            allBlockDat.columns = col_names
            allBlockDat = pd.DataFrame(allBlockDat).convert_dtypes()
            allBlockDat = allBlockDat.reset_index(drop = True)

            #set numeric columns to dtype numeric
            num_cols = allBlockDat.loc[:, allBlockDat.columns != 'block'].apply(pd.to_numeric).round(3)

            #replace in orig dataset
            allBlockDat.loc[:, num_cols.columns] = num_cols

            #get session subsets
            db_sessions = allBlockDat.ses.unique()

            #make wide data set
            if len(db_sessions) > 1:
                allBlockDat_ses1_dat = allBlockDat.groupby('ses').get_group(1)
                allBlockDat_ses2_dat = allBlockDat.groupby('ses').get_group(2)

                #make wide data set
                allBlockDat_ses1_wide = allBlockDat_ses1_dat.pivot(columns='block', index='sub', values=col_names[3:19])
                allBlockDat_ses1_wide.columns = ['_'.join(col) for col in allBlockDat_ses1_wide.columns.reorder_levels(order=[1, 0])]

                allBlockDat_ses2_wide = allBlockDat_ses2_dat.pivot(columns='block', index='sub', values=col_names[3:19])
                allBlockDat_ses2_wide.columns = ['_'.join(col) for col in allBlockDat_ses2_wide.columns.reorder_levels(order=[1, 0])]

                #make the sub index into a dataset column
                allBlockDat_ses1_wide = allBlockDat_ses1_wide.reset_index(level = 0)
                allBlockDat_ses2_wide = allBlockDat_ses2_wide.reset_index(level = 0)

                #add session
                allBlockDat_ses1_wide.insert(1, 'ses', 1)
                allBlockDat_ses1_wide.insert(1, 'ses', 2)


                #concatonate databases
                allBlockDat_wide = pd.concat([allBlockDat_ses1_wide, allBlockDat_ses2_wide],ignore_index=True)

            else:
                #make wide data set
                allBlockDat_wide = allBlockDat.pivot(columns='block', index='sub', values = col_names[3:19])
                allBlockDat_wide.columns = ['_'.join(col) for col in allBlockDat_wide.columns.reorder_levels(order=[1, 0])]

                #make the sub index into a dataset column
                allBlockDat_wide = allBlockDat_wide.reset_index(level = 0)

                #add session
                allBlockDat_wide.insert(1, 'ses', db_sessions[0])

            #re-order columns
            columnnames_reorder = ['sub', 'ses',
            'b0_n_targets', 'b0_n_fill', 'b0_n_trials', 'b0_n_acc','b0_p_acc',
            'b0_n_target_hit','b0_p_target_hit', 'b0_n_target_miss',
            'b0_p_target_miss','b0_n_fill_corr','b0_p_fill_corr',
            'b0_n_fill_fa', 'b0_p_fill_fa','b0_p_target_ba',
            'b0_rt_mean_target_hit','b0_rt_med_target_hit',
            'b1_n_targets', 'b1_n_fill', 'b1_n_trials', 'b1_n_acc','b1_p_acc',
            'b1_n_target_hit','b1_p_target_hit','b1_n_target_miss',
            'b1_p_target_miss', 'b1_n_fill_corr','b1_p_fill_corr',
            'b1_n_fill_fa','b1_p_fill_fa','b1_p_target_ba',
            'b1_rt_mean_target_hit','b1_rt_med_target_hit',
            'b2_n_targets', 'b2_n_fill', 'b2_n_trials', 'b2_n_acc','b2_p_acc',
            'b2_n_target_hit','b2_p_target_hit', 'b2_n_target_miss',
            'b2_p_target_miss','b2_n_fill_corr','b2_p_fill_corr',
            'b2_n_fill_fa','b2_p_fill_fa','b2_p_target_ba',
            'b2_rt_mean_target_hit','b2_rt_med_target_hit']

            allBlockDat_wide = allBlockDat_wide.reindex(columns=columnnames_reorder)

            ## load databases
            #derivative data path
            derivative_data_path = Path(bids_dir).joinpath('derivatives/preprocessed/beh')

            #load databases
            Nback_database = pd.read_csv(str(Path(derivative_data_path).joinpath('task-nback_summary.tsv')), sep = '\t')
            Nback_database_long = pd.read_csv(str(Path(derivative_data_path).joinpath('task-nback_summary_long.tsv')), sep = '\t')

            #if overwriting participants
            if overwrite_flag == True:
                #function to drop rows based on values
                def filter_rows_by_values(df, sub_values, sesnum):
                    #filter based on sub and ses
                    return df[(df['sub'].isin(sub_values) == False) & (df['ses'] == sesnum)]

                #filter out/remove exisiting subs to overwrit~
                if len(db_sessions) > 1:
                    #get list of subs by ses to filter in wide and long data
                    wide_sub_list = allBlockDat_wide.groupby('ses')['sub'].unique()
                    long_sub_list = allBlockDat.groupby('ses')['sub'].unique()

                    Nback_database_ses1 = filter_rows_by_values(Nback_database, wide_sub_list[0], 1)
                    Nback_database_ses2 = filter_rows_by_values(Nback_database, wide_sub_list[1], 2)

                    Nback_database_ses1_long = filter_rows_by_values(Nback_database_long, long_sub_list[0], 1)
                    Nback_database_ses2_long = filter_rows_by_values(Nback_database_long, long_sub_list[1], 2)

                    #concatonate databases
                    Nback_database = pd.concat([Nback_database_ses1, Nback_database_ses2],ignore_index=True)
                    Nback_database_long = pd.concat([Nback_database_ses1_long, Nback_database_ses2_long],ignore_index=True)

                else:
                    wide_sub_list = list(allBlockDat_wide['sub'].unique())
                    long_sub_list = list(allBlockDat['sub'].unique())

                    #filter by ses and sub
                    Nback_database_ses = filter_rows_by_values(Nback_database, wide_sub_list, db_sessions[0])
                    Nback_database_long_ses = filter_rows_by_values(Nback_database_long, long_sub_list, db_sessions[0])

                    #concatonate with other session in full database
                    Nback_database = pd.concat([Nback_database[Nback_database['ses'] != db_sessions[0]], Nback_database_ses],ignore_index=True)
                    Nback_database_long = pd.concat([Nback_database_long[Nback_database_long['ses'] != db_sessions[0]], Nback_database_long_ses],ignore_index=True)

            #add newly processed data
            Nback_database = Nback_database.append(allBlockDat_wide)
            Nback_database_long = Nback_database_long.append(allBlockDat)

            #sort to ensure in sub order
            Nback_database = Nback_database.sort_values(by = ['ses', 'sub'])
            Nback_database_long = Nback_database_long.sort_values(by = ['ses', 'sub', 'block'])

            #round to 3 decimal points
            Nback_database = Nback_database.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)
            Nback_database_long = Nback_database_long.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)

            #write databases
            Nback_database.to_csv(str(Path(derivative_data_path).joinpath('task-nback_summary.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
            Nback_database_long.to_csv(str(Path(derivative_data_path).joinpath('task-nback_summary_long.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
        else:
            Nback_database = 'allBlockDat no pd.DataFrame'
            Nback_database_long = 'allBlockDat no pd.DataFrame'

    return Nback_database, Nback_database_long

* overwrite_flag : False


Execution Inputs
----------------


* bids_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* block_sumDat : ['no files']
* function_str : def updateDatabase_save(block_sumDat, overwrite_flag, bids_dir):
    import numpy as np
    import pandas as pd
    from pathlib import Path
    from nipype.interfaces.base import Bunch

    #check to see if it is filepath str or 'no files' message
    if isinstance(block_sumDat[0], str):

        print('******** No new data to be processed ********')

        Nback_database = 'no new data files'
        Nback_database_long = 'no new data files'

    else:
        #get a Bunch object if more than 1 participant
        if isinstance(block_sumDat, Bunch):
            #get output data from node
            np_allBlockDat = block_sumDat.summaryNback_dat

        #if only 1 participant/dataset then it is a list
        elif isinstance(block_sumDat, list):
            if len(block_sumDat) == 1:
                np_allBlockDat = block_sumDat[0]
            else:
                np_allBlockDat = block_sumDat

        #convert np subarrays to pandas
        def np2pds(t):
            return [pd.DataFrame(sublist) for sublist in t]

        pandas_allBlockDat = np2pds(np_allBlockDat)

        #combine datasets
        allBlockDat = pd.concat(pandas_allBlockDat)

        #if a pandas dataframe
        if isinstance(allBlockDat, pd.DataFrame):
            col_names = ['sub', 'ses', 'block','n_targets', 'n_fill', 'n_trials', 'n_acc', 'p_acc', 'n_target_hit', 'p_target_hit', 'n_target_miss', 'p_target_miss', 'n_fill_corr', 'p_fill_corr', 'n_fill_fa', 'p_fill_fa', 'p_target_ba', 'rt_mean_target_hit', 'rt_med_target_hit']
            allBlockDat.columns = col_names
            allBlockDat = pd.DataFrame(allBlockDat).convert_dtypes()
            allBlockDat = allBlockDat.reset_index(drop = True)

            #set numeric columns to dtype numeric
            num_cols = allBlockDat.loc[:, allBlockDat.columns != 'block'].apply(pd.to_numeric).round(3)

            #replace in orig dataset
            allBlockDat.loc[:, num_cols.columns] = num_cols

            #get session subsets
            db_sessions = allBlockDat.ses.unique()

            #make wide data set
            if len(db_sessions) > 1:
                allBlockDat_ses1_dat = allBlockDat.groupby('ses').get_group(1)
                allBlockDat_ses2_dat = allBlockDat.groupby('ses').get_group(2)

                #make wide data set
                allBlockDat_ses1_wide = allBlockDat_ses1_dat.pivot(columns='block', index='sub', values=col_names[3:19])
                allBlockDat_ses1_wide.columns = ['_'.join(col) for col in allBlockDat_ses1_wide.columns.reorder_levels(order=[1, 0])]

                allBlockDat_ses2_wide = allBlockDat_ses2_dat.pivot(columns='block', index='sub', values=col_names[3:19])
                allBlockDat_ses2_wide.columns = ['_'.join(col) for col in allBlockDat_ses2_wide.columns.reorder_levels(order=[1, 0])]

                #make the sub index into a dataset column
                allBlockDat_ses1_wide = allBlockDat_ses1_wide.reset_index(level = 0)
                allBlockDat_ses2_wide = allBlockDat_ses2_wide.reset_index(level = 0)

                #add session
                allBlockDat_ses1_wide.insert(1, 'ses', 1)
                allBlockDat_ses1_wide.insert(1, 'ses', 2)


                #concatonate databases
                allBlockDat_wide = pd.concat([allBlockDat_ses1_wide, allBlockDat_ses2_wide],ignore_index=True)

            else:
                #make wide data set
                allBlockDat_wide = allBlockDat.pivot(columns='block', index='sub', values = col_names[3:19])
                allBlockDat_wide.columns = ['_'.join(col) for col in allBlockDat_wide.columns.reorder_levels(order=[1, 0])]

                #make the sub index into a dataset column
                allBlockDat_wide = allBlockDat_wide.reset_index(level = 0)

                #add session
                allBlockDat_wide.insert(1, 'ses', db_sessions[0])

            #re-order columns
            columnnames_reorder = ['sub', 'ses',
            'b0_n_targets', 'b0_n_fill', 'b0_n_trials', 'b0_n_acc','b0_p_acc',
            'b0_n_target_hit','b0_p_target_hit', 'b0_n_target_miss',
            'b0_p_target_miss','b0_n_fill_corr','b0_p_fill_corr',
            'b0_n_fill_fa', 'b0_p_fill_fa','b0_p_target_ba',
            'b0_rt_mean_target_hit','b0_rt_med_target_hit',
            'b1_n_targets', 'b1_n_fill', 'b1_n_trials', 'b1_n_acc','b1_p_acc',
            'b1_n_target_hit','b1_p_target_hit','b1_n_target_miss',
            'b1_p_target_miss', 'b1_n_fill_corr','b1_p_fill_corr',
            'b1_n_fill_fa','b1_p_fill_fa','b1_p_target_ba',
            'b1_rt_mean_target_hit','b1_rt_med_target_hit',
            'b2_n_targets', 'b2_n_fill', 'b2_n_trials', 'b2_n_acc','b2_p_acc',
            'b2_n_target_hit','b2_p_target_hit', 'b2_n_target_miss',
            'b2_p_target_miss','b2_n_fill_corr','b2_p_fill_corr',
            'b2_n_fill_fa','b2_p_fill_fa','b2_p_target_ba',
            'b2_rt_mean_target_hit','b2_rt_med_target_hit']

            allBlockDat_wide = allBlockDat_wide.reindex(columns=columnnames_reorder)

            ## load databases
            #derivative data path
            derivative_data_path = Path(bids_dir).joinpath('derivatives/preprocessed/beh')

            #load databases
            Nback_database = pd.read_csv(str(Path(derivative_data_path).joinpath('task-nback_summary.tsv')), sep = '\t')
            Nback_database_long = pd.read_csv(str(Path(derivative_data_path).joinpath('task-nback_summary_long.tsv')), sep = '\t')

            #if overwriting participants
            if overwrite_flag == True:
                #function to drop rows based on values
                def filter_rows_by_values(df, sub_values, sesnum):
                    #filter based on sub and ses
                    return df[(df['sub'].isin(sub_values) == False) & (df['ses'] == sesnum)]

                #filter out/remove exisiting subs to overwrit~
                if len(db_sessions) > 1:
                    #get list of subs by ses to filter in wide and long data
                    wide_sub_list = allBlockDat_wide.groupby('ses')['sub'].unique()
                    long_sub_list = allBlockDat.groupby('ses')['sub'].unique()

                    Nback_database_ses1 = filter_rows_by_values(Nback_database, wide_sub_list[0], 1)
                    Nback_database_ses2 = filter_rows_by_values(Nback_database, wide_sub_list[1], 2)

                    Nback_database_ses1_long = filter_rows_by_values(Nback_database_long, long_sub_list[0], 1)
                    Nback_database_ses2_long = filter_rows_by_values(Nback_database_long, long_sub_list[1], 2)

                    #concatonate databases
                    Nback_database = pd.concat([Nback_database_ses1, Nback_database_ses2],ignore_index=True)
                    Nback_database_long = pd.concat([Nback_database_ses1_long, Nback_database_ses2_long],ignore_index=True)

                else:
                    wide_sub_list = list(allBlockDat_wide['sub'].unique())
                    long_sub_list = list(allBlockDat['sub'].unique())

                    #filter by ses and sub
                    Nback_database_ses = filter_rows_by_values(Nback_database, wide_sub_list, db_sessions[0])
                    Nback_database_long_ses = filter_rows_by_values(Nback_database_long, long_sub_list, db_sessions[0])

                    #concatonate with other session in full database
                    Nback_database = pd.concat([Nback_database[Nback_database['ses'] != db_sessions[0]], Nback_database_ses],ignore_index=True)
                    Nback_database_long = pd.concat([Nback_database_long[Nback_database_long['ses'] != db_sessions[0]], Nback_database_long_ses],ignore_index=True)

            #add newly processed data
            Nback_database = Nback_database.append(allBlockDat_wide)
            Nback_database_long = Nback_database_long.append(allBlockDat)

            #sort to ensure in sub order
            Nback_database = Nback_database.sort_values(by = ['ses', 'sub'])
            Nback_database_long = Nback_database_long.sort_values(by = ['ses', 'sub', 'block'])

            #round to 3 decimal points
            Nback_database = Nback_database.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)
            Nback_database_long = Nback_database_long.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)

            #write databases
            Nback_database.to_csv(str(Path(derivative_data_path).joinpath('task-nback_summary.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
            Nback_database_long.to_csv(str(Path(derivative_data_path).joinpath('task-nback_summary_long.tsv')), sep = '\t', encoding='utf-8-sig', index = False)
        else:
            Nback_database = 'allBlockDat no pd.DataFrame'
            Nback_database_long = 'allBlockDat no pd.DataFrame'

    return Nback_database, Nback_database_long

* overwrite_flag : False


Execution Outputs
-----------------


* allBlocks_longDat : ('no new data files', 'no new data files')


Runtime info
------------


* duration : 0.004094
* hostname : nut-azp271-10239
* prev_wd : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* working_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/Nback/_session_id_2/concatBlocksLong


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

