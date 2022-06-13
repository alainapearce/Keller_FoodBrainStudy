# import csv with list of IDs to include in fmri analyses
fmri_index <- read.table("~/Desktop/ids.csv", quote="\"", comment.char="")
colnames(fmri_index) <- c("id")

# import anthro data
anthro_data <- read_sav("~/OneDrive - The Pennsylvania State University/b-childfoodlab_Shared/Active_Studies/RO1_Brain_Mechanisms_IRB_5357/Participant_Data/Databases/anthro_data.sav")

# Add values of risk_status_mom from anthro_data to ids by matching participant ID
fmri_index$risk_status_mom <- anthro_data$risk_status_mom[match(fmri_index$id, anthro_data$id)]

# make separate dataframes for high and low risk

## high risk
highrisk <- fmri_index[ which(fmri_index$risk_status_mom==1), ]

## low risk
lowrisk <- fmri_index[ which(fmri_index$risk_status_mom==0), ]
