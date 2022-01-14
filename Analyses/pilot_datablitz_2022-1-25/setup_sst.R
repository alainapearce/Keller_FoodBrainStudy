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
r01_sst_long <- read.csv("data_2022-01-25/task-sst_summary_blockslong.tsv", header = TRUE, sep = "\t")
r01_sst_cond <- read.csv("data_2022-01-25/task-sst_summary_condwide.tsv", header = TRUE, sep = "\t")

#merge
r01_sst_long <- merge(r01_demo[c(1:16, 337:338, 19:24)], r01_sst_long, by = 'sub', all.x = FALSE, all.y = TRUE)
r01_sst_cond <- merge(r01_demo[c(1:16, 337:338, 19:24)], r01_sst_cond, by = 'sub', all.x = FALSE, all.y = TRUE)

#remove 2 that were removed for ADHD
r01_sst_long <- r01_sst_long[r01_sst_long$sub != 31 & r01_sst_long$sub != 34, ]
r01_sst_cond <- r01_sst_cond[r01_sst_cond$sub != 31 & r01_sst_cond$sub != 34, ]

#make long by condition - ED
r01_sst_cond$ED_racehorse_check <- ifelse(r01_sst_cond$h_ed_racehorse_check == 1 & r01_sst_cond$l_ed_racehorse_check == 1, 1, 0)

r01_sst_EDlong <- melt(r01_sst_cond[!is.na(r01_sst_cond$ED_racehorse_check) & r01_sst_cond$ED_racehorse_check == 1, c(1:24, 39, 53)], id.vars = names(r01_sst_cond)[1:24])
r01_sst_EDlong$ED <- ifelse(r01_sst_EDlong$variable == 'h_ed_racehorse_check', 'High ED', 'Low ED')
r01_sst_EDlong$ED <- factor(r01_sst_EDlong$ED, levels = c('Low ED', 'High ED'))

r01_sst_EDlong$racehorse_check <- r01_sst_EDlong$value

goRT_EDlong <- melt(r01_sst_cond[!is.na(r01_sst_cond$ED_racehorse_check) & r01_sst_cond$ED_racehorse_check == 1, c(42, 56)])
names(goRT_EDlong)[2] <- 'go_rt'
nError_EDlong <- melt(r01_sst_cond[!is.na(r01_sst_cond$ED_racehorse_check) & r01_sst_cond$ED_racehorse_check == 1, c(45, 59)])
names(nError_EDlong)[2] <- 'n_error'
nMiss_EDlong <- melt(r01_sst_cond[!is.na(r01_sst_cond$ED_racehorse_check) & r01_sst_cond$ED_racehorse_check == 1, c(47, 61)])
names(nMiss_EDlong)[2] <- 'n_miss'
pResp_EDlong <- melt(r01_sst_cond[!is.na(r01_sst_cond$ED_racehorse_check) & r01_sst_cond$ED_racehorse_check == 1, c(48, 62)])
names(pResp_EDlong)[2] <- 'prop_resp'
ssd_EDlong <- melt(r01_sst_cond[!is.na(r01_sst_cond$ED_racehorse_check) & r01_sst_cond$ED_racehorse_check == 1, c(50, 64)])
names(ssd_EDlong)[2] <- 'ssd'
ssrtMean_EDlong <- melt(r01_sst_cond[!is.na(r01_sst_cond$ED_racehorse_check) & r01_sst_cond$ED_racehorse_check == 1, c(51, 65)])
names(ssrtMean_EDlong)[2] <- 'ssrt_mean'
ssrtInt_EDlong <- melt(r01_sst_cond[!is.na(r01_sst_cond$ED_racehorse_check) & r01_sst_cond$ED_racehorse_check == 1, c(52, 66)])
names(ssrtInt_EDlong)[2] <- 'ssrt_int'

r01_sst_EDlong <- cbind.data.frame(r01_sst_EDlong[c(1:24, 27:28)], goRT_EDlong[2], nError_EDlong[2], nMiss_EDlong[2], pResp_EDlong[2], ssd_EDlong[2], ssrtMean_EDlong[2], ssrtInt_EDlong[2])

