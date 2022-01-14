############ Basic Data Load/Setup ############
library(reporttools)
library(xtable)
library(car)
library(lme4)
library(lmerTest)
library(ggplot2)
library(MASS)
library(lsmeans)
library(reshape)
library(lsr)
#library(LDdiag)
library(stats)
library(mediation)
library(lavaan)
library(emmeans)
library(rstudioapi)

#### set up ####

#set working directory to location of script--not needed when called 
#through Rmarkdown doc. Uncomment below if running locally/manually
this.dir = getActiveDocumentContext()$path
setwd(dirname(this.dir))

source('functions.R')

#### Load Task Data ####
R01_GNG = read.csv("Data/GNG_database_19-Feb-2020.csv")
R01_GNG_long = read.csv("Data/GNG_database_BlocksLong_19-Feb-2020.csv")

R01_Nback = read.csv("Data/NBack_database_23-Mar-2020.csv")
R01_Nback_long = read.csv("Data/NBack_database_LoadLong_23-Mar-2020.csv")

R01_SST = read.csv("Data/SST_database_23-Mar-2020.csv")
R01_SST_long = read.csv("Data/SST_database_BlockLong_23-Mar-2020.csv")

R01_SpaceGame = read.csv("Data/SpaceGame_database_21-Feb-2020.csv")
R01_SpaceGame_long = read.csv("Data/SpaceGame_database_BlocksLong_21-Feb-2020.csv")
R01_SpaceGame_DM = read.csv("Data/SpaceGame_DM_database_21-Feb-2020.csv")

#### Load fMRI Data ####
R01_fMRI = read.csv("Data/RiskStatus_2sampleT_3.31.20.csv")

#### Assign Group Membership to data ####
GroupMembership = read.csv("Data/GroupMembership.csv")
GroupMembership = GroupMembership[GroupMembership$Risk.Group == "Low" | GroupMembership$Risk.Group == "High", ]

## R01_GNG
R01_GNG = merge(R01_GNG, GroupMembership[c(1,3)], by.x = "ParID", by.y = "ParticipantID", all.y = FALSE)
R01_GNG_long = merge(R01_GNG_long, GroupMembership[c(1,3)], by.x = "ParID", by.y = "ParticipantID", all.y = FALSE)

## R01_Nback
R01_Nback = merge(R01_Nback, GroupMembership[c(1,3)], by.x = "ParID", by.y = "ParticipantID", all.y = FALSE)
R01_Nback_long = merge(R01_Nback_long, GroupMembership[c(1,3)], by.x = "ParID", by.y = "ParticipantID", all.y = FALSE)
R01_Nback$Risk.Group = factor(R01_Nback$Risk.Group, levels = c("High", "Low"))
R01_Nback_long$Risk.Group = factor(R01_Nback_long$Risk.Group, levels = c("High", "Low"))
R01_Nback_long$Load = factor(R01_Nback_long$Load)

## R01_SST
R01_SST = merge(R01_SST, GroupMembership[c(1,3)], by.x = "ParID", by.y = "ParticipantID", all.y = FALSE)
R01_SST_long = merge(R01_SST_long, GroupMembership[c(1,3)], by.x = "ParID", by.y = "ParticipantID", all.y = FALSE)
R01_SST$Risk.Group = factor(R01_SST$Risk.Group, levels = c("High", "Low"))
R01_SST_long$Risk.Group = factor(R01_SST_long$Risk.Group, levels = c("High", "Low"))
R01_SST_long$Order = factor(R01_SST_long$Order, levels = c("1", "2", "3", "4"))

## R01_SpaceGame
R01_SpaceGame = merge(R01_SpaceGame, GroupMembership[c(1,3)], by.x = "ParID", by.y = "ParticipantID", all.y = FALSE)
R01_SpaceGame_long = merge(R01_SpaceGame_long, GroupMembership[c(1,3)], by.x = "ParID", by.y = "ParticipantID", all.y = FALSE)
R01_SpaceGame_DM = merge(R01_SpaceGame_DM, GroupMembership[c(1,3)], by.x = "ParID", by.y = "ParticipantID", all.y = FALSE)

#### Clean up data ####
## R01_GNG
R01_GNG$Risk.Group = factor(R01_GNG$Risk.Group, levels = c("High", "Low"))
R01_GNG = R01_GNG[R01_GNG$ParID != 31, ]

R01_GNG_long$Risk.Group = factor(R01_GNG_long$Risk.Group, levels = c("High", "Low"))
R01_GNG_long$Block = factor(R01_GNG_long$Block)
R01_GNG_long = R01_GNG_long[R01_GNG_long$ParID != 31, ]

