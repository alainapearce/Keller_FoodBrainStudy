# This script was written by Alaina Pearce in January 2022
# to set up demographic tables by risk status for the Food and Brain Study
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

#### set up ####

## 1) Load Data ####
r01_demo <- as.data.frame(read_spss(("data_2022-01-25/demographics_data.sav")))
names(r01_demo)[1] <- 'sub'

#remove 2 that were removed for ADHD
r01_demo = r01_demo[r01_demo$sub != 31 & r01_demo$sub != 34, ]

## 2) Get Variable Labes and Re-Level ####

# risk status
r01_demo$risk_status_mom <- droplevels(as_factor(r01_demo$risk_status_mom))
r01_demo$risk_status_both <- droplevels(as_factor(r01_demo$risk_status_both))
r01_demo$sex <- as_factor(r01_demo$sex)

# income
r01_demo$income <- ifelse(is.na(r01_demo$income), NA, ifelse(r01_demo$income < 3, '< $51,000', ifelse(r01_demo$income < 5, "$51,000 - $100,000", '>$100,000')))

# parental ed
r01_demo$mom_ed <- ifelse(r01_demo$measured_parent == 0, ifelse(r01_demo$parent_ed == 0, 'High School/GED', ifelse(r01_demo$parent_ed < 3, 'AA/Technical Degree', ifelse(r01_demo$parent_ed == 3, 'Bachelor Degree', ifelse(r01_demo$parent_ed < 8, '> Bachelor Degree', 'Other/NA')))), ifelse(r01_demo$partner_ed == 0, 'High School/GED', ifelse(r01_demo$partner_ed < 3, 'AA/Technical Degree', ifelse(r01_demo$partner_ed == 3, 'Bachelor Degree', ifelse(r01_demo$partner_ed < 8, '> Bachelor Degree', 'Other/NA')))))

r01_demo$dad_ed <- ifelse(r01_demo$measured_parent == 1, ifelse(r01_demo$parent_ed == 0, 'High School/GED', ifelse(r01_demo$parent_ed < 3, 'AA/Technical Degree', ifelse(r01_demo$parent_ed == 3, 'Bachelor Degree', ifelse(r01_demo$parent_ed < 8, '> Bachelor Degree', 'Other/NA')))), ifelse(r01_demo$partner_ed == 0, 'High School/GED', ifelse(r01_demo$partner_ed < 3, 'AA/Technical Degree', ifelse(r01_demo$partner_ed == 3, 'Bachelor Degree', ifelse(r01_demo$partner_ed < 8, '> Bachelor Degree', 'Other/NA')))))

# race
r01_demo$race <- ifelse(r01_demo$race == 0, 'White/Caucasian', ifelse(r01_demo$race == 2, 'Asian', ifelse(r01_demo$race == 3, 'Black/AA', 'Other')))

# ethnicity
r01_demo$ethnicity <- ifelse(r01_demo$ethnicity == 0, 'Not Hispanic/Lantinx', 'Hispanic/Lantinx')

# tanner
r01_demo$pds_tanner_cat <- droplevels(as_factor(r01_demo$pds_tanner_cat))
r01_demo$tanner_silhouette <- ifelse(r01_demo$sex == 'Male', r01_demo$tanner_male, r01_demo$tanner_female)
r01_demo$tanner_silhouette <- ifelse(r01_demo$tanner_silhouette == 99, 'Skip', ifelse(r01_demo$tanner_silhouette == 1, 'Prepubertal', ifelse(r01_demo$tanner_silhouette == 2, 'Early Puberty', ifelse(r01_demo$tanner_silhouette == 3, 'Mid-Puberty', ifelse(r01_demo$tanner_silhouette == 4, 'Late Puberty', 'Postpubertal')))))

# food insecurity
r01_demo$hfssm_6item_cat <- droplevels(as_factor(r01_demo$hfssm_6item_cat))
r01_demo$hfssm_household_cat <- droplevels(as_factor(r01_demo$hfssm_household_cat))
r01_demo$hfssm_adult_cat <- droplevels(as_factor(r01_demo$hfssm_adult_cat))
r01_demo$hfssm_child_cat <- droplevels(as_factor(r01_demo$hfssm_child_cat))