#make long by condition - PS
r01_sst_cond$PS_racehorse_check <- ifelse(r01_sst_cond$l_port_racehorse_check == 1 & r01_sst_cond$s_port_racehorse_check == 1, 1, 0)

r01_sst_PSlong <- melt(r01_sst_cond[!is.na(r01_sst_cond$PS_racehorse_check) & r01_sst_cond$PS_racehorse_check == 1, c(1:24, 67, 81)], id.vars = names(r01_sst_cond)[1:24])
r01_sst_PSlong$PS <- ifelse(r01_sst_PSlong$variable == 'l_port_racehorse_check', 'Large PS', 'Small PS')
r01_sst_PSlong$PS <- factor(r01_sst_PSlong$PS, levels = c('Small PS', 'Large PS'))


r01_sst_PSlong$racehorse_check <- r01_sst_PSlong$value

goRT_PSlong <- melt(r01_sst_cond[!is.na(r01_sst_cond$PS_racehorse_check) & r01_sst_cond$PS_racehorse_check == 1, c(70, 84)])
names(goRT_PSlong)[2] <- 'go_rt'
nError_PSlong <- melt(r01_sst_cond[!is.na(r01_sst_cond$PS_racehorse_check) & r01_sst_cond$PS_racehorse_check == 1, c(73, 87)])
names(nError_PSlong)[2] <- 'n_error'
nMiss_PSlong <- melt(r01_sst_cond[!is.na(r01_sst_cond$PS_racehorse_check) & r01_sst_cond$PS_racehorse_check == 1, c(75, 89)])
names(nMiss_PSlong)[2] <- 'n_miss'
pResp_PSlong <- melt(r01_sst_cond[!is.na(r01_sst_cond$PS_racehorse_check) & r01_sst_cond$PS_racehorse_check == 1, c(76, 90)])
names(pResp_PSlong)[2] <- 'prop_resp'
ssd_PSlong <- melt(r01_sst_cond[!is.na(r01_sst_cond$PS_racehorse_check) & r01_sst_cond$PS_racehorse_check == 1, c(78, 92)])
names(ssd_PSlong)[2] <- 'ssd'
ssrtMean_PSlong <- melt(r01_sst_cond[!is.na(r01_sst_cond$PS_racehorse_check) & r01_sst_cond$PS_racehorse_check == 1, c(79, 93)])
names(ssrtMean_PSlong)[2] <- 'ssrt_mean'
ssrtInt_PSlong <- melt(r01_sst_cond[!is.na(r01_sst_cond$PS_racehorse_check) & r01_sst_cond$PS_racehorse_check == 1, c(80, 94)])
names(ssrtInt_PSlong)[2] <- 'ssrt_int'

r01_sst_PSlong <- cbind.data.frame(r01_sst_PSlong[c(1:24, 27:28)], goRT_PSlong[2], nError_PSlong[2], nMiss_PSlong[2], pResp_PSlong[2], ssd_PSlong[2], ssrtMean_PSlong[2], ssrtInt_PSlong[2])

#check all conditions for racehorse
racehorse_check_fn <- function(data, id){
  id_data <- data[data$sub == id,]
  ncond <- sum(id_data$racehorse_check == 1)
  return(ncond)
}

r01_sst_long$ncond_racehorse_good <- sapply(r01_sst_long$sub, FUN = racehorse_check_fn, data = r01_sst_long)

#make conditions for interaction among all blocks
r01_sst_long$ED <- ifelse(r01_sst_long$condition == 'hED_sPort' | r01_sst_long$condition == 'hED_lPort', 'High ED', 'Low ED')
r01_sst_long$ED <- factor(r01_sst_long$ED, levels = c('Low ED', 'High ED'))
r01_sst_long$PS <- ifelse(r01_sst_long$condition == 'hED_sPort' | r01_sst_long$condition == 'lED_sPort', 'Small PS', 'Large PS')
r01_sst_long$PS <- factor(r01_sst_long$PS, levels = c('Small PS', 'Large PS'))
r01_sst_long$block <- factor(r01_sst_long$block)

# get orders

