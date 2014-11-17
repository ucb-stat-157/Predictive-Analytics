#!/usr/bin/env python

# TEAM 11: PREDICTIVE ANALYTICS
# BY: MELANIE HAN ZHAO

# Starter code from "How to write a naive bayes algorithm on MapReduce" by Yannet Interian

"""
Input format:
FEATURE_NAME1 [tab] FEATURE_VALUE1 [tab] FEATURE_NAME2 [tab] FEATURE_VALUE2 [tab] ... [tab] CLICKS [tab] IMPRESSIONS
^ FEATURE_NAME and FEATURE_VALUE for every feature used

Output format:
Pr(Click | Data) [tab] CLICK (0 or 1, 0=no_click, 1=click) [tab] IMPRESSION (1)

"""


import sys
import os.path
sys.path.append(os.path.dirname(__file__))

feature_dict = { 5: "ad_id", 6: "advert_id" }
prob_dict = {}

# in order to access this file from s3 you need to add
# something like this to your job
# -cacheFile s3://stat157-uq85def/home/yannet/code/testing_nb/sample_prob.txt#sample_prob.txt
def read_probs():
    """ Reads the probability file and outputs a dictionary.
    The file has the form:
    advert_id 10040 0.00184842883549 0.00377969762419
    advert_id 1007 0.00184842883549 0.00107991360691
    ad_id 10110295 0.00109170305677 0.000898069151325
    ad_id 10110317 0.00109170305677 0.000898069151325
    ad_id UNK 0.00109170305677 0.000449034575662
    advert_id UNK 0.00184842883549 0.000539956803456
    Total Total 0.033185840708 0.966814159292
    """
    probs = {}
    # read prob file
    with open("sample_prob.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        feature, value, prob_click, prob_no_click = line.split()
        key = "%s,%s" % (feature, value)
        probs[key] = (float(prob_click), float(prob_no_click))
    return probs

def get_prob_from_dict(feature, value):
    """ Given feature and value returns probs.
    Returns 
    (Prob(feature = value | click), Prob(feature = value | no click))
    if value is not in the dictionary
    (Prob(feature = "UNK" | click), Prob(feature = "UNK" | no click))
    """
    key = "%s,%s" % (feature, value)
    if key in prob_dict:
        return prob_dict[key]
    key = "%s,%s" % (feature, "UNK")
    if key in prob_dict:
        return prob_dict[key]
    return None


prob_dict = read_probs()
# Reading validation / test lines
for line in sys.stdin:
    line = line.strip()
    fields = line.split()

    # Temporary dictionary (per instance) mapping feature_name to feature_value for that instance
    features_dict = {}

    i = 0
    while i < len(fields)-2:
        features_dict[fields[i]] = fields[i+1]
        i += 2
    clicks, impressions = fields[i], fields[i+1]

    prob_value_given_click = 1.0
    prob_value_given_no_click = 1.

    for feature_name in features_dict.keys():
        prob_value_given_click *= get_prob_from_dict(feature_name, features_dict[feature_name])[0]
        prob_value_given_no_click *= get_prob_from_dict(feature_name, features_dict[feature_name])[1]

    prob_click = get_prob_from_dict("Total", "Total")[0]
    prob_no_click = get_prob_from_dict("Total", "Total")[1]

    prob_click_given_data = prob_value_given_click*prob_click
    prob_no_click_given_data = prob_value_given_no_click*prob_no_click

    final_prob = prob_click_given_data/(prob_click_given_data + prob_no_click_given_data)

    i = 0
    clicks_remaining = int(clicks)
    while i < int(impressions):
        if clicks_remaining > 0:
            print "%s\t%s\t%s" % (final_prob, 1, 1)
        else:
            print "%s\t%s\t%s" % (final_prob, 0, 1)
        clicks_remaining -= 1
        i += 1


