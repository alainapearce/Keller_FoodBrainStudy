# This script was written by Alaina Pearce in January 2022
# to set up functions needed for the Food and Brain Study
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

## gtsummary table functions ####

my_ttest <- function(data, variable, by, ...) {
  round(t.test(data[[variable]] ~ as.factor(data[[by]]))$p.value, 3)
}

my_chifisher <- function(data, variable, by, ...) {
  tab <- xtabs(~data[[variable]] + data[[by]])
  if (min(tab) <= 5){
    round(fisher.test(tab)$p.value, 3)
  } else {
    round(chisq.test(tab)$p.value, 3)
  }
}
