# This script was written by Alaina Pearce in January 2022
# to set up qs_cpsgraphic tables by risk status for the Food and Brain Study
# Data Blitz Meeting
#
#     Copyright (C) 2022 Alaina L Pearce
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

############ Basic Data Load/Setup ############
# need to uncomment if running indipendently - not needed if compiling with FBS_Datablitz_2022-01-25.Rmd

# library(haven)
# library(gtsummary)
# theme_gtsummary_compact()
#
# source('functions.R')

# source('setup_demo.R')

#### set up ####

## 1) Load Data ####
r01_qs_cps <- as.data.frame(read_spss(("data_2022-01-25/qs_cog_psych_soc.sav")))
names(r01_qs_cps)[1] <- 'sub'

r01_qs_cps_labels <- lapply(r01_qs_cps, function(x) attributes(x)$label)

#remove 2 that were removed for ADHD
r01_qs_cps <- r01_qs_cps[r01_qs_cps$sub != 31 & r01_qs_cps$sub != 34, ]

## 2) Get Variable Labels and Re-Level ####

# risk status
r01_qs_cps$risk_status_mom <- droplevels(as_factor(r01_qs_cps$risk_status_mom))
r01_qs_cps$risk_status_both <- droplevels(as_factor(r01_qs_cps$risk_status_both))
r01_qs_cps$sex <- as_factor(r01_qs_cps$sex)

# income
r01_qs_cps$income <- ifelse(is.na(r01_qs_cps$income), NA, ifelse(r01_qs_cps$income < 3, '< $51,000', ifelse(r01_qs_cps$income < 5, "$51,000 - $100,000", '>$100,000')))

# parental ed
r01_qs_cps$mom_ed <- ifelse(r01_qs_cps$measured_parent == 0, ifelse(r01_qs_cps$parent_ed == 0, 'High School/GED', ifelse(r01_qs_cps$parent_ed < 3, 'AA/Technical Degree', ifelse(r01_qs_cps$parent_ed == 3, 'Bachelor Degree', ifelse(r01_qs_cps$parent_ed < 8, '> Bachelor Degree', 'Other/NA')))), ifelse(r01_qs_cps$partner_ed == 0, 'High School/GED', ifelse(r01_qs_cps$partner_ed < 3, 'AA/Technical Degree', ifelse(r01_qs_cps$partner_ed == 3, 'Bachelor Degree', ifelse(r01_qs_cps$partner_ed < 8, '> Bachelor Degree', 'Other/NA')))))

r01_qs_cps$dad_ed <- ifelse(r01_qs_cps$measured_parent == 1, ifelse(r01_qs_cps$parent_ed == 0, 'High School/GED', ifelse(r01_qs_cps$parent_ed < 3, 'AA/Technical Degree', ifelse(r01_qs_cps$parent_ed == 3, 'Bachelor Degree', ifelse(r01_qs_cps$parent_ed < 8, '> Bachelor Degree', 'Other/NA')))), ifelse(r01_qs_cps$partner_ed == 0, 'High School/GED', ifelse(r01_qs_cps$partner_ed < 3, 'AA/Technical Degree', ifelse(r01_qs_cps$partner_ed == 3, 'Bachelor Degree', ifelse(r01_qs_cps$partner_ed < 8, '> Bachelor Degree', 'Other/NA')))))

# rcmas
r01_qs_cps$rcmas_total_normcat <- droplevels(as_factor(r01_qs_cps$rcmas_total_normcat))
r01_qs_cps$rcmas_total_cutcat <- droplevels(as_factor(r01_qs_cps$rcmas_total_cutcat))
r01_qs_cps$rcmas_sd_total_normcat <- droplevels(as_factor(r01_qs_cps$rcmas_sd_total_normcat))

# breif - 2
r01_qs_cps$brief2_negativity_cat <- droplevels(as_factor(r01_qs_cps$brief2_negativity_cat))
r01_qs_cps$brief2_inconsistency_cat <- droplevels(as_factor(r01_qs_cps$brief2_inconsistency_cat))
r01_qs_cps$brief2_infrequency_cat <- droplevels(as_factor(r01_qs_cps$brief2_infrequency_cat))

r01_qs_cps$v7_brief2_negativity_cat <- droplevels(as_factor(r01_qs_cps$v7_brief2_negativity_cat))
r01_qs_cps$v7_brief2_inconsistency_cat <- droplevels(as_factor(r01_qs_cps$v7_brief2_inconsistency_cat))
r01_qs_cps$v7_brief2_infrequency_cat <- droplevels(as_factor(r01_qs_cps$v7_brief2_infrequency_cat))

## 2) Tables ####

## 2a) Anxiety ####

## all
anx <- r01_qs_cps[!is.na(r01_qs_cps$rcmas_sd_total), c(12, 10, 65:70, 73:74)]

