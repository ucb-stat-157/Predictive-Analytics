# Author: Michael Raftery
# The procedure and idea for factor reduce and expand row are from Prof's sample code

require(ff);require(ffbase); require(AUC); require(ROCR)
# userid.ff <- read.table.ffdf(file="~/1 Statistics/157/HW4/userid_profile.txt")
#save.ffdf(userid.ff, dir="~/1 Statistics/157/PROJECT TEAM/userid")
load.ffdf("~/1 Statistics/157/PROJECT/userid")

# validation micro is the first part of validation20, it is near a million rows
v.t <- read.delim("~/1 Statistics/157/PROJECT/validation micro", header=FALSE)
colnames(v.t)=c("ratio","type","Click","Impression","DisplayURL","AdID",
              "AdvertiserID","Depth", "Position","QueryID",
                "KeywordID","TitleID","DescriptionID","UserID")
v.data=v.t[,c("Click","Impression","DisplayURL","AdID",
              "AdvertiserID","Depth", "Position","QueryID",
              "KeywordID","TitleID","DescriptionID","UserID")]

# v.data is a first part of validation being used as part training and part validation
### basic project
colnames(v.data)=c(tolower(colnames(v.data)))
colnames(userid.ff)=c("userid","gender", "age")

train=v.data[,c("click", "impression","adid", "advertiserid","userid","position", "depth")]
small.train.user=merge(train,userid.ff,"userid",all.x = TRUE)

small.train.user$no_clicks = small.train.user$impression - small.train.user$click

# The below are the mini case trial; it seems bad validation sampling; I want process to work
small.train.user=small.train.user[1:800000]
validation=small.train.user[-c(1:800000),]

#### GLM
library(stats)
model.one.glm <- glm(cbind(click, no_clicks) ~ age+gender+position+depth,
                   family = binomial, data = small.train.user)

summary(model.one.glm)

validation$prob <- predict(model.one.glm, newdata=validation, type="response")

#warning output: prediction from a rank-deficient fit, so may be imperfect model

## ROC analysis
# This expand row makes click binary for each row by expanding the grouped data
expandRow <- function(x) {
  prob <- rep(x$prob, x$impression)
  response <- c(rep(1, x$click), rep(0, x$no_clicks))
  data.frame(prob=prob, response=response)
}

#  not fast with large data
val_list <- lapply(1:nrow(validation), function(x) expandRow(validation[x,]))
valid_expand <- do.call(rbind, val_list)


#########################
#######  AUC   ##########
#########################
install.packages("pROC")
library("pROC")
auc(valid_expand$response, valid_expand$prob)
### Area under the curve: 0.5762    
# This is on small trainging size 800,000 and predicted on validation of size 104936

###########################################################################
###########################################################################
# EXPAND GLM model
#  Now we include ad and advid, EXPAND GLM model
# reduce the factors of ad advid, because memory and efficiency


reduceFactorLevels <- function(data, var, n=1024) {
  data <- data[,c(var, "impression")]
  vec <- as.character(data[,var])
  data_grouped <- aggregate(data["impression"], data[var], sum)
  data_grouped <- data_grouped[order(data_grouped$impression, decreasing=T),]
  new_n <- min(nrow(data_grouped), n - 1)
  keep <- as.character(data_grouped[1:new_n,var])
  vec <- ifelse(vec %in% keep, vec, "other")
  as.factor(vec)
}

matchFactorLevels <- function(data, data_to_match, var) {
  keep <- as.character(levels(data_to_match[,var]))
  vec <- as.character(data[, var])
  vec <- ifelse(vec %in% keep, vec, "other")
  as.factor(vec)
}

small.train.user$adid <- reduceFactorLevels(small.train.user, "adid", 50)
small.train.user$advertiserid <- reduceFactorLevels(small.train.user, "advertiserid", 50)

model.two.glm <- glm(cbind(click, no_clicks) ~ age+gender+position+depth+adid+advertiserid,
                     family = binomial, data = small.train.user)

validation$adid <- matchFactorLevels(validation, small.train.user, "adid")
validation$advertiserid <- matchFactorLevels(validation, small.train.user, "advertiserid")

validation$prob <- predict(model.two.glm, newdata=validation, type="response")
# Again the warning of rank-deficient

val_list <- lapply(1:nrow(validation), function(x) expandRow(validation[x,]))
valid_expand <- do.call(rbind, val_list)
auc(valid_expand$response, valid_expand$prob)
# Area under the curve: 0.6197

require(ROCR)
pred <- prediction(valid_expand$prob, valid_expand$response)
perf <- performance(pred,"tpr","fpr")
plot(perf, main="ROC curve for logistic reg model \n with 50 factor adid and advid")

################################################
######   BASIC MODEL PERFORMANCE ON TEST #######
################################################

# To see how model performs on test set
require(ff);require(ffbase)
#test <- read.table.ffdf(file="~/1 Statistics/157/PROJECT/userid/test.txt")
load.ffdf("~/1 Statistics/157/PROJECT/test")

colnames(test)=c("ratio","type","Click","Impression","DisplayURL","AdID",
                "AdvertiserID","Depth", "Position","QueryID",
                "KeywordID","TitleID","DescriptionID","UserID")
test.data=test[,c("Click","Impression","DisplayURL","AdID",
              "AdvertiserID","Depth", "Position","QueryID",
              "KeywordID","TitleID","DescriptionID","UserID")]

colnames(test.data)=c(tolower(colnames(test.data)))
colnames(userid.ff)=c("userid","gender", "age")

small.test=test.data[1:200000,]
small.test.w.user=merge(small.test,userid.ff,"userid",all.x = TRUE)

small.test.w.user$no_clicks = small.test.w.user$impression - small.test.w.user$click
small.test.w.user$prob <- predict(model.one.glm,
                                  newdata=small.test.w.user,
                                  type="response")

val_list <- lapply(1:nrow(small.test.w.user),
                   function(x) expandRow(small.test.w.user[x,]))

valid_expand <- do.call(rbind, val_list)
auc(valid_expand$response, valid_expand$prob)
# Area under the curve: 0.5973
