Predictive-Analytics
====================

Team 11: David San Juan, Jessica Li, Melanie Zhao, Michael Raftery

# Aggregating Data

Acquire the training, validation, and testing sets from https://www.kddcup2012.org/c/kddcup2012-track2. For Stat 157, the data was in shared folder of Amazon Web Service.

To aggregate data locally, have the 'features_lib.py' and 'userid_profile.py' files in the same directory as the training, test, and validation sets that you are woking in. The 'feautures_lib.py' file can be found on GitHub. The 'userid_profile.py' file involves a bit of computation. The userid_profile.txt file can be found under the S3 shared folder. After downloading, follow the steps provided on the final report to convert userid_profile.txt into python script userid_profile.py. You will also need the MapReduce files which are all on Github.

The next step is to aggregate the data from the training, validation, and test sets so that the probabilities can be computed by our models. For Naive Bayes, training and validation/test sets require different input format.

To aggregate the data from the training set, MapReduce the dataset using train_mapper.py as mapper and train_reducer.py as reducer.

To aggregate the data from the validation and testing sets, MapReduce the dataset using test_mapper.py as mapper and test_reducer.py as reducer.

These outputed formats will be the input to our models.

# Naive Bayes Classifier
The Python implementation of Naive Bayes comes with 3 Python script files: compute_probabilities.py, naivebayes_mapper.py, and find_auc.py. These three files should be ran in that order.

1.) Use aggregated Training set data as input for compute_probabilities.py and save the output into a plain text file. Name this text file sample_prob.txt. Make sure that this output file is explicitly named "sample_prob.txt".

2.) Use aggregated Validation or Test (depending on if calculating the Validation set AUC or Test set AUC) data as input for naivebayes_mapper.py, with sample_prob.txt as a helper file. If running locally, make sure that sample_prob.txt is in the same directory. Use an identity reducer as necessary if running on AWS. Save the output of this MapReduce progress to use as input for find_auc.py (see section: Calculating AUC).

# Calculating AUC
For Naive Bayes AUC calculations, the script find_auc.py uses the output of naivebayes_mapper.py to output an AUC score.
The R code for logistic regression model, uses the pROC package, which requires the format probability and binary click.

# Other Models
For Logistic Regression only a small amount of training was able to be run in R. The small training is AWS validation part.00000.

Three functions from Professor to help logistic regression run.
reduceFactorLevels: recodes factors based only on the top ordered impression. 
matchFactorLevels: makes the factors kept between data groups the same
expandRow: since the data is in grouped form (clicks not binary)
the expand makes the click become binary in each row up to the amount of impressions.

R package ff and ffbase were used to handle big data. Merging userid file and training is used in R code.