anx_tab <-
  tbl_summary(
    data = anx,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", rcmas_phys ~ "Physical", rcmas_worry ~ "Worry", rcmas_concentration ~ "Concentration", rcmas_total ~ "Total", rcmas_total_normcat ~ "Grade Norm Category", rcmas_total_cutcat ~ "Cutoff Score Category", rcmas_sd_total ~ "Social Desirability", rcmas_sd_total_normcat ~ "Social Desirability Norm Category"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", rcmas_phys ~ "Physical", rcmas_worry ~ "Worry", rcmas_concentration ~ "Concentration", rcmas_total ~ "Total", rcmas_total_normcat ~ "Grade Norm Category", rcmas_total_cutcat ~ "Cutoff Score Category", rcmas_sd_total ~ "Social Desirability", rcmas_sd_total_normcat ~ "Social Desirability Norm Category"),
    type = list(rcmas_phys ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# mom risk
anx_risk_mom <- r01_qs_cps[!is.na(r01_qs_cps$rcmas_sd_total) & r01_qs_cps$risk_status_mom != 'Neither', c(8, 12, 10, 65:70, 73:74)]

anx_risk_mom$risk_status_mom <- droplevels(anx_risk_mom$risk_status_mom)

anx_risk_mom_tab <-
  tbl_summary(
    data = anx_risk_mom,
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", rcmas_phys ~ "Physical", rcmas_worry ~ "Worry", rcmas_concentration ~ "Concentration", rcmas_total ~ "Total", rcmas_total_normcat ~ "Grade Norm Category", rcmas_total_cutcat ~ "Cutoff Score Category", rcmas_sd_total ~ "Social Desirability", rcmas_sd_total_normcat ~ "Social Desirability Norm Category"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", rcmas_phys ~ "Physical", rcmas_worry ~ "Worry", rcmas_concentration ~ "Concentration", rcmas_total ~ "Total", rcmas_total_normcat ~ "Grade Norm Category", rcmas_total_cutcat ~ "Cutoff Score Category", rcmas_sd_total ~ "Social Desirability", rcmas_sd_total_normcat ~ "Social Desirability Norm Category"),
    type = list(rcmas_phys ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# strict/both risk
anx_risk_both <- r01_qs_cps[!is.na(r01_qs_cps$rcmas_sd_total) & r01_qs_cps$risk_status_both != 'Neither', c(9, 12, 10, 65:70, 73:74)]

anx_risk_both$risk_status_both <- droplevels(anx_risk_both$risk_status_both)

anx_risk_both_tab <-
  tbl_summary(
    data = anx_risk_both,
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", rcmas_phys ~ "Physical", rcmas_worry ~ "Worry", rcmas_concentration ~ "Concentration", rcmas_total ~ "Total", rcmas_total_normcat ~ "Grade Norm Category", rcmas_total_cutcat ~ "Cutoff Score Category", rcmas_sd_total ~ "Social Desirability", rcmas_sd_total_normcat ~ "Social Desirability Norm Category"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", rcmas_phys ~ "Physical", rcmas_worry ~ "Worry", rcmas_concentration ~ "Concentration", rcmas_total ~ "Total", rcmas_total_normcat ~ "Grade Norm Category", rcmas_total_cutcat ~ "Cutoff Score Category", rcmas_sd_total ~ "Social Desirability", rcmas_sd_total_normcat ~ "Social Desirability Norm Category"),
    type = list(rcmas_phys ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

qs_anx_merge_tab <-
  tbl_merge(
    tbls = list(anx_tab, anx_risk_mom_tab, anx_risk_both_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )

## 2b) Temperament ####

## all
temp <- r01_qs_cps[c(12, 10, 169:186)]
temp$all_na <- rowSums(is.na(temp))
temp <- temp[temp$all_na < 18, ]

temp_tab <-
  tbl_summary(
    data = temp[1:20],
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", cbq_activity ~ "Activity Level", cbq_anger ~ "Anger/Frustration", cbq_approach ~ "Approach/Positive Anticipation", cbq_attention ~ "Attentional Focusing", cbq_discomfort ~ "Discomfort", cbq_soothability ~ "Falling Reactivity/Soothability", cbq_fear ~ "Fear", cbq_highintensity_pleasure ~ "High Intensity Pleasure", cbq_impulsivity ~ "Impulsivity", cbq_inhibitory_cont ~ "Inhibitory control", cbq_lowintensity_pleasure ~ "Low Intesity Pleasure", cbq_perceptual_sensitivity ~ "Perceptual Sensitivity", cbq_sadness ~ "Sadness", cbq_shyness ~ "Shyness", cbq_smile_laughter ~ "Similing and Laughter", cbq_surgency ~ "Big 3 - Surgency", cbq_neg_affect ~ "Big 3 - Negative Affect", cbq_effortful_cont ~ "Big 3 - Effortful Control"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", cbq_activity ~ "Activity Level", cbq_anger ~ "Anger/Frustration", cbq_approach ~ "Approach/Positive Anticipation", cbq_attention ~ "Attentional Focusing", cbq_discomfort ~ "Discomfort", cbq_soothability ~ "Falling Reactivity/Soothability", cbq_fear ~ "Fear", cbq_highintensity_pleasure ~ "High Intensity Pleasure", cbq_impulsivity ~ "Impulsivity", cbq_inhibitory_cont ~ "Inhibitory control", cbq_lowintensity_pleasure ~ "Low Intesity Pleasure", cbq_perceptual_sensitivity ~ "Perceptual Sensitivity", cbq_sadness ~ "Sadness", cbq_shyness ~ "Shyness", cbq_smile_laughter ~ "Similing and Laughter", cbq_surgency ~ "Big 3 - Surgency", cbq_neg_affect ~ "Big 3 - Negative Affect", cbq_effortful_cont ~ "Big 3 - Effortful Control"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# mom risk
temp_risk_mom <- r01_qs_cps[r01_qs_cps$risk_status_mom != 'Neither', c(8, 12, 10, 169:186)]
temp_risk_mom$all_na <- rowSums(is.na(temp_risk_mom))
temp_risk_mom$risk_status_mom <- droplevels(temp_risk_mom$risk_status_mom)

temp_risk_mom <- temp_risk_mom[temp_risk_mom$all_na < 18, ]

temp_risk_mom_tab <-
  tbl_summary(
    data = temp_risk_mom[1:21],
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", cbq_activity ~ "Activity Level", cbq_anger ~ "Anger/Frustration", cbq_approach ~ "Approach/Positive Anticipation", cbq_attention ~ "Attentional Focusing", cbq_discomfort ~ "Discomfort", cbq_soothability ~ "Falling Reactivity/Soothability", cbq_fear ~ "Fear", cbq_highintensity_pleasure ~ "High Intensity Pleasure", cbq_impulsivity ~ "Impulsivity", cbq_inhibitory_cont ~ "Inhibitory control", cbq_lowintensity_pleasure ~ "Low Intesity Pleasure", cbq_perceptual_sensitivity ~ "Perceptual Sensitivity", cbq_sadness ~ "Sadness", cbq_shyness ~ "Shyness", cbq_smile_laughter ~ "Similing and Laughter", cbq_surgency ~ "Big 3 - Surgency", cbq_neg_affect ~ "Big 3 - Negative Affect", cbq_effortful_cont ~ "Big 3 - Effortful Control"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", cbq_activity ~ "Activity Level", cbq_anger ~ "Anger/Frustration", cbq_approach ~ "Approach/Positive Anticipation", cbq_attention ~ "Attentional Focusing", cbq_discomfort ~ "Discomfort", cbq_soothability ~ "Falling Reactivity/Soothability", cbq_fear ~ "Fear", cbq_highintensity_pleasure ~ "High Intensity Pleasure", cbq_impulsivity ~ "Impulsivity", cbq_inhibitory_cont ~ "Inhibitory control", cbq_lowintensity_pleasure ~ "Low Intesity Pleasure", cbq_perceptual_sensitivity ~ "Perceptual Sensitivity", cbq_sadness ~ "Sadness", cbq_shyness ~ "Shyness", cbq_smile_laughter ~ "Similing and Laughter", cbq_surgency ~ "Big 3 - Surgency", cbq_neg_affect ~ "Big 3 - Negative Affect", cbq_effortful_cont ~ "Big 3 - Effortful Control"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# strict/both risk
temp_risk_both <- r01_qs_cps[r01_qs_cps$risk_status_both != 'Neither', c(9, 12, 10, 169:186)]
temp_risk_both$risk_status_both <- droplevels(temp_risk_both$risk_status_both)
temp_risk_both$all_na <- rowSums(is.na(temp_risk_both))
temp_risk_both <- temp_risk_both[temp_risk_both$all_na < 18, ]

temp_risk_both_tab <-
  tbl_summary(
    data = temp_risk_both[1:21],
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", cbq_activity ~ "Activity Level", cbq_anger ~ "Anger/Frustration", cbq_approach ~ "Approach/Positive Anticipation", cbq_attention ~ "Attentional Focusing", cbq_discomfort ~ "Discomfort", cbq_soothability ~ "Falling Reactivity/Soothability", cbq_fear ~ "Fear", cbq_highintensity_pleasure ~ "High Intensity Pleasure", cbq_impulsivity ~ "Impulsivity", cbq_inhibitory_cont ~ "Inhibitory control", cbq_lowintensity_pleasure ~ "Low Intesity Pleasure", cbq_perceptual_sensitivity ~ "Perceptual Sensitivity", cbq_sadness ~ "Sadness", cbq_shyness ~ "Shyness", cbq_smile_laughter ~ "Similing and Laughter", cbq_surgency ~ "Big 3 - Surgency", cbq_neg_affect ~ "Big 3 - Negative Affect", cbq_effortful_cont ~ "Big 3 - Effortful Control"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", cbq_activity ~ "Activity Level", cbq_anger ~ "Anger/Frustration", cbq_approach ~ "Approach/Positive Anticipation", cbq_attention ~ "Attentional Focusing", cbq_discomfort ~ "Discomfort", cbq_soothability ~ "Falling Reactivity/Soothability", cbq_fear ~ "Fear", cbq_highintensity_pleasure ~ "High Intensity Pleasure", cbq_impulsivity ~ "Impulsivity", cbq_inhibitory_cont ~ "Inhibitory control", cbq_lowintensity_pleasure ~ "Low Intesity Pleasure", cbq_perceptual_sensitivity ~ "Perceptual Sensitivity", cbq_sadness ~ "Sadness", cbq_shyness ~ "Shyness", cbq_smile_laughter ~ "Similing and Laughter", cbq_surgency ~ "Big 3 - Surgency", cbq_neg_affect ~ "Big 3 - Negative Affect", cbq_effortful_cont ~ "Big 3 - Effortful Control"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

qs_temp_merge_tab <-
  tbl_merge(
    tbls = list(temp_tab, temp_risk_mom_tab, temp_risk_both_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )

## 2c) BIS/BAS and SPSRQ ####

## all
reward <- r01_qs_cps[c(12, 10, 212:216, 265:275)]
reward$all_na <- rowSums(is.na(reward))
reward <- reward[reward$all_na < 16, ]

reward_tab <-
  tbl_summary(
    data = reward[1:18],
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", bis ~ "Behavioral Inhibition, BIS/BAS", bas ~ "Behavioral Approach, BIS/BAS", bas_funseeking ~ "Funseeking, BIS/BAS", bas_drive ~ "Drive, BIS/BAS", bas_rewardresp ~ "Rewrad Responsiveness, BIS/BAS", spsrq34_punishment ~ "Sensitivity to Punishment, SPSRQ-34", spsrq34_impfun ~ "Impulsivity/Fun Seeking, SPSRQ-34", spsrq34_drive ~ "Drive, SPSRQ-34", spsrq34_rewardresp ~ "Reward Responsiveness, SPSRQ-34", spsrq48_fearshy ~ "Fear/Shyness, SPSRQ-48", spsrq48_anxiety ~ "Anxiety, SPSRQ-48", spsrq48_conflictavoid ~ "Conflict Avoidence, SPSRQ-48", spsrq48_impfun ~ "Impulsivity/Fun Seeking, SPSRQ-48", spsrq48_drive ~ "Drive, SPSRQ-48", spsrq48_socialapproval ~ "Social Approval, SPSRQ-48", spsrq48_sensoryreward ~ "Sensory Reward, SPSRQ-48"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", bis ~ "Behavioral Inhibition, BIS/BAS", bas ~ "Behavioral Approach, BIS/BAS", bas_funseeking ~ "Funseeking, BIS/BAS", bas_drive ~ "Drive, BIS/BAS", bas_rewardresp ~ "Reward Responsiveness, BIS/BAS", spsrq34_punishment ~ "Sensitivity to Punishment, SPSRQ-34", spsrq34_impfun ~ "Impulsivity/Fun Seeking, SPSRQ-34", spsrq34_drive ~ "Drive, SPSRQ-34", spsrq34_rewardresp ~ "Reward Responsiveness, SPSRQ-34", spsrq48_fearshy ~ "Fear/Shyness, SPSRQ-48", spsrq48_anxiety ~ "Anxiety, SPSRQ-48", spsrq48_conflictavoid ~ "Conflict Avoidence, SPSRQ-48", spsrq48_impfun ~ "Impulsivity/Fun Seeking, SPSRQ-48", spsrq48_drive ~ "Drive, SPSRQ-48", spsrq48_socialapproval ~ "Social Approval, SPSRQ-48", spsrq48_sensoryreward ~ "Sensory Reward, SPSRQ-48"),
    type = list(bas_rewardresp ~ 'continuous', spsrq48_conflictavoid ~ 'continuous', spsrq48_sensoryreward ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# mom risk
reward_risk_mom <- r01_qs_cps[r01_qs_cps$risk_status_mom != 'Neither', c(8, 12, 10, 212:216, 265:275)]
reward_risk_mom$all_na <- rowSums(is.na(reward_risk_mom))
reward_risk_mom$risk_status_mom <- droplevels(reward_risk_mom$risk_status_mom)

reward_risk_mom <- reward_risk_mom[reward_risk_mom$all_na < 16, ]

reward_risk_mom_tab <-
  tbl_summary(
    data = reward_risk_mom[1:19],
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", bis ~ "Behavioral Inhibition, BIS/BAS", bas ~ "Behavioral Approach, BIS/BAS", bas_funseeking ~ "Funseeking, BIS/BAS", bas_drive ~ "Drive, BIS/BAS", bas_rewardresp ~ "Rewrad Responsiveness, BIS/BAS", spsrq34_punishment ~ "Sensitivity to Punishment, SPSRQ-34", spsrq34_impfun ~ "Impulsivity/Fun Seeking, SPSRQ-34", spsrq34_drive ~ "Drive, SPSRQ-34", spsrq34_rewardresp ~ "Reward Responsiveness, SPSRQ-34", spsrq48_fearshy ~ "Fear/Shyness, SPSRQ-48", spsrq48_anxiety ~ "Anxiety, SPSRQ-48", spsrq48_conflictavoid ~ "Conflict Avoidence, SPSRQ-48", spsrq48_impfun ~ "Impulsivity/Fun Seeking, SPSRQ-48", spsrq48_drive ~ "Drive, SPSRQ-48", spsrq48_socialapproval ~ "Social Approval, SPSRQ-48", spsrq48_sensoryreward ~ "Sensory Reward, SPSRQ-48"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", bis ~ "Behavioral Inhibition, BIS/BAS", bas ~ "Behavioral Approach, BIS/BAS", bas_funseeking ~ "Funseeking, BIS/BAS", bas_drive ~ "Drive, BIS/BAS", bas_rewardresp ~ "Reward Responsiveness, BIS/BAS", spsrq34_punishment ~ "Sensitivity to Punishment, SPSRQ-34", spsrq34_impfun ~ "Impulsivity/Fun Seeking, SPSRQ-34", spsrq34_drive ~ "Drive, SPSRQ-34", spsrq34_rewardresp ~ "Reward Responsiveness, SPSRQ-34", spsrq48_fearshy ~ "Fear/Shyness, SPSRQ-48", spsrq48_anxiety ~ "Anxiety, SPSRQ-48", spsrq48_conflictavoid ~ "Conflict Avoidence, SPSRQ-48", spsrq48_impfun ~ "Impulsivity/Fun Seeking, SPSRQ-48", spsrq48_drive ~ "Drive, SPSRQ-48", spsrq48_socialapproval ~ "Social Approval, SPSRQ-48", spsrq48_sensoryreward ~ "Sensory Reward, SPSRQ-48"),
    type = list(bas_rewardresp ~ 'continuous', spsrq48_conflictavoid ~ 'continuous', spsrq48_sensoryreward ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# strict/both risk
reward_risk_both <- r01_qs_cps[r01_qs_cps$risk_status_both != 'Neither', c(9, 12, 10, 212:216, 265:275)]
reward_risk_both$risk_status_both <- droplevels(reward_risk_both$risk_status_both)
reward_risk_both$all_na <- rowSums(is.na(reward_risk_both))
reward_risk_both <- reward_risk_both[reward_risk_both$all_na < 16, ]

reward_risk_both_tab <-
  tbl_summary(
    data = reward_risk_both[1:19],
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", bis ~ "Behavioral Inhibition, BIS/BAS", bas ~ "Behavioral Approach, BIS/BAS", bas_funseeking ~ "Funseeking, BIS/BAS", bas_drive ~ "Drive, BIS/BAS", bas_rewardresp ~ "Rewrad Responsiveness, BIS/BAS", spsrq34_punishment ~ "Sensitivity to Punishment, SPSRQ-34", spsrq34_impfun ~ "Impulsivity/Fun Seeking, SPSRQ-34", spsrq34_drive ~ "Drive, SPSRQ-34", spsrq34_rewardresp ~ "Reward Responsiveness, SPSRQ-34", spsrq48_fearshy ~ "Fear/Shyness, SPSRQ-48", spsrq48_anxiety ~ "Anxiety, SPSRQ-48", spsrq48_conflictavoid ~ "Conflict Avoidence, SPSRQ-48", spsrq48_impfun ~ "Impulsivity/Fun Seeking, SPSRQ-48", spsrq48_drive ~ "Drive, SPSRQ-48", spsrq48_socialapproval ~ "Social Approval, SPSRQ-48", spsrq48_sensoryreward ~ "Sensory Reward, SPSRQ-48"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", bis ~ "Behavioral Inhibition, BIS/BAS", bas ~ "Behavioral Approach, BIS/BAS", bas_funseeking ~ "Funseeking, BIS/BAS", bas_drive ~ "Drive, BIS/BAS", bas_rewardresp ~ "Reward Responsiveness, BIS/BAS", spsrq34_punishment ~ "Sensitivity to Punishment, SPSRQ-34", spsrq34_impfun ~ "Impulsivity/Fun Seeking, SPSRQ-34", spsrq34_drive ~ "Drive, SPSRQ-34", spsrq34_rewardresp ~ "Reward Responsiveness, SPSRQ-34", spsrq48_fearshy ~ "Fear/Shyness, SPSRQ-48", spsrq48_anxiety ~ "Anxiety, SPSRQ-48", spsrq48_conflictavoid ~ "Conflict Avoidence, SPSRQ-48", spsrq48_impfun ~ "Impulsivity/Fun Seeking, SPSRQ-48", spsrq48_drive ~ "Drive, SPSRQ-48", spsrq48_socialapproval ~ "Social Approval, SPSRQ-48", spsrq48_sensoryreward ~ "Sensory Reward, SPSRQ-48"),
    type = list(bas_rewardresp ~ 'continuous', spsrq48_conflictavoid ~ 'continuous', spsrq48_sensoryreward ~ 'continuous', bas_funseeking ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

qs_reward_merge_tab <-
  tbl_merge(
    tbls = list(reward_tab, reward_risk_mom_tab, reward_risk_both_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )

## 2d) BRIEF-2 ####

## all
brief_v1 <- r01_qs_cps[c(12, 10, 342, 345, 348, 351, 354, 357, 360, 363, 366, 369, 372, 375, 378, 382, 385, 388)]
brief_v1$all_na <- rowSums(is.na(brief_v1[c('brief2_bri_t', 'brief2_eri_t', 'brief2_cri_t', 'brief2_gec_t')]))
brief_v1 <- brief_v1[brief_v1$all_na < 4, ]

brief_v7 <- r01_qs_cps[c(12, 10, 454, 457, 460, 463, 466, 469, 472, 475, 478, 481, 484, 487, 490, 494, 497, 500)]
brief_v7$all_na <- rowSums(is.na(brief_v7[c('v7_brief2_bri_t', 'v7_brief2_eri_t', 'v7_brief2_cri_t', 'v7_brief2_gec_t')]))
brief_v7 <- brief_v7[brief_v7$all_na < 4, ]

brief_v1_tab <-
  tbl_summary(
    data = brief_v1[1:18],
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", brief2_inhibit_t ~ "Inhibition, T", brief2_selfmon_t ~ "Self-Monitoring, T", brief2_shift_t ~ "Shifting, T", brief2_emcont_t ~ "Emotional Control, T", brief2_initiate_t ~ "Initiate, T", brief2_wm_t ~ "Working Memory, T", brief2_planorg_t ~ "Planning and Organization, T", brief2_taskmon_t ~ "Task Monitoring, T", brief2_orgmat_t ~ "Organization of Materials, T", brief2_bri_t ~ "Behavioral Regulation Index, T", brief2_eri_t ~ "Emotional Regulation Index, T", brief2_cri_t ~ "Cogntive Regulation Index, T", brief2_gec_t ~ "General Executive Composite, T", brief2_negativity_cat ~ "Negativity Check", brief2_inconsistency_cat ~ "Inconsistency Check", brief2_infrequency_cat ~ "Infrequency Check"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", brief2_inhibit_t ~ "Inhibition, T", brief2_selfmon_t ~ "Self-Monitoring, T", brief2_shift_t ~ "Shifting, T", brief2_emcont_t ~ "Emotional Control, T", brief2_initiate_t ~ "Initiate, T", brief2_wm_t ~ "Working Memory, T", brief2_planorg_t ~ "Planning and Organization, T", brief2_taskmon_t ~ "Task Monitoring, T", brief2_orgmat_t ~ "Organization of Materials, T", brief2_bri_t ~ "Behavioral Regulation Index, T", brief2_eri_t ~ "Emotional Regulation Index, T", brief2_cri_t ~ "Cogntive Regulation Index, T", brief2_gec_t ~ "General Executive Composite, T", brief2_negativity_cat ~ "Negativity Check", brief2_inconsistency_cat ~ "Inconsistency Check", brief2_infrequency_cat ~ "Infrequency Check"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

brief_v7_tab <-
  tbl_summary(
    data = brief_v7[1:18],
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_brief2_inhibit_t ~ "Inhibition, T", v7_brief2_selfmon_t ~ "Self-Monitoring, T", v7_brief2_shift_t ~ "Shifting, T", v7_brief2_emcont_t ~ "Emotional Control, T", v7_brief2_initiate_t ~ "Initiate, T", v7_brief2_wm_t ~ "Working Memory, T", v7_brief2_planorg_t ~ "Planning and Organization, T", v7_brief2_taskmon_t ~ "Task Monitoring, T", v7_brief2_orgmat_t ~ "Organization of Materials, T", v7_brief2_bri_t ~ "Behavioral Regulation Index, T", v7_brief2_eri_t ~ "Emotional Regulation Index, T", v7_brief2_cri_t ~ "Cogntive Regulation Index, T", v7_brief2_gec_t ~ "General Executive Composite, T", v7_brief2_negativity_cat ~ "Negativity Check", v7_brief2_inconsistency_cat ~ "Inconsistency Check", v7_brief2_infrequency_cat ~ "Infrequency Check"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_brief2_inhibit_t ~ "Inhibition, T", v7_brief2_selfmon_t ~ "Self-Monitoring, T", v7_brief2_shift_t ~ "Shifting, T", v7_brief2_emcont_t ~ "Emotional Control, T", v7_brief2_initiate_t ~ "Initiate, T", v7_brief2_wm_t ~ "Working Memory, T", v7_brief2_planorg_t ~ "Planning and Organization, T", v7_brief2_taskmon_t ~ "Task Monitoring, T", v7_brief2_orgmat_t ~ "Organization of Materials, T", v7_brief2_bri_t ~ "Behavioral Regulation Index, T", v7_brief2_eri_t ~ "Emotional Regulation Index, T", v7_brief2_cri_t ~ "Cogntive Regulation Index, T", v7_brief2_gec_t ~ "General Executive Composite, T", v7_brief2_negativity_cat ~ "Negativity Check", v7_brief2_inconsistency_cat ~ "Inconsistency Check", v7_brief2_infrequency_cat ~ "Infrequency Check"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# mom risk
brief_risk_mom_v1 <- r01_qs_cps[r01_qs_cps$risk_status_mom != 'Neither', c(8, 12, 10, 342, 345, 348, 351, 354, 357, 360, 363, 366, 369, 372, 375, 378, 382, 385, 388)]
brief_risk_mom_v1$risk_status_mom <- droplevels(brief_risk_mom_v1$risk_status_mom)

brief_risk_mom_v1$all_na <- rowSums(is.na(brief_risk_mom_v1[c('brief2_bri_t', 'brief2_eri_t', 'brief2_cri_t', 'brief2_gec_t')]))
brief_risk_mom_v1 <- brief_risk_mom_v1[brief_risk_mom_v1$all_na < 4, ]

brief_risk_mom_v7 <- r01_qs_cps[r01_qs_cps$risk_status_mom != 'Neither', c(8, 12, 10, 454, 457, 460, 463, 466, 469, 472, 475, 478, 481, 484, 487, 490, 494, 497, 500)]
brief_risk_mom_v7$risk_status_mom <- droplevels(brief_risk_mom_v7$risk_status_mom)

brief_risk_mom_v7$all_na <- rowSums(is.na(brief_risk_mom_v7[c('v7_brief2_bri_t', 'v7_brief2_eri_t', 'v7_brief2_cri_t', 'v7_brief2_gec_t')]))
brief_risk_mom_v7 <- brief_risk_mom_v7[brief_risk_mom_v7$all_na < 4, ]

brief_risk_mom_v1_tab <-
  tbl_summary(
    data = brief_risk_mom_v1[1:19],
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", brief2_inhibit_t ~ "Inhibition, T", brief2_selfmon_t ~ "Self-Monitoring, T", brief2_shift_t ~ "Shifting, T", brief2_emcont_t ~ "Emotional Control, T", brief2_initiate_t ~ "Initiate, T", brief2_wm_t ~ "Working Memory, T", brief2_planorg_t ~ "Planning and Organization, T", brief2_taskmon_t ~ "Task Monitoring, T", brief2_orgmat_t ~ "Organization of Materials, T", brief2_bri_t ~ "Behavioral Regulation Index, T", brief2_eri_t ~ "Emotional Regulation Index, T", brief2_cri_t ~ "Cogntive Regulation Index, T", brief2_gec_t ~ "General Executive Composite, T", brief2_negativity_cat ~ "Negativity Check", brief2_inconsistency_cat ~ "Inconsistency Check", brief2_infrequency_cat ~ "Infrequency Check"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", brief2_inhibit_t ~ "Inhibition, T", brief2_selfmon_t ~ "Self-Monitoring, T", brief2_shift_t ~ "Shifting, T", brief2_emcont_t ~ "Emotional Control, T", brief2_initiate_t ~ "Initiate, T", brief2_wm_t ~ "Working Memory, T", brief2_planorg_t ~ "Planning and Organization, T", brief2_taskmon_t ~ "Task Monitoring, T", brief2_orgmat_t ~ "Organization of Materials, T", brief2_bri_t ~ "Behavioral Regulation Index, T", brief2_eri_t ~ "Emotional Regulation Index, T", brief2_cri_t ~ "Cogntive Regulation Index, T", brief2_gec_t ~ "General Executive Composite, T", brief2_negativity_cat ~ "Negativity Check", brief2_inconsistency_cat ~ "Inconsistency Check", brief2_infrequency_cat ~ "Infrequency Check"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

brief_risk_mom_v7_tab <-
  tbl_summary(
    data = brief_risk_mom_v7[1:19],
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_brief2_inhibit_t ~ "Inhibition, T", v7_brief2_selfmon_t ~ "Self-Monitoring, T", v7_brief2_shift_t ~ "Shifting, T", v7_brief2_emcont_t ~ "Emotional Control, T", v7_brief2_initiate_t ~ "Initiate, T", v7_brief2_wm_t ~ "Working Memory, T", v7_brief2_planorg_t ~ "Planning and Organization, T", v7_brief2_taskmon_t ~ "Task Monitoring, T", v7_brief2_orgmat_t ~ "Organization of Materials, T", v7_brief2_bri_t ~ "Behavioral Regulation Index, T", v7_brief2_eri_t ~ "Emotional Regulation Index, T", v7_brief2_cri_t ~ "Cogntive Regulation Index, T", v7_brief2_gec_t ~ "General Executive Composite, T", v7_brief2_negativity_cat ~ "Negativity Check", v7_brief2_inconsistency_cat ~ "Inconsistency Check", v7_brief2_infrequency_cat ~ "Infrequency Check"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_brief2_inhibit_t ~ "Inhibition, T", v7_brief2_selfmon_t ~ "Self-Monitoring, T", v7_brief2_shift_t ~ "Shifting, T", v7_brief2_emcont_t ~ "Emotional Control, T", v7_brief2_initiate_t ~ "Initiate, T", v7_brief2_wm_t ~ "Working Memory, T", v7_brief2_planorg_t ~ "Planning and Organization, T", v7_brief2_taskmon_t ~ "Task Monitoring, T", v7_brief2_orgmat_t ~ "Organization of Materials, T", v7_brief2_bri_t ~ "Behavioral Regulation Index, T", v7_brief2_eri_t ~ "Emotional Regulation Index, T", v7_brief2_cri_t ~ "Cogntive Regulation Index, T", v7_brief2_gec_t ~ "General Executive Composite, T", v7_brief2_negativity_cat ~ "Negativity Check", v7_brief2_inconsistency_cat ~ "Inconsistency Check", v7_brief2_infrequency_cat ~ "Infrequency Check"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# strict/both risk
brief_risk_both_v1 <- r01_qs_cps[r01_qs_cps$risk_status_both != 'Neither', c(9, 12, 10, 342, 345, 348, 351, 354, 357, 360, 363, 366, 369, 372, 375, 378, 382, 385, 388)]
brief_risk_both_v1$risk_status_both <- droplevels(brief_risk_both_v1$risk_status_both)

brief_risk_both_v1$all_na <- rowSums(is.na(brief_risk_both_v1[c('brief2_bri_t', 'brief2_eri_t', 'brief2_cri_t', 'brief2_gec_t')]))
brief_risk_both_v1 <- brief_risk_both_v1[brief_risk_both_v1$all_na < 4, ]

brief_risk_both_v7 <- r01_qs_cps[r01_qs_cps$risk_status_both != 'Neither', c(9, 12, 10, 454, 457, 460, 463, 466, 469, 472, 475, 478, 481, 484, 487, 490, 494, 497, 500)]
brief_risk_both_v7$risk_status_both <- droplevels(brief_risk_both_v7$risk_status_both)

brief_risk_both_v7$all_na <- rowSums(is.na(brief_risk_both_v7[c('v7_brief2_bri_t', 'v7_brief2_eri_t', 'v7_brief2_cri_t', 'v7_brief2_gec_t')]))
brief_risk_both_v7 <- brief_risk_both_v7[brief_risk_both_v7$all_na < 4, ]

brief_risk_both_v1_tab <-
  tbl_summary(
    data = brief_risk_both_v1[1:19],
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", brief2_inhibit_t ~ "Inhibition, T", brief2_selfmon_t ~ "Self-Monitoring, T", brief2_shift_t ~ "Shifting, T", brief2_emcont_t ~ "Emotional Control, T", brief2_initiate_t ~ "Initiate, T", brief2_wm_t ~ "Working Memory, T", brief2_planorg_t ~ "Planning and Organization, T", brief2_taskmon_t ~ "Task Monitoring, T", brief2_orgmat_t ~ "Organization of Materials, T", brief2_bri_t ~ "Behavioral Regulation Index, T", brief2_eri_t ~ "Emotional Regulation Index, T", brief2_cri_t ~ "Cogntive Regulation Index, T", brief2_gec_t ~ "General Executive Composite, T", brief2_negativity_cat ~ "Negativity Check", brief2_inconsistency_cat ~ "Inconsistency Check", brief2_infrequency_cat ~ "Infrequency Check"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", brief2_inhibit_t ~ "Inhibition, T", brief2_selfmon_t ~ "Self-Monitoring, T", brief2_shift_t ~ "Shifting, T", brief2_emcont_t ~ "Emotional Control, T", brief2_initiate_t ~ "Initiate, T", brief2_wm_t ~ "Working Memory, T", brief2_planorg_t ~ "Planning and Organization, T", brief2_taskmon_t ~ "Task Monitoring, T", brief2_orgmat_t ~ "Organization of Materials, T", brief2_bri_t ~ "Behavioral Regulation Index, T", brief2_eri_t ~ "Emotional Regulation Index, T", brief2_cri_t ~ "Cogntive Regulation Index, T", brief2_gec_t ~ "General Executive Composite, T", brief2_negativity_cat ~ "Negativity Check", brief2_inconsistency_cat ~ "Inconsistency Check", brief2_infrequency_cat ~ "Infrequency Check"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

brief_risk_both_v7_tab <-
  tbl_summary(
    data = brief_risk_both_v7[1:19],
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_brief2_inhibit_t ~ "Inhibition, T", v7_brief2_selfmon_t ~ "Self-Monitoring, T", v7_brief2_shift_t ~ "Shifting, T", v7_brief2_emcont_t ~ "Emotional Control, T", v7_brief2_initiate_t ~ "Initiate, T", v7_brief2_wm_t ~ "Working Memory, T", v7_brief2_planorg_t ~ "Planning and Organization, T", v7_brief2_taskmon_t ~ "Task Monitoring, T", v7_brief2_orgmat_t ~ "Organization of Materials, T", v7_brief2_bri_t ~ "Behavioral Regulation Index, T", v7_brief2_eri_t ~ "Emotional Regulation Index, T", v7_brief2_cri_t ~ "Cogntive Regulation Index, T", v7_brief2_gec_t ~ "General Executive Composite, T", v7_brief2_negativity_cat ~ "Negativity Check", v7_brief2_inconsistency_cat ~ "Inconsistency Check", v7_brief2_infrequency_cat ~ "Infrequency Check"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_brief2_inhibit_t ~ "Inhibition, T", v7_brief2_selfmon_t ~ "Self-Monitoring, T", v7_brief2_shift_t ~ "Shifting, T", v7_brief2_emcont_t ~ "Emotional Control, T", v7_brief2_initiate_t ~ "Initiate, T", v7_brief2_wm_t ~ "Working Memory, T", v7_brief2_planorg_t ~ "Planning and Organization, T", v7_brief2_taskmon_t ~ "Task Monitoring, T", v7_brief2_orgmat_t ~ "Organization of Materials, T", v7_brief2_bri_t ~ "Behavioral Regulation Index, T", v7_brief2_eri_t ~ "Emotional Regulation Index, T", v7_brief2_cri_t ~ "Cogntive Regulation Index, T", v7_brief2_gec_t ~ "General Executive Composite, T", v7_brief2_negativity_cat ~ "Negativity Check", v7_brief2_inconsistency_cat ~ "Inconsistency Check", v7_brief2_infrequency_cat ~ "Infrequency Check"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

qs_brief_merge_v1_tab <-
  tbl_merge(
    tbls = list(brief_v1_tab, brief_risk_mom_v1_tab, brief_risk_both_v1_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )

qs_brief_merge_v7_tab <-
  tbl_merge(
    tbls = list(brief_v7_tab, brief_risk_mom_v7_tab, brief_risk_both_v7_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )
