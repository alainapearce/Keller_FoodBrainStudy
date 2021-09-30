#subx=scan("sublistx.txt",what="list")
#suby=scan("sublisty.txt",what="list")


subs=scan("list_of_subs.txt",what="list")
nsubx=length(subs)

datamat=matrix(0,nsubx,9)

for(i in 1:nsubx){

#dd1=sprintf("%s.csv",subx[i])
#dd2=sprintf("%s.csv",suby[i])


################

#x=matrix(scan(),ncol=4,byrow=T)
x=read.csv(subs[i],header=T)
x=x[,-1]
#x=x[-1,];y=y[-1,];

totgo=length(x[,1][x[,1]==1])
totcom=length(x[,1][x[,1]==2]);

xgo=x[,3][x[,1]==1 & x[,2]==1]
xmiss=x[,3][x[,1]==1 & x[,2]==2]
xcom=x[,3][x[,1]==2 & x[,2]==1]


datamat[i,]=c(length(xgo)/totgo, length(xgo), quantile(xgo,probs=c(.1,.3,.5,.7,.9)),length(xcom)/totcom,median(xcom))



#################


datamat=round(datamat,3)


write(t(datamat),file="all_subs_data",ncol=9,append=T)
}
