#!/usr/bin/env python
#Team 11: Predictive Analytics
#Author: Jessica Li 

"Output Format: value_1 \t name_1 \t value_2 \t name_2 \t click \t impression"

from operator import itemgetter
import sys

current_value1 = None
current_value2 = None
current_feature1 = None
current_feature2 = None
current_click = 0
current_impression = 0

# input comes from STDIN
for line in sys.stdin:
    line = line.strip()
    value1, feature1, value2, feature2, click, imp = line.split('\t', 5)

    # convert click and impression (currently a string) to int
    try:
        click = int(click)
        imp = int(imp)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: feature value) before it is passed to the reducer
    if current_value1 == value1 and current_value2 == value2:
        current_click += click
        current_impression += imp
    else:
        if current_value1 and current_value2:
            #we use this to ignore lines where the user information is unknown
            if current_value1 != 'unknown':
            # write result to STDOUT
                print '%s\t%s\t%s\t%s\t%s\t%s' % (current_value1, feature1, current_value2,\
                                        feature2, current_click, current_impression)
        current_click = click
        current_impression = imp
        current_value1 = value1
        current_value2 = value2
        current_feature1 = feature1
        current_feature2 = feature2

# do not forget to output the last user if needed!
if current_value1 == value1 and current_value2 == value2:
    # we use this to ignore lines where the user information is unknown
    if current_value1 != 'unknown':
        print '%s\t%s\t%s\t%s\t%s\t%s' % (current_value1, current_feature1, current_value2,\
                                        current_feature2, current_click, current_impression)
