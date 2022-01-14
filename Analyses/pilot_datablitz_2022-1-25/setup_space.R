# This script was written by Alaina Pearce in January 2022
# to set up N-Back tables by risk status for the Food and Brain Study
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
#
# library(haven)
# library(gtsummary)
# theme_gtsummary_compact()
#
# source('functions.R')

# source('setup_demo.R')

#### set up ####

## 1) Load Data ####

source('setup_space_dm.R')

r01_space <- read.csv("data_2022-01-25/task-space_summary.tsv", header = TRUE, sep = "\t")

#merge - demo
r01_space <- merge(r01_demo[c(1:16, 337:338, 19:24)], r01_space, by = 'sub', all.x = FALSE, all.y = TRUE)

#merge - decision making model
r01_space <- merge(r01_space, r01_space_dm_best, by = c('sub', 'ses'), all = TRUE)

#remove 2 that were removed for ADHD
r01_space = r01_space[r01_space$sub != 31 & r01_space$sub != 34, ]

## 2) Tables ####

## 2a) All Table ####
space_all_ses1 <- r01_space[r01_space$ses == 1, c(11, 13, 26, 29:30, 33:38, 93:98)]
space_all_ses2 <- r01_space[r01_space$ses == 2, c(11, 13, 26, 29:30, 33:38, 93:98)]