## R01_Nback
R01_Nback$Risk.Group = factor(R01_Nback$Risk.Group, levels = c("High", "Low"))
R01_Nback = R01_Nback[R01_Nback$ParID != 31, ]
R01_Nback$Session = factor(R01_Nback$Session, levels = c("1", "2"))
R01_Nback_baseline = R01_Nback[R01_Nback$Session == 1, ]

R01_Nback_long$Risk.Group = factor(R01_Nback_long$Risk.Group, levels = c("High", "Low"))
R01_Nback_long$Load = factor(R01_Nback_long$Load)
R01_Nback_long$Session = factor(R01_Nback_long$Session, levels = c("1", "2"))
R01_Nback_long = R01_Nback_long[R01_Nback_long$ParID != 31, ]
R01_Nback_baseline_long = R01_Nback_long[R01_Nback_long$Session == 1, ]

## R01_SST
R01_SST$Risk.Group = factor(R01_SST$Risk.Group, levels = c("High", "Low"))
R01_SST = R01_SST[R01_SST$ParID != 31, ]

R01_SST_long$Risk.Group = factor(R01_SST_long$Risk.Group, levels = c("High", "Low"))
R01_SST_long = R01_SST_long[R01_SST_long$Block != "Dup", ]
R01_SST_long$Order = factor(R01_SST_long$Order, levels = c("1", "2", "3", "4"))
R01_SST_long = R01_SST_long[R01_SST_long$ParID != 31, ]

## R01_SpaceGame
R01_SpaceGame$Risk.Group = factor(R01_SpaceGame$Risk.Group, levels = c("High", "Low"))
R01_SpaceGame = R01_SpaceGame[R01_SpaceGame$ParID != 31, ]
R01_SpaceGame$Session = factor(R01_SpaceGame$Session, levels = c("1", "2"))
R01_SpaceGame_baseline = R01_SpaceGame[R01_SpaceGame$Session == 1, ]

R01_SpaceGame_long$Risk.Group = factor(R01_SpaceGame_long$Risk.Group, levels = c("High", "Low"))
R01_SpaceGame_long$Block = factor(R01_SpaceGame_long$Block, levels = c("1", "2", "3", "4"))
R01_SpaceGame_long = R01_SpaceGame_long[R01_SpaceGame_long$ParID != 31, ]
R01_SpaceGame_long$Session = factor(R01_SpaceGame_long$Session, levels = c("1", "2"))
R01_SpaceGame_baseline_long = R01_SpaceGame_long[R01_SpaceGame_long$Session == 1, ]

R01_SpaceGame_DM$Risk.Group = factor(R01_SpaceGame_DM$Risk.Group, levels = c("High", "Low"))
R01_SpaceGame_DM = R01_SpaceGame_DM[R01_SpaceGame_DM$ParID != 31, ]
R01_SpaceGame_DM$Session = factor(R01_SpaceGame_DM$Session, levels = c("1", "2"))
R01_SpaceGame_DM_baseline = R01_SpaceGame_DM[R01_SpaceGame_DM$Session == 1, ]

#### Make SST long Conditions ####
R01_SST_long$Portion = ifelse(R01_SST_long$Block == "lED_lPort", "Large", ifelse(
  R01_SST_long$Block == "hED_lPort", "Large", ifelse(
    R01_SST_long$Block == "lED_sPort", "Small", ifelse(
      R01_SST_long$Block == "hED_sPort", "Small", NA
    )
  )
))

R01_SST_long$ED = ifelse(R01_SST_long$Block == "lED_lPort", "Low", ifelse(
  R01_SST_long$Block == "hED_lPort", "High", ifelse(
    R01_SST_long$Block == "lED_sPort", "Low", ifelse(
      R01_SST_long$Block == "hED_sPort", "High", NA
    )
  )
))

#### Make Long Dsets Across Outcomes for plotting####
## R01_GNG
R01_GNG_out.long = melt(R01_GNG[c(1:3, 6, 11:16, 105:113)], id.vars = c("ParID", "Session", "Risk.Group"))
R01_GNG_out.long$OutcomeMeasure = R01_GNG_out.long$variable
R01_GNG_out.long$OutcomeEstimate = R01_GNG_out.long$value
R01_GNG_out.long = R01_GNG_out.long[c(1:3, 6:7)]

## R01_Nback
R01_Nback_out.long = melt(R01_Nback_baseline_long[c(1:3, 6, 8:9, 12, 14:16)], id.vars = c("ParID", "Session", "Load", "Risk.Group"))
R01_Nback_out.long$OutcomeMeasure = R01_Nback_out.long$variable
R01_Nback_out.long$OutcomeEstimate = R01_Nback_out.long$value
R01_Nback_out.long = R01_Nback_out.long[c(1:4, 7:8)]

