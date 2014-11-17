#!/usr/bin/env python

# TEAM 11: PREDICTIVE ANALYTICS
# BY: MELANIE HAN ZHAO


"""
Input format:
Pr(Click | Data) [tab] CLICK (0 or 1, 0=no_click, 1=click) [tab] IMPRESSION (1)

Output format:
a number signifying the AUC of the dataset

"""
import sys
import sklearn

from sklearn.metrics import roc_curve, auc, roc_auc_score

y_true = []
y_score = []

for line in sys.stdin:
    line = line.strip()
    words = line.split('\t')
    y_true.append(int(words[1]))
    y_score.append(float(words[0]))

auc_score = sklearn.metrics.roc_auc_score(y_true, y_score,)

print auc_score

