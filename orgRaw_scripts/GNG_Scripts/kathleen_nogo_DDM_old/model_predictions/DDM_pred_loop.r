
para=read.table("all_subs_params")
params=para[,2:12];
source("diffusion_nogo.r")

ntrials=1000
nsubs=length(params[,1])
pred=matrix(0,(nsubs*2),8)

eta=0;ster=0;


for(s in 1:nsubs){

        matcount=s*2-1

        par_sim=params[s,]

    for(i in 1:2){

        if(i==1){z=par_sim[1,8];v=par_sim[1,4];v2=par_sim[1,5];a=par_sim[1,1]}
        if(i==2){z=par_sim[1,9];v=par_sim[1,6];v2=par_sim[1,7];a=par_sim[1,2]}
        sz=par_sim[1,10]
        simdata= diffusion_nogo(a,par_sim[1,3],v,z,sz,ntrials)
        simdatano= diffusion_nogo(a,par_sim[1,3],v2,z,sz,ntrials)



           datmat=c(length(simdata$u_resp)/ntrials,quantile(simdata$u_resp,probs=c(.1,.3,.5,.7,.9)),(length(simdatano$u_resp)/ntrials),median(simdatano$u_resp))

          pred[(matcount+i-1),]=datmat

        }

}

write(t(pred),file="all_pred_data",ncol=8,sep="\t")


             

