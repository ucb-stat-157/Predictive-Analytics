# R Code work by Michael Raftery

# These are packages that need to be loaded
require(ff); require(RMOA); require(ffbase); require(AUC); require(ROCR)


# From one of the competition readings, a team mentioned using ff package; it works with patience

#training.ff <- read.table.ffdf(file="~/1 Statistics/157/HW4/training.txt")
#userid.ff <- read.table.ffdf(file="~/1 Statistics/157/HW4/userid_profile.txt")
#save.ffdf(userid.ff, dir="~/1 Statistics/157/PROJECT TEAM/userid")
#save.ffdf(training.ff, dir="~/1 Statistics/157/PROJECT TEAM")
#load.ffdf("~/1 Statistics/157/PROJECT TEAM")
#load.ffdf("~/1 Statistics/157/PROJECT TEAM/userid")
#colnames(training.ff)=c("Click","Impression","DisplayURL","AdID",
#                        "AdvertiserID","Depth", "Position","QueryID",
#                        "KeywordID","TitleID","DescriptionID","UserID")

# I experimented with userid, but as yet has not fully run 
#colnames(userid.ff)=c("UserID","Gender", "Age")
#head(userid.ff)
#training.w.userid=merge(training.ff,userid.ff, by="UserID")
#save.ffdf(training.w.userid, dir="~/1 Statistics/157/PROJECT TEAM/merge")
load.ffdf("~/1 Statistics/157/PROJECT TEAM/merge/training.w.userid")

head(table(training.ff$Impression))
head(table(training.ff$Impression))
# I have learned that number of clicks is not just 0 or 1, but larger numbers as well. 
# At this stage, the first attempts were model predicts only binary click
# I do think it useful info, but I don't know the impact on Bayes having more categories
# so far the model predict isn't doing well for correct predicting click instances, that is mostly no click, but minimal click
Click
#      0         1         2         3         4         5         6         
# 142,981,069   6359105    190699     43118     18570     10481      6773      


# The used is validation single part (close to million) from AWS S3
## One has to be careful to correct to the right columns to conform with training columns
v.t <- read.delim("~/1 Statistics/157/PROJECT TEAM/validation micro", header=FALSE)
colnames(v.t)=c("ratio","type","Click","Impression","DisplayURL","AdID",
                "AdvertiserID","Depth", "Position","QueryID",
                "KeywordID","TitleID","DescriptionID","UserID")
v.data=v.t[,c("Click","Impression","DisplayURL","AdID",
              "AdvertiserID","Depth", "Position","QueryID",
              "KeywordID","TitleID","DescriptionID","UserID")]

# RMOA package that works with chunks of data
instances <- read.delim("~/1 Statistics/157/HW4/instances.txt", header=FALSE)
colnames(instances)=c("Click","Impression","DisplayURL","AdID",
                      "AdvertiserID","Depth", "Position","QueryID",
                      "KeywordID","TitleID","DescriptionID","UserID")
# Click must be character type; conforming to required format for this package; otherwise predict doesn't work

v.data.small=v.data[1:100000,]
table(v.data.small$Click,v.data.small$Impression)
binary.v.data.small=v.data.small[c(v.data.small$Click<=1),]
binary.v.data.small$Click=as.character(binary.v.data.small$Click)
binary.v.data.small=factorise(binary.v.data.small)

t.data.small=training.ff[1:1000000,]
binary.t.data.small=t.data.small[c(t.data.small$Click<=1),]

t.data.small$Click=as.character(t.data.small$Click)
t.data.small=factorise(t.data.small)

t.data.datastream <- datastream_dataframe(data=t.data.small)
v.data.datastream <- datastream_dataframe(data=v.data.small)

# above compromise because using all training data was increasingly time-consuming
# The below is where model is specified
b.ctrl <- MOAoptions(model = "NaiveBayes")
b.mymodel <- NaiveBayes(control=b.ctrl)

trained.t <- trainMOA(model = b.mymodel, Click ~ Impression +AdID+Depth+Position,
                      data = t.data.datastream, chunk=100000, trace=TRUE)

# The below is the predicted for new data
b.predictions=predict(object = trained.b, 
               newdata=v.data.small,
               type="response")
table(b.predictions, v.data.small$Click)
table(b.predictions); table(sort(v.data.small$Click))
# The below gives probability for events
b.votes=predict(object = trained.b, 
               newdata=instances,
               type="votes")

# THe below is the format for ROCR/AUC function
ROCR.b=as.data.frame(cbind(b.predictions, v.data.small$Click))
colnames(ROCR.b)=c("predictions","labels")

auc(roc(ROCR.b$predictions,ROCR.b$labels)) ; # 0.5013288

# ONLY BINARY CLICK OR NOT CLICK: Uses ROCR package and code found from StackOverflow    http://stackoverflow.com/questions/4903092/calculate-auc-in-r
pred <- prediction(as.numeric(ROCR.b$predictions),ROCR.b$labels)
auc.tmp <- performance(pred,"auc"); auc <- as.numeric(auc.tmp@y.values)
# the auc from previous Naive Bayes is 0.5047448, so seems bad




