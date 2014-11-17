#!/usr/bin/env python

# TEAM 11: PREDICTIVE ANALYTICS
# BY: MELANIE HAN ZHAO

"""
Input format:
FEATURE_VALUE [tab] FEATURE_NAME [tab] CLICKS [tab] IMPRESSIONS


Output format:
FEATURE_NAME [tab] FEATURE_VALUE [tab] Pr(feature_name = feature_value | click) [tab] Pr(feature_name = feature_value | no-click)
^ repeated for every FEATURE_VALUE in every FEATURE_NAME
...
FEATURE_NAME [tab] UNK [tab] Pr(feature_name = "UNK" | click) [tab] Pr(feature_name = "UNK" | no-click)
^ repeated for every FEATURE_NAME
...
Total [tab] Total [tab] Pr(click) [tab] Pr(no_click)

"""
m = 1.0 #smoothing parameter

import sys

"""
features - a dictionary with entries in following format:
{FEATURE_NAME: {FEATURE_VALUE: (CLICKS, IMPRESSIONS)}}

* Dictionary keys are FEATURE_NAME.
* Dictionary values are python dictionaries with FEATURE_VALUE as keys, and a
	tuple (CLICKS, IMPRESSIONS)
	as values.
"""
features = {}

"""
feature_unique_ids - a dictionary that maps from FEATURE_NAME to # of unique values
	for that feature
{FEATURE_NAME: NUM_UNIQUE_VALUES}
"""
features_unique_values = {}


total_clicks = 0.0
total_impressions = 0.0

for line in sys.stdin:
    line = line.strip()
    words = line.split('\t')
    feature_value, feature_name = words[0], words[1]
    clicks, impressions = float(words[2]), float(words[3])

    if not features.has_key(feature_name):
    	features[feature_name] = {feature_value: (clicks, impressions)}
    else:
    	features[feature_name][feature_value] = (clicks, impressions)

    if not features_unique_values.has_key(feature_name):
    	features_unique_values[feature_name] = 1
    else:
    	features_unique_values[feature_name] += 1

    total_clicks += clicks
    total_impressions += impressions


#helper functions solving probabilities

def prob_feature_given_click(feature_name, feature_value):
	"""
	Pr(feature_name = feature_value | click)
	"""
	numerator = features[feature_name][feature_value][0] + m
	denominator = total_clicks + ((features_unique_values[feature_name]+1.0)*m)
	return numerator/denominator

def prob_feature_given_no_click(feature_name, feature_value):
	"""
	Pr(feature_name = feature_value | no-click)
	"""
	numerator = features[feature_name][feature_value][1] - features[feature_name][feature_value][0] + m
	denominator = total_impressions - total_clicks + ((features_unique_values[feature_name]+1.0)*m)
	return numerator/denominator

def prob_unknown_given_click(feature_name):
	"""
	Pr(feature_name = "UNK" | click)
	"""
	numerator = m
	denominator = total_clicks + ((features_unique_values[feature_name]+1.0)*m)
	return numerator/denominator

def prob_unknown_given_no_click(feature_name):
	"""
	Pr(feature_name = "UNK" | no-click)
	"""
	numerator = m
	denominator = total_impressions - total_clicks + ((features_unique_values[feature_name]+1.0)*m)
	return numerator/denominator

def prob_click():
	"""
	Pr(click)
	"""
	numerator = total_clicks
	denominator = total_impressions
	return numerator/denominator

def prob_no_click():
	"""
	Pr(no-click)
	"""
	numerator = total_impressions - total_clicks
	denominator = total_impressions
	return numerator/denominator


for feature_name in sorted(features.keys()):
	for feature_value in sorted(features[feature_name].keys()):
		if_click = prob_feature_given_click(feature_name, feature_value)
		if_no_click = prob_feature_given_no_click(feature_name, feature_value)
		print "%s\t%s\t%s\t%s" % (feature_name, feature_value, if_click, if_no_click)
	unk_click = prob_unknown_given_click(feature_name)
	unk_no_click = prob_unknown_given_no_click(feature_name)
	print "%s\t%s\t%s\t%s" % (feature_name, "UNK", if_click, if_no_click)

tot_click = prob_click()
tot_no_click = prob_no_click()
print "%s\t%s\t%s\t%s" % ("Total", "Total", tot_click, tot_no_click)



