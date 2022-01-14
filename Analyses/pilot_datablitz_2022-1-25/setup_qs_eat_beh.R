# This script was written by Alaina Pearce in January 2022
# to set up eating behavior and food parenting tables by risk
# status for the Food and Brain Study Data Blitz Meeting
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
r01_qs_eat <- as.data.frame(read_spss(("data_2022-01-25/qs_eat_beh.sav")))
names(r01_qs_eat)[1] <- 'sub'

r01_qs_eat_labels <- lapply(r01_qs_eat, function(x) attributes(x)$label)

#remove 2 that were removed for ADHD
r01_qs_eat <- r01_qs_eat[r01_qs_eat$sub != 31 & r01_qs_eat$sub != 34, ]

## 2) Get Variable Labels and Re-Level ####

# risk status
r01_qs_eat$risk_status_mom <- droplevels(as_factor(r01_qs_eat$risk_status_mom))
r01_qs_eat$risk_status_both <- droplevels(as_factor(r01_qs_eat$risk_status_both))
r01_qs_eat$sex <- as_factor(r01_qs_eat$sex)

# income
r01_qs_eat$income <- ifelse(is.na(r01_qs_eat$income), NA, ifelse(r01_qs_eat$income < 3, '< $51,000', ifelse(r01_qs_eat$income < 5, "$51,000 - $100,000", '>$100,000')))

# parental ed
r01_qs_eat$mom_ed <- ifelse(r01_qs_eat$measured_parent == 0, ifelse(r01_qs_eat$parent_ed == 0, 'High School/GED', ifelse(r01_qs_eat$parent_ed < 3, 'AA/Technical Degree', ifelse(r01_qs_eat$parent_ed == 3, 'Bachelor Degree', ifelse(r01_qs_eat$parent_ed < 8, '> Bachelor Degree', 'Other/NA')))), ifelse(r01_qs_eat$partner_ed == 0, 'High School/GED', ifelse(r01_qs_eat$partner_ed < 3, 'AA/Technical Degree', ifelse(r01_qs_eat$partner_ed == 3, 'Bachelor Degree', ifelse(r01_qs_eat$partner_ed < 8, '> Bachelor Degree', 'Other/NA')))))

r01_qs_eat$dad_ed <- ifelse(r01_qs_eat$measured_parent == 1, ifelse(r01_qs_eat$parent_ed == 0, 'High School/GED', ifelse(r01_qs_eat$parent_ed < 3, 'AA/Technical Degree', ifelse(r01_qs_eat$parent_ed == 3, 'Bachelor Degree', ifelse(r01_qs_eat$parent_ed < 8, '> Bachelor Degree', 'Other/NA')))), ifelse(r01_qs_eat$partner_ed == 0, 'High School/GED', ifelse(r01_qs_eat$partner_ed < 3, 'AA/Technical Degree', ifelse(r01_qs_eat$partner_ed == 3, 'Bachelor Degree', ifelse(r01_qs_eat$partner_ed < 8, '> Bachelor Degree', 'Other/NA')))))

# family food behavior
r01_qs_eat$feedschild <- droplevels(as_factor(r01_qs_eat$feedschild))
r01_qs_eat$buysfood <- droplevels(as_factor(r01_qs_eat$buysfood))
r01_qs_eat$family_foodcond <- droplevels(as_factor(r01_qs_eat$family_foodcond))
r01_qs_eat$freq_eatout <- droplevels(as_factor(r01_qs_eat$freq_eatout))

r01_qs_eat$v7_feedschild <- droplevels(as_factor(r01_qs_eat$v7_feedschild))
r01_qs_eat$v7_buysfood <- droplevels(as_factor(r01_qs_eat$v7_buysfood))
r01_qs_eat$v7_family_foodcond <- droplevels(as_factor(r01_qs_eat$v7_family_foodcond))
r01_qs_eat$v7_freq_eatout <- droplevels(as_factor(r01_qs_eat$v7_freq_eatout))

# loc
r01_qs_eat$loc1 <- droplevels(as_factor(r01_qs_eat$loc1))
r01_qs_eat$v7_loc1 <- droplevels(as_factor(r01_qs_eat$v7_loc1))

# dg
r01_qs_eat$dg_wait <- droplevels(as_factor(r01_qs_eat$dg_wait))

# kfq
r01_qs_eat$kfq_grains_modefreq <- droplevels(as_factor(r01_qs_eat$kfq_grains_modefreq))
r01_qs_eat$kfq_veg_modefreq <- droplevels(as_factor(r01_qs_eat$kfq_veg_modefreq))
r01_qs_eat$kfq_fruit_modefreq <- droplevels(as_factor(r01_qs_eat$kfq_fruit_modefreq))
r01_qs_eat$kfq_dairy_modefreq <- droplevels(as_factor(r01_qs_eat$kfq_dairy_modefreq))
r01_qs_eat$kfq_protein_modefreq <- droplevels(as_factor(r01_qs_eat$kfq_protein_modefreq))
r01_qs_eat$kfq_bev_modefreq <- droplevels(as_factor(r01_qs_eat$kfq_bev_modefreq))
r01_qs_eat$kfq_snack_modefreq <- droplevels(as_factor(r01_qs_eat$kfq_snack_modefreq))
r01_qs_eat$kfq_desert_modefreq <- droplevels(as_factor(r01_qs_eat$kfq_desert_modefreq))
r01_qs_eat$kfq_cond_modefreq <- droplevels(as_factor(r01_qs_eat$kfq_cond_modefreq))

## 2) Tables ####

## 2a) Family Food/Home ####

## all
fam_home_v1 <- r01_qs_eat[c(12, 10, 27, 29, 31:34, 88:90, 563:566, 536:542)]
fam_home_v7 <- r01_qs_eat[c(12, 10, 725, 727, 729:732, 868:870, 808:814)]

#get only those with V7
fam_home_v7$nNA <- rowSums(is.na(fam_home_v7))
fam_home_v7 <- fam_home_v7[fam_home_v7$nNA < 16, ]

