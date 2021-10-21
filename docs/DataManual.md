# Data Manual - R01: Food and Brain Study

- [Data Manual - R01: Food and Brain Study](#data-manual---r01-food-and-brain-study)
  - [Introduction](#introduction)
  - [Study Design](#study-design)
    - [Overview](#overview)
    - [DEXA](#dexa)
    - [Actigraph](#actigraph)
    - [fMRI Food Paradigm](#fmri-food-paradigm)
        - [Task Design](#task-design)
      - [Scan Procedures](#scan-procedures)
      - [Food Task Design](#food-task-design)
      - [Food Ratings](#food-ratings)
        - [Outcome Metrics](#outcome-metrics)
    - [WASI](#wasi)
    - [Cogntive Performance Tasks](#cogntive-performance-tasks)
      - [Go-No Go](#go-no-go)
        - [Task Design](#task-design-1)
        - [Outcomes of Interest](#outcomes-of-interest)
      - [Letter N-Back](#letter-n-back)
        - [Task Design](#task-design-2)
        - [Outcomes of Interest](#outcomes-of-interest-1)
      - [Food Stop-Signal Task](#food-stop-signal-task)
        - [Task Design](#task-design-3)
        - [Outcomes of Interest](#outcomes-of-interest-2)
      - [Reward-Related Decision-Making (Space Game)](#reward-related-decision-making-space-game)
        - [Task Design](#task-design-4)
        - [Outcomes of Interest](#outcomes-of-interest-3)
    - [Parent-Reported Questionnaires](#parent-reported-questionnaires)
      - [General](#general)
      - [Household Demographics](#household-demographics)
      - [Child Puberty](#child-puberty)
      - [Tanner](#tanner)
      - [Child Physical Activity](#child-physical-activity)
      - [Portion Size Survey (PSS)](#portion-size-survey-pss)
      - [Feeding Strategies](#feeding-strategies)
      - [Child Behavior Questionnaire (CBQ)](#child-behavior-questionnaire-cbq)
      - [Child Eating Behavior Questionnaire (CEBQ)](#child-eating-behavior-questionnaire-cebq)
      - [Binge Eating Scale (BES)](#binge-eating-scale-bes)
      - [Family Food Behavior (FFB)](#family-food-behavior-ffb)
      - [Child Sleep Habits Questionnaire (CSHQ)](#child-sleep-habits-questionnaire-cshq)
      - [Tempest Self-Regulation of Eating (TESQE)](#tempest-self-regulation-of-eating-tesqe)
      - [Lifestyle Behavior Checklist (LBC)](#lifestyle-behavior-checklist-lbc)
      - [Sensitivity to Reward and Punishment (SRSPQP)](#sensitivity-to-reward-and-punishment-srspqp)
      - [Parent Weight Loss Behavior (PWLB)](#parent-weight-loss-behavior-pwlb)
      - [Three Factor Eating Questionnaire (TFEQ)](#three-factor-eating-questionnaire-tfeq)
      - [Household Food Security Survey Module (HFFSM)](#household-food-security-survey-module-hffsm)
      - [Household Food Insecurity Access Scale (HFIAS)](#household-food-insecurity-access-scale-hfias)
      - [Community Childhood Hunger Identification Project (CCHIP)](#community-childhood-hunger-identification-project-cchip)
      - [Behavioral Rating Inventory of Executive Function-2 (BRIEF-2)](#behavioral-rating-inventory-of-executive-function-2-brief-2)
      - [Alcohol Use Disorders Identification Test (AUDIT)](#alcohol-use-disorders-identification-test-audit)
    - [Child-Reported Questionnaires](#child-reported-questionnaires)
      - [Portion Size Survey (PSS)](#portion-size-survey-pss-1)
      - [Portion Size Discrimination (PSD)](#portion-size-discrimination-psd)
      - [Kid’s Food Questionnaire (KFQ)](#kids-food-questionnaire-kfq)
      - [Revised Children’s Manifest Anxiety Scale (RCMAS)](#revised-childrens-manifest-anxiety-scale-rcmas)
      - [Delay Discounting](#delay-discounting)
      - [Child Weight Concerns (CWC)](#child-weight-concerns-cwc)
      - [Child Body Image Scale (CBIS)](#child-body-image-scale-cbis)
      - [Parent Responsiveness (PRM/PRF)](#parent-responsiveness-prmprf)
      - [Loss of Control Eating (LOC)](#loss-of-control-eating-loc)
      - [Communities that Care (CtC)](#communities-that-care-ctc)
  - [Directory Organization](#directory-organization)
  - [Data Management Workflow](#data-management-workflow)
    - [Data Documentation](#data-documentation)
    - [Pre-Processing Pipeline](#pre-processing-pipeline)
      - [Installation Instructions](#installation-instructions)
        - [Python](#python)
        - [R](#r)
        - [Matlab](#matlab)
        - [LaTex](#latex)
      - [Pipeline Execution](#pipeline-execution)
        - [1) Raw Data](#1-raw-data)
          - [1a) Exporting](#1a-exporting)
          - [1b) Quality Control](#1b-quality-control)
        - [2) ...](#2-)
  - [Interactive Reports and Tables](#interactive-reports-and-tables)
  - [Analyses: Guidelines for Reproducibility and Documentation](#analyses-guidelines-for-reproducibility-and-documentation)

## Introduction

overview of study...  
purpose ...  
outline ...?

## Study Design

### Overview

get visit image/table?  
list inclusion/exclusion criteria?  
other??

### DEXA

### Actigraph

### fMRI Food Paradigm

Theoretical background...(brief)

##### Task Design

#### Scan Procedures

#### Food Task Design

Instructions…  
Design...  
Stim images...

#### Food Ratings

Instructions…  
Design...  

##### Outcome Metrics

### WASI

### Cogntive Performance Tasks

#### Go-No Go

Theoretical background...(brief)

##### Task Design

Instructions…
12 practice trials. 5 blocks of 40 trials (30 Go/10 NoGo). Timing info… Between blocks…
Stim images...

##### Outcomes of Interest

Performace on the GNG task is typicall assessed based on correct responses and errors. Correct responses are often called ‘Hits’. There are two primary errors that can occur in the GNG task. Omission errors are when the participant failed to respond to a target/go stimuli while commission errors occur when the participant response to a NoGo trial. These types of errors are often called ‘misses’ and ‘false alarms’, respectively. In addition to response correctness, reaction time is also used to look at differences between correct responses and false alarms.

Signal Detection Theory (SDT) attempts to determine thresholds at which a person can distinguish a pattern (e.g., signal) from random patterns of noise. In the context of GNG, it is a technique to assess the ability to detect the NoGo signal during the task. Below are metrics that can be used to test signal detection and the accompanying equations. Non-parametric measures were included due to the fact because it is likely that the signal and noise distributions do not meet the following assumptions: 1) both are normal; and 2) have the same SD. It is not possible to test these assumptions with Yes/No tasks like GNG. When these assumptions are not met, sensory sensitivity will vary with differing response biases. See the following paper for an explanation of the selected measures and has excellent references for further reading: (Stanislaw & Todorov, 1999).

* d’: d-prime is a parametric measure of sensory sensitivity—it is equal to the distance between the noise distribution and the signal and noise distribution

>> $d^{\prime} = \phi^{- H} - \phi^{-FA} → z(H)-z(FA)$  
H:percent hits; FA: percent false alarms; and z is derived from the normal inverse distribution

* A’: A-prime is a non-parametric measure of sensory sensitivity; generally between 0.5 - 1

>> $A^{\prime} = .5 + \frac{(H - FA)(1 + H - FA)}{4H(1 - FA)}$ when $H \ge FA$  
$A^{\prime} = .5 - \frac{(FA - H)(1 + FA - H)}{4H(1 - H)}$ when $FA \ge H$  
H: percent hits; FA: percent false alarms

* c: is a measure of bias—distance between the criterion and a neutral point where neither response is favored—the neutral point is where the signal and noise distributions overlap. Negative values correspond to bias to respond ‘yes’ (i.e., press for Go) and positive corresponds to bias to respond ‘No’

>> $c = \frac{\phi^-H + \phi^- FA)}{2} → \frac{z(H)+ z(FA)}{2}$  
 H:percent hits; FA: percent false alarms; and z is derived from the normal inverse distribution

* β’’ (Geir’s β): is a non-parametric measure of response bias—it is the ratio of the ordinate (i.e., height) of the signal and noise distribution at the criterion to the the ordinate of the noise distribution

>> $β^{\prime\prime} = \frac{H(1 - H) - FA(1 - FA)}{H(1 - H) + FA(1 - FA)}$ when $H \ge FA$  
$β^{\prime\prime} = \frac{FA(1 - FA) - H(1 - H)}{FA(1 - FA) + H(1 - H)}$ when $FA \ge H$  
H:percent hits;FA:percent false alarms

#### Letter N-Back

Theoretical background...(brief)

##### Task Design

Stim images...

##### Outcomes of Interest

Participants’ stop-signal reaction times (SSRT) was computed using the integration method after replacing omitted go responses with the participants’ slowest go RT (Verbruggen et al., 2019). SSRT was only computed if the assumptions of the racehorse model were met (i.e., go RT > unsuccessful stop RT; Verbruggen et al., 2019). Of the children with usable resting state data, 1 participant was excluded for not meeting the assumptions of the race model, and was therefore treated as missing data and imputed in subsequent analyses.

#### Food Stop-Signal Task

The stop-signal task (SST) assesses inhibitory control by measuring the latency of response inhibition. The SST was adapted from the implementation in (Verbruggen, Logan, & Stevens, 2008). For a thorough discussion of the theoretical basis for the race-horse model of response inhibition see (Verbruggen & Logan, 2009). The basic premise is that participants will first activate a go-response to a stimuli. After seeing the stop stimuli, they will activate a nogo-response. If they are successful in inhibiting the go-response, the nogo-response was faster. If they fail to inhibit the go-response, the nogo-response was too slow. In this task, inhibition can be measured by manipulating the delay of the stop signal using a step-like function to hold successful stopping at a .5 probability.

![Racehorse_Model](./images/sst_racehorse_model.png)

##### Task Design

The SST was administered using Matlab2018b and Psychtoolbox3. Plates of food were presented with a triangle-folded napkin on either the left or right side of the plate (go stimulus; see Figure 1) for 1500 ms with an inter-stimulus-interval of 50 ms (i.e., fixation). Children were asked to sort the plates according to which side of the plate the napkin was on and to press the left or right arrow keys when the napkin appeared on the left or right side of the plate, respectively. They were encouraged to respond as quickly as possible. They were also told that the plate would be sometimes get covered with a warmer dome (i.e., stop-signal; see Figure 1) and were instructed not to respond if the dome appeared.  The warmer dome (i.e., stop-signal) was presented after variable delay on 25% of trials. The variable stop-signal delay (SSD) was determined by a step-wise adaptive procedure which increased the SSD 50ms after each successful stop trial and reduced the SSD by 50 ms after each unsuccessful stop trial with the first SSD = 250 ms. This adaptive procedure maintained ~0.50 probability of successful response inhibition. The task parameters were based on specifications articulated by Verbruggen and colleagues (2019) for best practices in measuring stop-signal reaction time according to the theoretical racehorse model. 
The task consisted of 256 trial across 4 randomized blocks (i.e., 64 trials per block), two of which included foods with high-energy density (ED; i.e. a chocolate brownie) and two of which included foods with low-ED (i.e. blueberries). The portion size (e.g., large vs small) of presented foods varied across trials. Prior to the task, children completed 32 practice trials to ensure they understood the instructions. After the practice, children were reminded to respond quickly and told that they may be encourage to respond quickly during the task. To prevent children from slowing throughout the task, which is a known issue, the message ‘Faster’ was presented after trials in which they responded slower than 1.5 standard deviations below their mean reaction time in practice. Between each block, children were given the opportunity to take a break and were shown their average response time (e.g., ‘How Fast Were You?’), given encouragement for how quickly the were responding (e.g., ‘Wow, that is faster than a second’), and were reminded not to press the arrow keys if the dome covered the plate.  

Stim images...

##### Outcomes of Interest

#### Reward-Related Decision-Making (Space Game)

Theoretical background...(brief)

##### Task Design

Instructions…  
Design...  
Stim images...

##### Outcomes of Interest

General  

Decision Making Model  

### Parent-Reported Questionnaires

#### General

short description...  
link to pdf on OneDrive, citation(?)

#### Household Demographics

short description...  
link to pdf on OneDrive, citation(?)

#### Child Puberty 

short description...  
link to pdf on OneDrive, citation(?)

#### Tanner

short description...  
link to pdf on OneDrive, citation(?)

#### Child Physical Activity

short description...  
link to pdf on OneDrive, citation(?)

#### Portion Size Survey (PSS)

short description...  
link to pdf on OneDrive, citation(?)

#### Feeding Strategies

short description...  
link to pdf on OneDrive, citation(?)

#### Child Behavior Questionnaire (CBQ)

short description...  
link to pdf on OneDrive, citation(?)

#### Child Eating Behavior Questionnaire (CEBQ)

short description...  
link to pdf on OneDrive, citation(?)

#### Binge Eating Scale (BES)

short description...  
link to pdf on OneDrive, citation(?)

#### Family Food Behavior (FFB)

short description...  
link to pdf on OneDrive, citation(?)

#### Child Sleep Habits Questionnaire (CSHQ)

short description...  
link to pdf on OneDrive, citation(?)

#### Tempest Self-Regulation of Eating (TESQE)

short description...  
link to pdf on OneDrive, citation(?)

#### Lifestyle Behavior Checklist (LBC)

short description...  
link to pdf on OneDrive, citation(?)

#### Sensitivity to Reward and Punishment (SRSPQP)

short description...  
link to pdf on OneDrive, citation(?)

#### Parent Weight Loss Behavior (PWLB)

short description...  
link to pdf on OneDrive, citation(?)

#### Three Factor Eating Questionnaire (TFEQ)

short description...  
link to pdf on OneDrive, citation(?)

#### Household Food Security Survey Module (HFFSM)

short description...  
link to pdf on OneDrive, citation(?)

#### Household Food Insecurity Access Scale (HFIAS)

short description...  
link to pdf on OneDrive, citation(?)

#### Community Childhood Hunger Identification Project (CCHIP)

short description...  
link to pdf on OneDrive, citation(?)

#### Behavioral Rating Inventory of Executive Function-2 (BRIEF-2)

The Behavioral Rating Index of Executive Function-2 (BRIEF-2) is a parent-report measure of everyday executive behaviors that is normed for age and gender. T scores of 60 or greater indicate high risk/clinical relevance for symptoms. There are 9 subscales, 4 index measures, and 3 parental response checks that are calculated.

ADD CITATION

Subscales:  

* Inhibit - define/describe
* Self-Monitor - define/describe
* Shift - define/describe
* Emotional Control - define/describe
* Initiate - define/describe
* Working Memory - define/describe
* Plan/Organize - define/describe
* Task-Monitor - define/describe
* Organization of Materials - define/describe
  
Index Measures:

* Behavioral Regulation Index: Inhibit and Self-Monitor
* Emotional Regulation Index: Shift and Emotional Control
* Cognitive Regulation Index: Initiate, Working Memory, Plan/Organize, and Task-Monitor
* General Executive Composite: all scales

Parental Response Checks:

* Inconsistency - define/describe
* Negativity - define/describe
* Infrequency - define/describe

#### Alcohol Use Disorders Identification Test (AUDIT)

short description...  
link to pdf on OneDrive, citation(?)

### Child-Reported Questionnaires

#### Portion Size Survey (PSS)

short description...  
link to pdf on OneDrive, citation(?)

#### Portion Size Discrimination (PSD)

short description...  
link to pdf on OneDrive, citation(?)

#### Kid’s Food Questionnaire (KFQ)

short description...  
link to pdf on OneDrive, citation(?)

#### Revised Children’s Manifest Anxiety Scale (RCMAS)

short description...  
link to pdf on OneDrive, citation(?)

#### Delay Discounting

short description...  
link to pdf on OneDrive, citation(?)

#### Child Weight Concerns (CWC)

short description...  
link to pdf on OneDrive, citation(?)

#### Child Body Image Scale (CBIS)

short description...  
link to pdf on OneDrive, citation(?)

#### Parent Responsiveness (PRM/PRF)

short description...  
link to pdf on OneDrive, citation(?)

#### Loss of Control Eating (LOC)

short description...  
link to pdf on OneDrive, citation(?)

#### Communities that Care (CtC)

short description...  
link to pdf on OneDrive, citation(?)

## Directory Organization

directory structure...  
image of directory organizaiton

## Data Management Workflow

### Data Documentation

details on codebook (need to make) and variable descriptions (.jsons)

### Pre-Processing Pipeline

narative overview with steps...  
image of pipeline  

#### Installation Instructions

##### Python

Mac

Windows

##### R

Mac

Windows

##### Matlab

Mac

Windows

##### LaTex

Mac

Windows

#### Pipeline Execution

##### 1) Raw Data

###### 1a) Exporting

###### 1b) Quality Control

##### 2) ...

## Interactive Reports and Tables

description or reports through .Rmd

## Analyses: Guidelines for Reproducibility and Documentation