# This script was written by Alaina Pearce in January 2022
# to set up Go-NoGo tables by risk status for the Food and Brain Study
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

r01_gng <- read.csv("data_2022-01-25/task-gng_summary.tsv", header = TRUE, sep = "\t")

#merge
r01_gng <- merge(r01_demo[c(1:16, 337:338, 19:24)], r01_gng[1:31], by = 'sub', all.x = FALSE, all.y = TRUE)

#remove 2 that were removed for ADHD
r01_gng = r01_gng[r01_gng$sub != 31 & r01_gng$sub != 34, ]

#remove 51 - task not administered correctly (only responded on NoGo)
r01_gng = r01_gng[r01_gng$sub != 51, ]

## 2) Tables ####

## 2a) All Table ####
#change proportion to percent
r01_gng[33:36] <- r01_gng[33:36]*100

#add ballanced accuracy
r01_gng$all_bal_acc <- (r01_gng$all_pGo_Hit + r01_gng$all_pNoGo_Corr)/2

gng_all <- r01_gng[r01_gng$all_pGo_Hit >= 50, c(10, 33, 37, 39, 36, 38, 40, 55)]

#fix names
gng_all_tab <-
  tbl_summary(
    data=gng_all,
    value = list(all_pGo_Hit ~ "Hits, %", all_RTmeanGo_Hit ~ "Hits, mean RT", all_RTmedGo_Hit ~ "Hits, median RT", all_pNoGo_FA ~ "False Alarm, %", all_RTmeanNoGo_FA ~ "False Alarm, mean RT", all_RTmedNoGo_FA ~ "False Alarms, median RT", all_bal_acc ~ 'Ballanced Acc, %'),
    label = list(all_pGo_Hit ~ "Hits, %", all_RTmeanGo_Hit ~ "Hits, mean RT", all_RTmedGo_Hit ~ "Hits, median RT", all_pNoGo_FA ~ "False Alarm, %", all_RTmeanNoGo_FA ~ "False Alarm, mean RT", all_RTmedNoGo_FA ~ "False Alarms, median RT", all_bal_acc ~ 'Ballanced Acc, %'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 0)

## 2b) Mom Risk Status Table ####
gng_risk_mom <- droplevels(r01_gng[r01_gng$all_pGo_Hit >= 50, c(8, 10, 33, 37, 39, 36, 38, 40, 55)])

#fix names
gng_risk_mom_tab <-
  tbl_summary(
    data=gng_risk_mom,
    by = risk_status_mom,
    value = list(all_pGo_Hit ~ "Hits, %", all_RTmeanGo_Hit ~ "Hits, mean RT", all_RTmedGo_Hit ~ "Hits, median RT", all_pNoGo_FA ~ "False Alarm, %", all_RTmeanNoGo_FA ~ "False Alarm, mean RT", all_RTmedNoGo_FA ~ "False Alarms, median RT", all_bal_acc ~ 'Ballanced Acc, %'),
    label = list(all_pGo_Hit ~ "Hits, %", all_RTmeanGo_Hit ~ "Hits, mean RT", all_RTmedGo_Hit ~ "Hits, median RT", all_pNoGo_FA ~ "False Alarm, %", all_RTmeanNoGo_FA ~ "False Alarm, mean RT", all_RTmedNoGo_FA ~ "False Alarms, median RT", all_bal_acc ~ 'Ballanced Acc, %'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 0)

# with t-test
# gng_risk_mom_tab <-
#   tbl_summary(
#     data=gng_risk_mom,
#     by = risk_status_mom,
#     value = list(all_pGo_Hit ~ "Hits, %", all_RTmeanGo_Hit ~ "Hits, mean RT", all_RTmedGo_Hit ~ "Hits, median RT", all_pNoGo_FA ~ "False Alarm, %", all_RTmeanNoGo_FA ~ "False Alarm, mean RT", all_RTmedNoGo_FA ~ "False Alarms, median RT", all_bal_acc ~ 'Ballanced Acc, %'),
#     label = list(all_pGo_Hit ~ "Hits, %", all_RTmeanGo_Hit ~ "Hits, mean RT", all_RTmedGo_Hit ~ "Hits, median RT", all_pNoGo_FA ~ "False Alarm, %", all_RTmeanNoGo_FA ~ "False Alarm, mean RT", all_RTmedNoGo_FA ~ "False Alarms, median RT", all_bal_acc ~ 'Ballanced Acc, %'),
#     statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
#     missing = "ifany",
#     digits = all_continuous() ~ 0) %>%
#   add_stat(fns = all_continuous() ~ my_ttest) %>%
#   modify_header(
#     list(
#       add_stat_1 ~ "**t-test, p**",
#       all_stat_cols() ~ "**{level}**"
#     )
#   )

## 2c) Strict Risk Table ####
gng_risk_both <- droplevels(r01_gng[r01_gng$all_pGo_Hit >= 50 & r01_gng$risk_status_both != 'Neither', c(9, 10, 33, 37, 39, 36, 38, 40, 55)])

#fix names
gng_risk_both_tab <-
  tbl_summary(
    data=gng_risk_both,
    by = risk_status_both,
    value = list(all_pGo_Hit ~ "Hits, %", all_RTmeanGo_Hit ~ "Hits, mean RT", all_RTmedGo_Hit ~ "Hits, median RT", all_pNoGo_FA ~ "False Alarm, %", all_RTmeanNoGo_FA ~ "False Alarm, mean RT", all_RTmedNoGo_FA ~ "False Alarms, median RT", all_bal_acc ~ 'Ballanced Acc, %'),
    label = list(all_pGo_Hit ~ "Hits, %", all_RTmeanGo_Hit ~ "Hits, mean RT", all_RTmedGo_Hit ~ "Hits, median RT", all_pNoGo_FA ~ "False Alarm, %", all_RTmeanNoGo_FA ~ "False Alarm, mean RT", all_RTmedNoGo_FA ~ "False Alarms, median RT", all_bal_acc ~ 'Ballanced Acc, %'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 0)

# with t-test
# gng_risk_both_tab <-
#   tbl_summary(
#     data=gng_risk_both,
#     by = risk_status_both,
#     value = list(all_pGo_Hit ~ "Hits, %", all_RTmeanGo_Hit ~ "Hits, mean RT", all_RTmedGo_Hit ~ "Hits, median RT", all_pNoGo_FA ~ "False Alarm, %", all_RTmeanNoGo_FA ~ "False Alarm, mean RT", all_RTmedNoGo_FA ~ "False Alarms, median RT", all_bal_acc ~ 'Ballanced Acc, %'),
#     label = list(all_pGo_Hit ~ "Hits, %", all_RTmeanGo_Hit ~ "Hits, mean RT", all_RTmedGo_Hit ~ "Hits, median RT", all_pNoGo_FA ~ "False Alarm, %", all_RTmeanNoGo_FA ~ "False Alarm, mean RT", all_RTmedNoGo_FA ~ "False Alarms, median RT", all_bal_acc ~ 'Ballanced Acc, %'),
#     statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
#     missing = "ifany",
#     digits = all_continuous() ~ 0) %>%
#   add_stat(fns = all_continuous() ~ my_ttest) %>%
#   modify_header(
#     list(
#       add_stat_1 ~ "**t-test, p**",
#       all_stat_cols() ~ "**{level}**"
#     )
#   )


## 2d) Merge Tables ####
gng_merge_tab <-
  tbl_merge(
    tbls = list(gng_all_tab, gng_risk_mom_tab, gng_risk_both_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )
