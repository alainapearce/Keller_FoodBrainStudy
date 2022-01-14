Node: utility
=============


 Hierarchy : _summaryData0
 Exec ID : _summaryData0


Original Inputs
---------------


* Space_file : No subfiles
* base_directory : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* function_str : def summarySpace(Space_file, base_directory):
    import numpy as np
    import pandas as pd
    import scipy.io as sio
    from pathlib import Path

    ###################################################################
    ####                   Sub-function script                     ####

    #need to sub-functions within the function that is called by the node just 
    #like you need to re-import libraries
    def summary_stats(Space_data):

        #Earth RT
        earthRT_mean = Space_data.loc[Space_data['rt_earth'] > 0, 'rt_earth'].mean(axis = 0)*1000  
        earthRT_median = Space_data.loc[Space_data['rt_earth'] > 0, 'rt_earth'].median(axis = 0)*1000  

        #Earth missed
        earth_n_miss = Space_data['missed_earth'].sum(axis = 0)
        earth_p_miss = Space_data['missed_earth'].sum(axis = 0)/Space_data['missed_earth'].shape[0]

        #Planet RT
        planetRT_mean = Space_data.loc[Space_data['rt_planet'] > 0, 'rt_planet'].mean(axis = 0)*1000  
        planetRT_median = Space_data.loc[Space_data['rt_planet'] > 0, 'rt_planet'].median(axis = 0)*1000  

        #Planet missed
        planet_n_miss = Space_data['missed_planet'].sum(axis = 0)
        planet_p_miss = Space_data['missed_planet'].sum(axis = 0)/Space_data['missed_planet'].shape[0]

        #reward rate
        reward_rate = Space_data.loc[(Space_data['missed_earth'] == 0) & (Space_data['missed_planet'] == 0), 'points'].mean(axis = 0)

        #average reward overall across both options
        rewards = Space_data[['rewards1', 'rewards2']].values.tolist()
        rewards_flat = [item for sublist in rewards for item in sublist]
        avg_reward = sum(rewards_flat)/len(rewards_flat)

        #corrected reward rate
        reward_rate_corrected = reward_rate - avg_reward

        #stay probabilities (always won previously as no negatives) for if
        #earth state is same or different
        prob_sameplanet_earthsame = Space_data.loc[(Space_data['same_earth'] == 1) & (Space_data['missed_earth'] == 0) & (Space_data['missed_planet'] == 0), 'same_planet'].mean(axis = 0)
        prob_sameplanet_earthdif = Space_data.loc[(Space_data['same_earth'] == 0) & (Space_data['missed_earth'] == 0) & (Space_data['missed_planet'] == 0), 'same_planet'].mean(axis = 0)

        summary_results = [earthRT_mean, earthRT_median, earth_n_miss, earth_p_miss, planetRT_mean, planetRT_median, 
                            planet_n_miss, planet_p_miss, reward_rate, avg_reward, reward_rate_corrected, 
                            prob_sameplanet_earthsame, prob_sameplanet_earthdif]

        return(summary_results)

    ###################################################################
    ####                Primary function script                    ####

    #summary column names
    colnames = ['sub', 'ses', 'block', 'earth_rt_mean', 'earth_rt_median', 'earth_n_miss', 'earth_p_miss', 'planet_rt_mean', 
                'planet_rt_median', 'planet_n_miss', 'planet_p_miss', 'reward_rate', 'avg_reward', 
                'reward_rate_corrected', 'prob_sameplanet_earthsame', 'prob_sameplanet_earthdif']

    #check if str
    if isinstance(Space_file, str):

        #check to see if it is filepath str or 'No subfiles' message
        if '.tsv' in Space_file:
            #if only 1 file, will be string and we want an array
            Space_file = [Space_file]
        else:
            Space_file = []

    if len(Space_file) > 0:

        #loop counter
        count = 0

        #supress warning
        pd.options.mode.chained_assignment = None

        for file in Space_file:

            #load data 
            Space_ProcData = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python') 

            #add previous trial data
            Space_ProcData['prev_state_earth'] = Space_ProcData['state_earth'].shift(1)
            Space_ProcData['prev_state_earth'] = np.where(np.isnan(Space_ProcData['prev_state_earth']), 0, Space_ProcData['prev_state_earth'])

            Space_ProcData['prev_state_planet'] = Space_ProcData['state_planet'].shift(1)
            Space_ProcData['prev_state_planet'] = np.where(np.isnan(Space_ProcData['prev_state_planet']), 0, Space_ProcData['prev_state_planet'])

            Space_ProcData['same_earth'] = np.where(Space_ProcData['state_earth'] == Space_ProcData['prev_state_earth'], 1, 0)
            Space_ProcData['same_planet'] = np.where(Space_ProcData['state_planet'] == Space_ProcData['prev_state_planet'], 1, 0)

            #summary stats - across all blocks
            all_trials_stat = summary_stats(Space_ProcData)
            all_trials_stat.insert(0, Space_ProcData.loc[0, 'sub'])
            all_trials_stat.insert(1, Space_ProcData.loc[0, 'ses'])
            all_trials_stat.insert(2, 'all')

            if count == 0:
                #make summary dataset
                overall_summary_data = pd.DataFrame(all_trials_stat).T
                overall_summary_data.columns = colnames

                #make group_trailsdat dataset
                space_group_trialsdat = Space_ProcData
            else:
                #add to summary dataset
                overall_summary_data.loc[len(overall_summary_data)] = all_trials_stat

                #add to group_trailsdat dataset
                space_group_trialsdat = Space_ProcData
                space_group_trialsdat = pd.concat([space_group_trialsdat, Space_ProcData],ignore_index=True)

            # summary stats - by block 
            for b in np.unique(Space_ProcData['block']):
                #get block data
                block_data = Space_ProcData.loc[Space_ProcData['block'] == b]

                #re-do previous trial data base on just current block
                block_data['prev_state_earth'] = block_data['state_earth'].shift(1)
                block_data['prev_state_earth'] = np.where(np.isnan(block_data['prev_state_earth']), 0, block_data['prev_state_earth'])

                block_data['prev_state_planet'] = block_data['state_planet'].shift(1)
                block_data['prev_state_planet'] = np.where(np.isnan(block_data['prev_state_planet']), 0, block_data['prev_state_planet'])

                block_data['same_earth'] = np.where(block_data['state_earth'] == block_data['prev_state_earth'], 1, 0)
                block_data['same_planet'] = np.where(block_data['state_planet'] == block_data['prev_state_planet'], 1, 0)

                #get summary results
                block_trials_stat = summary_stats(block_data)
                block_trials_stat.insert(0, Space_ProcData.loc[0, 'sub'])
                block_trials_stat.insert(1, Space_ProcData.loc[0, 'ses'])

                block_name = 'b' + str(b)
                block_trials_stat.insert(2, block_name)

                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = block_trials_stat

            #update count for files loop
            count = 1

    else:
         overall_summary_data = 'no files'
         space_group_trialsdat = 'no files'

    return overall_summary_data, space_group_trialsdat



