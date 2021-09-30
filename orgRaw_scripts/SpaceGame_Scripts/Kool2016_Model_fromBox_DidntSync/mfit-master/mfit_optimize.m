function results = mfit_optimize(likfun,param,data,nstarts,results,m,ses)
    
    % Find maximum a posteriori parameter estimates.
    %
    % USAGE: results = mfit_optimize(likfun,param,data,[nstarts])
    %
    % INPUTS:
    %   likfun - likelihood function handle
    %   param - [K x 1] parameter structure
    %   data - [S x 1] data structure
    %   nstarts (optional) - number of random starts (default: 5)
    %
    %   APedit: added 
    %   results - existing results structure array
    %   m - model index
    %   ses - session index
    %
    % OUTPUTS:
    %   results - structure with the following fields:
    %               .x - [S x K] parameter estimates
    %               .logpost - [S x 1] log posterior
    %               .loglik - [S x 1] log likelihood
    %               .bic - [S x 1] Bayesian information criterion
    %               .aic - [S x 1] Akaike information criterion
    %               .H - [S x 1] cell array of Hessian matrices
    %               .latents - latent variables (only if likfun returns a second argument)
    %
    % Sam Gershman, March 2019
    
    % fill in missing options
    if nargin < 4 || isempty(nstarts); nstarts = 5; end
    K = length(param);
    results.session(ses).model(m).K = K;
    
    % save info to results structure
    results.session(ses).model(m).param = param;
    results.session(ses).model(m).likfun = likfun;
    
    % extract lower and upper bounds
    %APnote: if missing/not a field, fill with infinity
    if ~isfield(param,'lb'); lb = zeros(size(param)) + -inf; else lb = [param.lb]; end
    if ~isfield(param,'ub'); ub = zeros(size(param)) + inf; else ub = [param.ub]; end
    
    options = optimset('Display','off','MaxFunEvals',2000);
    warning off all
    
    if isfield(param,'x0'); nstarts = length(param(1).x0); end
    
    for s = 1:length(data)
        %APedit to report actual sub number
%         disp(['Subject ',num2str(s)]);
        parID_str = num2str(data(s).ParID);
        parID_num = data(s).ParID;
        disp(['Subject ', parID_str]);
        
        %1/21/20: APedit: added parID to results
        results.session(ses).model(m).ParID(parID_num,1) = parID_num;
        
        % construct posterior function
        f = @(x) -mfit_post(x,param,data(s),likfun);
        
        for i = 1:nstarts
            
            if all(isinf(lb)) && all(isinf(ub))
                if isfield(param,'x0')
                    for j = 1:length(param)
                        x0(j) = param(j).x0(i);
                    end
                else
                    x0 = randn(1,K);
                end
                %APnote: params were missing, they were filled with infinity
                %this finds the mimum of the link function when
                %unconstrained
                [x,nlogp,~,~,~,H] = fminunc(f,x0,options);
            else
                if isfield(param,'x0')
                    for j = 1:length(param)
                        x0(j) = param(j).x0(i);
                    end
                else
                    x0 = zeros(1,K);
                    for k = 1:K
                        x0(k) = unifrnd(param(k).lb,param(k).ub);
                    end
                end
                
                %APnote: this finds the mimum of the link function when
                %constrained by parameters; nlogp is the objective function 
                %value at the solution
                [x,nlogp,~,~,~,~,H] = fmincon(f,x0,[],[],[],[],lb,ub,[],options);
            end
            
            logp = -nlogp;
            
            %APnote: if first iteration or if function value is less than the
            %previous lowest then run the MB_MF_novel_rllik_PearceF32.m
            %script (i.e., 'likfun')
            
            %APedit: changed 's' indexing in results struct to parID_num so
            %that that the row corresponds to ID and wont get overwritten
            %when run again with new data/differe IDs
            
%             if i == 1 || results.logpost(s) < logp
%                 results.logpost(s) = logp;
%                 results.loglik(s) = likfun(x,data(s));
%                 results.x(s,:) = x;
%                 results.H{s} = H;
%             end
%         end
%         
%         %APnote: get fit solutions--BIC and AIC
%         results.bic(s,1) = K*log(data(s).Ntrials) - 2*results.loglik(s);
%         results.aic(s,1) = K*2 - 2*results.loglik(s);
%         
%         try
%             [~,results.latents(s)] = likfun(results.x(s,:), data(s));
%         catch
%             disp('no latents')
%             results.latents = [];
%         end

            if i == 1 || results.session(ses).model(m).logpost(parID_num) < logp
                results.session(ses).model(m).logpost(parID_num) = logp;
                results.session(ses).model(m).loglik(parID_num) = likfun(x,data(s));
                results.session(ses).model(m).x(parID_num,:) = x;
                results.session(ses).model(m).H{parID_num} = H;
            end
        end
        
        %APnote: get fit solutions--BIC and AIC
        results.session(ses).model(m).bic(parID_num,1) = K*log(data(s).Ntrials) - 2*results.session(ses).model(m).loglik(parID_num);
        results.session(ses).model(m).aic(parID_num,1) = K*2 - 2*results.session(ses).model(m).loglik(parID_num);
        
        try
            [~,results.session(ses).model(m).latents(parID_num)] = likfun(results.session(ses).model(m).x(parID_num,:), data(s));
        catch
            disp('no latents')
            results.session(ses).model(m).latents = [];
        end
    end