#fix names
space_all_tab_ses1 <-
  tbl_summary(
    data=space_all_ses1,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", all_earth_rt_mean ~ "Earth  Mean RT, ms", all_earth_p_miss ~ "Earth  Missed, %", all_planet_rt_mean ~ "Planet  Mean RT, ms", all_planet_p_miss ~ "Planet (Stage w) Missed, %", all_reward_rate ~ "Reward Rate", all_avg_reward ~ "Average Reward", all_reward_rate_corrected ~ "Corrected Reward Rate", all_prob_sameplanet_earthsame ~ "P (stay | same earth)", all_prob_sameplanet_earthdif ~ "P (stay | different earth", beta ~ "Inverse Temp", alpha ~ "Learning Rate", lambda ~ "Decay Rate", w ~ "Weighting Parameter", pi ~ "Choice 'Stickiness'", rho ~ "Response/Motor 'Stickiness'"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", all_earth_rt_mean ~ "Earth  Mean RT, ms", all_earth_p_miss ~ "Earth  Missed, %", all_planet_rt_mean ~ "Planet  Mean RT, ms", all_planet_p_miss ~ "Planet (Stage w) Missed, %", all_reward_rate ~ "Reward Rate", all_avg_reward ~ "Average Reward", all_reward_rate_corrected ~ "Corrected Reward Rate", all_prob_sameplanet_earthsame ~ "P (stay | same earth)", all_prob_sameplanet_earthdif ~ "P (stay | different earth", beta ~ "Inverse Temp", alpha ~ "Learning Rate", lambda ~ "Decay Rate", w ~ "Weighting Parameter", pi ~ "Choice 'Stickiness'", rho ~ "Response/Motor 'Stickiness'"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

space_all_tab_ses2 <-
  tbl_summary(
    data=space_all_ses2,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", all_earth_rt_mean ~ "Earth  Mean RT, ms", all_earth_p_miss ~ "Earth  Missed, %", all_planet_rt_mean ~ "Planet  Mean RT, ms", all_planet_p_miss ~ "Planet (Stage w) Missed, %", all_reward_rate ~ "Reward Rate", all_avg_reward ~ "Average Reward", all_reward_rate_corrected ~ "Corrected Reward Rate", all_prob_sameplanet_earthsame ~ "P (stay | same earth)", all_prob_sameplanet_earthdif ~ "P (stay | different earth", beta ~ "Inverse Temp", alpha ~ "Learning Rate", lambda ~ "Decay Rate", w ~ "Weighting Parameter", pi ~ "Choice 'Stickiness'", rho ~ "Response/Motor 'Stickiness'"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", all_earth_rt_mean ~ "Earth  Mean RT, ms", all_earth_p_miss ~ "Earth  Missed, %", all_planet_rt_mean ~ "Planet  Mean RT, ms", all_planet_p_miss ~ "Planet (Stage w) Missed, %", all_reward_rate ~ "Reward Rate", all_avg_reward ~ "Average Reward", all_reward_rate_corrected ~ "Corrected Reward Rate", all_prob_sameplanet_earthsame ~ "P (stay | same earth)", all_prob_sameplanet_earthdif ~ "P (stay | different earth", beta ~ "Inverse Temp", alpha ~ "Learning Rate", lambda ~ "Decay Rate", w ~ "Weighting Parameter", pi ~ "Choice 'Stickiness'", rho ~ "Response/Motor 'Stickiness'"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

## 2b) Mom Risk Status Table ####
space_risk_mom_ses1 <- r01_space[r01_space$ses == 1 & r01_space$risk_status_mom != 'Neither', c(9, 11, 13, 26, 29:30, 33:38, 93:98)]
space_risk_mom_ses1$risk_status_mom <- droplevels(space_risk_mom_ses1$risk_status_mom)

space_risk_mom_ses2 <- r01_space[r01_space$ses == 2 & r01_space$risk_status_mom != 'Neither', c(9, 11, 13, 26, 29:30, 33:38, 93:98)]
space_risk_mom_ses2$risk_status_mom <- droplevels(space_risk_mom_ses2$risk_status_mom)

space_risk_mom_tab_ses1 <-
  tbl_summary(
    data=space_risk_mom_ses1,
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", all_earth_rt_mean ~ "Earth  Mean RT, ms", all_earth_p_miss ~ "Earth  Missed, %", all_planet_rt_mean ~ "Planet  Mean RT, ms", all_planet_p_miss ~ "Planet (Stage w) Missed, %", all_reward_rate ~ "Reward Rate", all_avg_reward ~ "Average Reward", all_reward_rate_corrected ~ "Corrected Reward Rate", all_prob_sameplanet_earthsame ~ "P (stay | same earth)", all_prob_sameplanet_earthdif ~ "P (stay | different earth", beta ~ "Inverse Temp", alpha ~ "Learning Rate", lambda ~ "Decay Rate", w ~ "Weighting Parameter", pi ~ "Choice 'Stickiness'", rho ~ "Response/Motor 'Stickiness'"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", all_earth_rt_mean ~ "Earth  Mean RT, ms", all_earth_p_miss ~ "Earth  Missed, %", all_planet_rt_mean ~ "Planet  Mean RT, ms", all_planet_p_miss ~ "Planet (Stage w) Missed, %", all_reward_rate ~ "Reward Rate", all_avg_reward ~ "Average Reward", all_reward_rate_corrected ~ "Corrected Reward Rate", all_prob_sameplanet_earthsame ~ "P (stay | same earth)", all_prob_sameplanet_earthdif ~ "P (stay | different earth", beta ~ "Inverse Temp", alpha ~ "Learning Rate", lambda ~ "Decay Rate", w ~ "Weighting Parameter", pi ~ "Choice 'Stickiness'", rho ~ "Response/Motor 'Stickiness'"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

space_risk_mom_tab_ses2 <-
  tbl_summary(
    data=space_risk_mom_ses2,
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", all_earth_rt_mean ~ "Earth  Mean RT, ms", all_earth_p_miss ~ "Earth  Missed, %", all_planet_rt_mean ~ "Planet  Mean RT, ms", all_planet_p_miss ~ "Planet (Stage w) Missed, %", all_reward_rate ~ "Reward Rate", all_avg_reward ~ "Average Reward", all_reward_rate_corrected ~ "Corrected Reward Rate", all_prob_sameplanet_earthsame ~ "P (stay | same earth)", all_prob_sameplanet_earthdif ~ "P (stay | different earth", beta ~ "Inverse Temp", alpha ~ "Learning Rate", lambda ~ "Decay Rate", w ~ "Weighting Parameter", pi ~ "Choice 'Stickiness'", rho ~ "Response/Motor 'Stickiness'"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", all_earth_rt_mean ~ "Earth  Mean RT, ms", all_earth_p_miss ~ "Earth  Missed, %", all_planet_rt_mean ~ "Planet  Mean RT, ms", all_planet_p_miss ~ "Planet (Stage w) Missed, %", all_reward_rate ~ "Reward Rate", all_avg_reward ~ "Average Reward", all_reward_rate_corrected ~ "Corrected Reward Rate", all_prob_sameplanet_earthsame ~ "P (stay | same earth)", all_prob_sameplanet_earthdif ~ "P (stay | different earth", beta ~ "Inverse Temp", alpha ~ "Learning Rate", lambda ~ "Decay Rate", w ~ "Weighting Parameter", pi ~ "Choice 'Stickiness'", rho ~ "Response/Motor 'Stickiness'"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

## 2c) Strict Risk Table ####
space_risk_both_ses1 <- r01_space[r01_space$ses == 1 & r01_space$risk_status_both != 'Neither', c(10, 11, 13, 26, 29:30, 33:38, 93:98)]
space_risk_both_ses1$risk_status_both <- droplevels(space_risk_both_ses1$risk_status_both)

space_risk_both_ses2 <- r01_space[r01_space$ses == 2 & r01_space$risk_status_both != 'Neither', c(10, 11, 13, 26, 29:30, 33:38, 93:98)]
space_risk_both_ses2$risk_status_both <- droplevels(space_risk_both_ses2$risk_status_both)

space_risk_both_tab_ses1 <-
  tbl_summary(
    data=space_risk_both_ses1,
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", all_earth_rt_mean ~ "Earth  Mean RT, ms", all_earth_p_miss ~ "Earth  Missed, %", all_planet_rt_mean ~ "Planet  Mean RT, ms", all_planet_p_miss ~ "Planet (Stage w) Missed, %", all_reward_rate ~ "Reward Rate", all_avg_reward ~ "Average Reward", all_reward_rate_corrected ~ "Corrected Reward Rate", all_prob_sameplanet_earthsame ~ "P (stay | same earth)", all_prob_sameplanet_earthdif ~ "P (stay | different earth", beta ~ "Inverse Temp", alpha ~ "Learning Rate", lambda ~ "Decay Rate", w ~ "Weighting Parameter", pi ~ "Choice 'Stickiness'", rho ~ "Response/Motor 'Stickiness'"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", all_earth_rt_mean ~ "Earth  Mean RT, ms", all_earth_p_miss ~ "Earth  Missed, %", all_planet_rt_mean ~ "Planet  Mean RT, ms", all_planet_p_miss ~ "Planet (Stage w) Missed, %", all_reward_rate ~ "Reward Rate", all_avg_reward ~ "Average Reward", all_reward_rate_corrected ~ "Corrected Reward Rate", all_prob_sameplanet_earthsame ~ "P (stay | same earth)", all_prob_sameplanet_earthdif ~ "P (stay | different earth", beta ~ "Inverse Temp", alpha ~ "Learning Rate", lambda ~ "Decay Rate", w ~ "Weighting Parameter", pi ~ "Choice 'Stickiness'", rho ~ "Response/Motor 'Stickiness'"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

space_risk_both_tab_ses2 <-
  tbl_summary(
    data=space_risk_both_ses2,
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", all_earth_rt_mean ~ "Earth  Mean RT, ms", all_earth_p_miss ~ "Earth  Missed, %", all_planet_rt_mean ~ "Planet  Mean RT, ms", all_planet_p_miss ~ "Planet (Stage w) Missed, %", all_reward_rate ~ "Reward Rate", all_avg_reward ~ "Average Reward", all_reward_rate_corrected ~ "Corrected Reward Rate", all_prob_sameplanet_earthsame ~ "P (stay | same earth)", all_prob_sameplanet_earthdif ~ "P (stay | different earth", beta ~ "Inverse Temp", alpha ~ "Learning Rate", lambda ~ "Decay Rate", w ~ "Weighting Parameter", pi ~ "Choice 'Stickiness'", rho ~ "Response/Motor 'Stickiness'"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", all_earth_rt_mean ~ "Earth  Mean RT, ms", all_earth_p_miss ~ "Earth  Missed, %", all_planet_rt_mean ~ "Planet  Mean RT, ms", all_planet_p_miss ~ "Planet (Stage w) Missed, %", all_reward_rate ~ "Reward Rate", all_avg_reward ~ "Average Reward", all_reward_rate_corrected ~ "Corrected Reward Rate", all_prob_sameplanet_earthsame ~ "P (stay | same earth)", all_prob_sameplanet_earthdif ~ "P (stay | different earth", beta ~ "Inverse Temp", alpha ~ "Learning Rate", lambda ~ "Decay Rate", w ~ "Weighting Parameter", pi ~ "Choice 'Stickiness'", rho ~ "Response/Motor 'Stickiness'"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

## 2d) Merge Tables ####

space_merge_tab_v1 <-
  tbl_merge(
    tbls = list(space_all_tab_ses1, space_risk_mom_tab_ses1, space_risk_both_tab_ses1),
    tab_spanner = c("**All**", "**Baseline**", "**Follow-Up**")
  )

space_merge_tab_v7 <-
  tbl_merge(
    tbls = list(space_all_tab_ses2, space_risk_mom_tab_ses2, space_risk_both_tab_ses2),
    tab_spanner = c("**All**", "**Baseline**", "**Follow-Up**")
  )