Execution Inputs
----------------


* Space_file : No subfiles
* base_directory : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* function_str : def summarySpace(Space_file, base_directory):
    import numpy as np
    import pandas as pd
    import scipy.io as sio
    from pathlib import Path

    ###################################################################
    ####                   Sub-function script                     ####

    #need to sub-functions within the function that is called by the node just 
    #like you need to re-import libraries
    def summary_stats(Space_data):

        #Earth RT
        earthRT_mean = Space_data.loc[Space_data['rt_earth'] > 0, 'rt_earth'].mean(axis = 0)*1000  
        earthRT_median = Space_data.loc[Space_data['rt_earth'] > 0, 'rt_earth'].median(axis = 0)*1000  

        #Earth missed
        earth_n_miss = Space_data['missed_earth'].sum(axis = 0)
        earth_p_miss = Space_data['missed_earth'].sum(axis = 0)/Space_data['missed_earth'].shape[0]

        #Planet RT
        planetRT_mean = Space_data.loc[Space_data['rt_planet'] > 0, 'rt_planet'].mean(axis = 0)*1000  
        planetRT_median = Space_data.loc[Space_data['rt_planet'] > 0, 'rt_planet'].median(axis = 0)*1000  

        #Planet missed
        planet_n_miss = Space_data['missed_planet'].sum(axis = 0)
        planet_p_miss = Space_data['missed_planet'].sum(axis = 0)/Space_data['missed_planet'].shape[0]

        #reward rate
        reward_rate = Space_data.loc[(Space_data['missed_earth'] == 0) & (Space_data['missed_planet'] == 0), 'points'].mean(axis = 0)

        #average reward overall across both options
        rewards = Space_data[['rewards1', 'rewards2']].values.tolist()
        rewards_flat = [item for sublist in rewards for item in sublist]
        avg_reward = sum(rewards_flat)/len(rewards_flat)

        #corrected reward rate
        reward_rate_corrected = reward_rate - avg_reward

        #stay probabilities (always won previously as no negatives) for if
        #earth state is same or different
        prob_sameplanet_earthsame = Space_data.loc[(Space_data['same_earth'] == 1) & (Space_data['missed_earth'] == 0) & (Space_data['missed_planet'] == 0), 'same_planet'].mean(axis = 0)
        prob_sameplanet_earthdif = Space_data.loc[(Space_data['same_earth'] == 0) & (Space_data['missed_earth'] == 0) & (Space_data['missed_planet'] == 0), 'same_planet'].mean(axis = 0)

        summary_results = [earthRT_mean, earthRT_median, earth_n_miss, earth_p_miss, planetRT_mean, planetRT_median, 
                            planet_n_miss, planet_p_miss, reward_rate, avg_reward, reward_rate_corrected, 
                            prob_sameplanet_earthsame, prob_sameplanet_earthdif]

        return(summary_results)

    ###################################################################
    ####                Primary function script                    ####

    #summary column names
    colnames = ['sub', 'ses', 'block', 'earth_rt_mean', 'earth_rt_median', 'earth_n_miss', 'earth_p_miss', 'planet_rt_mean', 
                'planet_rt_median', 'planet_n_miss', 'planet_p_miss', 'reward_rate', 'avg_reward', 
                'reward_rate_corrected', 'prob_sameplanet_earthsame', 'prob_sameplanet_earthdif']

    #check if str
    if isinstance(Space_file, str):

        #check to see if it is filepath str or 'No subfiles' message
        if '.tsv' in Space_file:
            #if only 1 file, will be string and we want an array
            Space_file = [Space_file]
        else:
            Space_file = []

    if len(Space_file) > 0:

        #loop counter
        count = 0

        #supress warning
        pd.options.mode.chained_assignment = None

        for file in Space_file:

            #load data 
            Space_ProcData = pd.read_csv(str(file), sep = '\t', encoding = 'utf-8-sig', engine='python') 

            #add previous trial data
            Space_ProcData['prev_state_earth'] = Space_ProcData['state_earth'].shift(1)
            Space_ProcData['prev_state_earth'] = np.where(np.isnan(Space_ProcData['prev_state_earth']), 0, Space_ProcData['prev_state_earth'])

            Space_ProcData['prev_state_planet'] = Space_ProcData['state_planet'].shift(1)
            Space_ProcData['prev_state_planet'] = np.where(np.isnan(Space_ProcData['prev_state_planet']), 0, Space_ProcData['prev_state_planet'])

            Space_ProcData['same_earth'] = np.where(Space_ProcData['state_earth'] == Space_ProcData['prev_state_earth'], 1, 0)
            Space_ProcData['same_planet'] = np.where(Space_ProcData['state_planet'] == Space_ProcData['prev_state_planet'], 1, 0)

            #summary stats - across all blocks
            all_trials_stat = summary_stats(Space_ProcData)
            all_trials_stat.insert(0, Space_ProcData.loc[0, 'sub'])
            all_trials_stat.insert(1, Space_ProcData.loc[0, 'ses'])
            all_trials_stat.insert(2, 'all')

            if count == 0:
                #make summary dataset
                overall_summary_data = pd.DataFrame(all_trials_stat).T
                overall_summary_data.columns = colnames

                #make group_trailsdat dataset
                space_group_trialsdat = Space_ProcData
            else:
                #add to summary dataset
                overall_summary_data.loc[len(overall_summary_data)] = all_trials_stat

                #add to group_trailsdat dataset
                space_group_trialsdat = Space_ProcData
                space_group_trialsdat = pd.concat([space_group_trialsdat, Space_ProcData],ignore_index=True)

            # summary stats - by block 
            for b in np.unique(Space_ProcData['block']):
                #get block data
                block_data = Space_ProcData.loc[Space_ProcData['block'] == b]

                #re-do previous trial data base on just current block
                block_data['prev_state_earth'] = block_data['state_earth'].shift(1)
                block_data['prev_state_earth'] = np.where(np.isnan(block_data['prev_state_earth']), 0, block_data['prev_state_earth'])

                block_data['prev_state_planet'] = block_data['state_planet'].shift(1)
                block_data['prev_state_planet'] = np.where(np.isnan(block_data['prev_state_planet']), 0, block_data['prev_state_planet'])

                block_data['same_earth'] = np.where(block_data['state_earth'] == block_data['prev_state_earth'], 1, 0)
                block_data['same_planet'] = np.where(block_data['state_planet'] == block_data['prev_state_planet'], 1, 0)

                #get summary results
                block_trials_stat = summary_stats(block_data)
                block_trials_stat.insert(0, Space_ProcData.loc[0, 'sub'])
                block_trials_stat.insert(1, Space_ProcData.loc[0, 'ses'])

                block_name = 'b' + str(b)
                block_trials_stat.insert(2, block_name)

                #append new rows
                overall_summary_data.loc[len(overall_summary_data)] = block_trials_stat

            #update count for files loop
            count = 1

    else:
         overall_summary_data = 'no files'
         space_group_trialsdat = 'no files'

    return overall_summary_data, space_group_trialsdat



Execution Outputs
-----------------


* group_trialdat : no files
* summarySpace_dat : no files


Runtime info
------------


* duration : 0.004773
* hostname : nut-azp271-10239
* prev_wd : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* working_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/SpaceGame/_session_id_1/summaryData/mapflow/_summaryData0


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

