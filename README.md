Predictive-Analytics
====================

Team 11: David San Juan, Jessica Li, Melanie Zhao, Michael Raftery

# Aggregating Data
MapReduce files to aggregate the click and impression conditioned on selected demographic, position, and depth features.
The output are the progress train and test files.

# Naive Bayes Classifier
The Naive Bayes Python Implementation has another map reduce that computes probabilities.

# Calculating AUC
For Naive Bayes AUC calculations, the script find_auc.py uses the output of probabilities.

# Other Models
For Logistic Regression, only a small amount of training was able to be run in R.
When using the same four demographic and screen location features AUC on small validation is 0.5762
Expanding the small model to include adid and advid restricted to 50, the AUC improves to 0.6197
