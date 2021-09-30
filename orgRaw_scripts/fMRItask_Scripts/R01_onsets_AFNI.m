
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%      fMRI food viewing Onsets Script               %%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%This script was written by Alaina Pearce in August 2018 for
%%the purpose of processing onsets and behavioral data for the 
%%R01 imaging task

function  R01_onsets_AFNI(parID, session)
    %fixTab: table of fixation durations to be used in a shell script when
    %looping through participants--can add together to make database. See shell
    %script "TRT_procAFNI.m"

    %parID-participant id; can be a single ID or a vector of id's 
    %(e.g., [1, 3, 5])
    %session-time point, added in case particpants are brought back as part of
    %a pilot longitudinal grant (1 or 2)

    %Task conditions:
    %A: High ED-large portion
    %B: High ED-small portion
    %C: Low ED-large portion
    %D: Low ED-small portion
    %E: Office-large portion
    %F: Office-small portion

    %%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%                         Setup                       %%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %!need to edit this section (and all paths) if move script or any directories it calls!

    %get working directory path for where this script is saved
    %(individual path info '/Box Sync/b-childfoodlab_Shared/Test-retest Project/Bari_SPMreprocess/Scripts/AFNI_proc')
    script_wd = mfilename('fullpath');

    %get location/character number for '/" in file path
    if ismac()
        slashloc_wd = find(script_wd == '/');
        slash = '/';
    else 
        slashloc_wd = find(script_wd == '\');
        slash = '\';
    end

    %use all characters in path name upto the 7th slash (individual path info
    %'/Box Sync/b-childfoodlab Shared/Test-retest Project/)
    task_base_wd = [script_wd(1:slashloc_wd(9)) slash 'R01_fMRI_task'];

    %this will tell matlab to look at all files withing the base_wd--so any
    %subfolder will be added to search path
    %addpath(genpath(task_base_wd));

    %make raw directory path 
    raw_data_wd = [task_base_wd slash 'R01_fMRI_Raw_Data_Files'];

    %make onsets directory path 
    onsets_data_wd = [task_base_wd slash 'R01_fMRI_Onset_Data_Files'];

    %make processed data directory path 
    proc_data_wd = [task_base_wd slash 'R01_fMRI_Processed_Data_Files'];

    %make databse directory path and go there
    database_wd = [task_base_wd slash 'R01_fMRI_Databases'];


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%         Load Databases and Clean up old ones        %%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    cd(database_wd);

    %create str to identify files using wildcard '*'
    database_file_str = 'R01_fMRI_*.csv';

    %use str to identify files--save as table
    database_file = dir(char(database_file_str));
    database_file_tab = struct2table(database_file);

    %create str to identify only 'BlocksLong' files using wildcard '*' and
    %identify those that match--save as table
    long_datfile_str = struct2table(dir(char('R01_fMRI_database_BlocksLong*.csv')));

    %create an matrix of zeros that has as many rows as 'database_file_tab' and
    %as many collumns as the rows of 'long_datfile_str'--will use to fill in
    %logical indicators for matching filenames with long_datfile_str
    long_datfile_ind = zeros(height(database_file_tab), height(long_datfile_str));

    %loop through length of long_datfile_str to identify which files identified
    %in 'database_file_tab' are 'BlockLong' databases (match names in
    %'long_datafile_str'. When using strcmp, can compare all strings in array
    %(i.e, database_file_tab.name) to single string (i.e.,
    %long_datfile_str.name(s). each loop we add the logical indicator to
    %collumn s (loop number) of the zero matrix we created previously.
    %note: need the check to see if more than 1 because if only one, using (s)
    %will select character s of the name and not name s
    for s = 1:height(long_datfile_str)
        if height(long_datfile_str) > 1
            ind = strcmp(database_file_tab.name, long_datfile_str.name(s));
        else
           ind = strcmp(database_file_tab.name, long_datfile_str.name);
        end
        long_datfile_ind(:,s) = ind;
    end

    %add across rows of indicator matrix to determine which rows of
    %'database_file_tab' have names matching 'long_datfile_str'--identifile
    %'LongBlock' databases. Rows with zeros instead of 1's will indicate the
    %regular database files. Note: need to tell matlab to save as logical
    %becuase we computed a sum, which is numeric by default
    long_datfile_ind = logical(sum(long_datfile_ind, 2));

    %use datfile indicator to separate file names by database type (i.e., long
    %or regular) and then sort those tables by date. Note: useing
    %'~long_datafile_long' keeps those that are zero--means 'not true' in this
    %sense where 'long_datafile_long' is a logical indicator (1-true/0-false)
    database_file_long_tab = database_file_tab(long_datfile_ind, :);
    database_file_reg_tab = database_file_tab(~long_datfile_ind, :);

    %sort indetified flies by date created -- load only the most recent
    database_file_long_tab = sortrows(database_file_long_tab, 3, 'descend');
    database_file_reg_tab = sortrows(database_file_reg_tab, 3, 'descend');

    R01_fMRI_dat = readtable(char(database_file_reg_tab.name(1)), 'ReadVariableNames', true);
    R01_fMRI_dat_VN = R01_fMRI_dat.Properties.VariableNames;

    R01_fMRI_dat_long = readtable(char(database_file_long_tab.name(1)), 'ReadVariableNames', true);
    R01_fMRI_dat_long_VN = R01_fMRI_dat_long.Properties.VariableNames;

    %make sure first collumn variable name is 'ParticipantID' for both databases-- 
    %sometimes reads first collumn header in weird (e.g., 'x__ParticipantID');
    if ~strcmp(R01_fMRI_dat_VN(1), 'ParticipantID')
        R01_fMRI_dat_VN(1) = {'ParticipantID'};
        R01_fMRI_dat.Properties.VariableNames = R01_fMRI_dat_VN;
    end

    if ~strcmp(R01_fMRI_dat_long_VN(1), 'ParticipantID')
        R01_fMRI_dat_long_VN(1) = {'ParticipantID'};
        R01_fMRI_dat_long.Properties.VariableNames = R01_fMRI_dat_long_VN;
    end

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%              Participant ID loop Setup              %%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %get number of participants
    npar = length(parID);

    %create empty tables to store summary data in wide and long format (by
    %block) and add variable names from loaded databases. Create one row per
    %participant for wide and 5 per participant for long format
    summary_data = array2table(zeros(npar*5, 60));
    summary_data.Properties.VariableNames = R01_fMRI_dat_VN;
    summary_data.Version = string(summary_data.Version);
    r_prev_row = 0; %no runs in yet

    summary_data_long = array2table(zeros((npar*5*6), 14));
    summary_data_long.Properties.VariableNames = R01_fMRI_dat_long_VN;
    summary_data_long.Version = string(summary_data_long.Version);
    summary_data_long.Block = string(summary_data_long.Block);
    rb_prev_row = 0; %no runs/blocks in yet


    %track number of duplicates so can remove extra rows at end
    n_duplicate = 0;
    run_count = 0;
    block_count = 0;

    %start loop based on number of inputs in parID variable
    for p = 1:npar

        %convert participant ID to string with 3 digit before the decimal point
        %(specified by '%03.f'). This ensures 1 is converted to '001' to match
        %naming convention of .txt files
        %convert session to string
        parID_num = parID(p);

        if length(session) > 1
            session_num = session(p);
        else
            session_num = session;
        end
        session_str = num2str(session_num);
        parID_str = num2str(parID_num, '%03.f');

        %check to see if participant exists in database
        par_ind = R01_fMRI_dat.ParticipantID == parID_num;
        session_ind = R01_fMRI_dat.Session == session_num;
        if sum(par_ind & session_ind) > 0
            disp(sprintf('Participant %s exists in database for session %s. Please delete data from database if want to overwrite', parID_str, session_str));
            n_duplicate = n_duplicate + 1;
        else

            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%        Process Particpant Raw Task Data             %%%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %Go to raw data and load .txt file that was exported
            cd(raw_data_wd);

            %get name for onset file using wildcard ('*'): want file that starts with
            %ID number Session (e.g., 101A) and ends in '.csv'
            IDfile = strcat('*Raw_', parID_str, '-', session_str, '.txt');

            %get name of onset file. 
            %NOTE: since we used a wildcard ('*') to fill in parts of file names that
            %differ between participants, we need to do 2 things to get file name in
            %script:
            %1) cd to directory where file is (we did this above on line 40)
            %2) use {dir(char(...)} syntasx--this makes the IDfile a character type of
            %data and then the 'dir' says it will be looking for a directory. Without
            %the use of 'dir' it won't incorporate '*' as a wildcard and will search
            %for exact string (e.g., '101A*.csv')
            raw_data_file = {dir(char(IDfile))};

            %load onsets file as a table--Delimiter is to indicate how values are
            %separated in file (e.g., comma for csv, tab ('/t') for some .txt). We want
            %this to also read in the first row as a header so set 'ReadVariableNames'
            %to true
            R01_fMRI_raw_dat = readtable(raw_data_file{1}.name,'ReadVariableNames',true);

            file_name = raw_data_file{1}.name;
            file_uscore = find(file_name == '_');
            version_str = file_name((file_uscore(1)+1):(file_uscore(2)-1));


            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%           Get cleaned dataset                       %%%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %select only variables interested in using for processed data
            R01_fMRI_raw_dat.Version(:) = 'A';
            R01_fMRI_vars = {'Subject', 'Session', 'Version', 'RunList', 'Trial', 'Condition', 'Filename', 'StimSlide_OnsetTime', 'StimSlide_OnsetToOnsetTime', 'StimSlide_RESP', 'StimSlide_RT'};
            R01_fMRI_ProcData = R01_fMRI_raw_dat(:, R01_fMRI_vars); 

            %rename the 'Stim_**' and other collumns.
            R01_fMRI_ProcData.Properties.VariableNames = {'ParID', 'Session', 'Version', 'Run', 'Block', 'Condition', 'StimList', 'StimOnset', 'StimOnset2Onset', 'WantResp','WantRT'};
            R01_fMRI_ProcData.StimOnset_zsync(:) = 0;
            R01_fMRI_ProcData.StimOnset_rzsync(:) = 0;

            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%           Extract Summary Data                      %%%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

            %create empty errors cell array to fill in with error messages later if
            %needed
            errors = [];
            %set number of errors foudn to 0; will update later if needed
            error_num = 0;

            %loop structure:
            %for runs 1 to 6 (r=1:6)
            %%%for blocks 1 to number of blocks (b=1:t_blocks)
            nruns_unique = unique(R01_fMRI_ProcData.Run);
            nruns = length(nruns_unique);
            
            run_count = run_count + nruns;
            
            %create onset data per participant
            onsets_dat = array2table(zeros(nruns, 6));

            %create fixation data per participant
            fix_dat = array2table(zeros(nruns*6, 4));
            fix_dat.Properties.VariableNames = {'ParticipantID', 'Run', 'PrevBlock', 'FixAfterBlock'}; 
            for r=1:nruns
                if r == 1
                    r_start = r_prev_row + r;
                    r_row = r_start;
                end
                
                %make logical indicator to mark rows of table where Run = run number
                %will update run number (r) with each loop
                r_ind = R01_fMRI_ProcData.Run == r;

                %reduce collumns to match nblocks in all run data (some runs
                %may have fewer but
                nblock_runs_unique = unique(R01_fMRI_ProcData.Block);
                nblocks_runs = length(nblock_runs_unique);
                onsets_dat = onsets_dat(:, 1:nblocks_runs);

                %use logical indicator vector to select only rows that match current
                %run
                run_dat =  R01_fMRI_ProcData(r_ind, :);

                %zero onsets to start of run--need to remember to throw out the
                %initial fixation (2TRs?) in afni_proc.py. 0 sec will
                %correspond to first image of first block of a run
                init_onset = run_dat.StimOnset(1);
                run_dat.StimOnset_zsync = (run_dat.StimOnset - init_onset)/1000;
                run_dat.StimOnset_rzsync = round(run_dat.StimOnset_zsync);
                
                %add to proccessed/cleaned dataset
                R01_fMRI_ProcData.StimOnset_zsync(r_ind) = run_dat.StimOnset_zsync(:);
                R01_fMRI_ProcData.StimOnset_rzsync(r_ind) = run_dat.StimOnset_rzsync(:);

                nblock_unique = unique(run_dat.Block);
                nblocks = length(nblock_unique);
                
                block_count = block_count + nblocks;

                for b=1:nblocks
                    if b == 1
                        rb_start = rb_prev_row + b;
                        rb_row = rb_start;

                        if r == 1
                            rb_start_run = rb_prev_row + b;
                        end
                    end

                    %make logical indicator to mark rows of table where block = block number
                    %will update block number (b) with each loop
                    b_ind = run_dat.Block == b;

                    %use logical indicator vector to select only rows that match current
                    %run
                    block_dat =  run_dat(b_ind, :);

                    if r == 1 && b == 1
                        %final block stim onset
                        fblock_onset = block_dat.StimOnset_rzsync(end);
                        f_row = 1;
                        f_start = f_row;
                    else
                        if b == 1
                            f_row = f_row + 1;
                            f_start = f_row;
                            fix_dat.PrevBlock(f_row) = nblocks;
                            %stim dur = 2.5 sec and inter-block-interval = 0.5
                            fix_dat.FixAfterBlock(f_row) = round(block_dat.StimOnset(1)/1000) - (fblock_onset+2.5+.5);
                            fblock_onset = block_dat.StimOnset_rzsync(end);
                        else 
                            f_row = f_row + 1;
                            fix_dat.PrevBlock(f_row) = b - 1;
                            %stim dur = 2.5 sec and inter-block-interval = 0.5
                            fix_dat.FixAfterBlock(f_row) = block_dat.StimOnset_rzsync(1) - (fblock_onset+2.5+.5);

                            if b == nblocks
                                fblock_onset = round(block_dat.StimOnset(end)/1000);
                            else
                                %final block stim onset
                                fblock_onset = block_dat.StimOnset_rzsync(end);
                            end
                        end

                    end

                    %get condition number
                    c_letter = block_dat.StimList{1}(1);
                    %get condition number
                    if strcmp(c_letter, 'A')
                        c_num = 1;
                        c_name = 'HighLarge';
                    elseif strcmp(c_letter, 'B')
                        c_num = 2;
                        c_name = 'HighSmall';
                    elseif strcmp(c_letter, 'C')
                        c_num = 3;
                        c_name = 'LowLarge';
                    elseif strcmp(c_letter, 'D')
                        c_num = 4;
                        c_name = 'LowSmall';
                    elseif strcmp(c_letter, 'E')
                        c_num = 5;
                        c_name = 'OfficeLarge';
                    elseif strcmp(c_letter, 'F')
                        c_num = 6;
                        c_name = 'OfficeSmall';
                    end

                    %add name to onsets var names
                    if r == 1
                        onsets_dat.Properties.VariableNames(c_num) = {c_name};
                    end
                    onsets_dat(r, c_num) = {block_dat.StimOnset_rzsync(1)};

                    %add vector index for starting data column and the number of caluclated
                    %values each block dataset in summary data. need 8 calculated
                    %values so multiply by block number.
                    %add 5 to that to get start because starting and column
                    %13.
                    dat_start = (8*(c_num))+5;
                    dat_end = dat_start+7;

                    %Get block specific summary data
                    nWant_ind = strcmp(block_dat.WantResp, 'd');
                    nMiss_ind = strcmp(block_dat.WantResp, '');
                    nWant = sum(nWant_ind);
                    pWant = nWant/length(nWant_ind);
                    nDontWant = sum(~nWant_ind);
                    pDontWant = nDontWant/length(nWant_ind);
                    nMiss = sum(nMiss_ind);
                    pMiss = nMiss/length(nMiss_ind);
                    meanRT = mean(block_dat.WantRT(~nMiss_ind));
                    medRT = median(block_dat.WantRT(~nMiss_ind));

                    dat_tab = array2table([nWant, pWant, nDontWant, pDontWant, nMiss, pMiss, meanRT, medRT]);

                    %wide data
                    summary_data(r_row, dat_start:dat_end) = dat_tab;

                    %long data
                    summary_data_long.Order(rb_row) = b;
                    summary_data_long.Block(rb_row) = c_name;
                    summary_data_long(rb_row, 7:14) = dat_tab;

                    %steup up next block row
                    if b == nblocks
                        rb_prev_row = rb_row;
                    else
                        rb_row = rb_row + 1;
                    end
                end

                %get avg run data
                nWant_ind_run = strcmp(run_dat.WantResp, 'c') | strcmp(run_dat.WantResp, 'a');
                nMiss_ind_run = strcmp(run_dat.WantResp, '');
                nWant_run = sum(nWant_ind_run);
                pWant_run = nWant_run/length(nWant_ind_run);
                nDontWant_run = sum(~nWant_ind_run);
                pDontWant_run = nDontWant_run/length(nWant_ind_run);
                nMiss_run = sum(nMiss_ind_run);
                pMiss_run = nMiss/length(nMiss_ind_run);
                meanRT_run = mean(run_dat.WantRT(~nMiss_ind_run));
                medRT_run = median(run_dat.WantRT(~nMiss_ind_run));

                %Add wide run data
                dat_tab_run = array2table([nWant_run, pWant_run, nDontWant_run, pDontWant_run, nMiss_run, pMiss_run, meanRT_run, medRT_run]);
                summary_data(r_row, 5:12) = dat_tab_run;
                summary_data.Run(r_row) = r;

                %add wide data same for all blocks
                summary_data_long.Run(rb_start:rb_row) = r;

                %Add fix data
                fix_dat.Run(f_start:f_row) = r;

                if nblocks ~= 6
                    block_error = sprintf('Participant %s has %d blocks in run %d in session %s for task version %s', parID_str, nblocks, r, session_str, version_str);
                    disp(block_error);
                    errors = [errors; block_error];
                    error_num = error_num + 1;
                end

                %steup up next run row
                if r == nruns
                    r_prev_row = r_row;
                else
                    r_row = r_row + 1;
                end

            end

            if nruns ~= 5
                run_error = sprintf('Participant %s has %d runs in session %s for task version %s', parID_str, nruns, session_str, version_str);
                disp(run_error);
                errors = [errors; run_error];
                error_num = error_num + 1;
            end


            %Add wide run data
            summary_data.ParticipantID(r_start:r_prev_row) = parID_num;
            summary_data.Session(r_start:r_prev_row) = session;
            summary_data.Version(r_start:r_prev_row) = version_str;

            %add wide data same for all blocks
            summary_data_long.ParticipantID(rb_start_run:rb_row) = parID_num;
            summary_data_long.Session(rb_start_run:rb_row) = session;
            summary_data_long.Version(rb_start_run:rb_row) = version_str;

            %Add fix data
            fix_dat.ParticipantID(1:f_row) = parID_num;

            %output cleaned/process database with onsets synced to run 0's
            today_date = date;
            writetable(R01_fMRI_ProcData, [proc_data_wd slash sprintf('R01_%s_Processed_%s_%s_%s.txt', version_str, parID_str, session_str, today_date)], 'WriteRowNames',true)
            %%

            %output onsets
            for d = 1:width(onsets_dat)
                onsets_cond = onsets_dat(:, d);
                onsets_cond.Properties.VariableNames = {'Cond'};
                onsets_cond.AM = strcat(string(table2array(onsets_cond(:, 1))), repmat('*',nruns, 1), string(1:1:nruns)');
                onsets_cond.star = repmat('*', nruns, 1);
                condname = onsets_dat.Properties.VariableNames(d);
                writetable(onsets_cond(:, {'Cond', 'star'}), [onsets_data_wd  slash 'TaskOnsets_AFNI' slash sprintf('R01_%s-%s_%s_%s_AFNIonsets.txt', parID_str, session_str, version_str, condname{1})], 'Encoding', 'US-ASCII', 'WriteVariableNames', 0, 'Delimiter','tab');
                writetable(onsets_cond(:, {'AM', 'star'}), [onsets_data_wd  slash 'TaskOnsets_AFNI' slash sprintf('R01_%s-%s_%s_%s_AFNIonsets_RunAM.txt', parID_str, session_str, version_str, condname{1})], 'Encoding', 'US-ASCII', 'WriteVariableNames', 0, 'Delimiter','tab');

            end

            %output fixations
            writetable(fix_dat, [onsets_data_wd  slash 'TaskFixDurations' slash sprintf('R01_%s_%s-%s_FixDur.txt', version_str, parID_str, session_str)]);

            %if the 'errors' cell array is not empty (i.e., there were errors), then
            %convert to table ('cell2table(errors)') and export file beigning with 
            %"ErrorMsgs and using sprintf to name file with parID and session
            %if 'errors' cell array is empty, then export empty tabel with file
            %starting "NoErrorMsgs" and using sprintf for parID and session
            %NOTE: exported empty files with different start to file name so easily
            %able to know that all participants were checked and number with/without
            %errors.
            if error_num > 0
                if ischar(errors)
                    writetable(cell2table(cellstr(string(errors))), [onsets_data_wd  slash 'TaskOnsetErrors' slash sprintf('ErrorMsgs_%s_%s.txt', parID_str, session_str)]);
                elseif iscell(errors)
                    writetable(cell2table(errors), [onsets_data_wd  slash 'TaskOnsetErrors' slash sprintf('ErrorMsgs_%s_%s.txt', parID_str, session_str)]);
                end
            else
                writetable(table(errors), [onsets_data_wd slash 'TaskOnsetErrors' slash sprintf('NoErrorMsgs_%s_%s.txt', parID_str, session_str)]);
            end
        end
    end  

    %remove extra rows
    summary_data((run_count+1):end, :) = [];
    summary_data_long((block_count + 1):end, :) = [];

    %combine data and export
    if height(summary_data) > 0
        today_date = date;

        R01_fMRI_dat = [R01_fMRI_dat; summary_data];
        R01_fMRI_dat_long = [R01_fMRI_dat_long; summary_data_long];

        cd(database_wd);

        %cleanup old files--move all files to 'Old_database_backup'
        for m = 1:height(database_file_tab)
            movefile(char(database_file_tab.name(m)), 'Old_database_backup/');
        end

        writetable(R01_fMRI_dat, sprintf('R01_fMRI_database_%s.csv', today_date), 'WriteRowNames',true);
        writetable(R01_fMRI_dat_long, sprintf('R01_fMRI_database_BlocksLong_%s.csv', today_date), 'WriteRowNames',true);
    end
          
end
