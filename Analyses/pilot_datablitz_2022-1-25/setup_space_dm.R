# This script was written by Alaina Pearce in January 2022
# to process Space Game Decision Making model data
# for the Food and Brain Study Data Blitz Meeting
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
r01_space_dm <- read.csv("data_2022-01-25/task-space_dm_summary.tsv", header = TRUE, sep = "\t")

r01_space_dm$model <- ifelse(r01_space_dm$model == 'HybridModel_NoStimSticky_NoRespSticky', 'hybrid', ifelse(r01_space_dm$model == 'ModelBased_NoStimSticky_NoRespSticky', 'mb', ifelse(r01_space_dm$model == 'ModelFree_NoStimSticky_NoRespSticky', 'mf', ifelse(r01_space_dm$model == 'HybridModel_StimSticky_NoRespSticky', 'hybrid_stimstick', ifelse(r01_space_dm$model == 'ModelBased_StimSticky_NoRespSticky', 'mb_stimstick', ifelse(r01_space_dm$model == 'ModelFree_StimSticky_NoRespSticky', 'mf_stimstick', ifelse(r01_space_dm$model == 'HybridModel_NoStimSticky_RespSticky', 'hybrid_respstick', ifelse(r01_space_dm$model == 'ModelBased_NoStimSticky_RespSticky', 'mb_respstick', ifelse(r01_space_dm$model == 'ModelFree_NoStimSticky_RespSticky', 'mf_respstick', ifelse(r01_space_dm$model == 'HybridModel_StimSticky_RespSticky', 'hybrid_stimstick_respstick', ifelse(r01_space_dm$model == 'ModelBased_StimSticky_RespSticky', 'mb_simstick_respstick', ifelse(r01_space_dm$model == 'ModelFree_StimSticky_RespSticky', 'mf_stimstick_respstick', NA))))))))))))

## 2) Clean Decision Making Data ####

## Participant Loop for Best model

## McFadden's R^2: (R -  loglikelihood)/R where R is the log-likelihood for the chance model (ntrials*ln(1/2))
# reference and link to the original McFadden article where he defines his pseudo-R2 measure:
# McFadden, D. (1974) “Conditional logit analysis of qualitative choice behavior.” Pp. 105-142 in P. Zarembka (ed.), Frontiers in Econometrics. Academic Press. elsa.berkeley.edu/reprints/mcfadden/zarembka.pdf

R = 100*log(1/2)

r01_space_dm$bic_comp = (2*(r01_space_dm$loglikelihood-R))-((r01_space_dm$params-1)*(log(100)))

r01_space_dm$mc_fadden_r = (R - r01_space_dm$loglikelihood)/R

r01_space_dmfit = data.frame(r01_space_dm[1:2])
r01_space_dmfit$bic_fit = 'NA'
r01_space_dmfit$aic_fit = 'NA'
r01_space_dmfit$loglikelihood_fit = 'NA'
r01_space_dmfit$mc_fadden_r_fit = 'NA'

for(r in 1:nrow(r01_space_dmfit)){
  sub = r01_space_dmfit[[r, 'sub']]
  parDat = r01_space_dm[r01_space_dm$sub == sub, ]
  bic_mod = parDat[parDat$bic == min(parDat$bic), ]$model
  aic_mod = parDat[parDat$aic == min(parDat$aic), ]$model
  ll_mod = parDat[parDat$loglikelihood == max(parDat$loglikelihood), ]$model
  r_mod = parDat[parDat$mc_fadden_r == max(parDat$mc_fadden_r), ]$model
  r01_space_dmfit[r, 'bic_fit'] = as.character(bic_mod)
  r01_space_dmfit[r, 'aic_fit'] = as.character(aic_mod)
  r01_space_dmfit[r, 'loglikelihood_fit'] = as.character(ll_mod)
  r01_space_dmfit[r, 'mc_fadden_r_fit'] = as.character(r_mod)
}

mc_fadden_fit_tab = xtabs(~mc_fadden_r_fit, data = r01_space_dmfit)

## model Loop for average values
dm_names = levels(factor(r01_space_dm$model))
dm_fit = data.frame(loglikelihood = rep(as.double(NA), 12),
                    bic_mean = rep(as.double(NA), 12),
                    aic_mean = rep(as.double(NA), 12),
                    ind_mc_fadden_r_mean = rep(as.double(NA), 12),
                    ind_mc_fadden_r_min = rep(as.double(NA), 12),
                    ind_mc_fadden_r_max = rep(as.double(NA), 12))
dm_fit$model = dm_names