## R01_SST
R01_SST_out.long = melt(R01_SST_long[c(1:10, 13:14, 16:18)], id.vars = c("ParID", "Session", "Block", "Order", "Portion", "ED", "Risk.Group"))
R01_SST_out.long$OutcomeMeasure = R01_SST_out.long$variable
R01_SST_out.long$OutcomeEstimate = R01_SST_out.long$value
R01_SST_out.long = R01_SST_out.long[c(1:7, 10:11)]

## R01_SpaceGame
R01_SpaceGame_out.long = melt(R01_SpaceGame_baseline[c(1:4, 7:8, 11:12, 14:16, 73)], id.vars = c("ParID", "Session", "Risk.Group"))
R01_SpaceGame_out.long$OutcomeMeasure = R01_SpaceGame_out.long$variable
R01_SpaceGame_out.long$OutcomeEstimate = R01_SpaceGame_out.long$value
R01_SpaceGame_out.long = R01_SpaceGame_out.long[c(1:3, 6:7)]

R01_SpaceGame_DM_out.long = melt(R01_SpaceGame_DM_baseline[c(1:3, 5:13, 15)], id.vars = c("ParID", "Session", "Model", "Risk.Group"))
R01_SpaceGame_DM_out.long$OutcomeMeasure = R01_SpaceGame_DM_out.long$variable
R01_SpaceGame_DM_out.long$OutcomeEstimate = R01_SpaceGame_DM_out.long$value
R01_SpaceGame_DM_out.long = R01_SpaceGame_DM_out.long[c(1:4, 7:8)]


############# fMRI data
#### Violin Plots ####
## Risk Status 2 sample t  High > Low all PS
ggplot(data=R01_fMRI, aes(x=RiskStatus, y=Large.Small_allED1, fill = RiskStatus)) + 
  scale_fill_manual(values=c("cornflowerblue", "cadetblue1")) +
  geom_violin(alpha = 1, position = position_dodge(1)) + 
  geom_boxplot(width=0.1, fill = "white") + 
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),  panel.background = element_rect(fill = "transparent",colour = NA), 
        plot.background = element_rect(fill = "transparent",colour = NA), axis.line = element_line(colour = "black")) + 
  stat_summary(fun.y=mean, colour="black", fill = "blue", geom="point", shape=23, size=4,show.legend = FALSE) + 
  geom_hline(yintercept = 0, col="black", linetype = 3) + 
  geom_jitter(width = 0.1, size=2, shape = 1) + 
  labs(title="Risk Status difference for Large > Small, All ED", y= "Left Occiptial (Mid/Sup) and Lingual gyri", x="Group")

ggplot(data=R01_fMRI, aes(x=RiskStatus, y=Large.Small_allED2, fill = RiskStatus)) + 
  scale_fill_manual(values=c("cornflowerblue", "cadetblue1")) +
  geom_violin(alpha = 1, position = position_dodge(1)) + 
  geom_boxplot(width=0.1, fill = "white") + 
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),  panel.background = element_rect(fill = "transparent",colour = NA), 
        plot.background = element_rect(fill = "transparent",colour = NA), axis.line = element_line(colour = "black")) + 
  stat_summary(fun.y=mean, colour="black", fill = "blue", geom="point", shape=23, size=4,show.legend = FALSE) + 
  geom_hline(yintercept = 0, col="black", linetype = 3) + 
  geom_jitter(width = 0.1, size=2, shape = 1) + 
  labs(title="Risk Status difference for Large > Small, All ED", y= "Left Occiptial (Sup) Gyrus and Precuneus", x="Group")

## Risk Status 2 sample t Large > Small all ED
ggplot(data=R01_fMRI, aes(x=RiskStatus, y=High.Low_allPS, fill = RiskStatus)) + 
  scale_fill_manual(values=c("cornflowerblue", "cadetblue1")) +
  geom_violin(alpha = 1, position = position_dodge(1)) + 
  geom_boxplot(width=0.1, fill = "white") + 
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),  panel.background = element_rect(fill = "transparent",colour = NA), 
        plot.background = element_rect(fill = "transparent",colour = NA), axis.line = element_line(colour = "black")) + 
  stat_summary(fun.y=mean, colour="black", fill = "blue", geom="point", shape=23, size=4,show.legend = FALSE) + 
  geom_hline(yintercept = 0, col="black", linetype = 3) + 
  geom_jitter(width = 0.1, size=2, shape = 1) + 
  labs(title="Risk Status difference for High > Low, All Portions", y= "Right Cerebellum", x="Group")
