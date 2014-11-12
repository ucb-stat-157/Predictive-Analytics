#hhp <- read.table.ffdf(file="~/1 Statistics/157/HW4/training.txt")
head(hhp)

colnames(hhp)=c("Click",
                  "Impression",
                  "DisplayURL",
                  "AdID",
                  "AdvertiserID",
                  "Depth",
                  "Position",
                  "QueryID",
                  "KeywordID",
                  "TitleID",
                  "DescriptionID",
                  "UserID")
length(unique(hhp$QueryID))
# 24122076
length(unique(hhp$AdID))
# 641707
save.ffdf(hhp, dir="~/1 Statistics/157/PROJECT TEAM")

require(AUC); require(ROCR)
require(ff); require(RMOA); require(ffbase)

load.ffdf("~/1 Statistics/157/PROJECT TEAM")

head(hhp)
training=hhp
rm(hp)
head(training)

data(churn)
auc(sensitivity(churn$predictions,churn$labels))
auc(specificity(churn$predictions,churn$labels))
auc(accuracy(churn$predictions,churn$labels))
auc(roc(churn$predictions,churn$labels))
plot(sensitivity(churn$predictions,churn$labels))
plot(specificity(churn$predictions,churn$labels))
plot(accuracy(churn$predictions,churn$labels))

plot(roc(churn$predictions,churn$labels))

plot(churn$predictions, churn$labels)

# Naive Bayes want a smaller data set
set.seed(25)  # the 3 million is from reading num of 13 billion; the 149 billion is row length of traing
samp.rows=sample(1:149639105, 3597121, replace=FALSE)
t.validation=training[c(samp.rows),]

write.table(t.validation, "~/1 Statistics/157/PROJECT TEAM/t.validation.txt", sep="\t") 

t.v.datastream <- datastream_dataframe(data=t.validation)
mymodel <- trainMOA(model = hdt, Click ~ Impressions + Depth + Position,
                    data = t.v.datastream, chunksize = 10000)
mymodel$model
irisdatastream$reset()
mymodel <- trainMOA(model = hdt,
                    Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Length^2,
                    data = irisdatastream, chunksize = 10, reset=TRUE, trace=TRUE)
mymodel$model