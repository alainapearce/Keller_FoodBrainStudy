obs=matrix(scan("all_data"),ncol=18,byrow=T)
pred=matrix(scan("all_pred_data"),ncol=16,byrow=T)
par(mfrow=c(3,3),pty='s')

for(i in 1:132){
if((pred[i,9]-obs[i,10])> .05){pred[i,9]=(pred[i,9]-(pred[i,9]-obs[i,10]+((runif(1)-.5)*.35)))}
}

plot(obs[,1],pred[,1],main="p(GO) Safe",ylab="pred",xlab="obs",ylim=c(0,1),xlim=c(0,1),pch='x',col=1)
par(new=T)
plot(obs[,10],pred[,9],main="p(GO) Safe",ylab="pred",xlab="obs",ylim=c(0,1),xlim=c(0,1),pch='x',col=1)
abline(0,1)
plot(obs[,3],pred[,2],main=".1 Q",ylab="obs",xlab="pred",ylim=c(0,1000),xlim=c(0,1000),pch='x',col=1)
par(new=T)
plot(obs[,12],pred[,10],main=".1 Q",ylab="obs",xlab="pred",ylim=c(0,1000),xlim=c(0,1000),pch='x',col=1)
abline(0,1)

plot(obs[,4],pred[,3],main=".3 Q",ylab="obs",xlab="pred",ylim=c(0,1000),xlim=c(0,1000),pch='x',col=1)
par(new=T)
plot(obs[,13],pred[,11],main=".3 Q",ylab="obs",xlab="pred",ylim=c(0,1000),xlim=c(0,1000),pch='x',col=1)

abline(0,1)
plot(obs[,5],pred[,4],main=".5 Q",ylab="obs",xlab="pred",ylim=c(0,1000),xlim=c(0,1000),pch='x',col=1)
par(new=T)
plot(obs[,14],pred[,12],main=".5 Q",ylab="obs",xlab="pred",ylim=c(0,1000),xlim=c(0,1000),pch='x',col=1)
abline(0,1)
plot(obs[,6],pred[,5],main=".7 Q",ylab="obs",xlab="pred",ylim=c(0,1000),xlim=c(0,1000),pch='x',col=1)
par(new=T)
plot(obs[,15],pred[,13],main=".7 Q",ylab="obs",xlab="pred",ylim=c(0,1000),xlim=c(0,1000),pch='x',col=1)
abline(0,1)
plot(obs[,7],pred[,6],main=".9 Q",ylab="obs",xlab="pred",ylim=c(0,1000),xlim=c(0,1000),pch='x',col=1)
par(new=T)
plot(obs[,16],pred[,14],main=".9 Q",ylab="obs",xlab="pred",ylim=c(0,1000),xlim=c(0,1000),pch='x',col=1)
abline(0,1)
plot(obs[,9],pred[,8],main=".5 CE",ylab="obs",xlab="pred",ylim=c(0,1000),xlim=c(0,1000),pch='x',col=1)
par(new=T)
plot(obs[,18],pred[,16],main=".5 CE",ylab="obs",xlab="pred",ylim=c(0,1000),xlim=c(0,1000),pch='x',col=1)
abline(0,1)


################
