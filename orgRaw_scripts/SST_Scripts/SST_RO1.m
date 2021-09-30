%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%           SST data processing script              %%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%This script was written by Bari Fuchs and Alaina Pearce in March 2018 for 
%the purpose of processing the SST task used in the RO1 grant. 
function SST_RO1(parID, session)
%parID-participant id; can be a single ID or a vector of id's 
%(e.g., [1, 3, 5])
%session-time point, added in case particpants are brought back as part of
%a pilot longitudinal grant

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%                         Setup                       %%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%!need to edit this section (and all paths) if move script or any directories it calls!

%get working directory path for where this script is saved
%(individual path info '/Box Sync/b-childfoodlab Shared/RO1_Brain_Mechanisms_IRB_5357/Participant Data/SST/Scripts')
script_wd = mfilename('fullpath');

if ismac()
    slash_loc = find(script_wd == '/');
    slash = '/';
else 
    slash_loc = find(script_wd == '\');
    slash = '\';
end


%get location/character number for '/" in file path
slashloc_wd=find(script_wd==slash);

%use all characters in path name upto the 7th slash (individual path info
%'/Box Sync/b-childfoodlab Shared/RO1_Brain_Mechanisms_IRB_5357/Participant Data/SST)
base_wd = script_wd(1:slashloc_wd(end-1));

%this will tell matlab to look at all files withing the base_wd--so any
%subfolder will be added to search path
addpath(genpath(base_wd));

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%         Load Databases and Clean up old ones        %%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cd([base_wd 'SST_Databases']);

%create str to identify files using wildcard '*'
database_file_str = 'SST_database*.csv';

%use str to identify files--save as table
database_file = dir(char(database_file_str));
database_file_tab = struct2table(database_file);

%create str to identify only 'BlockLong' files using wildcard '*' and
%identify those that match--save as table
long_datfile_str = struct2table(dir(char('SST_database_BlockLong*.csv')));

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

SST_dat = readtable(char(database_file_reg_tab.name(1)), 'ReadVariableNames', true);
SST_dat_VN = SST_dat.Properties.VariableNames;

SST_dat_long = readtable(char(database_file_long_tab.name(1)), 'ReadVariableNames', true, 'TreatAsEmpty',{'NA'});
SST_dat_long_VN = SST_dat_long.Properties.VariableNames;

%make sure first collumn variable name is 'ParID' for both databases-- 
%sometimes reads first collumn header in weird (e.g., 'x__ParID');
if ~strcmp(SST_dat_VN(1), 'ParID')
    SST_dat_VN(1) = {'ParID'};
    SST_dat.Properties.VariableNames = SST_dat_VN;
end

if ~strcmp(SST_dat_long_VN(1), 'ParID')
    SST_dat_long_VN(1) = {'ParID'};
    SST_dat_long.Properties.VariableNames = SST_dat_long_VN;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%              Participant ID loop Setup              %%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%get number of participants
npar = length(parID);

%create empty tables to store summary data in wide and long format (by
%block) and add variable names from loaded databases. Create one row per
%participant for wide and 5 per participant for long format
summary_data = array2table(zeros(npar, 74));
summary_data.Properties.VariableNames = SST_dat_VN;

summary_data_long = array2table(zeros((npar*4), 20));
summary_data_long.Properties.VariableNames = SST_dat_long_VN;
summary_data_long.Block = string(summary_data_long.Block);
%track number of duplicates so can remove extra rows at end
n_duplicate = 0;
row_count = 0;
%start loop based on number of inputs in parID variable
for p = 1:npar
    errors = [];
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
    parID_str1 = num2str(parID_num);
    
    if length(parID_str1) == 1
        parID_str = ['00', parID_str1];
    elseif length(parID_str1) == 2
        parID_str = ['0', parID_str1];
    end
    
    %check to see if participant exists in database
    par_ind = SST_dat.ParID == parID_num;
    session_ind = SST_dat.Session == session_num;
    par_session_ind = par_ind & session_ind;
    if sum(par_ind & session_ind) > 0
        disp(sprintf('Participant %s exists in database for session %s. Please delete data from database if want to overwrite', parID_str, session_str));
        n_duplicate = n_duplicate + 1;
    else
        row_count = row_count + 1;
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%        Process Particpant Raw Task Data             %%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %Go to raw data and load .txt file that was exported
        cd([base_wd 'SST_Raw_Data_Files']);

        %get name for data file using wildcard ('*'): want file that ends with
        %'###-#.txt' (e.g., '001-1.txt')
        IDfile = strcat('stop-', parID_str1, '-', session_str, ".txt");

        %get name of onset file. 
        %NOTE: since we used a wildcard ('*') to fill in parts of file names that
        %differ between participants, we need to do 2 things to get file name in
        %script:
        %1) cd to directory where file is (we did this above on line 40)
        %2) use {dir(char(...)} syntasx--this makes the IDfile a character type of
        %data and then the 'dir' says it will be looking for a directory. Without
        %the use of 'dir' it won't incorporate '*' as a wildcard and will search
        %for exact string (e.g., '101A*.csv')
        SST_datfiles = struct2table(dir(char(IDfile)));

        %load .txt files as a table--Delimiter is to indicate how values are
        %separated in file (e.g., comma for csv, tab ('/t') for some .txt). We want
        %this to also read in the first row as a header so set 'ReadVariableNames'
        %to true
        SST_RawData = readtable(SST_datfiles.name, 'ReadVariableNames',true);

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%           Get cleaned dataset                       %%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


        %select only variables interested in using for processed data
        SST_vars = {'block', 'block_cond', 'food_cond', 'port_cond', 'stim', 'signal', 'reqSSD', 'correct', 'resp1', 'rt1', 'trueSSD', 'stimName'};
        SST_ProcData = SST_RawData(:, SST_vars); 
        SST_ProcData.Properties.VariableNames = {'Block', 'BlockCond', 'FoodCond', 'PortCond', 'Stim', 'Signal', 'reqSSD', 'Correct', 'Resp', 'RT', 'trueSSD', 'stimName'};

        SST_ProcData.ParID = repmat(parID_num, height(SST_ProcData), 1);
        SST_ProcData.Session = repmat(session_num, height(SST_ProcData), 1);
        SST_ProcData = [SST_ProcData(:, 13), SST_ProcData(:, 14), SST_ProcData(:, 1:12)];
        %rename the 'Stim_**' and other collumns.

        %go to directory where processed data are saved (individual path info '/Box
        %Sync/b-childfoodlab Shared/RO1_Brain_Mechanisms_IRB_5357/Participant
        %Data/SST/SST_Processed_Data_Files/)
        cd([base_wd 'SST_Processed_Data_Files']);

        %export datatable and use sprintf to name file with participant name and
        %session
        today = date;
        writetable(SST_ProcData, [sprintf('SST_Processed_%s_%s_%s.txt', parID_str, session_str, today)], 'WriteRowNames',true)
        %%

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%           Extract Summary Data                      %%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %instered portions from the "analyze_it.m" script are marked

        %add participant and session number
        summary_data.ParID(row_count) = parID_num;
        summary_data.Session(row_count) = session_num;

        %number of runs 
        nblocks = unique(SST_ProcData.Block);
        
        %remove first trial of each block
        for b=1:length(nblocks)
            if b == 1
                SST_ProcData_noT1 = SST_ProcData(2:end, :);
            else
                ind_block = SST_ProcData_noT1.Block == b;
                row_remove=find(any(ind_block==1,2),1);
                SST_ProcData_noT1(row_remove, :) = [];
            end
        end  

        %identify Signal and NoSignal trials using indicator variables for when 'Signal'
        %matches respectively and create two datasets
        Signal_ind = SST_ProcData_noT1.Signal == 1;
        NoSignal_ind = SST_ProcData_noT1.Signal == 0;

        SST_ProcData_noT1_Stop = SST_ProcData_noT1(Signal_ind, :);
        SST_ProcData_noT1_Go = SST_ProcData_noT1(NoSignal_ind, :);

        %summary measures - all trials
        RTmean_goAll = mean(SST_ProcData_noT1_Go.RT(SST_ProcData_noT1_Go.RT ~= 0)); %go_RTmean_all
        RTsd_goAll = std(SST_ProcData_noT1_Go.RT(SST_ProcData_noT1_Go.RT ~= 0)); %go_RTsd_all
        go_cor = sum(SST_ProcData_noT1_Go.Correct == 4); %go correct
        RTmean_goCorrect = mean(SST_ProcData_noT1_Go.RT(SST_ProcData_noT1_Go.Correct == 4 & SST_ProcData_noT1_Go.RT ~= 0)); %go_RTmean_correct
        go_error = sum(SST_ProcData_noT1_Go.Correct == 2); %go_error
        RTmean_goError = mean(SST_ProcData_noT1_Go.RT(SST_ProcData_noT1_Go.Correct == 2 & SST_ProcData_noT1_Go.RT ~= 0)); %go_RTmean_error
        go_miss = sum(SST_ProcData_noT1_Go.Correct == 1); %go_missed
        stop_RTmean_us = mean(SST_ProcData_noT1_Stop.RT(SST_ProcData_noT1_Stop.Correct == 3 & SST_ProcData_noT1_Stop.RT ~= 0)); %stop_RTmean_us
        
        %get number with zero RT
        ntrials_zero = sum(SST_ProcData_noT1_Go.RT == 0 & SST_ProcData_noT1_Go.Correct == 4);

        %%below is edited from the analyze_it script
        % calculate p(respond|signal)
        Signal_presp = sum(SST_ProcData_noT1_Stop.Correct == 3)/height(SST_ProcData_noT1_Stop);

        %number of trials
        goN = height(SST_ProcData_noT1_Go);
        stopN = height(SST_ProcData_noT1_Stop);
        
        % calculate average SSD
        SSD = mean(SST_ProcData_noT1_Stop.trueSSD);

        % calculate SSRT using the means method
        ssrtMean = mean(SST_ProcData_noT1_Go.RT(SST_ProcData_noT1_Go.Correct ~= 1)) - SSD;

        %replace omissions with max RT
        miss_ind = SST_ProcData_noT1_Go.RT == 0;
        SST_ProcData_noT1_Go.RT_withReplace = SST_ProcData_noT1_Go.RT;
        SST_ProcData_noT1_Go.RT_withReplace(miss_ind) = max(SST_ProcData_noT1_Go.RT);
        
        % calculate SSRT using the integration method
        nthRT = prctile(SST_ProcData_noT1_Go.RT_withReplace, (Signal_presp*100));
        ssrtInt = nthRT - SSD;

        %check race model assumptions: RT failed stop not greater than RT go
        racehorse_check = stop_RTmean_us < RTmean_goAll;
        
        %get vector of summary measures
        dat_tab = array2table([racehorse_check, RTmean_goAll, RTsd_goAll, go_cor, RTmean_goCorrect, ...
            go_error, RTmean_goError, go_miss, stop_RTmean_us, Signal_presp, goN, stopN, ...
            SSD, ssrtMean, ssrtInt, ntrials_zero]);
        summary_data(row_count, 3:18) = dat_tab;
        
        %%By ED and PS conditions %%
        conditions = {'hED' 'lED' 'lPort' 'sPort'};
        
        for c = 1:length(conditions)
            cond_ind = contains(SST_ProcData_noT1.BlockCond, conditions{c});
            SST_ProcData_noT1_cond = SST_ProcData_noT1(cond_ind, : );
            
            %identify Signal and NoSignal trials using indicator variables for when 'Signal'
            %matches respectively and create two datasets
            Signal_ind = SST_ProcData_noT1_cond.Signal == 1;
            NoSignal_ind = SST_ProcData_noT1_cond.Signal == 0;

            SST_ProcData_noT1_cond_Stop = SST_ProcData_noT1_cond(Signal_ind, :);
            SST_ProcData_noT1_cond_Go = SST_ProcData_noT1_cond(NoSignal_ind, :);

            %summary measures - all trials
            RTmean_goAll = mean(SST_ProcData_noT1_cond_Go.RT(SST_ProcData_noT1_cond_Go.RT ~= 0)); %go_RTmean_all
            go_cor = sum(SST_ProcData_noT1_cond_Go.Correct == 4); %go correct
            RTmean_goCorrect = mean(SST_ProcData_noT1_cond_Go.RT(SST_ProcData_noT1_cond_Go.Correct == 4 & SST_ProcData_noT1_cond_Go.RT ~= 0)); %go_RTmean_correct
            go_error = sum(SST_ProcData_noT1_cond_Go.Correct == 2); %go_error
            RTmean_goError = mean(SST_ProcData_noT1_cond_Go.RT(SST_ProcData_noT1_cond_Go.Correct == 2 & SST_ProcData_noT1_cond_Go.RT ~= 0)); %go_RTmean_error
            go_miss = sum(SST_ProcData_noT1_cond_Go.Correct == 1); %go_missed
            stop_RTmean_us = mean(SST_ProcData_noT1_cond_Stop.RT(SST_ProcData_noT1_cond_Stop.Correct == 3 & SST_ProcData_noT1_cond_Stop.RT ~= 0)); %stop_RTmean_us

            %get number with zero RT
            ntrials_zero = sum(SST_ProcData_noT1_cond_Go.RT == 0 & SST_ProcData_noT1_cond_Go.Correct == 4);

            %%below is edited from the analyze_it script
            % calculate p(respond|signal)
            Signal_presp = sum(SST_ProcData_noT1_cond_Stop.Correct == 3)/height(SST_ProcData_noT1_cond_Stop);

            %number of trials
            goN = height(SST_ProcData_noT1_cond_Go);
            stopN = height(SST_ProcData_noT1_cond_Stop);

            % calculate average SSD
            SSD = mean(SST_ProcData_noT1_cond_Stop.trueSSD);

            % calculate SSRT using the means method
            ssrtMean = mean(SST_ProcData_noT1_cond_Go.RT(SST_ProcData_noT1_cond_Go.Correct ~= 1)) - SSD;

            %replace omissions with max RT
            miss_ind = SST_ProcData_noT1_cond_Go.RT == 0;
            SST_ProcData_noT1_cond_Go.RT_withReplace = SST_ProcData_noT1_cond_Go.RT;
            SST_ProcData_noT1_cond_Go.RT_withReplace(miss_ind) = max(SST_ProcData_noT1_cond_Go.RT);

            % calculate SSRT using the integration method
            nthRT = prctile(SST_ProcData_noT1_cond_Go.RT_withReplace, (Signal_presp*100));
            ssrtInt = nthRT - SSD;

            %get vector of summary measures
            dat_tab = array2table([RTmean_goAll, go_cor, RTmean_goCorrect, ...
                go_error, RTmean_goError, go_miss, stop_RTmean_us, Signal_presp, goN, stopN, ...
                SSD, ssrtMean, ssrtInt, ntrials_zero]);
            col_start = c*14 + 5;
            col_end = col_start + 13;
            summary_data(row_count, col_start:col_end) = dat_tab;
        end
        
        %% by block - long data %%
        %get rows for block data set--the ending for/row number 4 for the
        %participant will be participant number times 4--i.e., participant 3
        %will end on row 16. The start should be 3 less (16-3 = 13) because 9
        %is counted in the four rows.
        pend = row_count*4;
        pstart = pend - 3;
        
        %loop through runs
        for b=1:length(nblocks)
            
            b_num = b;
            
            %identify trials for a run indicator variables for when 'Block'
            %matches respectively and create dataset with each loop
            Run_ind = SST_ProcData.Block == b_num;
            SST_ProcData_Run = SST_ProcData(Run_ind, :);
            
            if height(SST_ProcData_Run) == 64
                %get condition number
                if strcmp(SST_ProcData_Run.BlockCond(1), 'hED_lPort')
                    c_num = 1;
                elseif strcmp(SST_ProcData_Run.BlockCond(1), 'lED_lPort')
                    c_num = 2;
                elseif strcmp(SST_ProcData_Run.BlockCond(1), 'hED_sPort')
                    c_num = 3;
                elseif strcmp(SST_ProcData_Run.BlockCond(1), 'lED_sPort')
                    c_num = 4;
                end
                
            %remove first trial of block
            SST_ProcData_Run = SST_ProcData_Run(2:end, :);
            
            %identify Signal and NoSignal trials using indicator variables for when 'Signal'
            %matches respectively and create two datasets
            Signal_ind = SST_ProcData_Run.Signal == 1;
            NoSignal_ind = SST_ProcData_Run.Signal == 0;

            SST_ProcData_Run_Stop = SST_ProcData_Run(Signal_ind, :);
            SST_ProcData_Run_Go = SST_ProcData_Run(NoSignal_ind, :);

            %summary measures - all trials
            RTmean_goAll = mean(SST_ProcData_Run_Go.RT(SST_ProcData_Run_Go.RT ~= 0)); %go_RTmean_all
            RTsd_goAll = std(SST_ProcData_Run_Go.RT(SST_ProcData_Run_Go.RT ~= 0)); %go_RTsd_all
            go_cor = sum(SST_ProcData_Run_Go.Correct == 4); %go correct
            RTmean_goCorrect = mean(SST_ProcData_Run_Go.RT(SST_ProcData_Run_Go.Correct == 4 & SST_ProcData_Run_Go.RT ~= 0)); %go_RTmean_correct
            go_error = sum(SST_ProcData_Run_Go.Correct == 2); %go_error
            RTmean_goError = mean(SST_ProcData_Run_Go.RT(SST_ProcData_Run_Go.Correct == 2 & SST_ProcData_Run_Go.RT ~= 0)); %go_RTmean_error
            go_miss = sum(SST_ProcData_Run_Go.Correct == 1); %go_missed
            stop_RTmean_us = mean(SST_ProcData_Run_Stop.RT(SST_ProcData_Run_Stop.Correct == 3 & SST_ProcData_Run_Stop.RT ~= 0)); %stop_RTmean_us

            %get number with zero RT
            ntrials_zero = sum(SST_ProcData_Run_Go.RT == 0 & SST_ProcData_Run_Go.Correct == 4);

            %%below is edited from the analyze_it script
            % calculate p(respond|signal)
            Signal_presp = sum(SST_ProcData_Run_Stop.Correct == 3)/height(SST_ProcData_Run_Stop);

            %number of trials
            goN = height(SST_ProcData_Run_Go);
            stopN = height(SST_ProcData_Run_Stop);

            % calculate average SSD
            SSD = mean(SST_ProcData_Run_Stop.trueSSD);

            % calculate SSRT using the means method
            ssrtMean = mean(SST_ProcData_Run_Go.RT(SST_ProcData_Run_Go.Correct ~= 1)) - SSD;

            %replace omissions with max RT
            miss_ind = SST_ProcData_Run_Go.RT == 0;
            SST_ProcData_Run_Go.RT_withReplace = SST_ProcData_Run_Go.RT;
            SST_ProcData_Run_Go.RT_withReplace(miss_ind) = max(SST_ProcData_Run_Go.RT);

            % calculate SSRT using the integration method
            nthRT = prctile(SST_ProcData_Run_Go.RT_withReplace, (Signal_presp*100));
            ssrtInt = nthRT - SSD;

            %check race model assumptions: RT failed stop not greater than RT go
            racehorse_check = stop_RTmean_us < RTmean_goAll;

            %get vector of summary measures
            dat_tab = array2table([racehorse_check, RTmean_goAll, RTsd_goAll, go_cor, RTmean_goCorrect, ...
                go_error, RTmean_goError, go_miss, stop_RTmean_us, Signal_presp, goN, stopN, ...
                SSD, ssrtMean, ssrtInt, ntrials_zero]);

            summary_data_long(pstart+b_num-1, 3) = SST_ProcData_Run.BlockCond(1);
            summary_data_long(pstart+b_num-1, 4) = num2cell(b_num);
            summary_data_long(pstart+b_num-1, 5:end) = dat_tab;
            
            %add participant and session number
            summary_data_long.ParID(pstart+b_num-1) = parID_num;
            summary_data_long.Session(pstart+b_num-1) = session_num;
            
            else
                ntrials = height(SST_ProcData_Run);
                errors =[errors; cellstr(sprintf('Participant %s had only %d trials on block %d', parID_str, ntrials, b))];
            end    
        end  
        
        
    end     
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%              Write out summary data                 %%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%remove extra rows for duplicates
if n_duplicate > 0
    %get number of particpants processed/not duplicates
    npar_proc = npar - n_duplicate;

    %remove extra rows
    summary_data((npar_proc+1):end, :) = [];
    summary_data_long((npar_proc*4 + 1):end, :) = [];
end

%combine data and export
if height(summary_data) > 0
    SST_dat = [SST_dat; summary_data];
    
    SST_dat_long = [SST_dat_long; summary_data_long];

    cd([base_wd 'SST_Databases']);
    
    %cleanup old files--move all files to 'Old_database_backup'
    for m = 1:height(database_file_tab)
        movefile(char(database_file_tab.name(m)), 'Old_database_backup/');
    end
    
    writetable(SST_dat, sprintf('SST_database_%s.csv', today), 'WriteRowNames',true);
    writetable(SST_dat_long, sprintf('SST_database_BlockLong_%s.csv', today), 'WriteRowNames',true);
end

%export errors
if ~isempty(errors)
    cd([base_wd 'SST_Processed_Data_Files']);
    writetable(cell2table(errors), sprintf('SST_ErrorsProcessed_%s_%s_%s.txt', parID_str, session_str, today), 'WriteRowNames',true);
end

end
