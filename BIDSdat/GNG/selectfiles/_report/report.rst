Node: selectfiles (io)
======================


 Hierarchy : GNG.selectfiles
 Exec ID : selectfiles


Original Inputs
---------------


* base_directory : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data
* drop_blank_outputs : False
* field_template : <undefined>
* raise_on_empty : True
* sort_filelist : True
* subject_ids : ['031', '033', '034', '035', '036']
* template : sub-%s/ses-1/beh/*task-gng*.tsv
* template_args : {'gngFiles': [['subject_ids']]}


Execution Inputs
----------------


* base_directory : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data
* drop_blank_outputs : False
* field_template : <undefined>
* raise_on_empty : True
* sort_filelist : True
* subject_ids : ['031', '033', '034', '035', '036']
* template : sub-%s/ses-1/beh/*task-gng*.tsv
* template_args : {'gngFiles': [['subject_ids']]}


Execution Outputs
-----------------


* gngFiles : ['/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-031/ses-1/beh/sub-031_ses-1_task-gng_events.tsv', '/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-033/ses-1/beh/sub-033_ses-1_task-gng_events.tsv', '/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-034/ses-1/beh/sub-034_ses-1_task-gng_events.tsv', '/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-035/ses-1/beh/sub-035_ses-1_task-gng_events.tsv', '/Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/raw_data/sub-036/ses-1/beh/sub-036_ses-1_task-gng_events.tsv']


Runtime info
------------


* duration : 0.021606
* hostname : H8-NTR-GCH12202
* prev_wd : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat
* working_dir : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/GNG/selectfiles


Environment
~~~~~~~~~~~


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
* HOME : /Users/baf44
* HOMEBREW_CELLAR : /opt/homebrew/Cellar
* HOMEBREW_PREFIX : /opt/homebrew
* HOMEBREW_REPOSITORY : /opt/homebrew
* HOMEBREW_SHELLENV_PREFIX : /opt/homebrew
* INFOPATH : /opt/homebrew/share/info:
* LANG : en_US.UTF-8
* LOCAL_DIR : /Users/baf44/freesurfer/local
* LOGNAME : baf44
* MANPATH : /opt/homebrew/share/man:
* MINC_BIN_DIR : /Users/baf44/freesurfer/mni/bin
* MINC_LIB_DIR : /Users/baf44/freesurfer/mni/lib
* MNI_DATAPATH : /Users/baf44/freesurfer/mni/data
* MNI_DIR : /Users/baf44/freesurfer/mni
* MNI_PERL5LIB : /Users/baf44/freesurfer/mni/lib/../Library/Perl/Updates/5.12.3
* OLDPWD : /Users/baf44
* OS : Darwin
* PATH : /Users/baf44/opt/anaconda3/bin:/Users/baf44/opt/anaconda3/condabin:/opt/homebrew/bin:/opt/homebrew/sbin:/Users/baf44/freesurfer/bin:/Users/baf44/freesurfer/fsfast/bin:/Users/baf44/freesurfer/mni/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Users/baf44/abin
* PERL5LIB : /Users/baf44/freesurfer/mni/lib/../Library/Perl/Updates/5.12.3
* PWD : /Users/baf44/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/BIDSdat/code
* SHELL : /bin/bash
* SHLVL : 1
* SSH_AUTH_SOCK : /private/tmp/com.apple.launchd.IGHDFDpBhr/Listeners
* SUBJECTS_DIR : /Users/baf44/freesurfer/subjects
* TERM : xterm-256color
* TERM_PROGRAM : Apple_Terminal
* TERM_PROGRAM_VERSION : 440
* TERM_SESSION_ID : E284AFD2-CB89-4563-819F-34ED4239660B
* TMPDIR : /var/folders/73/mkrc96td4nv8hyspvjhndxt40000gp/T/
* USER : baf44
* XPC_FLAGS : 0x0
* XPC_SERVICE_NAME : 0
* _ : ./GNG_WF.py
* _CE_CONDA : 
* _CE_M : 
* __CFBundleIdentifier : com.apple.Terminal