fam_home_v1_tab <-
  tbl_summary(
    data = fam_home_v1,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", feedschild ~ "Feeds Child", buysfood ~ "Buys Food", freq_eatout ~ "Eat Out", freq_familydinner ~ "Family Dinner, d/wk", freq_homelunch ~ "Brings Home Lunch, d/wk", family_foodcond ~ "Family Special Dietary Needs", encourage_plateclean_vas ~ "Encourage Plate-Cleaning", child_plateclean_vas ~ "Child Plate-Cleans", percieved_child_kcal ~ "Percieved kcals Child Eats", ffbs_control ~ "Maternal Control, FFBS", ffbs_presence ~ "Maternal Presence, FFBS", ffbs_ch_choice ~ "Child Choice, FFBS", ffbs_org ~ "Organization, FFBS", cfq_resp ~ "Percieved Responsibility, CFQ", cfq_pcw ~ "Percieved Child Weight, CFQ", cfq_ppw ~ "Percieved Parent Weight, CFQ", cfq_cwc ~ "Child Weight Concerns, CFQ", cfq_rest ~ "Restriction, CFQ", cfq_pressure ~ "Pressure, CFQ", cfq_mon ~ "Monitoring, CFQ"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", feedschild ~ "Feeds Child", buysfood ~ "Buys Food", freq_eatout ~ "Eat Out", freq_familydinner ~ "Family Dinner, d/wk", freq_homelunch ~ "Brings Home Lunch, d/wk", family_foodcond ~ "Family Special Dietary Needs", encourage_plateclean_vas ~ "Encourage Plate-Cleaning", child_plateclean_vas ~ "Child Plate-Cleans", percieved_child_kcal ~ "Percieved kcals Child Eats", ffbs_control ~ "Maternal Control, FFBS", ffbs_presence ~ "Maternal Presence, FFBS", ffbs_ch_choice ~ "Child Choice, FFBS", ffbs_org ~ "Organization, FFBS", cfq_resp ~ "Percieved Responsibility, CFQ", cfq_pcw ~ "Percieved Child Weight, CFQ", cfq_ppw ~ "Percieved Parent Weight, CFQ", cfq_cwc ~ "Child Weight Concerns, CFQ", cfq_rest ~ "Restriction, CFQ", cfq_pressure ~ "Pressure, CFQ", cfq_mon ~ "Monitoring, CFQ"),
    type = list(freq_familydinner ~ 'continuous', freq_homelunch ~ 'continuous', cfq_resp ~ 'continuous', cfq_mon ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

fam_home_v7_tab <-
  tbl_summary(
    data = fam_home_v7[1:18],
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_feedschild ~ "Feeds Child", v7_buysfood ~ "Buys Food", v7_freq_eatout ~ "Eat Out", v7_freq_familydinner ~ "Family Dinner, d/wk", v7_freq_homelunch ~ "Brings Home Lunch, d/wk", v7_family_foodcond ~ "Family Special Dietary Needs", v7_encourage_plateclean_vas ~ "Encourage Plate-Cleaning", v7_child_plateclean_vas ~ "Child Plate-Cleans", v7_percieved_child_kcal ~ "Percieved kcals Child Eats", v7_cfq_resp ~ "Percieved Responsibility, CFQ", v7_cfq_pcw ~ "Percieved Child Weight, CFQ", v7_cfq_ppw ~ "Percieved Parent Weight, CFQ", v7_cfq_cwc ~ "Child Weight Concerns, CFQ", v7_cfq_rest ~ "Restriction, CFQ", v7_cfq_pressure ~ "Pressure, CFQ", v7_cfq_mon ~ "Monitoring, CFQ"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_feedschild ~ "Feeds Child", v7_buysfood ~ "Buys Food", v7_freq_eatout ~ "Eat Out", v7_freq_familydinner ~ "Family Dinner, d/wk", v7_freq_homelunch ~ "Brings Home Lunch, d/wk", v7_family_foodcond ~ "Family Special Dietary Needs", v7_encourage_plateclean_vas ~ "Encourage Plate-Cleaning", v7_child_plateclean_vas ~ "Child Plate-Cleans", v7_percieved_child_kcal ~ "Percieved kcals Child Eats", v7_cfq_resp ~ "Percieved Responsibility, CFQ", v7_cfq_pcw ~ "Percieved Child Weight, CFQ", v7_cfq_ppw ~ "Percieved Parent Weight, CFQ", v7_cfq_cwc ~ "Child Weight Concerns, CFQ", v7_cfq_rest ~ "Restriction, CFQ", v7_cfq_pressure ~ "Pressure, CFQ", v7_cfq_mon ~ "Monitoring, CFQ"),
    type = list(v7_freq_familydinner ~ 'continuous', v7_freq_homelunch ~ 'continuous', v7_cfq_resp ~ 'continuous', v7_cfq_pcw ~ 'continuous', v7_cfq_mon ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# mom risk
fam_home_risk_mom_v1 <- r01_qs_eat[r01_qs_eat$risk_status_mom != 'Neither', c(8, 12, 10, 27, 29, 31:34, 88:90, 563:566, 536:542)]
fam_home_risk_mom_v1$risk_status_mom <- droplevels(fam_home_risk_mom_v1$risk_status_mom)

fam_home_risk_mom_v7 <- r01_qs_eat[r01_qs_eat$risk_status_mom != 'Neither', c(8, 12, 10, 725, 727, 729:732, 868:870, 808:814)]
fam_home_risk_mom_v7$risk_status_mom <- droplevels(fam_home_risk_mom_v7$risk_status_mom)

#get only those with V7
fam_home_risk_mom_v7$nNA <- rowSums(is.na(fam_home_risk_mom_v7))
fam_home_risk_mom_v7 <- fam_home_risk_mom_v7[fam_home_risk_mom_v7$nNA < 16, ]

fam_home_risk_mom_v1_tab <-
  tbl_summary(
    data = fam_home_risk_mom_v1,
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", feedschild ~ "Feeds Child", buysfood ~ "Buys Food", freq_eatout ~ "Eat Out", freq_familydinner ~ "Family Dinner, d/wk", freq_homelunch ~ "Brings Home Lunch, d/wk", family_foodcond ~ "Family Special Dietary Needs", encourage_plateclean_vas ~ "Encourage Plate-Cleaning", child_plateclean_vas ~ "Child Plate-Cleans", percieved_child_kcal ~ "Percieved kcals Child Eats", ffbs_control ~ "Maternal Control, FFBS", ffbs_presence ~ "Maternal Presence, FFBS", ffbs_ch_choice ~ "Child Choice, FFBS", ffbs_org ~ "Organization, FFBS", cfq_resp ~ "Percieved Responsibility, CFQ", cfq_pcw ~ "Percieved Child Weight, CFQ", cfq_ppw ~ "Percieved Parent Weight, CFQ", cfq_cwc ~ "Child Weight Concerns, CFQ", cfq_rest ~ "Restriction, CFQ", cfq_pressure ~ "Pressure, CFQ", cfq_mon ~ "Monitoring, CFQ"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", feedschild ~ "Feeds Child", buysfood ~ "Buys Food", freq_eatout ~ "Eat Out", freq_familydinner ~ "Family Dinner, d/wk", freq_homelunch ~ "Brings Home Lunch, d/wk", family_foodcond ~ "Family Special Dietary Needs", encourage_plateclean_vas ~ "Encourage Plate-Cleaning", child_plateclean_vas ~ "Child Plate-Cleans", percieved_child_kcal ~ "Percieved kcals Child Eats", ffbs_control ~ "Maternal Control, FFBS", ffbs_presence ~ "Maternal Presence, FFBS", ffbs_ch_choice ~ "Child Choice, FFBS", ffbs_org ~ "Organization, FFBS", cfq_resp ~ "Percieved Responsibility, CFQ", cfq_pcw ~ "Percieved Child Weight, CFQ", cfq_ppw ~ "Percieved Parent Weight, CFQ", cfq_cwc ~ "Child Weight Concerns, CFQ", cfq_rest ~ "Restriction, CFQ", cfq_pressure ~ "Pressure, CFQ", cfq_mon ~ "Monitoring, CFQ"),
    type = list(freq_familydinner ~ 'continuous', freq_homelunch ~ 'continuous', cfq_resp ~ 'continuous', cfq_mon ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

fam_home_risk_mom_v7_tab <-
  tbl_summary(
    data = fam_home_risk_mom_v7[1:19],
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_feedschild ~ "Feeds Child", v7_buysfood ~ "Buys Food", v7_freq_eatout ~ "Eat Out", v7_freq_familydinner ~ "Family Dinner, d/wk", v7_freq_homelunch ~ "Brings Home Lunch, d/wk", v7_family_foodcond ~ "Family Special Dietary Needs", v7_encourage_plateclean_vas ~ "Encourage Plate-Cleaning", v7_child_plateclean_vas ~ "Child Plate-Cleans", v7_percieved_child_kcal ~ "Percieved kcals Child Eats", v7_cfq_resp ~ "Percieved Responsibility, CFQ", v7_cfq_pcw ~ "Percieved Child Weight, CFQ", v7_cfq_ppw ~ "Percieved Parent Weight, CFQ", v7_cfq_cwc ~ "Child Weight Concerns, CFQ", v7_cfq_rest ~ "Restriction, CFQ", v7_cfq_pressure ~ "Pressure, CFQ", v7_cfq_mon ~ "Monitoring, CFQ"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_feedschild ~ "Feeds Child", v7_buysfood ~ "Buys Food", v7_freq_eatout ~ "Eat Out", v7_freq_familydinner ~ "Family Dinner, d/wk", v7_freq_homelunch ~ "Brings Home Lunch, d/wk", v7_family_foodcond ~ "Family Special Dietary Needs", v7_encourage_plateclean_vas ~ "Encourage Plate-Cleaning", v7_child_plateclean_vas ~ "Child Plate-Cleans", v7_percieved_child_kcal ~ "Percieved kcals Child Eats", v7_cfq_resp ~ "Percieved Responsibility, CFQ", v7_cfq_pcw ~ "Percieved Child Weight, CFQ", v7_cfq_ppw ~ "Percieved Parent Weight, CFQ", v7_cfq_cwc ~ "Child Weight Concerns, CFQ", v7_cfq_rest ~ "Restriction, CFQ", v7_cfq_pressure ~ "Pressure, CFQ", v7_cfq_mon ~ "Monitoring, CFQ"),
    type = list(v7_freq_familydinner ~ 'continuous', v7_freq_homelunch ~ 'continuous', v7_cfq_resp ~ 'continuous', v7_cfq_pcw ~ 'continuous', v7_cfq_mon ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# strict/both risk
fam_home_risk_both_v1 <- r01_qs_eat[r01_qs_eat$risk_status_both != 'Neither', c(9, 12, 10, 27, 29, 31:34, 88:90, 563:566, 536:542)]
fam_home_risk_both_v1$risk_status_both <- droplevels(fam_home_risk_both_v1$risk_status_both)

fam_home_risk_both_v7 <- r01_qs_eat[r01_qs_eat$risk_status_both != 'Neither', c(9, 12, 10, 725, 727, 729:732, 868:870, 808:814)]
fam_home_risk_both_v7$risk_status_both <- droplevels(fam_home_risk_both_v7$risk_status_both)

#get only those with V7
fam_home_risk_both_v7$nNA <- rowSums(is.na(fam_home_risk_both_v7))
fam_home_risk_both_v7 <- fam_home_risk_both_v7[fam_home_risk_both_v7$nNA < 16, ]

fam_home_risk_both_v1_tab <-
  tbl_summary(
    data = fam_home_risk_both_v1,
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", feedschild ~ "Feeds Child", buysfood ~ "Buys Food", freq_eatout ~ "Eat Out", freq_familydinner ~ "Family Dinner, d/wk", freq_homelunch ~ "Brings Home Lunch, d/wk", family_foodcond ~ "Family Special Dietary Needs", encourage_plateclean_vas ~ "Encourage Plate-Cleaning", child_plateclean_vas ~ "Child Plate-Cleans", percieved_child_kcal ~ "Percieved kcals Child Eats", ffbs_control ~ "Maternal Control, FFBS", ffbs_presence ~ "Maternal Presence, FFBS", ffbs_ch_choice ~ "Child Choice, FFBS", ffbs_org ~ "Organization, FFBS", cfq_resp ~ "Percieved Responsibility, CFQ", cfq_pcw ~ "Percieved Child Weight, CFQ", cfq_ppw ~ "Percieved Parent Weight, CFQ", cfq_cwc ~ "Child Weight Concerns, CFQ", cfq_rest ~ "Restriction, CFQ", cfq_pressure ~ "Pressure, CFQ", cfq_mon ~ "Monitoring, CFQ"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", feedschild ~ "Feeds Child", buysfood ~ "Buys Food", freq_eatout ~ "Eat Out", freq_familydinner ~ "Family Dinner, d/wk", freq_homelunch ~ "Brings Home Lunch, d/wk", family_foodcond ~ "Family Special Dietary Needs", encourage_plateclean_vas ~ "Encourage Plate-Cleaning", child_plateclean_vas ~ "Child Plate-Cleans", percieved_child_kcal ~ "Percieved kcals Child Eats", ffbs_control ~ "Maternal Control, FFBS", ffbs_presence ~ "Maternal Presence, FFBS", ffbs_ch_choice ~ "Child Choice, FFBS", ffbs_org ~ "Organization, FFBS", cfq_resp ~ "Percieved Responsibility, CFQ", cfq_pcw ~ "Percieved Child Weight, CFQ", cfq_ppw ~ "Percieved Parent Weight, CFQ", cfq_cwc ~ "Child Weight Concerns, CFQ", cfq_rest ~ "Restriction, CFQ", cfq_pressure ~ "Pressure, CFQ", cfq_mon ~ "Monitoring, CFQ"),
    type = list(freq_familydinner ~ 'continuous', freq_homelunch ~ 'continuous', cfq_resp ~ 'continuous', cfq_pcw ~ 'continuous', cfq_mon ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

fam_home_risk_both_v7_tab <-
  tbl_summary(
    data = fam_home_risk_both_v7[1:19],
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_feedschild ~ "Feeds Child", v7_buysfood ~ "Buys Food", v7_freq_eatout ~ "Eat Out", v7_freq_familydinner ~ "Family Dinner, d/wk", v7_freq_homelunch ~ "Brings Home Lunch, d/wk", v7_family_foodcond ~ "Family Special Dietary Needs", v7_encourage_plateclean_vas ~ "Encourage Plate-Cleaning", v7_child_plateclean_vas ~ "Child Plate-Cleans", v7_percieved_child_kcal ~ "Percieved kcals Child Eats", v7_cfq_resp ~ "Percieved Responsibility, CFQ", v7_cfq_pcw ~ "Percieved Child Weight, CFQ", v7_cfq_ppw ~ "Percieved Parent Weight, CFQ", v7_cfq_cwc ~ "Child Weight Concerns, CFQ", v7_cfq_rest ~ "Restriction, CFQ", v7_cfq_pressure ~ "Pressure, CFQ", v7_cfq_mon ~ "Monitoring, CFQ"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_feedschild ~ "Feeds Child", v7_buysfood ~ "Buys Food", v7_freq_eatout ~ "Eat Out", v7_freq_familydinner ~ "Family Dinner, d/wk", v7_freq_homelunch ~ "Brings Home Lunch, d/wk", v7_family_foodcond ~ "Family Special Dietary Needs", v7_encourage_plateclean_vas ~ "Encourage Plate-Cleaning", v7_child_plateclean_vas ~ "Child Plate-Cleans", v7_percieved_child_kcal ~ "Percieved kcals Child Eats", v7_cfq_resp ~ "Percieved Responsibility, CFQ", v7_cfq_pcw ~ "Percieved Child Weight, CFQ", v7_cfq_ppw ~ "Percieved Parent Weight, CFQ", v7_cfq_cwc ~ "Child Weight Concerns, CFQ", v7_cfq_rest ~ "Restriction, CFQ", v7_cfq_pressure ~ "Pressure, CFQ", v7_cfq_mon ~ "Monitoring, CFQ"),
    type = list(v7_freq_familydinner ~ 'continuous', v7_freq_homelunch ~ 'continuous', v7_cfq_resp ~ 'continuous', v7_cfq_pcw ~ 'continuous', v7_cfq_mon ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

qs_fam_home_merge_v1_tab <-
  tbl_merge(
    tbls = list(fam_home_v1_tab, fam_home_risk_mom_v1_tab, fam_home_risk_both_v1_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )

qs_fam_home_merge_v7_tab <-
  tbl_merge(
    tbls = list(fam_home_v7_tab, fam_home_risk_mom_v7_tab, fam_home_risk_both_v7_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )

## 2b) Parent Portion Size ####

## all
portions_v1 <- r01_qs_eat[c(12, 10, 91:94, 331:340)]
portions_v7 <- r01_qs_eat[c(12, 10, 871:874)]

portions_v7$nNA <- rowSums(is.na(portions_v7))
portions_v7 <- portions_v7[portions_v7$nNA < 4, ]

portions_v1_tab <-
  tbl_summary(
    data = portions_v1,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", pcent_parent_portionchoice ~ "Parent Portions Food, % time", pcent_partner_portionchoice ~ "Partner Portions Food, % time", pcent_child_portionchoice ~ "Child Portions Food, % time", pcent_other_portionchoice ~ "Other Portions Food, % time", p_pss_vas_lookonplate ~ "Strategy: Look at Plate", p_pss_vas_childusualintake ~ "Strategy: Child Usual Intake", p_pss_vas_platesize ~ "Strategy: Plate Size", p_pss_vas_measuringtool ~ "Strategy: Measure", p_pss_vas_health_proffesional ~ "Strategy: Health Professional Advise", p_pss_vas_recipe ~ "Strategy: Recipe", p_pss_vas_familyadult_portion ~ "Strategy: Family Adult Amount", p_pss_vas_familychild_portion ~ "Strategy: Family Child Amount", p_pss_vas_preprotioned ~ "Strategy: Pre-Portioned Foods", p_pss_vas_child_selfregulate ~ "Strategy: Child Self-Regulation"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", pcent_parent_portionchoice ~ "Parent Portions Food, % time", pcent_partner_portionchoice ~ "Partner Portions Food, % time", pcent_child_portionchoice ~ "Child Portions Food, % time", pcent_other_portionchoice ~ "Other Portions Food, % time", p_pss_vas_lookonplate ~ "Strategy: Look at Plate", p_pss_vas_childusualintake ~ "Strategy: Child Usual Intake", p_pss_vas_platesize ~ "Strategy: Plate Size", p_pss_vas_measuringtool ~ "Strategy: Measure", p_pss_vas_health_proffesional ~ "Strategy: Health Professional Advise", p_pss_vas_recipe ~ "Strategy: Recipe", p_pss_vas_familyadult_portion ~ "Strategy: Family Adult Amount", p_pss_vas_familychild_portion ~ "Strategy: Family Child Amount", p_pss_vas_preprotioned ~ "Strategy: Pre-Portioned Foods", p_pss_vas_child_selfregulate ~ "Strategy: Child Self-Regulation"),
    type = list(pcent_other_portionchoice ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

portions_v7_tab <-
  tbl_summary(
    data = portions_v7[1:6],
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_pcent_parent_portionchoice ~ "Parent Portions Food, % time", v7_pcent_partner_portionchoice ~ "Partner Portions Food, % time", v7_pcent_child_portionchoice ~ "Child Portions Food, % time", v7_pcent_other_portionchoice ~ "Other Portions Food, % time"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_pcent_parent_portionchoice ~ "Parent Portions Food, % time", v7_pcent_partner_portionchoice ~ "Partner Portions Food, % time", v7_pcent_child_portionchoice ~ "Child Portions Food, % time", v7_pcent_other_portionchoice ~ "Other Portions Food, % time"),
    type = list(v7_pcent_other_portionchoice ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# mom risk
portions_risk_mom_v1 <- r01_qs_eat[c(8, 12, 10, 91:94, 331:340)]
portions_risk_mom_v1$risk_status_mom <- droplevels(portions_risk_mom_v1$risk_status_mom)

portions_risk_mom_v7 <- r01_qs_eat[c(8, 12, 10, 871:874)]
portions_risk_mom_v7$risk_status_mom <- droplevels(portions_risk_mom_v7$risk_status_mom)

portions_risk_mom_v7$nNA <- rowSums(is.na(portions_risk_mom_v7))
portions_risk_mom_v7 <- portions_risk_mom_v7[portions_risk_mom_v7$nNA < 4, ]

portions_risk_mom_v1_tab <-
  tbl_summary(
    data = portions_risk_mom_v1,
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", pcent_parent_portionchoice ~ "Parent Portions Food, % time", pcent_partner_portionchoice ~ "Partner Portions Food, % time", pcent_child_portionchoice ~ "Child Portions Food, % time", pcent_other_portionchoice ~ "Other Portions Food, % time", p_pss_vas_lookonplate ~ "Strategy: Look at Plate", p_pss_vas_childusualintake ~ "Strategy: Child Usual Intake", p_pss_vas_platesize ~ "Strategy: Plate Size", p_pss_vas_measuringtool ~ "Strategy: Measure", p_pss_vas_health_proffesional ~ "Strategy: Health Professional Advise", p_pss_vas_recipe ~ "Strategy: Recipe", p_pss_vas_familyadult_portion ~ "Strategy: Family Adult Amount", p_pss_vas_familychild_portion ~ "Strategy: Family Child Amount", p_pss_vas_preprotioned ~ "Strategy: Pre-Portioned Foods", p_pss_vas_child_selfregulate ~ "Strategy: Child Self-Regulation"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", pcent_parent_portionchoice ~ "Parent Portions Food, % time", pcent_partner_portionchoice ~ "Partner Portions Food, % time", pcent_child_portionchoice ~ "Child Portions Food, % time", pcent_other_portionchoice ~ "Other Portions Food, % time", p_pss_vas_lookonplate ~ "Strategy: Look at Plate", p_pss_vas_childusualintake ~ "Strategy: Child Usual Intake", p_pss_vas_platesize ~ "Strategy: Plate Size", p_pss_vas_measuringtool ~ "Strategy: Measure", p_pss_vas_health_proffesional ~ "Strategy: Health Professional Advise", p_pss_vas_recipe ~ "Strategy: Recipe", p_pss_vas_familyadult_portion ~ "Strategy: Family Adult Amount", p_pss_vas_familychild_portion ~ "Strategy: Family Child Amount", p_pss_vas_preprotioned ~ "Strategy: Pre-Portioned Foods", p_pss_vas_child_selfregulate ~ "Strategy: Child Self-Regulation"),
    type = list(pcent_other_portionchoice ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

portions_risk_mom_v7_tab <-
  tbl_summary(
    data = portions_risk_mom_v7[1:7],
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_pcent_parent_portionchoice ~ "Parent Portions Food, % time", v7_pcent_partner_portionchoice ~ "Partner Portions Food, % time", v7_pcent_child_portionchoice ~ "Child Portions Food, % time", v7_pcent_other_portionchoice ~ "Other Portions Food, % time"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_pcent_parent_portionchoice ~ "Parent Portions Food, % time", v7_pcent_partner_portionchoice ~ "Partner Portions Food, % time", v7_pcent_child_portionchoice ~ "Child Portions Food, % time", v7_pcent_other_portionchoice ~ "Other Portions Food, % time"),
    type = list(v7_pcent_other_portionchoice ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# strict/both risk
portions_risk_both_v1 <- r01_qs_eat[c(9, 12, 10, 91:94, 331:340)]
portions_risk_both_v1$risk_status_both <- droplevels(portions_risk_both_v1$risk_status_both)

portions_risk_both_v7 <- r01_qs_eat[c(9, 12, 10, 871:874)]
portions_risk_both_v7$risk_status_both <- droplevels(portions_risk_both_v7$risk_status_both)

portions_risk_both_v7$nNA <- rowSums(is.na(portions_risk_both_v7))
portions_risk_both_v7 <- portions_risk_both_v7[portions_risk_both_v7$nNA < 4, ]

portions_risk_both_v1_tab <-
  tbl_summary(
    data = portions_risk_both_v1,
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", pcent_parent_portionchoice ~ "Parent Portions Food, % time", pcent_partner_portionchoice ~ "Partner Portions Food, % time", pcent_child_portionchoice ~ "Child Portions Food, % time", pcent_other_portionchoice ~ "Other Portions Food, % time", p_pss_vas_lookonplate ~ "Strategy: Look at Plate", p_pss_vas_childusualintake ~ "Strategy: Child Usual Intake", p_pss_vas_platesize ~ "Strategy: Plate Size", p_pss_vas_measuringtool ~ "Strategy: Measure", p_pss_vas_health_proffesional ~ "Strategy: Health Professional Advise", p_pss_vas_recipe ~ "Strategy: Recipe", p_pss_vas_familyadult_portion ~ "Strategy: Family Adult Amount", p_pss_vas_familychild_portion ~ "Strategy: Family Child Amount", p_pss_vas_preprotioned ~ "Strategy: Pre-Portioned Foods", p_pss_vas_child_selfregulate ~ "Strategy: Child Self-Regulation"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", pcent_parent_portionchoice ~ "Parent Portions Food, % time", pcent_partner_portionchoice ~ "Partner Portions Food, % time", pcent_child_portionchoice ~ "Child Portions Food, % time", pcent_other_portionchoice ~ "Other Portions Food, % time", p_pss_vas_lookonplate ~ "Strategy: Look at Plate", p_pss_vas_childusualintake ~ "Strategy: Child Usual Intake", p_pss_vas_platesize ~ "Strategy: Plate Size", p_pss_vas_measuringtool ~ "Strategy: Measure", p_pss_vas_health_proffesional ~ "Strategy: Health Professional Advise", p_pss_vas_recipe ~ "Strategy: Recipe", p_pss_vas_familyadult_portion ~ "Strategy: Family Adult Amount", p_pss_vas_familychild_portion ~ "Strategy: Family Child Amount", p_pss_vas_preprotioned ~ "Strategy: Pre-Portioned Foods", p_pss_vas_child_selfregulate ~ "Strategy: Child Self-Regulation"),
    type = list(pcent_other_portionchoice ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

portions_risk_both_v7_tab <-
  tbl_summary(
    data = portions_risk_both_v7[1:7],
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_pcent_parent_portionchoice ~ "Parent Portions Food, % time", v7_pcent_partner_portionchoice ~ "Partner Portions Food, % time", v7_pcent_child_portionchoice ~ "Child Portions Food, % time", v7_pcent_other_portionchoice ~ "Other Portions Food, % time"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_pcent_parent_portionchoice ~ "Parent Portions Food, % time", v7_pcent_partner_portionchoice ~ "Partner Portions Food, % time", v7_pcent_child_portionchoice ~ "Child Portions Food, % time", v7_pcent_other_portionchoice ~ "Other Portions Food, % time"),
    type = list(v7_pcent_other_portionchoice ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

qs_portions_merge_v1_tab <-
  tbl_merge(
    tbls = list(portions_v1_tab, portions_risk_mom_v1_tab, portions_risk_mom_v1_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )

qs_portions_merge_v7_tab <-
  tbl_merge(
    tbls = list(portions_v7_tab, portions_risk_mom_v7_tab, portions_risk_mom_v7_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )

## 2c) Kid Food Frequency ####

## all
kfq <- r01_qs_eat[c(12, 10, 391, 393, 395, 397, 399, 401, 403, 405, 407)]
kfq$nNA <- rowSums(is.na(kfq))
kfq <- kfq[kfq$nNA < 9, ]

kfq_tab <-
  tbl_summary(
    data = kfq[1:7],
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", kfq_grains_modefreq ~ "Grains", kfq_veg_modefreq ~ "Vegetables", kfq_fruit_modefreq ~ "Fruit", kfq_dairy_modefreq ~ "Dairy", kfq_protein_modefreq ~ "Protein"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", kfq_grains_modefreq ~ "Grains", kfq_veg_modefreq ~ "Vegetables", kfq_fruit_modefreq ~ "Fruit", kfq_dairy_modefreq ~ "Dairy", kfq_protein_modefreq ~ "Protein"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

kfq_tab_cont <-
  tbl_summary(
    data = kfq[8:11],
    value = list(kfq_bev_modefreq ~ "Sugar Sweetend Beverages", kfq_snack_modefreq ~ "Snacks", kfq_desert_modefreq ~ "Desert", kfq_cond_modefreq ~ "Condiments"),
    label = list(kfq_bev_modefreq ~ "Sugar Sweetend Beverages", kfq_snack_modefreq ~ "Snacks", kfq_desert_modefreq ~ "Desert", kfq_cond_modefreq ~ "Condiments"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# mom risk
kfq_risk_mom <- r01_qs_eat[r01_qs_eat$risk_status_mom != 'Neither', c(8, 12, 10, 391, 393, 395, 397, 399, 401, 403, 405, 407)]
kfq_risk_mom$risk_status_mom <- droplevels(kfq_risk_mom$risk_status_mom)

kfq_risk_mom$nNA <- rowSums(is.na(kfq_risk_mom))
kfq_risk_mom <- kfq_risk_mom[kfq_risk_mom$nNA < 9, ]

kfq_risk_mom_tab <-
  tbl_summary(
    data = kfq_risk_mom[1:8],
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", kfq_grains_modefreq ~ "Grains", kfq_veg_modefreq ~ "Vegetables", kfq_fruit_modefreq ~ "Fruit", kfq_dairy_modefreq ~ "Dairy", kfq_protein_modefreq ~ "Protein"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", kfq_grains_modefreq ~ "Grains", kfq_veg_modefreq ~ "Vegetables", kfq_fruit_modefreq ~ "Fruit", kfq_dairy_modefreq ~ "Dairy", kfq_protein_modefreq ~ "Protein"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

kfq_risk_mom_tab_cont <-
  tbl_summary(
    data = kfq_risk_mom[c(1, 9:12)],
    by = risk_status_mom,
    value = list(kfq_bev_modefreq ~ "Sugar Sweetend Beverages", kfq_snack_modefreq ~ "Snacks", kfq_desert_modefreq ~ "Desert", kfq_cond_modefreq ~ "Condiments"),
    label = list(kfq_bev_modefreq ~ "Sugar Sweetend Beverages", kfq_snack_modefreq ~ "Snacks", kfq_desert_modefreq ~ "Desert", kfq_cond_modefreq ~ "Condiments"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# strict/both risk
kfq_risk_both <- r01_qs_eat[r01_qs_eat$risk_status_both != 'Neither', c(9, 12, 10, 391, 393, 395, 397, 399, 401, 403, 405, 407)]
kfq_risk_both$risk_status_both <- droplevels(kfq_risk_both$risk_status_both)

kfq_risk_both$nNA <- rowSums(is.na(kfq_risk_both))
kfq_risk_both <- kfq_risk_both[kfq_risk_both$nNA < 9, ]

kfq_risk_both_tab <-
  tbl_summary(
    data = kfq_risk_both[1:8],
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", kfq_grains_modefreq ~ "Grains", kfq_veg_modefreq ~ "Vegetables", kfq_fruit_modefreq ~ "Fruit", kfq_dairy_modefreq ~ "Dairy", kfq_protein_modefreq ~ "Protein"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", kfq_grains_modefreq ~ "Grains", kfq_veg_modefreq ~ "Vegetables", kfq_fruit_modefreq ~ "Fruit", kfq_dairy_modefreq ~ "Dairy", kfq_protein_modefreq ~ "Protein"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

kfq_risk_both_tab_cont <-
  tbl_summary(
    data = kfq_risk_both[c(1, 9:12)],
    by = risk_status_both,
    value = list(kfq_bev_modefreq ~ "Sugar Sweetend Beverages", kfq_snack_modefreq ~ "Snacks", kfq_desert_modefreq ~ "Desert", kfq_cond_modefreq ~ "Condiments"),
    label = list(kfq_bev_modefreq ~ "Sugar Sweetend Beverages", kfq_snack_modefreq ~ "Snacks", kfq_desert_modefreq ~ "Desert", kfq_cond_modefreq ~ "Condiments"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

qs_kfq_merge_tab <-
  tbl_merge(
    tbls = list(kfq_tab, kfq_risk_mom_tab, kfq_risk_both_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )

qs_kfq_merge_tab_cont <-
  tbl_merge(
    tbls = list(kfq_tab_cont, kfq_risk_mom_tab_cont, kfq_risk_both_tab_cont),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )

## 2d) Child Eat Behavior ####

## all
child_eatbeh_v1 <- r01_qs_eat[c(12, 10, 432, 434, 436, 438, 440, 442, 479:488, 505, 588:592, 693, 723)]
child_eatbeh_v7 <- r01_qs_eat[c(12, 10, 768:777, 1018)]
child_eatbeh_v7$nNA <- rowSums(is.na(child_eatbeh_v7))
child_eatbeh_v7 <- child_eatbeh_v7[child_eatbeh_v7$nNA < 11, ]

child_eatbeh_v1_tab <-
  tbl_summary(
    data = child_eatbeh_v1,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", tesqe_avoid ~ "Avoid Temptations, TESQE", tesqe_control ~ "Control Tempations, TESQE", tesqe_distract ~ "Distraction, TESQE", tesqe_supress ~ "Supression, TESQE", tesqe_goal_rules ~ "Goals and Rules, TESQE", tesqe_goal_delib ~ "Goal Deliberation, TESQE", cebq_fr ~ "Food Responsiveness, CEBQ", cebq_eoe ~ "Emotional Overeating, CEBQ", cebq_ef ~ "Enjoyment of Food, CEBQ", cebq_dd ~ "Desire to Drink, CEBQ", cebq_sr ~ "Satiety Responsiveness, CEBQ", cebq_se ~ "Slowness in Eating, CEBQ", cebq_eue ~ "Emotional Undereating, CEBQ", cebq_ff ~ "Food Fussiness, CEBQ", cebq_approach ~ "Approach Behaviors, CEBQ", cebq_avoid ~ "Avoidant Behaviors, CEBQ", bes_total ~ "Total, Binge Eating Scale", lbc_misbeh ~ 'Food-Related Misbehavior, LBC', lbc_overeat ~ 'Overeating, LBC', lbc_em_overweight ~ 'Emotion Related to Overweight, LBC', lbc_pa ~ 'Physical Activity, LBC', lbc_total ~ 'Total, LBC', loc1 ~ 'Loss of Control-Eating', dg_wait ~ 'Delay of Gratification'),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", tesqe_avoid ~ "Avoid Temptations, TESQE", tesqe_control ~ "Control Tempations, TESQE", tesqe_distract ~ "Distraction, TESQE", tesqe_supress ~ "Supression, TESQE", tesqe_goal_rules ~ "Goals and Rules, TESQE", tesqe_goal_delib ~ "Goal Deliberation, TESQE", cebq_fr ~ "Food Responsiveness, CEBQ", cebq_eoe ~ "Emotional Overeating, CEBQ", cebq_ef ~ "Enjoyment of Food, CEBQ", cebq_dd ~ "Desire to Drink, CEBQ", cebq_sr ~ "Satiety Responsiveness, CEBQ", cebq_se ~ "Slowness in Eating, CEBQ", cebq_eue ~ "Emotional Undereating, CEBQ", cebq_ff ~ "Food Fussiness, CEBQ", cebq_approach ~ "Approach Behaviors, CEBQ", cebq_avoid ~ "Avoidant Behaviors, CEBQ", bes_total ~ "Total, Binge Eating Scale", lbc_misbeh ~ 'Food-Related Misbehavior, LBC', lbc_overeat ~ 'Overeating, LBC', lbc_em_overweight ~ 'Emotion Related to Overweight, LBC', lbc_pa ~ 'Physical Activity, LBC', lbc_total ~ 'Total, LBC', loc1 ~ 'Loss of Control-Eating', dg_wait ~ 'Delay of Gratification'),
    type = list(bes_total ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

child_eatbeh_v7_tab <-
  tbl_summary(
    data = child_eatbeh_v7[1:13],
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_cebq_fr ~ "Food Responsiveness, CEBQ", v7_cebq_eoe ~ "Emotional Overeating, CEBQ", v7_cebq_ef ~ "Enjoyment of Food, CEBQ", v7_cebq_dd ~ "Desire to Drink, CEBQ", v7_cebq_sr ~ "Satiety Responsiveness, CEBQ", v7_cebq_se ~ "Slowness in Eating, CEBQ", v7_cebq_eue ~ "Emotional Undereating, CEBQ", v7_cebq_ff ~ "Food Fussiness, CEBQ", v7_cebq_approach ~ "Approach Behaviors, CEBQ", v7_cebq_avoid ~ "Avoidant Behaviors, CEBQ"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_cebq_fr ~ "Food Responsiveness, CEBQ", v7_cebq_eoe ~ "Emotional Overeating, CEBQ", v7_cebq_ef ~ "Enjoyment of Food, CEBQ", v7_cebq_dd ~ "Desire to Drink, CEBQ", v7_cebq_sr ~ "Satiety Responsiveness, CEBQ", v7_cebq_se ~ "Slowness in Eating, CEBQ", v7_cebq_eue ~ "Emotional Undereating, CEBQ", v7_cebq_ff ~ "Food Fussiness, CEBQ", v7_cebq_approach ~ "Approach Behaviors, CEBQ", v7_cebq_avoid ~ "Avoidant Behaviors, CEBQ", v7_loc1 ~ "Loss of Control-Eating"),
    type = list(v7_cebq_eoe ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# mom risk
child_eatbeh_risk_mom_v1 <- r01_qs_eat[r01_qs_eat$risk_status_mom != 'Neither', c(8, 12, 10, 432, 434, 436, 438, 440, 442, 479:488, 505, 588:592, 693, 723)]
child_eatbeh_risk_mom_v1$risk_status_mom <- droplevels(child_eatbeh_risk_mom_v1$risk_status_mom)

child_eatbeh_risk_mom_v7 <- r01_qs_eat[r01_qs_eat$risk_status_mom != 'Neither', c(8, 12, 10, 768:777, 1018)]
child_eatbeh_risk_mom_v7$risk_status_mom <- droplevels(child_eatbeh_risk_mom_v7$risk_status_mom)

child_eatbeh_risk_mom_v7$nNA <- rowSums(is.na(child_eatbeh_risk_mom_v7))
child_eatbeh_risk_mom_v7 <- child_eatbeh_risk_mom_v7[child_eatbeh_risk_mom_v7$nNA < 11, ]

child_eatbeh_risk_mom_v1_tab <-
  tbl_summary(
    data = child_eatbeh_risk_mom_v1,
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", tesqe_avoid ~ "Avoid Temptations, TESQE", tesqe_control ~ "Control Tempations, TESQE", tesqe_distract ~ "Distraction, TESQE", tesqe_supress ~ "Supression, TESQE", tesqe_goal_rules ~ "Goals and Rules, TESQE", tesqe_goal_delib ~ "Goal Deliberation, TESQE", cebq_fr ~ "Food Responsiveness, CEBQ", cebq_eoe ~ "Emotional Overeating, CEBQ", cebq_ef ~ "Enjoyment of Food, CEBQ", cebq_dd ~ "Desire to Drink, CEBQ", cebq_sr ~ "Satiety Responsiveness, CEBQ", cebq_se ~ "Slowness in Eating, CEBQ", cebq_eue ~ "Emotional Undereating, CEBQ", cebq_ff ~ "Food Fussiness, CEBQ", cebq_approach ~ "Approach Behaviors, CEBQ", cebq_avoid ~ "Avoidant Behaviors, CEBQ", bes_total ~ "Total, Binge Eating Scale", lbc_misbeh ~ 'Food-Related Misbehavior, LBC', lbc_overeat ~ 'Overeating, LBC', lbc_em_overweight ~ 'Emotion Related to Overweight, LBC', lbc_pa ~ 'Physical Activity, LBC', lbc_total ~ 'Total, LBC', loc1 ~ 'Loss of Control-Eating', dg_wait ~ 'Delay of Gratification'),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", tesqe_avoid ~ "Avoid Temptations, TESQE", tesqe_control ~ "Control Tempations, TESQE", tesqe_distract ~ "Distraction, TESQE", tesqe_supress ~ "Supression, TESQE", tesqe_goal_rules ~ "Goals and Rules, TESQE", tesqe_goal_delib ~ "Goal Deliberation, TESQE", cebq_fr ~ "Food Responsiveness, CEBQ", cebq_eoe ~ "Emotional Overeating, CEBQ", cebq_ef ~ "Enjoyment of Food, CEBQ", cebq_dd ~ "Desire to Drink, CEBQ", cebq_sr ~ "Satiety Responsiveness, CEBQ", cebq_se ~ "Slowness in Eating, CEBQ", cebq_eue ~ "Emotional Undereating, CEBQ", cebq_ff ~ "Food Fussiness, CEBQ", cebq_approach ~ "Approach Behaviors, CEBQ", cebq_avoid ~ "Avoidant Behaviors, CEBQ", bes_total ~ "Total, Binge Eating Scale", lbc_misbeh ~ 'Food-Related Misbehavior, LBC', lbc_overeat ~ 'Overeating, LBC', lbc_em_overweight ~ 'Emotion Related to Overweight, LBC', lbc_pa ~ 'Physical Activity, LBC', lbc_total ~ 'Total, LBC', loc1 ~ 'Loss of Control-Eating', dg_wait ~ 'Delay of Gratification'),
    type = list(bes_total ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

child_eatbeh_risk_mom_v7_tab <-
  tbl_summary(
    data = child_eatbeh_risk_mom_v7[1:14],
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_cebq_fr ~ "Food Responsiveness, CEBQ", v7_cebq_eoe ~ "Emotional Overeating, CEBQ", v7_cebq_ef ~ "Enjoyment of Food, CEBQ", v7_cebq_dd ~ "Desire to Drink, CEBQ", v7_cebq_sr ~ "Satiety Responsiveness, CEBQ", v7_cebq_se ~ "Slowness in Eating, CEBQ", v7_cebq_eue ~ "Emotional Undereating, CEBQ", v7_cebq_ff ~ "Food Fussiness, CEBQ", v7_cebq_approach ~ "Approach Behaviors, CEBQ", v7_cebq_avoid ~ "Avoidant Behaviors, CEBQ"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_cebq_fr ~ "Food Responsiveness, CEBQ", v7_cebq_eoe ~ "Emotional Overeating, CEBQ", v7_cebq_ef ~ "Enjoyment of Food, CEBQ", v7_cebq_dd ~ "Desire to Drink, CEBQ", v7_cebq_sr ~ "Satiety Responsiveness, CEBQ", v7_cebq_se ~ "Slowness in Eating, CEBQ", v7_cebq_eue ~ "Emotional Undereating, CEBQ", v7_cebq_ff ~ "Food Fussiness, CEBQ", v7_cebq_approach ~ "Approach Behaviors, CEBQ", v7_cebq_avoid ~ "Avoidant Behaviors, CEBQ", v7_loc1 ~ "Loss of Control-Eating"),
    type = list(v7_cebq_eoe ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# strict/both risk
child_eatbeh_risk_both_v1 <- r01_qs_eat[r01_qs_eat$risk_status_both != 'Neither', c(9, 12, 10, 432, 434, 436, 438, 440, 442, 479:488, 505, 588:592, 693, 723)]
child_eatbeh_risk_both_v1$risk_status_both <- droplevels(child_eatbeh_risk_both_v1$risk_status_both)

child_eatbeh_risk_both_v7 <- r01_qs_eat[r01_qs_eat$risk_status_both != 'Neither', c(9, 12, 10, 768:777, 1018)]
child_eatbeh_risk_both_v7$risk_status_both <- droplevels(child_eatbeh_risk_both_v7$risk_status_both)

child_eatbeh_risk_both_v7$nNA <- rowSums(is.na(child_eatbeh_risk_both_v7))
child_eatbeh_risk_both_v7 <- child_eatbeh_risk_both_v7[child_eatbeh_risk_both_v7$nNA < 11, ]

child_eatbeh_risk_both_v1_tab <-
  tbl_summary(
    data = child_eatbeh_risk_both_v1,
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", tesqe_avoid ~ "Avoid Temptations, TESQE", tesqe_control ~ "Control Tempations, TESQE", tesqe_distract ~ "Distraction, TESQE", tesqe_supress ~ "Supression, TESQE", tesqe_goal_rules ~ "Goals and Rules, TESQE", tesqe_goal_delib ~ "Goal Deliberation, TESQE", cebq_fr ~ "Food Responsiveness, CEBQ", cebq_eoe ~ "Emotional Overeating, CEBQ", cebq_ef ~ "Enjoyment of Food, CEBQ", cebq_dd ~ "Desire to Drink, CEBQ", cebq_sr ~ "Satiety Responsiveness, CEBQ", cebq_se ~ "Slowness in Eating, CEBQ", cebq_eue ~ "Emotional Undereating, CEBQ", cebq_ff ~ "Food Fussiness, CEBQ", cebq_approach ~ "Approach Behaviors, CEBQ", cebq_avoid ~ "Avoidant Behaviors, CEBQ", bes_total ~ "Total, Binge Eating Scale", lbc_misbeh ~ 'Food-Related Misbehavior, LBC', lbc_overeat ~ 'Overeating, LBC', lbc_em_overweight ~ 'Emotion Related to Overweight, LBC', lbc_pa ~ 'Physical Activity, LBC', lbc_total ~ 'Total, LBC', loc1 ~ 'Loss of Control-Eating', dg_wait ~ 'Delay of Gratification'),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", tesqe_avoid ~ "Avoid Temptations, TESQE", tesqe_control ~ "Control Tempations, TESQE", tesqe_distract ~ "Distraction, TESQE", tesqe_supress ~ "Supression, TESQE", tesqe_goal_rules ~ "Goals and Rules, TESQE", tesqe_goal_delib ~ "Goal Deliberation, TESQE", cebq_fr ~ "Food Responsiveness, CEBQ", cebq_eoe ~ "Emotional Overeating, CEBQ", cebq_ef ~ "Enjoyment of Food, CEBQ", cebq_dd ~ "Desire to Drink, CEBQ", cebq_sr ~ "Satiety Responsiveness, CEBQ", cebq_se ~ "Slowness in Eating, CEBQ", cebq_eue ~ "Emotional Undereating, CEBQ", cebq_ff ~ "Food Fussiness, CEBQ", cebq_approach ~ "Approach Behaviors, CEBQ", cebq_avoid ~ "Avoidant Behaviors, CEBQ", bes_total ~ "Total, Binge Eating Scale", lbc_misbeh ~ 'Food-Related Misbehavior, LBC', lbc_overeat ~ 'Overeating, LBC', lbc_em_overweight ~ 'Emotion Related to Overweight, LBC', lbc_pa ~ 'Physical Activity, LBC', lbc_total ~ 'Total, LBC', loc1 ~ 'Loss of Control-Eating', dg_wait ~ 'Delay of Gratification'),
    type = list(bes_total ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

child_eatbeh_risk_both_v7_tab <-
  tbl_summary(
    data = child_eatbeh_risk_both_v7[1:14],
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_cebq_fr ~ "Food Responsiveness, CEBQ", v7_cebq_eoe ~ "Emotional Overeating, CEBQ", v7_cebq_ef ~ "Enjoyment of Food, CEBQ", v7_cebq_dd ~ "Desire to Drink, CEBQ", v7_cebq_sr ~ "Satiety Responsiveness, CEBQ", v7_cebq_se ~ "Slowness in Eating, CEBQ", v7_cebq_eue ~ "Emotional Undereating, CEBQ", v7_cebq_ff ~ "Food Fussiness, CEBQ", v7_cebq_approach ~ "Approach Behaviors, CEBQ", v7_cebq_avoid ~ "Avoidant Behaviors, CEBQ"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", v7_cebq_fr ~ "Food Responsiveness, CEBQ", v7_cebq_eoe ~ "Emotional Overeating, CEBQ", v7_cebq_ef ~ "Enjoyment of Food, CEBQ", v7_cebq_dd ~ "Desire to Drink, CEBQ", v7_cebq_sr ~ "Satiety Responsiveness, CEBQ", v7_cebq_se ~ "Slowness in Eating, CEBQ", v7_cebq_eue ~ "Emotional Undereating, CEBQ", v7_cebq_ff ~ "Food Fussiness, CEBQ", v7_cebq_approach ~ "Approach Behaviors, CEBQ", v7_cebq_avoid ~ "Avoidant Behaviors, CEBQ", v7_loc1 ~ "Loss of Control-Eating"),
    type = list(v7_cebq_eoe ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

child_eatbeh_merge_v1_tab <-
  tbl_merge(
    tbls = list(child_eatbeh_v1_tab, child_eatbeh_risk_mom_v1_tab, child_eatbeh_risk_both_v1_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )

child_eatbeh_merge_v7_tab <-
  tbl_merge(
    tbls = list(child_eatbeh_v7_tab, child_eatbeh_risk_mom_v7_tab, child_eatbeh_risk_both_v7_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )

## 2e) Child Body Perception ####
body_img <- r01_qs_eat[c(12, 10, 685, 690:691)]

body_img$nNA <- rowSums(is.na(body_img))
body_img <- body_img[body_img$nNA < 3, ]

body_img_tab <-
  tbl_summary(
    data = body_img[1:5],
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", cwc_total ~ "Total, CWC", cbis_score ~ "Difference (Percieved - Ideal), CBIS", cbis_score_abs ~ "Difference (|Percieved - Ideal|), CBIS"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", cwc_total ~ "Total, CWC", cbis_score ~ "Difference (Percieved - Ideal), CBIS", cbis_score_abs ~ "Difference (|Percieved - Ideal|), CBIS"),
    type = list(cbis_score ~ 'continuous', cbis_score_abs ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# mom risk
body_img_mom_risk <- r01_qs_eat[r01_qs_eat$risk_status_mom != 'Neither', c(8, 12, 10, 685, 690:691)]
body_img_mom_risk$risk_status_mom <- droplevels(body_img_mom_risk$risk_status_mom)

body_img_mom_risk$nNA <- rowSums(is.na(body_img_mom_risk))
body_img_mom_risk <- body_img_mom_risk[body_img_mom_risk$nNA < 3, ]

body_img_mom_risk_tab <-
  tbl_summary(
    data = body_img_mom_risk[1:6],
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", cwc_total ~ "Total, CWC", cbis_score ~ "Difference (Percieved - Ideal), CBIS", cbis_score_abs ~ "Difference (|Percieved - Ideal|), CBIS"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", cwc_total ~ "Total, CWC", cbis_score ~ "Difference (Percieved - Ideal), CBIS", cbis_score_abs ~ "Difference (|Percieved - Ideal|), CBIS"),
    type = list(cbis_score ~ 'continuous', cbis_score_abs ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# strict/both risk
body_img_both_risk <- r01_qs_eat[r01_qs_eat$risk_status_both != 'Neither', c(9, 12, 10, 685, 690:691)]
body_img_both_risk$risk_status_both <- droplevels(body_img_both_risk$risk_status_both)

body_img_both_risk$nNA <- rowSums(is.na(body_img_both_risk))
body_img_both_risk <- body_img_both_risk[body_img_both_risk$nNA < 3, ]

body_img_both_risk_tab <-
  tbl_summary(
    data = body_img_both_risk[1:6],
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", cwc_total ~ "Total, CWC", cbis_score ~ "Difference (Percieved - Ideal), CBIS", cbis_score_abs ~ "Difference (|Percieved - Ideal|), CBIS"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", cwc_total ~ "Total, CWC", cbis_score ~ "Difference (Percieved - Ideal), CBIS", cbis_score_abs ~ "Difference (|Percieved - Ideal|), CBIS"),
    type = list(cbis_score ~ 'continuous', cbis_score_abs ~ 'continuous'),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

qs_body_img_merge_tab <-
  tbl_merge(
    tbls = list(body_img_tab, body_img_mom_risk_tab, body_img_both_risk_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )

## 2f) Parent Eating Behavior ####
parent_eatbeh <- r01_qs_eat[c(12, 10, 622:624, 676:678)]

parent_eatbeh_tab <-
  tbl_summary(
    data = parent_eatbeh,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", pwlb_healthy ~ "Healthy Strategy, PWLB", pwlb_unhealthy ~ "Unhealthy Strategy, PWLB", pwlb_total ~ "Total, PWLB", tfeq_cogcontrol ~ "Cognitive Control, TFEQ", tfeq_disinhibition ~ "Disinhibition, TFEQ", tfeq_hunger ~ "Susceptibility to Hunger, TFEQ"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", pwlb_healthy ~ "Healthy Strategy, PWLB", pwlb_unhealthy ~ "Unhealthy Strategy, PWLB", pwlb_total ~ "Total, PWLB", tfeq_cogcontrol ~ "Cognitive Control, TFEQ", tfeq_disinhibition ~ "Disinhibition, TFEQ", tfeq_hunger ~ "Susceptibility to Hunger, TFEQ"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)


# mom risk
parent_eatbeh_risk_mom <- r01_qs_eat[r01_qs_eat$risk_status_mom != 'Neither', c(8, 12, 10, 622:624, 676:678)]
parent_eatbeh_risk_mom$risk_status_mom <- droplevels(parent_eatbeh_risk_mom$risk_status_mom)

parent_eatbeh_risk_mom_tab <-
  tbl_summary(
    data = parent_eatbeh_risk_mom,
    by = risk_status_mom,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", pwlb_healthy ~ "Healthy Strategy, PWLB", pwlb_unhealthy ~ "Unhealthy Strategy, PWLB", pwlb_total ~ "Total, PWLB", tfeq_cogcontrol ~ "Cognitive Control, TFEQ", tfeq_disinhibition ~ "Disinhibition, TFEQ", tfeq_hunger ~ "Susceptibility to Hunger, TFEQ"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", pwlb_healthy ~ "Healthy Strategy, PWLB", pwlb_unhealthy ~ "Unhealthy Strategy, PWLB", pwlb_total ~ "Total, PWLB", tfeq_cogcontrol ~ "Cognitive Control, TFEQ", tfeq_disinhibition ~ "Disinhibition, TFEQ", tfeq_hunger ~ "Susceptibility to Hunger, TFEQ"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

# strict/both risk
parent_eatbeh_risk_both <- r01_qs_eat[r01_qs_eat$risk_status_both != 'Neither', c(9, 12, 10, 622:624, 676:678)]
parent_eatbeh_risk_both$risk_status_both <- droplevels(parent_eatbeh_risk_both$risk_status_both)

parent_eatbeh_risk_both_tab <-
  tbl_summary(
    data = parent_eatbeh_risk_both,
    by = risk_status_both,
    value = list(age_yr ~ "Age, yr", sex ~ "Sex", pwlb_healthy ~ "Healthy Strategy, PWLB", pwlb_unhealthy ~ "Unhealthy Strategy, PWLB", pwlb_total ~ "Total, PWLB", tfeq_cogcontrol ~ "Cognitive Control, TFEQ", tfeq_disinhibition ~ "Disinhibition, TFEQ", tfeq_hunger ~ "Susceptibility to Hunger, TFEQ"),
    label = list(age_yr ~ "Age, yr", sex ~ "Sex", pwlb_healthy ~ "Healthy Strategy, PWLB", pwlb_unhealthy ~ "Unhealthy Strategy, PWLB", pwlb_total ~ "Total, PWLB", tfeq_cogcontrol ~ "Cognitive Control, TFEQ", tfeq_disinhibition ~ "Disinhibition, TFEQ", tfeq_hunger ~ "Susceptibility to Hunger, TFEQ"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

parent_eatbeh_merge_tab <-
  tbl_merge(
    tbls = list(parent_eatbeh_tab, parent_eatbeh_risk_mom_tab, parent_eatbeh_risk_both_tab),
    tab_spanner = c("**All**", "**Risk Status - Mom BMI**", "**Risk Status - Strict**")
  )
