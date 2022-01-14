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
r01_nback <- read.csv("data_2022-01-25/task-nback_summary_long.tsv", header = TRUE, sep = "\t")

#merge
r01_nback <- merge(r01_demo[c(1:16, 337:338, 19:24)], r01_nback, by = 'sub', all.x = FALSE, all.y = TRUE)

#remove 2 that were removed for ADHD
r01_nback = r01_nback[r01_nback$sub != 31 & r01_nback$sub != 34, ]

#re-name blocks
r01_nback$block <- ifelse(r01_nback$block == 'b0', '0-Back', ifelse(r01_nback$block == 'b1', '1-Back', '2-Back'))

## 2) Tables ####

## 2a) All Table ####
#change proportion to percent
nback_all_ses1 <- r01_nback[r01_nback$ses == 1, c(26, 10, 12, 33, 39:42)]
nback_all_ses2 <- r01_nback[r01_nback$ses == 2, c(26, 10, 12, 33, 39:42)]

#fix names
nback_all_tab_ses1 <-
  tbl_summary(
    data=nback_all_ses1,
    by = block,
    value = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits, mean RT", rt_med_target_hit ~ "Hits, median RT"),
    label = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits Mean RT, ms", rt_med_target_hit ~ "Hits Median RT, ms"),
    type = list(p_fill_fa ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 0)

nback_all_tab_ses2 <-
  tbl_summary(
    data=nback_all_ses2,
    by = block,
    value = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits, mean RT", rt_med_target_hit ~ "Hits, median RT"),
    label = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits Mean RT, ms", rt_med_target_hit ~ "Hits Median RT, ms"),
    type = list(p_fill_fa ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 0)

## 2b) Mom Risk Status Table ####
nback_all_momLR_ses1 <- r01_nback[r01_nback$ses == 1 & r01_nback$risk_status_mom == 'Low Risk', c(26, 10, 12, 33, 39:42)]
nback_all_momLR_ses2 <- r01_nback[r01_nback$ses == 2 & r01_nback$risk_status_mom == 'Low Risk', c(26, 10, 12, 33, 39:42)]

nback_all_momHR_ses1 <- r01_nback[r01_nback$ses == 1 & r01_nback$risk_status_mom == 'High Risk', c(26, 10, 12, 33, 39:42)]
nback_all_momHR_ses2 <- r01_nback[r01_nback$ses == 2 & r01_nback$risk_status_mom == 'High Risk', c(26, 10, 12, 33, 39:42)]

nback_momLR_tab_ses1 <-
  tbl_summary(
    data=nback_all_momLR_ses1,
    by = block,
    value = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits, mean RT", rt_med_target_hit ~ "Hits, median RT"),
    label = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits Mean RT, ms", rt_med_target_hit ~ "Hits Median RT, ms"),
    type = list(p_target_hit ~ 'continuous', p_fill_fa ~ 'continuous', p_target_ba ~ "continuous", rt_mean_target_hit ~ "continuous", rt_med_target_hit ~ "continuous"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 0)

nback_momLR_tab_ses2 <-
  tbl_summary(
    data=nback_all_momLR_ses2,
    by = block,
    value = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits, mean RT", rt_med_target_hit ~ "Hits, median RT"),
    label = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits Mean RT, ms", rt_med_target_hit ~ "Hits Median RT, ms"),
    type = list(p_target_hit ~ 'continuous', p_fill_fa ~ 'continuous', p_target_ba ~ "continuous", rt_mean_target_hit ~ "continuous", rt_med_target_hit ~ "continuous"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 0)

nback_momHR_tab_ses1 <-
  tbl_summary(
    data=nback_all_momHR_ses1,
    by = block,
    value = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits, mean RT", rt_med_target_hit ~ "Hits, median RT"),
    label = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits Mean RT, ms", rt_med_target_hit ~ "Hits Median RT, ms"),
    type = list(p_target_hit ~ 'continuous', p_fill_fa ~ 'continuous', p_target_ba ~ "continuous", rt_mean_target_hit ~ "continuous", rt_med_target_hit ~ "continuous"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 0)

nback_momHR_tab_ses2 <-
  tbl_summary(
    data=nback_all_momHR_ses2,
    by = block,
    value = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits, mean RT", rt_med_target_hit ~ "Hits, median RT"),
    label = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits Mean RT, ms", rt_med_target_hit ~ "Hits Median RT, ms"),
    type = list(p_target_hit ~ 'continuous', p_fill_fa ~ 'continuous', p_target_ba ~ "continuous", rt_mean_target_hit ~ "continuous", rt_med_target_hit ~ "continuous"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 0)

nback_momrisk_merge_tab_ses1 <-
  tbl_merge(
    tbls = list(nback_momLR_tab_ses1, nback_momHR_tab_ses1),
    tab_spanner = c("**Low Risk**", "**High Risk**")
  )

nback_momrisk_merge_tab_ses2 <-
  tbl_merge(
    tbls = list(nback_momLR_tab_ses2, nback_momHR_tab_ses2),
    tab_spanner = c("**Low Risk**", "**High Risk**")
  )

## 2c) Strict Risk Table ####
nback_all_bothLR_ses1 <- r01_nback[r01_nback$ses == 1 & r01_nback$risk_status_both == 'Low Risk', c(26, 10, 12, 33, 39:42)]
nback_all_bothLR_ses2 <- r01_nback[r01_nback$ses == 2 & r01_nback$risk_status_both == 'Low Risk', c(26, 10, 12, 33, 39:42)]

nback_all_bothHR_ses1 <- r01_nback[r01_nback$ses == 1 & r01_nback$risk_status_both == 'High Risk', c(26, 10, 12, 33, 39:42)]
nback_all_bothHR_ses2 <- r01_nback[r01_nback$ses == 2 & r01_nback$risk_status_both == 'High Risk', c(26, 10, 12, 33, 39:42)]

#fix names
nback_bothLR_tab_ses1 <-
  tbl_summary(
    data=nback_all_bothLR_ses1,
    by = block,
    value = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits, mean RT", rt_med_target_hit ~ "Hits, median RT"),
    label = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits Mean RT, ms", rt_med_target_hit ~ "Hits Median RT, ms"),
    type = list(p_target_hit ~ 'continuous', p_fill_fa ~ 'continuous', p_target_ba ~ "continuous", rt_mean_target_hit ~ "continuous", rt_med_target_hit ~ "continuous"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 0)

nback_bothLR_tab_ses2 <-
  tbl_summary(
    data=nback_all_bothLR_ses2,
    by = block,
    value = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits, mean RT", rt_med_target_hit ~ "Hits, median RT"),
    label = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits Mean RT, ms", rt_med_target_hit ~ "Hits Median RT, ms"),
    type = list(p_target_hit ~ 'continuous', p_fill_fa ~ 'continuous', p_target_ba ~ "continuous", rt_mean_target_hit ~ "continuous", rt_med_target_hit ~ "continuous"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 0)

nback_bothHR_tab_ses1 <-
  tbl_summary(
    data=nback_all_bothHR_ses1,
    by = block,
    value = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits, mean RT", rt_med_target_hit ~ "Hits, median RT"),
    label = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits Mean RT, ms", rt_med_target_hit ~ "Hits Median RT, ms"),
    type = list(p_target_hit ~ 'continuous', p_fill_fa ~ 'continuous', p_target_ba ~ "continuous", rt_mean_target_hit ~ "continuous", rt_med_target_hit ~ "continuous"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 0)

nback_bothHR_tab_ses2 <-
  tbl_summary(
    data=nback_all_bothHR_ses2,
    by = block,
    value = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits, mean RT", rt_med_target_hit ~ "Hits, median RT"),
    label = list(p_target_hit ~ "Hits, %", p_fill_fa ~ "False Alarms, %", p_target_ba ~ "Ballanced Acc, %", rt_mean_target_hit ~ "Hits Mean RT, ms", rt_med_target_hit ~ "Hits Median RT, ms"),
    type = list(p_target_hit ~ 'continuous', p_fill_fa ~ 'continuous', p_target_ba ~ "continuous", rt_mean_target_hit ~ "continuous", rt_med_target_hit ~ "continuous"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 0)

nback_bothrisk_merge_tab_ses1 <-
  tbl_merge(
    tbls = list(nback_bothLR_tab_ses1, nback_bothHR_tab_ses1),
    tab_spanner = c("**Low Risk**", "**High Risk**")
  )

nback_bothrisk_merge_tab_ses2 <-
  tbl_merge(
    tbls = list(nback_bothLR_tab_ses2, nback_bothHR_tab_ses2),
    tab_spanner = c("**Low Risk**", "**High Risk**")
  )


## 2d) Merge Tables ####

nback_merge_tab <-
  tbl_merge(
    tbls = list(nback_all_tab_ses1, nback_all_tab_ses2),
    tab_spanner = c("**Baseline**", "**Follow-Up**")
  )

nback_momrisk_merge_tab <-
  tbl_stack(list(nback_momrisk_merge_tab_ses1, nback_momrisk_merge_tab_ses2), group_header = c("Baseline", "Follow-Up"), quiet = TRUE)

nback_bothrisk_merge_tab <-
  tbl_stack(list(nback_bothrisk_merge_tab_ses1, nback_bothrisk_merge_tab_ses2), group_header = c("Baseline", "Follow-Up"), quiet = TRUE)