r01_demo$hfias_category <- droplevels(as_factor(r01_demo$hfias_category))

r01_demo$cchip_category <- droplevels(as_factor(r01_demo$cchip_category))

# parents/community
r01_demo$audit_cat <- droplevels(as_factor(r01_demo$audit_cat))
r01_demo$v7_audit_cat <- droplevels(as_factor(r01_demo$v7_audit_cat))


## 2) Tables ####

## 2a) Demo Overview ####

# mom risk
demo <- r01_demo[c(12, 10, 14:16, 337:338, 44, 339)]

demo_tab <-
  tbl_summary(
    data = demo,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", ethnicity ~ "Ethnicity", race ~ "Race", income ~ "Income", mom_ed ~ "Mother's Education", dad_ed ~ "Father's Education", pds_tanner_cat ~ "Puberty, PDS", tanner_silhouette ~ "Tanner, Silhouette"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", ethnicity ~ "Ethnicity", race ~ "Race", income ~ "Income", mom_ed ~ "Mother's Education", dad_ed ~ "Father's Education", pds_tanner_cat ~ "Puberty, PDS", tanner_silhouette ~ "Tanner, Silhouette"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# mom risk
demo_risk_mom <- r01_demo[r01_demo$risk_status_mom != 'Neither', c(8, 12, 10, 14:16, 337:338, 44, 339)]

demo_risk_mom$risk_status_mom <- droplevels(demo_risk_mom$risk_status_mom)

demo_risk_mom_tab <-
  tbl_summary(
    data = demo_risk_mom,
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", ethnicity ~ "Ethnicity", race ~ "Race", income ~ "Income", mom_ed ~ "Mother's Education", dad_ed ~ "Father's Education", pds_tanner_cat ~ "Puberty, PDS", tanner_silhouette ~ "Tanner, Silhouette"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", ethnicity ~ "Ethnicity", race ~ "Race", income ~ "Income", mom_ed ~ "Mother's Education", dad_ed ~ "Father's Education", pds_tanner_cat ~ "Puberty, PDS", tanner_silhouette ~ "Tanner, Silhouette"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# strict/both risk
demo_risk_both <- r01_demo[r01_demo$risk_status_both != 'Neither', c(9, 12, 10, 14:16, 337:338, 44, 339)]

demo_risk_both$risk_status_both <- droplevels(demo_risk_both$risk_status_both)

demo_risk_both_tab <-
  tbl_summary(
    data = demo_risk_both,
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", ethnicity ~ "Ethnicity", race ~ "Race", income ~ "Income", mom_ed ~ "Mother's Education", dad_ed ~ "Father's Education", pds_tanner_cat ~ "Puberty, PDS", tanner_silhouette ~ "Tanner, Silhouette"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", ethnicity ~ "Ethnicity", race ~ "Race", income ~ "Income", mom_ed ~ "Mother's Education", dad_ed ~ "Father's Education", pds_tanner_cat ~ "Puberty, PDS", tanner_silhouette ~ "Tanner, Silhouette"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

demo_merge_tab <-
  tbl_merge(
    tbls = list(demo_tab, demo_risk_mom_tab, demo_risk_both_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )

## 2b) Food Insecurity Overview ####

# overall
foodinsecurity <- r01_demo[c(12, 10, 117:120, 140, 174)]

foodinsecurity_tab <-
  tbl_summary(
    data = foodinsecurity,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", hfssm_household_cat ~ "Houshold, HFSSM",  hfssm_adult_cat ~ "Adult, HFSSM", hfssm_6item_cat ~ "6-item (Adult + Household), HFSSM", hfssm_child_cat ~ "Child, HFSSM", hfias_category ~ "HFIAS", cchip_category ~ "CCHIP"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", hfssm_household_cat ~ "Houshold, HFSSM",  hfssm_adult_cat ~ "Adult, HFSSM", hfssm_6item_cat ~ "6-item (Adult + Household), HFSSM", hfssm_child_cat ~ "Child, HFSSM", hfias_category ~ "HFIAS", cchip_category ~ "CCHIP"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# mom risk
foodinsecurity_risk_mom <- r01_demo[r01_demo$risk_status_mom != 'Neither', c(8, 12, 10, 117:120, 140, 174)]

foodinsecurity_risk_mom$risk_status_mom <- droplevels(foodinsecurity_risk_mom$risk_status_mom)

foodinsecurity_risk_mom_tab <-
  tbl_summary(
    data = foodinsecurity_risk_mom,
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", hfssm_household_cat ~ "Houshold, HFSSM",  hfssm_adult_cat ~ "Adult, HFSSM", hfssm_6item_cat ~ "6-item (Adult + Household), HFSSM", hfssm_child_cat ~ "Child, HFSSM", hfias_category ~ "HFIAS", cchip_category ~ "CCHIP"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", hfssm_household_cat ~ "Houshold, HFSSM",  hfssm_adult_cat ~ "Adult, HFSSM", hfssm_6item_cat ~ "6-item (Adult + Household), HFSSM", hfssm_child_cat ~ "Child, HFSSM", hfias_category ~ "HFIAS", cchip_category ~ "CCHIP"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# strict/both risk
foodinsecurity_risk_both <- r01_demo[r01_demo$risk_status_both != 'Neither', c(9, 12, 10, 117:120, 140, 174)]

foodinsecurity_risk_both$risk_status_both <- droplevels(foodinsecurity_risk_both$risk_status_both)

foodinsecurity_risk_both_tab <-
  tbl_summary(
    data = foodinsecurity_risk_both,
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", hfssm_household_cat ~ "Houshold, HFSSM",  hfssm_adult_cat ~ "Adult, HFSSM", hfssm_6item_cat ~ "6-item (Adult + Household), HFSSM", hfssm_child_cat ~ "Child, HFSSM", hfias_category ~ "HFIAS", cchip_category ~ "CCHIP"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", hfssm_household_cat ~ "Houshold, HFSSM",  hfssm_adult_cat ~ "Adult, HFSSM", hfssm_6item_cat ~ "6-item (Adult + Household), HFSSM", hfssm_child_cat ~ "Child, HFSSM", hfias_category ~ "HFIAS", cchip_category ~ "CCHIP"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

foodinsecurity_merge_tab <-
  tbl_merge(
    tbls = list(foodinsecurity_tab, foodinsecurity_risk_mom_tab, foodinsecurity_risk_both_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )

## 2c) Parent/Community Risk ####

# overall
parents_v1 <- r01_demo[c(12, 10, 185:186, 204:207, 218, 219)]
parents_v7 <- r01_demo[!is.na(r01_demo$v7_date), c(12, 10, 309:312, 323, 324)]

#need to make v7 names match v1 names to get table to line up in merge
names(parents_v7)[3:8] <- names(parents_v1)[5:10]

parents_tab_v1 <-
  tbl_summary(
    data = parents_v1,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", psi_score_mom ~ "Mom Responsiveness, PSI",  psi_score_dad ~ "Dad Responsiveness, PSI", ctc_child_cool ~ "Cool-Child, CTC",  ctc_child_harmful ~ "Harmful-Child, CTC", ctc_friend_cool ~ "Cool-Friend, CTC", ctc_parent_disaprove ~ "Parent-Disapprove, CTC", audit_total ~ "Score, AUDIT", audit_cat ~ "Category, AUDIT"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", psi_score_mom ~ "Mom Responsiveness, PSI",  psi_score_dad ~ "Dad Responsiveness, PSI", ctc_child_cool ~ "Cool-Child, CTC",  ctc_child_harmful ~ "Harmful-Child, CTC", ctc_friend_cool ~ "Cool-Friend, CTC", ctc_parent_disaprove ~ "Parent-Disapprove, CTC", audit_total ~ "Score, AUDIT", audit_cat ~ "Category, AUDIT"),
    type = list(age_yr ~ "continuous", psi_score_mom ~ "continuous",  psi_score_dad ~ "continuous", ctc_child_cool ~ "continuous", ctc_child_harmful ~ "continuous", ctc_friend_cool ~ "continuous", ctc_parent_disaprove ~ "continuous",  audit_total ~ "continuous"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

parents_tab_v7 <-
  tbl_summary(
    data = parents_v7,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", ctc_child_cool ~ "Cool-Child, CTC",  ctc_child_harmful ~ "Harmful-Child, CTC", ctc_friend_cool ~ "Cool-Friend, CTC", ctc_parent_disaprove ~ "Parent-Disapprove, CTC", audit_total ~ "Score, AUDIT", audit_cat ~ "Category, AUDIT"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", ctc_child_cool ~ "Cool-Child, CTC",  ctc_child_harmful ~ "Harmful-Child, CTC", ctc_friend_cool ~ "Cool-Friend, CTC", ctc_parent_disaprove ~ "Parent-Disapprove, CTC", audit_total ~ "Score, AUDIT", audit_cat ~ "Category, AUDIT"),
    type = list(age_yr ~ "continuous", ctc_child_cool ~ "continuous", ctc_child_harmful ~ "continuous", ctc_friend_cool ~ "continuous", ctc_parent_disaprove ~ "continuous",  audit_total ~ "continuous"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

parents_merge_tab <-
  tbl_merge(
    tbls = list(parents_tab_v1, parents_tab_v7),
    tab_spanner = c("**Baseline**", "**Follow-Up**")
  )

# mom risk
parents_risk_mom_v1 <- r01_demo[r01_demo$risk_status_mom != 'Neither', c(8, 12, 10, 185:186, 204:207, 218, 219)]
parents_risk_mom_v1$risk_status_mom <- droplevels(parents_risk_mom_v1$risk_status_mom)

parents_risk_mom_v7 <- r01_demo[r01_demo$risk_status_mom != 'Neither' & !is.na(r01_demo$v7_date), c(8, 12, 10, 309:312, 323, 324)]
parents_risk_mom_v7$risk_status_mom <- droplevels(parents_risk_mom_v7$risk_status_mom)

#need to make v7 names match v1 names to get table to line up in merge
names(parents_risk_mom_v7)[4:9] <- names(parents_risk_mom_v1)[6:11]

parents_risk_mom_tab_v1 <-
  tbl_summary(
    data = parents_risk_mom_v1,
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", psi_score_mom ~ "Mom Responsiveness, PSI",  psi_score_dad ~ "Dad Responsiveness, PSI", ctc_child_cool ~ "Cool-Child, CTC",  ctc_child_harmful ~ "Harmful-Child, CTC", ctc_friend_cool ~ "Cool-Friend, CTC", ctc_parent_disaprove ~ "Parent-Disapprove, CTC", audit_total ~ "Score, AUDIT", audit_cat ~ "Category, AUDIT"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", psi_score_mom ~ "Mom Responsiveness, PSI",  psi_score_dad ~ "Dad Responsiveness, PSI", ctc_child_cool ~ "Cool-Child, CTC",  ctc_child_harmful ~ "Harmful-Child, CTC", ctc_friend_cool ~ "Cool-Friend, CTC", ctc_parent_disaprove ~ "Parent-Disapprove, CTC", audit_total ~ "Score, AUDIT", audit_cat ~ "Category, AUDIT"),
    type = list(age_yr ~ "continuous", psi_score_mom ~ "continuous",  psi_score_dad ~ "continuous", ctc_child_cool ~ "continuous", ctc_child_harmful ~ "continuous", ctc_friend_cool ~ "continuous", ctc_parent_disaprove ~ "continuous",  audit_total ~ "continuous"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

parents_risk_mom_tab_v7 <-
  tbl_summary(
    data = parents_risk_mom_v7,
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", ctc_child_cool ~ "Cool-Child, CTC",  ctc_child_harmful ~ "Harmful-Child, CTC", ctc_friend_cool ~ "Cool-Friend, CTC", ctc_parent_disaprove ~ "Parent-Disapprove, CTC", audit_total ~ "Score, AUDIT", audit_cat ~ "Category, AUDIT"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", ctc_child_cool ~ "Cool-Child, CTC",  ctc_child_harmful ~ "Harmful-Child, CTC", ctc_friend_cool ~ "Cool-Friend, CTC", ctc_parent_disaprove ~ "Parent-Disapprove, CTC", audit_total ~ "Score, AUDIT", audit_cat ~ "Category, AUDIT"),
    type = list(age_yr ~ "continuous", ctc_child_cool ~ "continuous", ctc_child_harmful ~ "continuous", ctc_friend_cool ~ "continuous", ctc_parent_disaprove ~ "continuous",  audit_total ~ "continuous"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

parents_risk_mom_merge_tab <-
  tbl_merge(
    tbls = list(parents_risk_mom_tab_v1, parents_risk_mom_tab_v7),
    tab_spanner = c("**Baseline**", "**Follow-Up**")
  )

# strict/both risk
parents_risk_both_v1 <- r01_demo[r01_demo$risk_status_both != 'Neither', c(9, 12, 10, 185:186, 204:207, 218, 219)]
parents_risk_both_v1$risk_status_both <- droplevels(parents_risk_both_v1$risk_status_both)

parents_risk_both_v7 <- r01_demo[r01_demo$risk_status_both != 'Neither' & !is.na(r01_demo$v7_date), c(9, 12, 10, 309:312, 323, 324)]
parents_risk_both_v7$risk_status_both <- droplevels(parents_risk_both_v7$risk_status_both)

#need to make v7 names match v1 names to get table to line up in merge
names(parents_risk_both_v7)[4:9] <- names(parents_risk_both_v1)[6:11]

parents_risk_both_tab_v1 <-
  tbl_summary(
    data = parents_risk_both_v1,
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", psi_score_mom ~ "Mom Responsiveness, PSI",  psi_score_dad ~ "Dad Responsiveness, PSI", ctc_child_cool ~ "Cool-Child, CTC",  ctc_child_harmful ~ "Harmful-Child, CTC", ctc_friend_cool ~ "Cool-Friend, CTC", ctc_parent_disaprove ~ "Parent-Disapprove, CTC", audit_total ~ "Score, AUDIT", audit_cat ~ "Category, AUDIT"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", psi_score_mom ~ "Mom Responsiveness, PSI",  psi_score_dad ~ "Dad Responsiveness, PSI", ctc_child_cool ~ "Cool-Child, CTC",  ctc_child_harmful ~ "Harmful-Child, CTC", ctc_friend_cool ~ "Cool-Friend, CTC", ctc_parent_disaprove ~ "Parent-Disapprove, CTC", audit_total ~ "Score, AUDIT", audit_cat ~ "Category, AUDIT"),
    type = list(age_yr ~ "continuous", psi_score_mom ~ "continuous",  psi_score_dad ~ "continuous", ctc_child_cool ~ "continuous", ctc_child_harmful ~ "continuous", ctc_friend_cool ~ "continuous", ctc_parent_disaprove ~ "continuous",  audit_total ~ "continuous"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

parents_risk_both_tab_v7 <-
  tbl_summary(
    data = parents_risk_both_v7,
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", ctc_child_cool ~ "Cool-Child, CTC",  ctc_child_harmful ~ "Harmful-Child, CTC", ctc_friend_cool ~ "Cool-Friend, CTC", ctc_parent_disaprove ~ "Parent-Disapprove, CTC", audit_total ~ "Score, AUDIT", audit_cat ~ "Category, AUDIT"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", ctc_child_cool ~ "Cool-Child, CTC",  ctc_child_harmful ~ "Harmful-Child, CTC", ctc_friend_cool ~ "Cool-Friend, CTC", ctc_parent_disaprove ~ "Parent-Disapprove, CTC", audit_total ~ "Score, AUDIT", audit_cat ~ "Category, AUDIT"),
    type = list(age_yr ~ "continuous", ctc_child_cool ~ "continuous", ctc_child_harmful ~ "continuous", ctc_friend_cool ~ "continuous", ctc_parent_disaprove ~ "continuous",  audit_total ~ "continuous"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

parents_risk_both_merge_tab <-
  tbl_merge(
    tbls = list(parents_risk_both_tab_v1, parents_risk_both_tab_v7),
    tab_spanner = c("**Baseline**", "**Follow-Up**")
  )

parents_all_baseline_merge_tab <-
  tbl_merge(
    tbls = list(parents_tab_v1, parents_risk_mom_tab_v1, parents_risk_both_tab_v1),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )

parents_all_followup_merge_tab <-
  tbl_merge(
    tbls = list(parents_tab_v7, parents_risk_mom_tab_v7, parents_risk_both_tab_v7),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )
