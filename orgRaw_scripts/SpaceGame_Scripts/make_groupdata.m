function [groupdata] = make_groupdata(SpaceGame_procdat_trials, groupdata)

    % Sets up groupdata structure array with the same fields as in
    % Kool 2016 data. Written Spring 2020 by Alaina Pearce
    parID_num = SpaceGame_procdat_trials.ParID(1);
    session_num = SpaceGame_procdat_trials.Session(1);
    
    groupdata.session(session_num).i(parID_num, 1) = parID_num;

    %not in Kool, but I added
    groupdata.session(session_num).subdata(parID_num).ParID = parID_num;
    
    %copy Kool et al data structure for subdat
    groupdata.session(session_num).subdata(parID_num).State_Earth = SpaceGame_procdat_trials.State_Earth;
    groupdata.session(session_num).subdata(parID_num).Stim_left = SpaceGame_procdat_trials.Stim_left;
    groupdata.session(session_num).subdata(parID_num).Stim_right = SpaceGame_procdat_trials.Stim_right;
    groupdata.session(session_num).subdata(parID_num).RT_Earth = SpaceGame_procdat_trials.RT_Earth;
    groupdata.session(session_num).subdata(parID_num).Choice_Earth = SpaceGame_procdat_trials.Choice_Earth;
    groupdata.session(session_num).subdata(parID_num).RT_planet = SpaceGame_procdat_trials.RT_planet;
    groupdata.session(session_num).subdata(parID_num).State_planet = SpaceGame_procdat_trials.State_planet;
    groupdata.session(session_num).subdata(parID_num).Points = SpaceGame_procdat_trials.Points;
    groupdata.session(session_num).subdata(parID_num).Win = SpaceGame_procdat_trials.Win;
    groupdata.session(session_num).subdata(parID_num).Score = SpaceGame_procdat_trials.Score;
    groupdata.session(session_num).subdata(parID_num).Practice = SpaceGame_procdat_trials.Practice;
    groupdata.session(session_num).subdata(parID_num).Rewards1 = SpaceGame_procdat_trials.Rewards1;
    groupdata.session(session_num).subdata(parID_num).Rewards2 = SpaceGame_procdat_trials.Rewards2;
    groupdata.session(session_num).subdata(parID_num).Trial = SpaceGame_procdat_trials.Trial;
    groupdata.session(session_num).subdata(parID_num).Ntrials = SpaceGame_procdat_trials.Ntrials(1);

    %others/Behavioral
    groupdata.session(session_num).subdata(parID_num).Missed = SpaceGame_procdat_trials.Missed;
    groupdata.session(session_num).subdata(parID_num).PrevMissed = SpaceGame_procdat_trials.PrevMissed;
    groupdata.session(session_num).subdata(parID_num).PrevState_Earth = SpaceGame_procdat_trials.PrevState_Earth;
    groupdata.session(session_num).subdata(parID_num).PrevState_planet = SpaceGame_procdat_trials.PrevState_planet;
    groupdata.session(session_num).subdata(parID_num).Earth_Same = SpaceGame_procdat_trials.Earth_Same;
    groupdata.session(session_num).subdata(parID_num).Planet_Stay = SpaceGame_procdat_trials.Planet_Stay;
    groupdata.session(session_num).subdata(parID_num).r = [SpaceGame_procdat_trials.PrevPoints, ...
       SpaceGame_procdat_trials.Earth_Same, SpaceGame_procdat_trials.RewardDiff_ChosenUnchosen, ...
       SpaceGame_procdat_trials.Planet_Stay];
end
