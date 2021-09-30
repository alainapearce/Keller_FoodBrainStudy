function results = mfit_wrapper

% Function that fits behavioral data to reinforcement learning models
% for the novel two-step paradigm in Kool, Cushman, & Gershman (2016).
% 
% USAGE: results = mfit_wrapper
%
% NOTES:
%   This function requires the mfit model-fitting package: https://github.com/sjgershm/mfit
%
% Wouter Kool, Aug 2016
%
% AP NOTES: results structure for each session/model, you will get
%   parID: sub ID -- AP added
%   K: number input paramenters
%   param: input parameters
%   likfun: the function used to fit data
%   logpost: log posterior
%   loglik: smallest fit negative log liklihood
%   x: fit parameters for model
%       x(1): softmax inverse temperature
%       x(2): learning rate
%       x(3): eligibility trace decay
%       x(4): mixing weight
%   H: hessian fit 4x4 matrix
%   bic: Bayesian information criterion for fit model
%   aic: Akaike information criterion for fit model


    %1/21/20: APedit-add preamable to get paths correct
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%                         Setup                       %%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %!need to edit this section (and all paths) if move script or any directories it calls!

    %get working directory path for where this script is saved
    %(individual path info '/Box Sync/b-childfoodlab Shared/RO1_Brain_Mechanisms_IRB_5357/Participant Data/SpaceGame/Scripts')
    script_wd = mfilename('fullpath');

