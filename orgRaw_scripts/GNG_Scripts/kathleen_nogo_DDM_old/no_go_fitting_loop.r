
#### fitting portion
chis=function(x){
chi=0
chi_top=0
chi_bottom=0

## fitting parameters
ntrials=10000   # determines specificity of simulation predictions, more trials is better
# mm=1000    #max number of steps  [i.e., only trials where decision takes 3000ms or less]
ncond=1 #number of lines (conditions) in the input data set

a1=x[1]
z1=x[4]
sz=0
eta=0
ter=x[2]
v1=x[3]

    
    #ter_in=x[3]
#ter_mi=x[4]
    #sz=x[4]
#ster=x[4]
#eta=x[6]
    #v1=x[3]


# set var params to zero for examples
#sz=0
ster=x[5]
    #eta=0



if(eta < 0){eta=0}  #keep var from going negative
if(eta > .25){eta=.25}  #keep var from going negative
if(eta < 0){eta=0}  #keep var from going negative
if(sz < 0){sz=0}
if(ster < 0){ster=0}

q_probs=c(.1,.2,.2,.2,.2,.1)   # probability densities between quantiles
b_probs=c(.5,.5)

#do fits for each condition, summing chi-squared value as you go
	simdata=diffusion_nogo(a1,ter,v1,z1,ster,ntrials)
    simdatanogo=diffusion_nogo(a1,ter,-v1,z1,ster,ntrials)
 	
	top_data=data1[1]*q_probs
	bot_data=data1[8]*b_probs
	
	pt1=length(simdata$u_resp[simdata$u_resp < data1[3]])/ntrials
	pt2=length(simdata$u_resp[(simdata$u_resp < data1[4] & simdata$u_resp >= data1[3])])/ntrials
	pt3=length(simdata$u_resp[(simdata$u_resp < data1[5] & simdata$u_resp >= data1[4])])/ntrials
	pt4=length(simdata$u_resp[(simdata$u_resp < data1[6] & simdata$u_resp >= data1[5])])/ntrials
	pt5=length(simdata$u_resp[(simdata$u_resp < data1[7] & simdata$u_resp >= data1[6])])/ntrials
	pt6=length(simdata$u_resp[simdata$u_resp > data1[7]])/ntrials
	
	pred_p=c(pt1,pt2,pt3,pt4,pt5,pt6)
	
	top_chi=sum((top_data-pred_p)^2/(pred_p+.0001))
	
	pt1=length(simdatanogo$u_resp[simdatanogo$u_resp < data1[9]])/ntrials
    pt2=length(simdatanogo$u_resp[(simdatanogo$u_resp >= data1[9])])/ntrials

	pred_p=c(pt1,pt2)
	
	bot_chi=sum((bot_data-pred_p)^2/(pred_p+.0001))
	
	totchi=(bot_chi+top_chi)*(data1[2])
	
	chi=chi+totchi
	
}   # end fitting loop



### run model fitting

source("diffusion_nogo.r")   # call diffusion code

###starting_values

b1_data=matrix(scan("all_subs_data"),ncol=9,byrow=T)
nsubs=length(b1_data[,1])
est_params=matrix(0,nsubs,6)

for(mmm in 1:nsubs){
#pick initial values
a1=.14
z1=.08   # starting point  [a/2 means unbiased]
#ter_in=.29
#ter_mi=.29
ster=.1    # var in nondecision time   [~  0 - 100]
sz=.05      # var in starting point    [~  0  -  a/3]
eta=.1    # var in drift             [~  0 -  .25]
v1=.2     # drift rate, + means top boundary, - means bottom  [~ -.40  -  .40]
#

b_data=b1_data[mmm,]
#b_data[3:7]=b_data[3:7]*1000
#b_data[10:14]=b_data[10:14]*1000

ter=(b_data[3]-150)/1000   # nondecision time in sec    [~  .200 -  .700]

	params=c(a1,ter,v1,z1,ster)
	
        data1=b_data
	
	best_params=optim(params,chis,control=list(maxit=500,trace=TRUE,parscale=c(.05,.1,.1,.05,.05)))
	
	est_params[mmm,]=c(best_params$par[1:5],best_params$value)
	
}
	
#	best_params=optim(params,chis,control=list(maxit=2000,trace=TRUE))	

	write(t(est_params),file="cont_params",ncol=6)

		
	
	
	