order_fn <- function(data, sub, cond){
  sub_order <- data[data[['sub']] == sub, 'condition']

  if (cond == 'ED'){
    ED_order <- as.numeric(grepl('hED', sub_order, fixed = TRUE))
    ED_order <- paste(ifelse(ED_order == 1, 'hED', 'lED'), collapse = '_')
    return(ED_order)
  }

  if (cond == 'PS') {
    PS_order <- as.numeric(grepl('lPort', sub_order, fixed = TRUE))
    PS_order <- paste(ifelse(PS_order == 1, 'lPS', 'sPS'), collapse = '_')
    return(PS_order)
  }

}

r01_sst_EDlong$order <- sapply(r01_sst_EDlong[['sub']], FUN = order_fn, data = r01_sst_long, cond = 'ED')
r01_sst_EDlong$order <- as.factor(r01_sst_EDlong$order)


r01_sst_PSlong$order <- sapply(r01_sst_PSlong[['sub']], FUN = order_fn, data = r01_sst_long, cond = 'PS')
r01_sst_PSlong$order <- as.factor(r01_sst_PSlong$order)

## 2) Tables ####

## 2a) All Table ####


# names need to match to merge
sst_all <- r01_sst_cond[r01_sst_cond$all_racehorse_check == 1, c(28, 31, 33:34, 36:38)]
sst_all_ED <- r01_sst_EDlong[c(25,27:33)]
sst_all_PS <- r01_sst_PSlong[c(25, 27:33)]

names(sst_all)[1:7] <- names(sst_all_ED)[2:8]

sst_all_tab <-
  tbl_summary(
    data=sst_all,
    value = list(go_rt ~ "Go Mean RT, ms", n_error ~ "L/R Error, N", n_miss ~ "Missed, N", prop_resp ~ "P(Resp|Stop Signal)", ssd ~ "SSD, ms", ssrt_mean ~ "SSRT - Mean, ms", ssrt_int ~ "SSRT - Integration, ms"),
    label = list(go_rt ~ "Go Mean RT, ms", n_error ~ "L/R Error, N", n_miss ~ "Missed, N", prop_resp ~ "P(Resp|Stop Signal)", ssd ~ "SSD, ms", ssrt_mean ~ "SSRT - Mean, ms", ssrt_int ~ "SSRT - Integration, ms"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

sst_all_ED_tab <-
  tbl_summary(
    data=sst_all_ED,
    by = ED,
    value = list(go_rt ~ "Go Mean RT, ms", n_error ~ "L/R Error, N", n_miss ~ "Missed, N", prop_resp ~ "P(Resp|Stop Signal)", ssd ~ "SSD, ms", ssrt_mean ~ "SSRT - Mean, ms", ssrt_int ~ "SSRT - Integration, ms"),
    label = list(go_rt ~ "Go Mean RT, ms", n_error ~ "L/R Error, N", n_miss ~ "Missed, N", prop_resp ~ "P(Resp|Stop Signal)", ssd ~ "SSD, ms", ssrt_mean ~ "SSRT - Mean, ms", ssrt_int ~ "SSRT - Integration, ms"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

sst_all_PS_tab <-
  tbl_summary(
    data=sst_all_PS,
    by = PS,
    value = list(go_rt ~ "Go Mean RT, ms", n_error ~ "L/R Error, N", n_miss ~ "Missed, N", prop_resp ~ "P(Resp|Stop Signal)", ssd ~ "SSD, ms", ssrt_mean ~ "SSRT - Mean, ms", ssrt_int ~ "SSRT - Integration, ms"),
    label = list(go_rt ~ "Go Mean RT, ms", n_error ~ "L/R Error, N", n_miss ~ "Missed, N", prop_resp ~ "P(Resp|Stop Signal)", ssd ~ "SSD, ms", ssrt_mean ~ "SSRT - Mean, ms", ssrt_int ~ "SSRT - Integration, ms"),
    statistic = all_continuous() ~ c("{mean} [{min} - {max}]"),
    missing = "ifany",
    digits = all_continuous() ~ 1)

sst_all_merge_tab <-
  tbl_merge(
    tbls = list(sst_all_tab, sst_all_ED_tab, sst_all_PS_tab),
    tab_spanner = c("**All Trials**", "**Energy Density Trial**", "**Portion Size Trials**")
  )

## 2b) Mom Risk Status Table ####