%     if ismac()
%         slash = '/';
%     else 
%         slash = '\';
%     end
    
    %cluster slash direction
    slash = '/';
    
    %get location/character number for '/" in file path
    slashloc_wd=find(script_wd==slash);

    %use all characters in path name upto the 7th slash (individual path info
    %'/Box Sync/b-childfoodlab Shared/RO1_Brain_Mechanisms_IRB_5357/Participant Data/SpaceGame)
    base_wd = script_wd(1:slashloc_wd(end-2));

    %this will tell matlab to look at all files withing the base_wd--so any
    %subfolder will be added to search path
    addpath(genpath(base_wd));

    %Start of Kool script
    %1/21/20: APedit load statement and moved down
%     load groupdata

    opts.model = [1 2 3]; % 1 = hybrid model, 2 = model-based 3 = model-free
    opts.st = [0 1]; % indexes presence of stimulus stickiness
    opts.respst = [0 1]; % indexes presence of response stickiness
    opts = factorial_models(opts);

    nstarts = 50;
    nrmodels = length(opts);
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%         Load Data        %%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    cd([base_wd 'SpaceGame_Databases']);
    
    %create str to identify files using wildcard '*'
    database_file_str = 'SpaceGame_DM*.csv';
    
    %use str to identify files--save as table
    database_file = dir(char(database_file_str));
    database_file_tab = struct2table(database_file);
    
    %load file
    SpaceGame_DM_dat = readtable(char(database_file_tab.name), 'ReadVariableNames', true);
    SpaceGame_DM_dat_VN = SpaceGame_DM_dat.Properties.VariableNames;

    %load group data
    groupdata = load('groupdata.mat');
    
    %1/21/20: APedit to add session and indicator in case a participant did not
    %complete and moved down into session loop
    % data = groupdata.session.subdata(groupdata.session.i);
    %1/21/20: APedit to look for results mat and load if exists
    if exist([base_wd 'SpaceGame_Databases' slash 'results.mat'], 'file')
        results = load([base_wd 'SpaceGame_Databases' slash 'results.mat']);
    else
        results = struct;
    end

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%         Run model        %%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %make session dset with correct varnames
    SpaceGame_DM_dat_session = array2table(cell(0, 14));
    SpaceGame_DM_dat_session.Properties.VariableNames = SpaceGame_DM_dat_VN;

    %make model a string variabl
    SpaceGame_DM_dat_session.Model = string(SpaceGame_DM_dat_session.Model);
    
    %1/21/20: APedit-added loop for session
    for s = 1:length(groupdata.session)
        %participant already modeled previously and only select
        %groupdata that haven't
        if isfield(results, 'session')
            if length(results.session) >= s
                exisitngIDs = results.session(s).model(1).ParID ~= 0; 
                existing_par = ismember(groupdata.session(s).i, results.session(s).model(1).ParID(exisitngIDs));
                data = groupdata.session(s).subdata(~existing_par & groupdata.session(s).i ~= 0);
            else
                data = groupdata.session(s).subdata(groupdata.session(s).i ~= 0);
            end
        else
            data = groupdata.session(s).subdata(groupdata.session(s).i ~= 0);
        end
        
        % run optimization
        for m = 1:nrmodels

            disp(['Fitting model ',num2str(m)])
            [options, params] = set_opts(opts(m));

            %1/21/20: APedit to change file name
            f = @(x,data) MB_MF_novel_rllik_PearceF32(x,data,options);

            %1/21/20: APedit to handle two sessions and added results to
            %function so can run mulitple times without overwriting
%             results(m) = mfit_optimize(f,params,data,nstarts);
%             results(m).opts = opts(model);

            results = mfit_optimize_SpaceGameEdits(f,params,data,nstarts,results,m,s);
            results.session(s).model(m).opts = opts(m);

            %1/21/20: APedit-added so easier to understand model
            model_str = {'HybridModel' 'ModelBased' 'ModelFree'};
            stim_str = {'NoStimSticky' 'StimSticky'};
            resp_str = {'NoRespSticky' 'RespSticky'};
            results.session(s).model(m).opts_label = [model_str{opts(m).model}, '_', ...
                stim_str{opts(m).st + 1}, '_', resp_str{opts(m).respst + 1}];
            
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%         make a table for R       %%%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %1/21/20: APedit - added to get nice output to use in R

            %make it easier/shorter to call data and get indicator for data
            res = results.session(s).model(m);
            res_ind = res.ParID ~= 0;
            
            rowstart = height(SpaceGame_DM_dat_session) + 1;
            rowend = height(SpaceGame_DM_dat_session) + sum(res_ind);
            
            %add data to end of session dset
            SpaceGame_DM_dat_session.ParID(rowstart:rowend) = num2cell(res.ParID(res_ind));
            SpaceGame_DM_dat_session.Session(rowstart:rowend) = num2cell(s);
            SpaceGame_DM_dat_session.Model(rowstart:rowend) = res.opts_label;
            SpaceGame_DM_dat_session.Parameters(rowstart:rowend) = num2cell(res.K);
            SpaceGame_DM_dat_session.bic(rowstart:rowend) = num2cell(res.bic(res_ind));
            SpaceGame_DM_dat_session.aic(rowstart:rowend) = num2cell(res.aic(res_ind));
            SpaceGame_DM_dat_session.loglikelihood(rowstart:rowend) = num2cell(res.loglik(res_ind));
            SpaceGame_DM_dat_session.beta(rowstart:rowend) = num2cell(res.x(res_ind, 1));
            SpaceGame_DM_dat_session.alpha(rowstart:rowend) = num2cell(res.x(res_ind, 2));
            SpaceGame_DM_dat_session.lambda(rowstart:rowend) = num2cell(res.x(res_ind, 3));
            
            %for models with more parameters
            if res.K > 3
                %only hybrid has w
                if opts(m).model == 1
                    SpaceGame_DM_dat_session.w(rowstart:rowend) = num2cell(res.x(res_ind, 4));
                    
                    %full model
                    if res.K == 6
                        SpaceGame_DM_dat_session.pi(rowstart:rowend) = num2cell(res.x(res_ind, 5));
                        SpaceGame_DM_dat_session.rho(rowstart:rowend) = num2cell(res.x(res_ind, 6));
                    else
                        %check which stickiness parameter was used
                        if opts(m).st == 1
                        	SpaceGame_DM_dat_session.pi(rowstart:rowend) = num2cell(res.x(res_ind, 5));
                        elseif opts(m).respst == 1
                            SpaceGame_DM_dat_session.rho(rowstart:rowend) = num2cell(res.x(res_ind, 5));
                        end
                    end
                    
                %both stickiness parameters for non-hybrid models
                elseif res.K == 5  
                    SpaceGame_DM_dat_session.pi(rowstart:rowend) = num2cell(res.x(res_ind, 4));
                    SpaceGame_DM_dat_session.rho(rowstart:rowend) = num2cell(res.x(res_ind, 5));
                elseif opts(m).st == 1
                    SpaceGame_DM_dat_session.pi(rowstart:rowend) = num2cell(res.x(res_ind, 4));
                elseif opts(m).respst == 1
                    SpaceGame_DM_dat_session.rho(rowstart:rowend) = num2cell(res.x(res_ind, 4));
                end  
            end
            
            %check to see if model had latents
            if isempty(res.latents)
                SpaceGame_DM_dat_session.latents(rowstart:rowend) = num2cell(0);
            else
                latent_ind = res.latents == 1;
                latent_parrow_ind = SpaceGame_DM_dat_session.ParID == res.ParID(latent_ind);
                
                SpaceGame_DM_dat_session.latents(latent_parrow_ind) = 1;
            end
        end  
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%         Export Data        %%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    today_date = date; 

    cd([base_wd 'SpaceGame_Databases']);
    
    if exist([base_wd 'SpaceGame_Databases' slash 'results.mat'], 'file')
        movefile('results.mat', ['Old_database_backup/results_', today_date, '.mat']);
    end

    save('results.mat', '-struct', 'results');
    
    %cleanup old files--move all files to 'Old_database_backup'
    for m = 1:height(database_file_tab)
        movefile(char(database_file_tab.name), 'Old_database_backup/');
    end
    
    writetable(SpaceGame_DM_dat_session, sprintf('SpaceGame_DM_database_%s.csv', today_date), 'WriteRowNames',true);
    
end
