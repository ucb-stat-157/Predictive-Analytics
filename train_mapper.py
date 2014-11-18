#!/usr/bin/env python
#Team 11: Predictive Analytics
#Author: Jessica Li & David San Juan

"Output Format: feature_value \t feature_name \t click \t impression"

import sys
import os.path
sys.path.append(os.path.dirname(__file__))
import features_lib as feat

# input comes from STDIN (standard input)
for line in sys.stdin:
    line = line.strip()
    instance = line.split("\t")

    #the indexes refer to the files Professor Interian provided with the
    #additional two columns in front of the original track2 data
    
    click = instance[2] #click is in col 3 of training data given 
    imp = instance[3] #impression is in col 4 of training data given
    demo = feat.get_demographic(instance[13]) #UserID is col 14
    #depth is col 8 and instance is col 9
    place = feat.get_placement(instance[7], instance[8]) 
    
    #For the progress report, we are using only using our first 2 features:
    # User Demographic & Relative Ad Placement
    print "%s\t%s\t%s\t%s" % (demo, 'User Demographic', click, imp)
    print "%s\t%s\t%s\t%s" % (place, 'Relative Ad Placement', click, imp)

    #We separate the features of the instance into separate lines for the 
    # training set data because that is the input necessary to get the 
    # information we will be using to train our model.