for(dm in 1:12){
  mod = dm_names[dm]
  mod_dat = r01_space_dm[r01_space_dm$model == mod, ]
  dm_fit[dm, 'loglikelihood'] = round(mean(mod_dat[[11]]), 3)
  dm_fit[dm, 'bic_mean'] = round(mean(mod_dat[[12]]), 3)
  dm_fit[dm, 'aic_mean'] = round(mean(mod_dat[[13]]), 3)
  dm_fit[dm, 'ind_mc_fadden_r_mean'] = round(mean(mod_dat[[16]]), 3)
  dm_fit[dm, 'ind_mc_fadden_r_min'] = round(min(mod_dat[[16]]), 3)
  dm_fit[dm, 'ind_mc_fadden_r_max'] = round(max(mod_dat[[16]]), 3)
}

## overall McFadden R
dm_fit$mc_fadden_r_mod = (R - dm_fit$loglikelihood)/R

## compare fits - likelihood ratio test
dm_fit$n2loglikelihood = -2*dm_fit$loglikelihood

# Hybrid models
dm_fit$hybrid_base_pchi = NA
dm_fit$hybrid_base_pchi[2] = pchisq((dm_fit[dm_fit$model == 'hybrid', 'n2loglikelihood'] - dm_fit[dm_fit$model == 'hybrid_respstick', 'n2loglikelihood']), 1)
dm_fit$hybrid_base_pchi[3] = pchisq((dm_fit[dm_fit$model == 'hybrid', 'n2loglikelihood'] - dm_fit[dm_fit$model == 'hybrid_stimstick', 'n2loglikelihood']), 1)
dm_fit$hybrid_base_pchi[4] = pchisq((dm_fit[dm_fit$model == 'hybrid', 'n2loglikelihood'] - dm_fit[dm_fit$model == 'hybrid_stimstick_respstick', 'n2loglikelihood']), 2)
dm_fit$hybrid_base_pchi[5] = pchisq((dm_fit[dm_fit$model == 'mb', 'n2loglikelihood'] - dm_fit[dm_fit$model == 'hybrid', 'n2loglikelihood']), 1)
dm_fit$hybrid_base_pchi[9] = pchisq((dm_fit[dm_fit$model == 'mf', 'n2loglikelihood'] - dm_fit[dm_fit$model == 'hybrid', 'n2loglikelihood']), 1)

# model Based models
dm_fit$model_base_pchi = NA
dm_fit$model_base_pchi[6] = pchisq((dm_fit[dm_fit$model == 'mb', 'n2loglikelihood'] - dm_fit[dm_fit$model == 'mb_respstick', 'n2loglikelihood']), 1)
dm_fit$model_base_pchi[7] = pchisq((dm_fit[dm_fit$model == 'mb', 'n2loglikelihood'] - dm_fit[dm_fit$model == 'mb_simstick_respstick', 'n2loglikelihood']), 2)
dm_fit$model_base_pchi[8] = pchisq((dm_fit[dm_fit$model == 'mb', 'n2loglikelihood'] - dm_fit[dm_fit$model == 'mb_stimstick', 'n2loglikelihood']), 1)

# model Free models
dm_fit$model_free_base_pchi = NA
dm_fit$model_free_base_pchi[10] = pchisq((dm_fit[dm_fit$model == 'mf', 'n2loglikelihood'] - dm_fit[dm_fit$model == 'mf_respstick', 'n2loglikelihood']), 1)
dm_fit$model_free_base_pchi[11] = pchisq((dm_fit[dm_fit$model == 'mf', 'n2loglikelihood'] - dm_fit[dm_fit$model == 'mf_stimstick', 'n2loglikelihood']), 1)
dm_fit$model_free_base_pchi[12] = pchisq((dm_fit[dm_fit$model == 'mf', 'n2loglikelihood'] -  dm_fit[dm_fit$model == 'mf_stimstick_respstick', 'n2loglikelihood']), 2)

best_mod_bic = dm_fit[dm_fit$bic == min(dm_fit$bic), ]$model
best_mod_aic = dm_fit[dm_fit$aic == min(dm_fit$aic), ]$model
best_mod_n2ll = dm_fit[dm_fit$n2loglikelihood == min(dm_fit$n2loglikelihood), ]$model
best_mod_mc_fadden_r = dm_fit[dm_fit$mc_fadden_r_mod == max(dm_fit$mc_fadden_r_mod), ]$model


## function for mode
mode <- function(x) {
  uniqv <- unique(x)
  uniqv[which.max(tabulate(match(x, uniqv)))]
}

n_mod_best <- mode(as.factor(c(best_mod_bic, best_mod_aic, best_mod_n2ll, best_mod_mc_fadden_r)))

if (length(n_mod_best) == 1){
  # Reduce Space Game Database to best model
  r01_space_dm_best = r01_space_dm[r01_space_dm$model == n_mod_best, ]
} else {
  stop('manual choice required')
}


