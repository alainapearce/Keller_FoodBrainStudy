
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%            GNG data processing script               %%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%This script was written by Alaina Pearce in March 2018 for the purpose of
%processing the GNG zoo neutral task used in the RO1 grant. 
function GNG_Zoo_neutal_RO1(parID, session)
%parID-participant id; can be a single ID or a vector of id's 
%(e.g., [1, 3, 5])
%session-time point, added in case particpants are brought back as part of
%a pilot longitudinal grant

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%                         Setup                       %%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%!need to edit this section (and all paths) if move script or any directories it calls!

%check if participant ID is 3--only use for participant 3!
if parID ~= 3
    disp('This script can only be used to process participant number 3s data from session 1');
    return
elseif session ~= 1
    disp('This script can only be used to process participant number 3s data from session 1');
    return
end
%get working directory path for where this script is saved
%(individual path info '/Box Sync/b-childfoodlab Shared/RO1_Brain_Mechanisms_IRB_5357/Participant Data/GNG/Scripts')
script_wd = mfilename('fullpath');

%get location/character number for '/" in file path
slashloc_wd=find(script_wd=='/');

%use all characters in path name upto the 7th slash (individual path info
%'/Box Sync/b-childfoodlab Shared/RO1_Brain_Mechanisms_IRB_5357/Participant Data/GNG)
base_wd = script_wd(1:slashloc_wd(end-1));
addpath(genpath(base_wd));

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%         Load Databases and Clean up old ones        %%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cd([base_wd 'GNG_Databases']);

%create str to identify files using wildcard '*'
database_file_str = 'GNG_*.csv';

%use str to identify files--save as table
database_file = dir(char(database_file_str));
database_file_tab = struct2table(database_file);

%create str to identify only 'BlockLong' files using wildcard '*' and
%identify those that match--save as table
long_datfile_str = struct2table(dir(char('GNG_database_Block*.csv')));

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

GNG_dat = readtable(char(database_file_reg_tab.name(1)), 'ReadVariableNames', true);
GNG_dat_VN = GNG_dat.Properties.VariableNames;

GNG_dat_long = readtable(char(database_file_long_tab.name(1)), 'ReadVariableNames', true);
GNG_dat_long_VN = GNG_dat_long.Properties.VariableNames;

%make sure first collumn variable name is 'ParID' for both databases-- 
%sometimes reads first collumn header in weird (e.g., 'x__ParID');
if ~strcmp(GNG_dat_VN(1), 'ParID')
    GNG_dat_VN(1) = {'ParID'};
    GNG_dat.Properties.VariableNames = GNG_dat_VN;
end

if ~strcmp(GNG_dat_long_VN(1), 'ParID')
    GNG_dat_long_VN(1) = {'ParID'};
    GNG_dat_long.Properties.VariableNames = GNG_dat_long_VN;
end

%%
%Load DDM database
%%
%create str to identify files using wildcard '*' Diffusion Drift Model
DDM_database_file_str = 'GNG_DDM*.txt';

%use str to identify files--save as table
DDM_database_file = dir(char(DDM_database_file_str));
DDM_database_file_tab = struct2table(DDM_database_file);

%sort indetified flies by date created -- load only the most recent
DDM_database_file_tab = sortrows(DDM_database_file_tab, 3, 'descend');

if height(DDM_database_file_tab) > 1
    GNG_DDM_dat = readtable(char(DDM_database_file_tab.name(1)), 'ReadVariableNames', true);
else
    GNG_DDM_dat = readtable(char(DDM_database_file_tab.name), 'ReadVariableNames', true);
end

GNG_DDM_VN = GNG_DDM_dat.Properties.VariableNames;

%make sure first collumn variable name is 'ParID' for both databases-- 
%sometimes reads first collumn header in weird (e.g., 'x__ParID');
if ~strcmp(GNG_DDM_VN(1), 'ParID')
    GNG_DDM_VN = {'ParID', 'nGo_Hit', 'RTq10Go', 'RTq30Go', 'RTq50Go', 'RTq70Go', 'RTq90Go', 'nNoGo_FA', 'RTq50NoGo'};
    GNG_DDM_dat.Properties.VariableNames = GNG_DDM_VN;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%              Participant ID loop Setup              %%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%get number of participants
npar = length(parID);

%create empty tables to store summary data in wide and long format (by
%block) and add variable names from loaded databases. Create one row per
%participant for wide and 5 per participant for long format
summary_data = array2table(zeros(npar, 112));
summary_data.Properties.VariableNames = GNG_dat_VN;
summary_data_long = array2table(zeros((npar*5), 19));
summary_data_long.Properties.VariableNames = GNG_dat_long_VN;

%create DDM empty table
DDM_summary_data = array2table(zeros(npar, 9));
DDM_summary_data.Properties.VariableNames = GNG_DDM_VN;

%track number of duplicates so can remove extra rows at end
n_duplicate = 0;

%start loop based on number of inputs in parID variable
for p = 1:npar
    %convert participant ID to string with 3 digit before the decimal point
    %(specified by '%03.f'). This ensures 1 is converted to '001' to match
    %naming convention of .txt files
    parID_num = parID(p);
    parID_str = num2str(parID_num, '%03.f');
    
    %convert session to string
    session_str = num2str(session);
    
    %check to see if participant exists in database
    par_ind = GNG_dat.ParID == parID_num;
    session_ind = GNG_dat.Session == session;
    par_session_ind = par_ind & session_ind;
    if sum(par_ind & session_ind) > 0
        disp(sprintf('Participant %s exists in database for session %s. Please delete data from database if want to overwrite', parID_str, session_str));
        n_duplicate = n_duplicate + 1;
    else
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%        Process Particpant Raw Task Data             %%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %Go to raw data and load .txt file that was exported
        cd([base_wd 'GNG_Raw_Data_Files']);

        %get name for data file using wildcard ('*'): want file that ends with
        %'###-#.txt' (e.g., '001-1.txt')
        IDfile = strcat('*Raw_', parID_str, '-', session_str, ".txt");

        %get name of onset file. 
        %NOTE: since we used a wildcard ('*') to fill in parts of file names that
        %differ between participants, we need to do 2 things to get file name in
        %script:
        %1) cd to directory where file is (we did this above on line 40)
        %2) use {dir(char(...)} syntasx--this makes the IDfile a character type of
        %data and then the 'dir' says it will be looking for a directory. Without
        %the use of 'dir' it won't incorporate '*' as a wildcard and will search
        %for exact string (e.g., '101A*.csv')
        GNG_Zoo_datfile = {dir(char(IDfile))};

        %load onsets file as a table--Delimiter is to indicate how values are
        %separated in file (e.g., comma for csv, tab ('/t') for some .txt). We want
        %this to also read in the first row as a header so set 'ReadVariableNames'
        %to true
        GNG_Zoo_RawData = readtable(GNG_Zoo_datfile{1}.name, 'ReadVariableNames',true);

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%           Get cleaned dataset                       %%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        %select only variables interested in using for processed data
        GNG_vars = {'Subject', 'Session', 'Procedure_Block_', 'Trial', 'CA', 'compatibility', 'imagecode', 'Stim_RESP','Stim_RT', 'Respond_RESP', 'Respond_RT', 'Target'};
        GNG_Zoo_ProcData = GNG_Zoo_RawData(:, GNG_vars); 

        %check responses that were made in the "response" or ISI time (i.e.,
        %'Respons_RESP'
        ISI_resp_ind = strcmp(GNG_Zoo_ProcData.Respond_RESP, '{SPACE}');

        %Find rows were response was in ISI and move the 'Respond_RESP' to the
        %'Stim_RESP' column so all response are in same column. Also,
        %move the RT information to 'Stim_RT' after adding 750ms--The Stim was
        %available for 750 so the RT in 'Respond_RESP' is in addition to that
        %750ms. 
        rows_ISI_resp = find(ISI_resp_ind==1);
        for r=1:length(rows_ISI_resp)
            row = rows_ISI_resp(r);
            GNG_Zoo_ProcData.Stim_RESP(row) = GNG_Zoo_ProcData.Respond_RESP(row);
            GNG_Zoo_ProcData.Stim_RT(row) = GNG_Zoo_ProcData.Respond_RT(row) + 750;
        end

        %Delete old 'Respond_RESP' and 'Respond_RT' collumns. 
        GNG_Zoo_ProcData.Respond_RESP = [];
        GNG_Zoo_ProcData.Respond_RT = [];

        %rename the 'Stim_**' and other collumns.
        GNG_Zoo_ProcData.Properties.VariableNames = {'ParID', 'Session', 'Block', 'Trial', 'Correct', 'StimType', 'imagecode', 'RESP','RT','Target'};

        %go to directory where processed data are saved (individual path info '/Box
        %Sync/b-childfoodlab Shared/RO1_Brain_Mechanisms_IRB_5357/Participant
        %Data/GNG/GNG_Processed_Data_Files/)
        cd([base_wd 'GNG_Processed_Data_Files']);

        %export datatable and use sprintf to name file with participant name and
        %session
        today = date;
        writetable(GNG_Zoo_ProcData, [sprintf('GNG_Zoo_Processed_%s_%s_%s.txt', today, parID_str, session_str)], 'WriteRowNames',true)
        %%

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%           Extract Summary Data                      %%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        %find the task trials (non-practice) and create a logical indicator for
        %those NOT practice--some have practice as part of task scripts, others may
        %have had a separate practice.
        Task_ind = ~strcmp(GNG_Zoo_ProcData.Block, 'PracticeProc');

        %use indicator to select only task trials
        GNG_Zoo_TaskData = GNG_Zoo_ProcData(Task_ind, :);
        
        %par3 edits--no response first set of block 1
        GNG_Zoo_TaskData(1:12, :) = [];
        
        %Get Accuracy data by creating an adding the indictor to a new variable
        %called "Acc_Resp"--indicates a 1 when the columns 'Correct' and 'RESP'
        %match
        GNG_Zoo_TaskData.Acc_Resp = strcmp(GNG_Zoo_TaskData.Correct, GNG_Zoo_TaskData.RESP);

        %get rows for block data set--the ending for/row number 5 for the
        %participant will be participant number times 5--i.e., participant 3
        %will end on row 15. The start should be 4 less (15-4 = 11) because 15
        %is counted in the five rows.
        pend = p*5;
        pstart = pend - 4;

        %add participant and session number
        summary_data.ParID(p) = parID_num;
        summary_data.Session(p) = session;

        summary_data_long.ParID(pstart:pend) = parID_num;
        summary_data_long.Session(pstart:pend) = session;

        %add vector index for starting data value and the number of caluclated
        %values each loop
        dat_start = 3;
        length_dat = 16;

        %loop through blocks to get summary outcomes--first loop is for all data
        %and then loops 1-5 are block. Add summary measures to vector each loop so
        %horizontally concatonate outcome measures

        for b = 0:length(unique(GNG_Zoo_TaskData.Block))
            if b == 0
                block_data = GNG_Zoo_TaskData;
            elseif b > 0
                block_str = strcat('Block', num2str(b));
                block_ind = strcmp(GNG_Zoo_TaskData.Block, block_str);
                block_data = GNG_Zoo_TaskData(block_ind, :);
            end

            %identify Go and NoGo trials using indicator variables for when 'StimType'
            %matches respectively and create two datasets
            Go_ind = strcmp(block_data.StimType, 'Go');
            NoGo_ind = strcmp(block_data.StimType, 'NoGo');

            block_data_Go = block_data(Go_ind, :);
            block_data_NoGo = block_data(NoGo_ind, :);

            %trial counts
            nGo = height(block_data_Go);
            nNoGo = height(block_data_NoGo);

            %Accuracy
            nAcc = sum(block_data.Acc_Resp);
            pAcc = sum(block_data.Acc_Resp)/height(block_data);

            %Go Hits/Misses 
            nGo_Hit = sum(block_data_Go.Acc_Resp);
            pGo_Hit = sum(block_data_Go.Acc_Resp)/height(block_data_Go);

            nGo_Miss = sum(block_data_Go.Acc_Resp == 0);
            pGo_Miss = sum(block_data_Go.Acc_Resp == 0)/height(block_data_Go);

            %NoGo Commissions (False Alarms) and Correct no responses
            nNoGo_Corr = sum(block_data_NoGo.Acc_Resp);
            pNoGo_Corr = sum(block_data_NoGo.Acc_Resp)/height(block_data_NoGo);

            nNoGo_FA = sum(block_data_NoGo.Acc_Resp == 0);
            pNoGo_FA = sum(block_data_NoGo.Acc_Resp == 0)/height(block_data_NoGo);

            %mean and median RT
            RTmeanGo_Hit = mean(block_data_Go.RT(block_data_Go.Acc_Resp==1));
            RTmedGo_Hit = median(block_data_Go.RT(block_data_Go.Acc_Resp==1));

            RTmeanNoGo_FA = mean(block_data_NoGo.RT(block_data_NoGo.Acc_Resp==0));
            RTmedNoGo_FA = median(block_data_NoGo.RT(block_data_NoGo.Acc_Resp==0));

            %get vector of summary measures
            dat_tab = array2table([nGo, nNoGo, nAcc, pAcc, nGo_Hit, nGo_Miss, nNoGo_Corr, nNoGo_FA, pGo_Hit, pGo_Miss, pNoGo_Corr, pNoGo_FA, RTmeanGo_Hit, RTmeanNoGo_FA, RTmedGo_Hit, RTmedNoGo_FA]);
            dat_end = dat_start + length_dat -1; 
            summary_data(p, dat_start:dat_end) = dat_tab;

            %add block data to the long dataset when working on blocks--skip loop
            %0 because it uses all data
            if b>0
                %get rownubmer for block--pstart is the row it should start on
                %so add block number and subtract one from it because block
                %starts with b = 1, not b = 0 and pstart is where it should
                %(i.e., if pstart = 1 and we add b=1, it wont start on the
                %correct row)
                brow = pstart + b - 1;
                summary_data_long.Block(brow) = b;
                summary_data_long(brow, 4:19) = dat_tab;
            end

            %reset dat_start to the next vector index to be used in next loop
            dat_start = dat_end + 1;


            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%                DDM summary data                     %%%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

            %if b == 0 then it means full data was used and subsetted. Extract
            %DDM summary data based on full data
            if b == 0

                DDM_summary_data.ParID(p) = parID_num;
                DDM_summary_data.nGo_Hit(p) = nGo_Hit;
                DDM_summary_data.nNoGo_FA(p) = nNoGo_FA;

                %get quantiles for Go Hit RT
                DDM_summary_data(p, 3:7) = num2cell(quantile(block_data_Go.RT, [.1, .3, .5, .7, .9]));

                %get RTs for False Alarms--first check that there are FAs, if
                %not use NaN
                if nNoGo_FA > 0
                    NoGo_FA_ind = block_data_NoGo.Acc_Resp == 0;
                    block_data_NoGo_FA = block_data_NoGo(NoGo_FA_ind, :);
                    DDM_summary_data.RTq50NoGo(p) = quantile(block_data_NoGo_FA.RT, .5);
                else
                    DDM_summary_data.RTq50NoGo(p) = NaN;
                end
            end    
        end   

        %%

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%               Extract SDT Data                      %%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        %get z-score for hit and false alarm rates
        summary_data.z_Hit(p) = norminv(summary_data.pGo_Hit(p));
        summary_data.z_FA(p) = norminv(summary_data.pNoGo_FA(p));

        %do Macmillian adjustments for extreme values: if hit rate = 1, new hit
        %rate = (nGo - 0.5)/nGo; if false alarm rate = 0, new false alarm rate
        %= 0.5/nNoGo. If no extreme value, then just save standard calculation
        %for z in that palce
        if summary_data.pGo_Hit(p) == 1
            pHit_mm = (summary_data.nGo(p)-0.5)/summary_data.nGo(p);
            summary_data.z_Hit_mm(p) = norminv(pHit_mm);
        else
            pHit_mm = summary_data.pGo_Hit(p);
            summary_data.z_Hit_mm(p) = norminv(pHit_mm);
        end

        if summary_data.pNoGo_FA(p) == 0
            pFA_mm = 0.5/summary_data.nNoGo(p);
            summary_data.z_FA_mm(p) = norminv(pFA_mm);
        else
            pFA_mm = summary_data.pNoGo_FA(p);
            summary_data.z_FA_mm(p) = norminv(pFA_mm);
        end

        %do loglinear adjustments: add 0.5 to NUMBER of hits and FA and add 1
        %to number of Go and NoGo trials. Then caluculate z off of new hit and
        %FA rates
        nHit_ll = summary_data.nGo_Hit(p)+0.5;
        nGo_ll = summary_data.nGo(p) + 1;
        nFA_ll = summary_data.nNoGo_FA(p)+0.5;
        nNoGo_ll = summary_data.nNoGo(p) + 1;
        pHit_ll = nHit_ll/nGo_ll;
        pFA_ll = nFA_ll/nNoGo_ll;
        summary_data.z_Hit_ll(p) = norminv(pHit_ll);
        summary_data.z_FA_ll(p) = norminv(pFA_ll);

        %calculate sensory sensitivity d'
        summary_data.d_prime_mm(p) = summary_data.z_Hit_mm(p) - summary_data.z_FA_mm(p);
        summary_data.d_prime_ll(p) = summary_data.z_Hit_ll(p) - summary_data.z_FA_ll(p);

        %calculate nonparametric sensory sensitivity A':
        %0.5+[sign(H-FA)*((H-FA)^2 + |H-FA|)/(4*max(H, FA) - 4*H*FA))
        summary_data.A_prime_mm(p) = .5 + (sign(pHit_mm-pFA_mm)*(((pHit_mm-pFA_mm)^2+abs(pHit_mm - pFA_mm))/(4*max(pHit_mm, pFA_mm) - 4*pHit_mm*pFA_mm)));
        summary_data.A_prime_ll(p) = .5 + (sign(pHit_ll-pFA_ll)*(((pHit_ll-pFA_ll)^2+abs(pHit_ll - pFA_ll))/(4*max(pHit_ll, pFA_ll) - 4*pHit_ll*pFA_ll)));

        %calculate c (criterion
        summary_data.c_mm(p) = (norminv(pHit_mm) + norminv(pFA_mm))/2;
        summary_data.c_ll(p) = (norminv(pHit_ll) + norminv(pFA_ll))/2;

        %calculate Grier's Beta--beta", a nonparametric response bias
        summary_data.Grier_beta_mm(p) = sign(pHit_mm-pFA_mm)*((pHit_mm*(1-pHit_mm)-pFA_mm*(1-pFA_mm))/(pHit_mm*(1-pHit_mm)+pFA_mm*(1-pFA_mm)));
        summary_data.Grier_beta_ll(p) = sign(pHit_ll-pFA_ll)*((pHit_ll*(1-pHit_ll)-pFA_ll*(1-pFA_ll))/(pHit_ll*(1-pHit_ll)+pFA_ll*(1-pFA_ll)));

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
    summary_data_long((npar_proc*5 + 1):end, :) = [];
    DDM_summary_data((npar_proc+1):end, :) = [];   
end

%combine data and export
if height(summary_data) > 0
    GNG_dat = [GNG_dat; summary_data];
    GNG_dat_long = [GNG_dat_long; summary_data_long];
    GNG_DDM_dat = [GNG_DDM_dat; DDM_summary_data];

    cd([base_wd 'GNG_Databases']);
    
    %cleanup old files--move all files to 'Old_database_backup'
    for m = 1:height(database_file_tab)
        movefile(char(database_file_tab.name(m)), 'Old_database_backup/');
    end
    
    if height(DDM_database_file_tab) > 1
        for m = 1:height(DDM_database_file_tab)
            movefile(char(DDM_database_file_tab.name(m)), 'Old_database_backup/');
        end
    else
        movefile(char(DDM_database_file_tab.name), 'Old_database_backup/');
    end
    
    writetable(GNG_dat, sprintf('GNG_database_%s.csv', today), 'WriteRowNames',true);
    writetable(GNG_dat_long, sprintf('GNG_database_BlocksLong_%s.csv', today), 'WriteRowNames',true);
    writetable(GNG_DDM_dat, sprintf('GNG_DDM_database_%s.txt', today), 'WriteRowNames',true); 
end

end
