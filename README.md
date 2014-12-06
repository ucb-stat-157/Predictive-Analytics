Predictive-Analytics
====================

Team 11: David San Juan, Jessica Li, Melanie Zhao, Michael Raftery

# Aggregating Data
MapReduce files to aggregate the click and impression conditioned on selected demographic, position, and depth features.
The output are the progress train and test files.

Aquire the training, validation, and testing sets from bcourses.

To run it locally make sure you have the 'features_lib.py' and 'userid_profile.py' files in the same directory as the training, test, and validation sets that you are woking in. The 'feautures_lib.py' file can be found on GitHub. The 'userid_profile.py' file involves a bit of computation. The userid_profile.txt file can be found under the S3 shared folder. When downloaded one can follow the steps provided on the final report to convert it into a python script. 

The next step is to aggregate the data so that the training, validation, and test sets can be run on our models. Each set Requires a different input format.

To run the training set on the Naive Bayes model you need to pass the set into the train_mapper and train_reducer files.

To run the validation set and testing sets on the Naive Bayes model you need to pass the set into the test_mapper and test_reducer files.

These outputed formats will be the input to the Naive Bayes model. The same outputs will also be used for our other models.

# Naive Bayes Classifier
The Naive Bayes Python Implementation has another map reduce that computes probabilities.

# Calculating AUC
For Naive Bayes AUC calculations, the script find_auc.py uses the output of probabilities.
The R code for logistic regression model, uses the pROC package

# Other Models
For Logistic Regression, only a small amount of training was able to be run in R.
When using the same four demographic and screen location features AUC on small validation is 0.5762
Expanding the small model to include adid and advid restricted to 50, the AUC improves to 0.6197
