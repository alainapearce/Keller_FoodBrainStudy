%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%        Space Game data processing script            %%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%This script was written by Alaina Pearce in December 2019 for 
%the purpose of processing the Nback task used in the RO1 grant
%as part of Pearce's F32 grant. 
function SpaceGame_R01(parID, session)
    %parID-participant id; can be a single ID or a vector of id's 
    %(e.g., [1, 3, 5])
    %session-time point, added in case particpants are brought back as part of
    %a pilot longitudinal grant

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%                         Setup                       %%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %!need to edit this section (and all paths) if move script or any directories it calls!

    %get working directory path for where this script is saved
    %(individual path info '/Box Sync/b-childfoodlab Shared/RO1_Brain_Mechanisms_IRB_5357/Participant Data/SpaceGame/Scripts')
    script_wd = mfilename('fullpath');

    if ismac()
        slash = '/';
    else 
        slash = '\';
    end

    %get location/character number for '/" in file path
    slashloc_wd=find(script_wd==slash);

    %use all characters in path name upto the 7th slash (individual path info
    %'/Box Sync/b-childfoodlab Shared/RO1_Brain_Mechanisms_IRB_5357/Participant Data/SpaceGame)
    base_wd = script_wd(1:slashloc_wd(end-1));

    %this will tell matlab to look at all files withing the base_wd--so any
    %subfolder will be added to search path
    addpath(genpath(base_wd));

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%         Load Databases and Clean up old ones        %%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    cd([base_wd 'SpaceGame_Databases']);

    %create str to identify files using wildcard '*'
    database_file_str = 'SpaceGame_database*.csv';

    %use str to identify files--save as table
    database_file = dir(char(database_file_str));
    database_file_tab = struct2table(database_file);

    %create str to identify only 'BlockLong' files using wildcard '*' and
    %identify those that match--save as table
    long_datfile_str = struct2table(dir(char('SpaceGame_database_BlocksLong*.csv')));

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

    SpaceGame_dat = readtable(char(database_file_reg_tab.name(1)), 'ReadVariableNames', true);
    SpaceGame_dat_VN = SpaceGame_dat.Properties.VariableNames;

    SpaceGame_dat_long = readtable(char(database_file_long_tab.name(1)), 'ReadVariableNames', true);
    SpaceGame_dat_long_VN = SpaceGame_dat_long.Properties.VariableNames;

    %make sure first collumn variable name is 'ParID' for both databases-- 
    %sometimes reads first collumn header in weird (e.g., 'x__ParID');
    if ~strcmp(SpaceGame_dat_VN(1), 'ParID')
        SpaceGame_dat_VN(1) = {'ParID'};
        SpaceGame_dat.Properties.VariableNames = SpaceGame_dat_VN;
    end

    if ~strcmp(SpaceGame_dat_long_VN(1), 'ParID')
        SpaceGame_dat_long_VN(1) = {'ParID'};
        SpaceGame_dat_long.Properties.VariableNames = SpaceGame_dat_long_VN;
    end

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%              Group Data Load              %%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    if exist('groupdata.mat')
        groupdata = load('groupdata.mat');
    else
        groupdata = struct;
    end

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%              Participant ID loop Setup              %%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %get number of participants
    npar = length(parID);

    %start loop based on number of inputs in parID variable
    for p_all = 1:npar

        %convert participant ID to string with 3 digit before the decimal point
        %(specified by '%03.f'). This ensures 1 is converted to '001' to match
        %naming convention of .txt files
        %convert session to string
        parID_num = parID(p_all);

        if length(session) > 1
            session_num = session(p_all);
        else
            session_num = session;
        end
        
        session_str = num2str(session_num);
        parID_str = num2str(parID_num);

        %check to see if participant exists in database
        par_ind = SpaceGame_dat.ParID == parID_num;
        session_ind = SpaceGame_dat.Session == session_num;
        par_session_ind = par_ind & session_ind;
        if par_session_ind > 0
            disp(sprintf('Participant %s exists in database for session %s. Please delete data from database if want to overwrite', parID_str, session_str));
            
            if p_all == 1
                par_include = 0;
            else
                par_include = [par_include, 0];
            end
        else
            if p_all == 1
                par_include = 1;
            else
                par_include = [par_include, 1];
            end
        end
    end
    
    parID_include = parID(logical(par_include));
    npar_include = length(parID_include);    
    
    for p = 1:npar_include
        
        %convert participant ID to string with 3 digit before the decimal point
        %(specified by '%03.f'). This ensures 1 is converted to '001' to match
        %naming convention of .txt files
        %convert session to string
        parID_num = parID_include(p);

        if length(session) > 1
            session_include = session(par_include);
            session_num = session_include(p);
        else
            session_num = session;
        end
        
        session_str = num2str(session_num);
        parID_str = num2str(parID_num);

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%        Process Particpant Raw Task Data             %%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %Go to raw data and load .txt file that was exported
        cd([base_wd 'SpaceGame_Raw_Data_Files']);

        %get name for data file using wildcard ('*'): want file that ends with
        %'###-#.txt' (e.g., '1-1.txt')
        IDfile = strcat('mbmfNovelStakes_', parID_str, '-', session_str, ".mat");

        %load file
        SpaceGame_datfile = load(IDfile);
        SpaceGame_par_dat = SpaceGame_datfile.data;

        %keys used
        keys_earth = {SpaceGame_par_dat.pms.leftKey SpaceGame_par_dat.pms.rightKey 'Timeout'};

        SpaceGame_dat_VN = {'ParID' 'Session' 'Block' 'Trial' ...
        'Practice' 'Timeout_Earth' 'Timeout_planet' ...
        'State_Earth' 'Stim_left' 'Stim_right' 'RT_Earth'...
        'Choice_Earth' 'Response_Earth' 'RT_planet'...
        'Points' 'State_planet' 'Stake' 'Win' 'Score'  ...
        'Rewards1' 'Rewards2' 'Missed' 'PrevMissed' ...
        'PrevChoice_Earth' 'PrevState_Earth' 'PrevState_planet' ...
        'PrevPoints' 'Earth_Same' 'Planet_Stay' ...
        'PrevUnChosen_Earth' 'PrevRewards1' 'PrevRewards2' ... 
        'RewardDiff_ChosenUnchosen' 'Ntrials'};

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%        Practice             %%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        SpaceGame_procdat_prac = array2table(zeros(SpaceGame_par_dat.pms.nrPracticeTrials, 34));
        SpaceGame_procdat_prac.Properties.VariableNames = SpaceGame_dat_VN;

        %participant info
        SpaceGame_procdat_prac.ParID(:) = parID_num;
        SpaceGame_procdat_prac.Session(:) = session_num;

        %keys practice
        keys_earth_prac = repmat([1,2], SpaceGame_par_dat.pms.nrPracticeTrials, 1);

        %fill block with NA
        SpaceGame_procdat_prac.Block(:) = NaN;

        %get practice trial numbers
        SpaceGame_procdat_prac.Trial = (1:1:SpaceGame_par_dat.pms.nrPracticeTrials)';

        %practice
        SpaceGame_procdat_prac.Practice = string(SpaceGame_procdat_prac.Practice);
        SpaceGame_procdat_prac.Practice(:) = 'Y';

        %did trial time out
        SpaceGame_procdat_prac.Timeout_Earth = string(SpaceGame_procdat_prac.Timeout_Earth);
        SpaceGame_procdat_prac.Timeout_Earth(:) = 'NA';

        SpaceGame_procdat_prac.Timeout_planet = string(SpaceGame_procdat_prac.Timeout_planet);
        SpaceGame_procdat_prac.Timeout_planet(:) = 'NA';

        %fill in rest of data
        SpaceGame_procdat_prac.State_Earth = SpaceGame_par_dat.practice.s(:,1);
        SpaceGame_procdat_prac.Stim_left = SpaceGame_par_dat.practice.stimuli(:, 1);
        SpaceGame_procdat_prac.Stim_right = SpaceGame_par_dat.practice.stimuli(:, 2);
        SpaceGame_procdat_prac.RT_Earth = SpaceGame_par_dat.practice.rt(:, 1);
        SpaceGame_procdat_prac.Choice_Earth = SpaceGame_par_dat.practice.choice(:);

        %key response
        ind_key_prac = SpaceGame_procdat_prac.Choice_Earth == SpaceGame_par_dat.practice.stimuli;
        SpaceGame_procdat_prac.Response_Earth = {keys_earth{keys_earth_prac(:,1).*ind_key_prac(:,1) + keys_earth_prac(:,2).*ind_key_prac(:,2)}}';

        %planet information
        SpaceGame_procdat_prac.RT_planet = SpaceGame_par_dat.practice.rt(:, 2);
        SpaceGame_procdat_prac.Points = SpaceGame_par_dat.practice.points(:);
        SpaceGame_procdat_prac.State_planet = SpaceGame_par_dat.practice.s(:, 2);

        SpaceGame_procdat_prac.Stake = string(SpaceGame_procdat_prac.Stake);
        SpaceGame_procdat_prac.Stake(:) = 'NA';

        SpaceGame_procdat_prac.Win = SpaceGame_par_dat.practice.points(:) > 0;

        SpaceGame_procdat_prac.Score = string(SpaceGame_procdat_prac.Score);
        SpaceGame_procdat_prac.Score(:) = 'NA';

        SpaceGame_procdat_prac.Rewards1 = SpaceGame_par_dat.practice.rews(:, 1);
        SpaceGame_procdat_prac.Rewards2 = SpaceGame_par_dat.practice.rews(:, 2);
        SpaceGame_procdat_prac.Missed(:) = SpaceGame_par_dat.practice.rt(:, 1) == -1 | SpaceGame_par_dat.practice.rt(:, 2) == -1;

        %overall and previous trial
        SpaceGame_procdat_prac.PrevMissed(:) = [1; SpaceGame_procdat_prac.Missed(1:end-1)];
        SpaceGame_procdat_prac.PrevChoice_Earth = [0; SpaceGame_par_dat.practice.choice(1:end-1)];
        SpaceGame_procdat_prac.PrevState_Earth = [0; SpaceGame_par_dat.practice.s(1:end-1, 1)];
        SpaceGame_procdat_prac.PrevState_planet = [0; SpaceGame_par_dat.practice.s(1:end-1, 2)];
        SpaceGame_procdat_prac.PrevPoints = [0; SpaceGame_par_dat.practice.points(1:end-1)];
        SpaceGame_procdat_prac.Earth_Same = SpaceGame_procdat_prac.State_Earth == SpaceGame_procdat_prac.PrevState_Earth;
        SpaceGame_procdat_prac.Planet_Stay = SpaceGame_procdat_prac.State_planet == SpaceGame_procdat_prac.PrevState_planet;

        ind_unchosen_prac = SpaceGame_procdat_prac.Choice_Earth ~= SpaceGame_par_dat.practice.stimuli;
        SpaceGame_procdat_prac.PrevUnChosen_Earth = [0; SpaceGame_par_dat.practice.stimuli(1:end-1, 1).*ind_unchosen_prac(1:end-1, 1) + SpaceGame_par_dat.practice.stimuli(1:end-1, 2).*ind_unchosen_prac(1:end-1, 2)];
        SpaceGame_procdat_prac.PrevRewards1 = [0; SpaceGame_par_dat.practice.rews(1:end-1, 1)];
        SpaceGame_procdat_prac.PrevRewards2 = [0; SpaceGame_par_dat.practice.rews(1:end-1, 2)];

        SpaceGame_procdat_prac.RewardDiff_ChosenUnchosen = (SpaceGame_par_dat.practice.rews(:, 1).*~ind_unchosen_prac(:, 1) + SpaceGame_par_dat.practice.rews(:, 2).*~ind_unchosen_prac(:, 2)) ...
                                                       - (SpaceGame_par_dat.practice.rews(:, 1).*ind_unchosen_prac(:, 1) + SpaceGame_par_dat.practice.rews(:, 2).*ind_unchosen_prac(:, 2));

        SpaceGame_procdat_prac.Ntrials(:) = SpaceGame_par_dat.pms.nrPracticeTrials; 

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%        Task             %%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        SpaceGame_procdat_trials = array2table(zeros(SpaceGame_par_dat.pms.nrTrials, 34));
        SpaceGame_procdat_trials.Properties.VariableNames = SpaceGame_dat_VN;

        %participant info
        SpaceGame_procdat_trials.ParID(:) = parID_num;
        SpaceGame_procdat_trials.Session(:) = session_num;

        %keys pract
        keys_earth_trials = repmat([1,2], SpaceGame_par_dat.pms.nrTrials, 1);

        %fill block with NA
        Blocknumbers = repmat(1:1:SpaceGame_par_dat.pms.nrBlocks, SpaceGame_par_dat.pms.nrTrialsPerBlock, 1);

        SpaceGame_procdat_trials.Block = Blocknumbers(:);

        %get practice trial numbers
        SpaceGame_procdat_trials.Trial = (1:1:SpaceGame_par_dat.pms.nrTrials)';

        %practice
        SpaceGame_procdat_trials.Practice = string(SpaceGame_procdat_trials.Practice);
        SpaceGame_procdat_trials.Practice(:) = 'N';

        %did trial time out
        SpaceGame_procdat_trials.Timeout_Earth = SpaceGame_par_dat.timeout(:, 1);
        SpaceGame_procdat_trials.Timeout_planet = SpaceGame_par_dat.timeout(:, 2);

        %fill in rest of data
        SpaceGame_procdat_trials.State_Earth = SpaceGame_par_dat.s(:,1);
        SpaceGame_procdat_trials.Stim_left = SpaceGame_par_dat.stimuli(:, 1);
        SpaceGame_procdat_trials.Stim_right = SpaceGame_par_dat.stimuli(:, 2);
        SpaceGame_procdat_trials.RT_Earth = SpaceGame_par_dat.rt(:, 1);
        SpaceGame_procdat_trials.Choice_Earth = SpaceGame_par_dat.choice(:);

        %key response
        ind_key_trials = SpaceGame_procdat_trials.Choice_Earth == SpaceGame_par_dat.stimuli;

        key_side = keys_earth_trials(:,1).*ind_key_trials(:,1) + keys_earth_trials(:,2).*ind_key_trials(:,2);
        key_side(key_side == 0) = 3;

        SpaceGame_procdat_trials.Response_Earth = {keys_earth{key_side}}';

        %planet information
        SpaceGame_procdat_trials.RT_planet = SpaceGame_par_dat.rt(:, 2);
        SpaceGame_procdat_trials.Points = SpaceGame_par_dat.points(:);
        SpaceGame_procdat_trials.State_planet = SpaceGame_par_dat.s(:, 2);

        SpaceGame_procdat_trials.Stake = string(SpaceGame_procdat_trials.Stake);
        SpaceGame_procdat_trials.Stake(:) = 'NA';

        SpaceGame_procdat_trials.Win = SpaceGame_par_dat.points(:) > 0;

        SpaceGame_procdat_trials.Score(:) = SpaceGame_par_dat.score;

        SpaceGame_procdat_trials.Rewards1 = SpaceGame_par_dat.rews(:, 1);
        SpaceGame_procdat_trials.Rewards2 = SpaceGame_par_dat.rews(:, 2);
        SpaceGame_procdat_trials.Missed(:) = SpaceGame_par_dat.rt(:, 1) == -1 | SpaceGame_par_dat.rt(:, 2) == -1;

        %overall and previous trial
        SpaceGame_procdat_trials.PrevMissed(:) = [1; SpaceGame_procdat_trials.Missed(1:end-1)];
        SpaceGame_procdat_trials.PrevChoice_Earth = [0; SpaceGame_par_dat.choice(1:end-1)];
        SpaceGame_procdat_trials.PrevState_Earth = [0; SpaceGame_par_dat.s(1:end-1, 1)];
        SpaceGame_procdat_trials.PrevState_planet = [0; SpaceGame_par_dat.s(1:end-1, 2)];
        SpaceGame_procdat_trials.PrevPoints = [0; SpaceGame_par_dat.points(1:end-1)];
        SpaceGame_procdat_trials.Earth_Same = SpaceGame_procdat_trials.State_Earth == SpaceGame_procdat_trials.PrevState_Earth;
        SpaceGame_procdat_trials.Planet_Stay = SpaceGame_procdat_trials.State_planet == SpaceGame_procdat_trials.PrevState_planet;

        ind_unchosen_trials = SpaceGame_procdat_trials.Choice_Earth ~= SpaceGame_par_dat.stimuli;
        SpaceGame_procdat_trials.PrevUnChosen_Earth = [0; SpaceGame_par_dat.stimuli(1:end-1, 1).*ind_unchosen_trials(1:end-1, 1) + SpaceGame_par_dat.stimuli(1:end-1, 2).*ind_unchosen_trials(1:end-1, 2)];
        SpaceGame_procdat_trials.PrevRewards1 = [0; SpaceGame_par_dat.rews(1:end-1, 1)];
        SpaceGame_procdat_trials.PrevRewards2 = [0; SpaceGame_par_dat.rews(1:end-1, 2)];

        SpaceGame_procdat_trials.RewardDiff_ChosenUnchosen = (SpaceGame_par_dat.rews(:, 1).*~ind_unchosen_trials(:, 1) + SpaceGame_par_dat.rews(:, 2).*~ind_unchosen_trials(:, 2)) ...
                                                       - (SpaceGame_par_dat.rews(:, 1).*ind_unchosen_trials(:, 1) + SpaceGame_par_dat.rews(:, 2).*ind_unchosen_trials(:, 2));

        SpaceGame_procdat_trials.Ntrials(:) = SpaceGame_par_dat.pms.nrTrials; 

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%        Combine and export             %%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        SpaceGame_procdat = [SpaceGame_procdat_prac; SpaceGame_procdat_trials];

        cd([base_wd 'SpaceGame_Processed_Data_Files']);
        writetable(SpaceGame_procdat, sprintf('SpaceGame_Processed_%d-%d.csv', parID_num, session_num), 'WriteRowNames',true);

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%               Summary Data              %%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % row index
        prow = height(SpaceGame_dat) + 1;

        %long row indes
        endrow = height(SpaceGame_dat_long) + 4;
        startrow = endrow - 3;

        %participant information
        SpaceGame_dat.ParID(prow) = parID_num;
        SpaceGame_dat_long.ParID(startrow:endrow) = parID_num;

        SpaceGame_dat.Session(prow) = session_num;
        SpaceGame_dat_long.Session(startrow:endrow) = session_num;

        %point
        SpaceGame_dat.TotalScore(prow) = SpaceGame_par_dat.currentScore;

        %Earth RT
        SpaceGame_dat.Earth_meanRT(prow) = mean(SpaceGame_procdat_trials.RT_Earth(~SpaceGame_procdat_trials.Timeout_Earth));
        SpaceGame_dat.Earth_medRT(prow) = median(SpaceGame_procdat_trials.RT_Earth(~SpaceGame_procdat_trials.Timeout_Earth));

        %Earth missed
        SpaceGame_dat.Earth_nMissed(prow) = sum(SpaceGame_procdat_trials.Timeout_Earth);
        SpaceGame_dat.Earth_pMiss(prow) = sum(SpaceGame_procdat_trials.Timeout_Earth)/SpaceGame_par_dat.pms.nrTrials;

        %Planet RT
        SpaceGame_dat.Planet_meanRT(prow) = mean(SpaceGame_procdat_trials.RT_planet(~SpaceGame_procdat_trials.Timeout_planet));
        SpaceGame_dat.Planet_medRT(prow) = median(SpaceGame_procdat_trials.RT_planet(~SpaceGame_procdat_trials.Timeout_planet));

        %Planet Missed
        SpaceGame_dat.Planet_nMissed(prow) = sum(SpaceGame_procdat_trials.Timeout_planet);
        SpaceGame_dat.Planet_pMiss(prow) = sum(SpaceGame_procdat_trials.Timeout_planet)/SpaceGame_par_dat.pms.nrTrials;

        %reward rate
        SpaceGame_dat.RewardRate(prow) = mean(SpaceGame_procdat_trials.Points(~SpaceGame_procdat_trials.Missed));

        %average reward overall across both options
        rewards = [SpaceGame_procdat_trials.Rewards1, SpaceGame_procdat_trials.Rewards2];
        SpaceGame_dat.AvgReward(prow) = mean(rewards(:));

        %corrected reward rate
        SpaceGame_dat.RewardRate_Cor(prow) = SpaceGame_dat.RewardRate(prow) - SpaceGame_dat.AvgReward(prow);

        %stay probabilities (always won previously as no negatives) for if
        %earth state is same or different

        SpaceGame_dat.probStay_Same1state(prow) = mean(SpaceGame_procdat_trials.Planet_Stay(SpaceGame_procdat_trials.Earth_Same & ~SpaceGame_procdat_trials.Missed));
        SpaceGame_dat.probStay_Diff1state(prow) = mean(SpaceGame_procdat_trials.Planet_Stay(~SpaceGame_procdat_trials.Earth_Same & ~SpaceGame_procdat_trials.Missed));

        %by block
        for b=1:SpaceGame_par_dat.pms.nrBlocks
            SpaceGame_procdat_trials_block = SpaceGame_procdat_trials(SpaceGame_procdat_trials.Block == b, :);

            totalscore_block(b) = sum(SpaceGame_procdat_trials_block.Points);

            earth_rtmean_block(b) = mean(SpaceGame_procdat_trials_block.RT_Earth(~SpaceGame_procdat_trials_block.Timeout_Earth));
            earth_rtmed_block(b) = median(SpaceGame_procdat_trials_block.RT_Earth(~SpaceGame_procdat_trials_block.Timeout_Earth));
            earth_missed_block(b) = sum(SpaceGame_procdat_trials_block.Timeout_Earth);
            earth_perc_missed_block(b) = sum(SpaceGame_procdat_trials_block.Timeout_Earth)/SpaceGame_par_dat.pms.nrTrialsPerBlock;

            planet_rtmean_block(b) = mean(SpaceGame_procdat_trials_block.RT_planet(~SpaceGame_procdat_trials_block.Timeout_planet));
            planet_rtmed_block(b) = median(SpaceGame_procdat_trials_block.RT_planet(~SpaceGame_procdat_trials_block.Timeout_planet));
            planet_missed_block(b) = sum(SpaceGame_procdat_trials_block.Timeout_planet);
            planet_perc_missed_block(b) = sum(SpaceGame_procdat_trials_block.Timeout_planet)/SpaceGame_par_dat.pms.nrTrialsPerBlock;

            rr_block(b) = mean(SpaceGame_procdat_trials_block.Points(~SpaceGame_procdat_trials_block.Missed));

            rewards_block = [SpaceGame_procdat_trials_block.Rewards1, SpaceGame_procdat_trials_block.Rewards2];
            avg_rr_block(b) = mean(rewards_block(:));

            rr_cor_block(b) = rr_block(b) - avg_rr_block(b);

            stayprob_Esame_block(b) = mean(SpaceGame_procdat_trials_block.Planet_Stay(SpaceGame_procdat_trials_block.Earth_Same & ~SpaceGame_procdat_trials_block.Missed));
            stayprob_Edif_block(b) = mean(SpaceGame_procdat_trials_block.Planet_Stay(~SpaceGame_procdat_trials_block.Earth_Same & ~SpaceGame_procdat_trials_block.Missed));

            block_num(b) = b;

            if b == 1
                sum_byblock = [totalscore_block(b), earth_rtmean_block(b), earth_rtmed_block(b), ...
                    earth_missed_block(b), earth_perc_missed_block(b), planet_rtmean_block(b), ...
                    planet_rtmed_block(b), planet_missed_block(b), planet_perc_missed_block(b), ...
                    rr_block(b), avg_rr_block(b), rr_cor_block(b), stayprob_Esame_block(b), ...
                    stayprob_Edif_block(b)];
            else
                sum_byblock = [sum_byblock, totalscore_block(b), earth_rtmean_block(b), earth_rtmed_block(b), ...
                    earth_missed_block(b), earth_perc_missed_block(b), planet_rtmean_block(b), ...
                    planet_rtmed_block(b), planet_missed_block(b), planet_perc_missed_block(b), ...
                    rr_block(b), avg_rr_block(b), rr_cor_block(b), stayprob_Esame_block(b), ...
                    stayprob_Edif_block(b)];
            end
        end

        %add to database
        SpaceGame_dat(prow, 17:end) = array2table(sum_byblock);

        %long format
        sum_byblock_long = [block_num', totalscore_block', earth_rtmean_block', earth_rtmed_block', ...
                earth_missed_block', earth_perc_missed_block', planet_rtmean_block', ...
                planet_rtmed_block', planet_missed_block', planet_perc_missed_block', ...
                rr_block', avg_rr_block', rr_cor_block', stayprob_Esame_block', ...
                stayprob_Edif_block'];

        %add to database
        SpaceGame_dat_long(startrow:endrow, 3:end) = array2table(sum_byblock_long);

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%               Group Data              %%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %subdata
        groupdata = make_groupdata(SpaceGame_procdat_trials, groupdata);

        %other behavioral data
        groupdata.session(session_num).rewardrate(parID_num, 1) = SpaceGame_dat.RewardRate(prow);
        groupdata.session(session_num).avg_rew(parID_num, 1) = SpaceGame_dat.AvgReward(prow);
        groupdata.session(session_num).rewardrate_corrected(parID_num, 1) = SpaceGame_dat.RewardRate_Cor(prow);
        groupdata.session(session_num).stayprobs(parID_num, 1) = SpaceGame_dat.probStay_Same1state(prow);
        groupdata.session(session_num).stayprobs(parID_num, 2) = SpaceGame_dat.probStay_Diff1state(prow);

        rdat_table = [SpaceGame_procdat_trials.ParID, SpaceGame_procdat_trials.PrevPoints, ...
        SpaceGame_procdat_trials.Earth_Same, SpaceGame_procdat_trials.RewardDiff_ChosenUnchosen, ...
        SpaceGame_procdat_trials.Planet_Stay];

        if isfield(groupdata.session(session_num), 'r')
            groupdata.session(session_num).r = [groupdata.session(session_num).r; rdat_table];
        else
            groupdata.session(session_num).r = rdat_table;               
        end
    end

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%              Write out summary data                 %%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    today_date = date; 

    cd([base_wd 'SpaceGame_Databases']);

    %cleanup old files--move all files to 'Old_database_backup'
    for m = 1:height(database_file_tab)
        movefile(char(database_file_tab.name(m)), 'Old_database_backup/');
    end

    %edit here! rename with date
    if exist([base_wd 'SpaceGame_Databases' slash 'groupdata.mat'], 'file')
        movefile('groupdata.mat', ['Old_database_backup/groupdata_', today_date, '.mat']);
    end

    save('groupdata.mat', '-struct', 'groupdata');
    writetable(SpaceGame_dat, sprintf('SpaceGame_database_%s.csv', today_date), 'WriteRowNames',true);
    writetable(SpaceGame_dat_long, sprintf('SpaceGame_database_BlocksLong_%s.csv', today_date), 'WriteRowNames',true);
end
