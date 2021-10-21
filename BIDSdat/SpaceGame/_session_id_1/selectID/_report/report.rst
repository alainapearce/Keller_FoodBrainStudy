Node: selectID (utility)
========================


 Hierarchy : SpaceGame.selectID
 Exec ID : selectID.a0


Original Inputs
---------------


* base_directory : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* dat_overwrite : True
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
* subject_list : [[['105', '089', '039', '080', '103', '077', '098', '120', '045', '056', '048', '073', '074', '054', '090', '075', '112', '041', '113', '095', '084', '106', '057', '072', '111', '119', '117', '055', '047', '021', '121', '071', '093', '104', '116', '052', '078', '083', '069', '070', '107', '051', '068', '118', '096', '101', '049']], [['089', '001', '049', '039', '080', '006', '002', '023', '020', '045', '009', '074', '073', '094', '028', '054', '019', '041', '095', '005', '084', '043', '003', '055', '007', '038', '026', '021', '033', '071', '093', '018', '052', '035', '078', '011', '083', '037', '040', '051', '068', '096', '017']]]


Execution Inputs
----------------


* base_directory : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* dat_overwrite : True
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
* subject_list : [[['105', '089', '039', '080', '103', '077', '098', '120', '045', '056', '048', '073', '074', '054', '090', '075', '112', '041', '113', '095', '084', '106', '057', '072', '111', '119', '117', '055', '047', '021', '121', '071', '093', '104', '116', '052', '078', '083', '069', '070', '107', '051', '068', '118', '096', '101', '049']], [['089', '001', '049', '039', '080', '006', '002', '023', '020', '045', '009', '074', '073', '094', '028', '054', '019', '041', '095', '005', '084', '043', '003', '055', '007', '038', '026', '021', '033', '071', '093', '018', '052', '035', '078', '011', '083', '037', '040', '051', '068', '096', '017']]]


Execution Outputs
-----------------


* sub_files : ['/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-105/ses-1/beh/sub-105_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-089/ses-1/beh/sub-089_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-039/ses-1/beh/sub-039_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-080/ses-1/beh/sub-080_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-103/ses-1/beh/sub-103_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-077/ses-1/beh/sub-077_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-098/ses-1/beh/sub-098_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-120/ses-1/beh/sub-120_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-045/ses-1/beh/sub-045_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-056/ses-1/beh/sub-056_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-048/ses-1/beh/sub-048_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-073/ses-1/beh/sub-073_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-074/ses-1/beh/sub-074_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-054/ses-1/beh/sub-054_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-090/ses-1/beh/sub-090_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-075/ses-1/beh/sub-075_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-112/ses-1/beh/sub-112_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-041/ses-1/beh/sub-041_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-113/ses-1/beh/sub-113_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-095/ses-1/beh/sub-095_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-084/ses-1/beh/sub-084_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-106/ses-1/beh/sub-106_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-057/ses-1/beh/sub-057_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-072/ses-1/beh/sub-072_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-111/ses-1/beh/sub-111_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-119/ses-1/beh/sub-119_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-117/ses-1/beh/sub-117_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-055/ses-1/beh/sub-055_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-047/ses-1/beh/sub-047_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-021/ses-1/beh/sub-021_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-121/ses-1/beh/sub-121_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-071/ses-1/beh/sub-071_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-093/ses-1/beh/sub-093_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-104/ses-1/beh/sub-104_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-116/ses-1/beh/sub-116_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-052/ses-1/beh/sub-052_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-078/ses-1/beh/sub-078_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-083/ses-1/beh/sub-083_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-069/ses-1/beh/sub-069_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-070/ses-1/beh/sub-070_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-107/ses-1/beh/sub-107_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-051/ses-1/beh/sub-051_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-068/ses-1/beh/sub-068_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-118/ses-1/beh/sub-118_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-096/ses-1/beh/sub-096_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-101/ses-1/beh/sub-101_ses-1_task-space_events.tsv', '/Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-049/ses-1/beh/sub-049_ses-1_task-space_events.tsv']


Runtime info
------------


* duration : 0.037321
* hostname : ND-NTR-FCH12085
* prev_wd : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* working_dir : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/SpaceGame/_session_id_1/selectID


Environment
~~~~~~~~~~~


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
* LaunchInstanceID : 0D478C5D-FF68-421D-8CCC-AB6D8F78AE4E
* OLDPWD : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/orgRaw_scripts
* PATH : /Users/azp271/opt/anaconda3/bin:/Users/azp271/opt/anaconda3/condabin:/Library/Frameworks/Python.framework/Versions/3.9/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/TeX/texbin:/opt/X11/bin
* PWD : /Users/azp271/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code
* SECURITYSESSIONID : 186a9
* SHELL : /bin/zsh
* SHLVL : 1
* SSH_AUTH_SOCK : /private/tmp/com.apple.launchd.7qhvbO6vQS/Listeners
* TERM : xterm-256color
* TERM_PROGRAM : Apple_Terminal
* TERM_PROGRAM_VERSION : 440
* TERM_SESSION_ID : B7C4C25B-1D63-438B-8F77-419357A4FCCB
* TMPDIR : /var/folders/y5/lybvr3s93wn9ny273pk2fhgr0000gp/T/
* USER : azp271
* XPC_FLAGS : 0x0
* XPC_SERVICE_NAME : 0
* _ : /Users/azp271/opt/anaconda3/bin/python3
* _CE_CONDA : 
* _CE_M : 
* __CFBundleIdentifier : com.apple.Terminal

