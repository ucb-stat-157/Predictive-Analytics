# R Code work by Michael Raftery


## COMMENTS FROM FIRST R FILE SHOULD BE READ FIRST; the process is same
# THE PROCESS followed is the same as R code Naive Bayes
# This code includes the features CTR.P and CTR.D which are from placement/depth and demographic


require(ff); require(RMOA); require(ffbase); require(AUC); require(ROCR)
load.ffdf("~/1 Statistics/157/PROJECT TEAM/merge")

progress_train_data <- read.delim("~/1 Statistics/157/PROJECT TEAM/progress_train_data_R.txt", header=FALSE)
colnames(progress_train_data)=c("Item","Pla","Cli","Imp")
progress_train_data$CTR=progress_train_data$Cli/progress_train_data$Imp
prog.p=progress_train_data[1:6,c(1,6)]; colnames(prog.p)=c("Pla","CTR.P")
prog.d=progress_train_data[7:18,c(1,6)]; colnames(prog.d)=c("Dem","CTR.D")
tu.data.small=training.w.userid[1:100000,]
head(tu.data.small)
tu.data.small[c(which(tu.data.small$Gender==1&tu.data.small$Age==1)),15]="M.1"
tu.data.small[c(which(tu.data.small$Gender==1&tu.data.small$Age==2)),15]="M.2"
tu.data.small[c(which(tu.data.small$Gender==1&tu.data.small$Age==3)),15]="M.3"
tu.data.small[c(which(tu.data.small$Gender==1&tu.data.small$Age==4)),15]="M.4"
tu.data.small[c(which(tu.data.small$Gender==1&tu.data.small$Age==5)),15]="M.5"
tu.data.small[c(which(tu.data.small$Gender==1&tu.data.small$Age==6)),15]="M.6"
tu.data.small[c(which(tu.data.small$Gender==2&tu.data.small$Age==1)),15]="F.1"
tu.data.small[c(which(tu.data.small$Gender==2&tu.data.small$Age==2)),15]="F.2"
tu.data.small[c(which(tu.data.small$Gender==2&tu.data.small$Age==3)),15]="F.3"
tu.data.small[c(which(tu.data.small$Gender==2&tu.data.small$Age==4)),15]="F.4"
tu.data.small[c(which(tu.data.small$Gender==2&tu.data.small$Age==5)),15]="F.5"
tu.data.small[c(which(tu.data.small$Gender==2&tu.data.small$Age==6)),15]="F.6"
tu.data.small$Dem=tu.data.small[,15]

tu.data.small[c(which(tu.data.small$Depth==1&tu.data.small$Position==1)),16]="1.1"
tu.data.small[c(which(tu.data.small$Depth==2&tu.data.small$Position==1)),16]="2.1"
tu.data.small[c(which(tu.data.small$Depth==2&tu.data.small$Position==2)),16]="2.2"
tu.data.small[c(which(tu.data.small$Depth==3&tu.data.small$Position==1)),16]="3.1"
tu.data.small[c(which(tu.data.small$Depth==3&tu.data.small$Position==2)),16]="3.2"
tu.data.small[c(which(tu.data.small$Depth==3&tu.data.small$Position==3)),16]="3.3"
tu.data.small$Pla=tu.data.small[,16]

tuc.data.small=merge(tu.data.small,prog.p, by="Pla")
tuc.data.small=merge(tuc.data.small,prog.d, by="Dem")

binary.tu.data.small=tuc.data.small[c(which(tuc.data.small$Click<=1)),]
binary.tu.data.small$Click=as.character(binary.tu.data.small$Click)
binary.tu.data.small=as.ffdf(factorise(binary.tu.data.small))

binary.tu.data.datastream <- datastream_ffdf(data=binary.tu.data.small[1:90000,])


######## SAME PROCEDURE


b.ctrl <- MOAoptions(model = "NaiveBayes")
b.mymodel <- NaiveBayes(control=b.ctrl)

trained.tuc <- trainMOA(model = b.mymodel, Click ~ Impression +AdID+Depth+Position+CTR.P+CTR.D,
                      data = binary.tu.data.datastream, chunk=10000, trace=TRUE)

v.set=binary.tu.data.small[-c(1:90000),]                   
b.predictions=predict(object = trained.tuc, 
                      newdata=v.set,
                      type="response")  

table(b.predictions,v.set$Click)
ROCR.b=as.data.frame(cbind(b.predictions, v.set$Click))
colnames(ROCR.b)=c("predictions","labels")

auc(roc(ROCR.b$predictions,ROCR.b$labels))


