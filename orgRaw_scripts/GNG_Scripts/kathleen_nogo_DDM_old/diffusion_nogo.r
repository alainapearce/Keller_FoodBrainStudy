#########sim version for random walk / diffusion process


diffusion_nogo=function(a,ter,v,z,ster,ntrials){


#scaling parameters
step=.001      #step size
ta=.001
st=ta/step
s=.1                 #drift coefficient, within trial variability (scaling parameter)
taas=sqrt(ta)/s

mm=1200    #max number of steps per trial (ms)
ntrials=ntrials   #number of sim trials

    #eta=0;sz=0;ster=0;

u_resp=0    #prepare counters for collecting responses at upper and lower bounds
l_resp=0
no_resp=0

a=a    # boundary sep
z=z    # starting point
ter=ter   # nondecision time
v=v       # drift rate
ster=ster  # var in ter
sz=0      # var in sz
#eta=eta    # var in drift
eta=0
## convert boundary separation and starting point into "steps" for random walk approx of diffusion process
    #z=a/2
th=a/2         #unbiased start point
xxx=z-th    # diff between z and unbiased starting point
del=sqrt(s*s*ta)          # scaling
ib=round(th/del)
kka=round(ib+xxx/del)      #starting point as number of steps
nn=2*ib-1        #upper bound in steps, so you start at kka and "walk" till you hit 0 or nn



## simulate ntrials


for(i in 1:ntrials){

n=0             #reset number of time steps

kk=kka+round((runif(1)-.5)*sz/del)     #pick starting point from uniform dist with width sz
if(kk<2){kk=2}      # keep z in good range (don't start at or beyond boundary)
if(kk>(nn-2)){kk=nn-2}      # keep z in good range

xt=round((ter*st/ta)+(ster*(runif(1)*.5)*st/ta))  #pick value of ter from uniform dist with width ster
												# scale by by st/ta (which is 1 if s = .1)

k=kk    #starting value for the walk, the value of k represents where the accumulator is during the walk

v_trial=rnorm(1,v,eta)   #pick value of drift from norm dist with mean v and SD eta



## start random walk, exit walk when boundary hit or mm steps taken
for(m in 1:mm){
qq=(1-v_trial*taas)/2.0      #convert drift into prob of stepping up or down, 
							 # scaled by drift noise (s determines taas)

temp=runif(1)        #pick random value from 0-1, if value larger than drift prob. (qq), take step up 
if(temp < qq){k=k-1}
if(temp >= qq){k=k+1}

n=n+1   #count the time step


if((k == 0) || (k==nn)){break}   #if bound hit, trial is over



}

## collect data from trial

n1=round(n*st+1+xt)   #scale number of steps taken into ms and add nondecision time (xt)

if(n1 < mm){

	if(k==0){
	l_resp=c(l_resp,n1)    #add count at that time, e.g., if 3 trials ended at 354 ms, then rc[354]=3
	}

	if(k==nn){
	u_resp=c(u_resp,n1)
	}
	}
	

}
u_resp=u_resp[-1]; l_resp=l_resp[-1];   # remove initial 0 values
list(l_resp=l_resp,u_resp=u_resp)
}


