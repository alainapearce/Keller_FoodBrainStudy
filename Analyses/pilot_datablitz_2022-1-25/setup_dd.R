# This script was written by Alaina Pearce in January 2022
# to set up delay discounting tables by risk status for the Food and Brain Study
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
r01_dd <- as.data.frame(read_spss(("data_2022-01-25/delay_discounting.sav")))
names(r01_dd)[1] <- 'sub'

r01_dd_labels <- lapply(r01_dd, function(x) attributes(x)$label)

#remove 2 that were removed for ADHD
r01_dd <- r01_dd[r01_dd$sub != 31 & r01_dd$sub != 34, ]

## 2) Get Variable Labels and Re-Level ####

# risk status
r01_dd$risk_status_mom <- droplevels(as_factor(r01_dd$risk_status_mom))
r01_dd$risk_status_both <- droplevels(as_factor(r01_dd$risk_status_both))
r01_dd$sex <- as_factor(r01_dd$sex)

# income
r01_dd$income <- ifelse(is.na(r01_dd$income), NA, ifelse(r01_dd$income < 3, '< $51,000', ifelse(r01_dd$income < 5, "$51,000 - $100,000", '>$100,000')))

# parental ed
r01_dd$mom_ed <- ifelse(r01_dd$measured_parent == 0, ifelse(r01_dd$parent_ed == 0, 'High School/GED', ifelse(r01_dd$parent_ed < 3, 'AA/Technical Degree', ifelse(r01_dd$parent_ed == 3, 'Bachelor Degree', ifelse(r01_dd$parent_ed < 8, '> Bachelor Degree', 'Other/NA')))), ifelse(r01_dd$partner_ed == 0, 'High School/GED', ifelse(r01_dd$partner_ed < 3, 'AA/Technical Degree', ifelse(r01_dd$partner_ed == 3, 'Bachelor Degree', ifelse(r01_dd$partner_ed < 8, '> Bachelor Degree', 'Other/NA')))))

r01_dd$dad_ed <- ifelse(r01_dd$measured_parent == 1, ifelse(r01_dd$parent_ed == 0, 'High School/GED', ifelse(r01_dd$parent_ed < 3, 'AA/Technical Degree', ifelse(r01_dd$parent_ed == 3, 'Bachelor Degree', ifelse(r01_dd$parent_ed < 8, '> Bachelor Degree', 'Other/NA')))), ifelse(r01_dd$partner_ed == 0, 'High School/GED', ifelse(r01_dd$partner_ed < 3, 'AA/Technical Degree', ifelse(r01_dd$partner_ed == 3, 'Bachelor Degree', ifelse(r01_dd$partner_ed < 8, '> Bachelor Degree', 'Other/NA')))))

# dd
r01_dd$dd_checks_exclude <- droplevels(as_factor(r01_dd$dd_checks_exclude))
r01_dd$dd_probmod <- droplevels(as_factor(r01_dd$dd_probmod))

## 2) DD Tables ####

## all
dd_dat <- r01_dd[c(12, 10, 98:99, 101:104)]

dd_dat_tab <-
  tbl_summary(
    data = dd_dat,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", dd_probmod ~ "Best Model", dd_probmod_prob ~ "Best Model, Probability", dd_ed50 ~ "Effective Dealy for 50% Value^", dd_mb_auc ~ "Area Under the Curve", dd_mb_auc_log10 ~ "Area Under the Curve, log10"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", dd_probmod ~ "Best Model", dd_probmod_prob ~ "Best Model, Probability", dd_ed50 ~ "Effective Dealy for 50% Value^", dd_mb_auc ~ "Area Under the Curve", dd_mb_auc_log10 ~ "Area Under the Curve, log10"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# mom risk
dd_risk_mom_v1 <- r01_dd[r01_dd$risk_status_mom != 'Neither', c(8, 12, 10, 98:99, 101:104)]
dd_risk_mom_v1$risk_status_mom <- droplevels(dd_risk_mom_v1$risk_status_mom)

dd_risk_mom_tab <-
  tbl_summary(
    data = dd_risk_mom_v1,
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", dd_probmod ~ "Best Model", dd_probmod_prob ~ "Best Model, Probability", dd_ed50 ~ "Effective Dealy for 50% Value^", dd_mb_auc ~ "Area Under the Curve", dd_mb_auc_log10 ~ "Area Under the Curve, log10"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", dd_probmod ~ "Best Model", dd_probmod_prob ~ "Best Model, Probability", dd_ed50 ~ "Effective Dealy for 50% Value^", dd_mb_auc ~ "Area Under the Curve", dd_mb_auc_log10 ~ "Area Under the Curve, log10"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# strict/both risk
dd_risk_both_v1 <- r01_dd[r01_dd$risk_status_both != 'Neither', c(9, 12, 10, 98:99, 101:104)]
dd_risk_both_v1$risk_status_both <- droplevels(dd_risk_both_v1$risk_status_both)

dd_risk_both_tab <-
  tbl_summary(
    data = dd_risk_both_v1,
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", dd_probmod ~ "Best Model", dd_probmod_prob ~ "Best Model, Probability", dd_ed50 ~ "Effective Dealy for 50% Value^", dd_mb_auc ~ "Area Under the Curve", dd_mb_auc_log10 ~ "Area Under the Curve, log10"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", dd_probmod ~ "Best Model", dd_probmod_prob ~ "Best Model, Probability", dd_ed50 ~ "Effective Dealy for 50% Value^", dd_mb_auc ~ "Area Under the Curve", dd_mb_auc_log10 ~ "Area Under the Curve, log10"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

dd_merge_tab <-
  tbl_merge(
    tbls = list(dd_dat_tab, dd_risk_mom_tab, dd_risk_both_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )
