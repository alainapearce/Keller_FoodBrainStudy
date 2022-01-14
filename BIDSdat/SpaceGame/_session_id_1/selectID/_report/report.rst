Node: selectID (utility)
========================


 Hierarchy : SpaceGame.selectID
 Exec ID : selectID.a0


Original Inputs
---------------


* base_directory : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* dat_overwrite : False
* function_str : def checkData(subject_list, session_id, base_directory, dat_overwrite):
    import pandas as pd
    from pathlib import Path
    from nipype import Node, DataGrabber
    from collections.abc import Iterable

    #raw data
    raw_data_path = Path(base_directory).joinpath('raw_data')

    #database
    database_path = Path(base_directory).joinpath('derivatives/preprocessed/beh/')

    #get session
    #check if session_id is an iterable
    if isinstance(session_id, Iterable) == True:
        session = str(''.join(session_id))
    else:
        session = str(session_id)

    session_num = int(session)

    #check if has 1 or 2 session lists
    if isinstance(subject_list[0], str) == True:
        subject_list_use = subject_list
    else:
        session = session_num - 1
        subject_list_use = subject_list[session][0]

    #check for existing data
    if dat_overwrite is False:
        #load data 
        database = Path(database_path).joinpath('task-space_summary.tsv')
        Space_database = pd.read_csv(str(database), sep = '\t', encoding = 'utf-8-sig', header = 0, engine='python')

        #check session in database
        db_sessions = Space_database.ses.unique()

        #if session number is in database
        if session_num in db_sessions:

            Space_database_ses = Space_database.groupby('ses').get_group(session_num)

            subs = list(subject_list_use)

            for sub in subs:

                #check if in database
                if len(Space_database_ses[Space_database_ses['sub']==int(sub)].index.tolist()) > 0:
                    #remove sub if in list that exists in database already
                    print('Skipping sub-' + str(sub) + ' for session' + str(session_num) + ' - Exists in database already.')
                    subject_list_use.remove(sub)

    #get file paths
    if len(subject_list_use) > 0:
        template_path = Path('sub-%s/ses-%s/beh/*task-space*.tsv')
        selectfiles = Node(DataGrabber(infields=['subject_ids', 'session_id'],
                      outfields=['sub_files'],
                      base_directory = str(raw_data_path), 
                      template = str(template_path),
                      sort_filelist = True),
          name='selectfiles')
        selectfiles.inputs.session_id = session_id
        selectfiles.inputs.subject_ids = subject_list_use

        sub_files = selectfiles.run().outputs.sub_files

    else:
        sub_files = 'No subfiles'

    return sub_files

* session_id : 1
* subject_list : [[[]], [['038', '019', '095', '040', '039', '007', '093', '074', '026', '033', '073', '049', '055', '096', '028', '020', '035', '078', '083', '005', '071', '023', '006', '045', '054', '080', '094', '018', '089', '002', '009', '021', '043', '051', '084', '037', '052', '017', '003', '001', '011', '041', '068']]]


Execution Inputs
----------------


* base_directory : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* dat_overwrite : False
* function_str : def checkData(subject_list, session_id, base_directory, dat_overwrite):
    import pandas as pd
    from pathlib import Path
    from nipype import Node, DataGrabber
    from collections.abc import Iterable

    #raw data
    raw_data_path = Path(base_directory).joinpath('raw_data')

    #database
    database_path = Path(base_directory).joinpath('derivatives/preprocessed/beh/')

    #get session
    #check if session_id is an iterable
    if isinstance(session_id, Iterable) == True:
        session = str(''.join(session_id))
    else:
        session = str(session_id)

    session_num = int(session)

    #check if has 1 or 2 session lists
    if isinstance(subject_list[0], str) == True:
        subject_list_use = subject_list
    else:
        session = session_num - 1
        subject_list_use = subject_list[session][0]

    #check for existing data
    if dat_overwrite is False:
        #load data 
        database = Path(database_path).joinpath('task-space_summary.tsv')
        Space_database = pd.read_csv(str(database), sep = '\t', encoding = 'utf-8-sig', header = 0, engine='python')

        #check session in database
        db_sessions = Space_database.ses.unique()

        #if session number is in database
        if session_num in db_sessions:

            Space_database_ses = Space_database.groupby('ses').get_group(session_num)

            subs = list(subject_list_use)

            for sub in subs:

                #check if in database
                if len(Space_database_ses[Space_database_ses['sub']==int(sub)].index.tolist()) > 0:
                    #remove sub if in list that exists in database already
                    print('Skipping sub-' + str(sub) + ' for session' + str(session_num) + ' - Exists in database already.')
                    subject_list_use.remove(sub)

    #get file paths
    if len(subject_list_use) > 0:
        template_path = Path('sub-%s/ses-%s/beh/*task-space*.tsv')
        selectfiles = Node(DataGrabber(infields=['subject_ids', 'session_id'],
                      outfields=['sub_files'],
                      base_directory = str(raw_data_path), 
                      template = str(template_path),
                      sort_filelist = True),
          name='selectfiles')
        selectfiles.inputs.session_id = session_id
        selectfiles.inputs.subject_ids = subject_list_use

        sub_files = selectfiles.run().outputs.sub_files

    else:
        sub_files = 'No subfiles'

    return sub_files

* session_id : 1
* subject_list : [[[]], [['038', '019', '095', '040', '039', '007', '093', '074', '026', '033', '073', '049', '055', '096', '028', '020', '035', '078', '083', '005', '071', '023', '006', '045', '054', '080', '094', '018', '089', '002', '009', '021', '043', '051', '084', '037', '052', '017', '003', '001', '011', '041', '068']]]


Execution Outputs
-----------------


* sub_files : No subfiles


Runtime info
------------


* duration : 0.271266
* hostname : nut-azp271-10239
* prev_wd : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* working_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/SpaceGame/_session_id_1/selectID


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

