# Author: Michael Raftery
# SEE PREVIOUS CODE FIRST
# This code does not have many comments, as the procedure is same as other R coding
# This procedure follows the Professor's code example without the factor reduction in adid/advid

aggtrain <- read.delim("~/Desktop/progress_train_data.txt", header=FALSE)
aggtest <- read.delim("~/Desktop/progress_test_data.txt", header=FALSE)

colnames(aggtrain)=c("feature","name","click", "impression")
aggtrain$no_clicks=aggtrain$impression-aggtrain$click

colnames(aggtest)=c("feature","name","click", "impression")
aggtest$no_clicks=aggtrain$impression-aggtrain$click

model.2.glm <- glm(cbind(click, no_clicks) ~ feature,
                   family = binomial,data = aggtrain)
summary(model.2.glm)

aggtest$prob <- predict(model.2.glm, newdata=aggtest, type="response")

## ROC analysis
# Getting a vector of probabilities and responses
  expandRow <- function(x) {
    prob <- rep(x$prob, x$impression)
    response <- c(rep(1, x$click), rep(0, x$no_clicks))
    data.frame(prob=prob, response=response)
  }
  
val_list <- lapply(1:nrow(aggtest), function(x) expandRow(aggtest[x,]))
valid_expand <- do.call(rbind, val_list)

### I am able to run up to this point: the valid_expand is close to 900 million rows

install.packages("pROC")
library("pROC")
auc(valid_expand$response, valid_expand$prob)


