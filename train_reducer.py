#!/usr/bin/env python
#Team 11: Predictive Analytics
#Author: Jessica Li

"Output Format: feature_value \t feature_name \t click \t impression"

from operator import itemgetter
import sys

current_value = None
current_feature = None
current_click = 0
current_impression = 0

# input comes from STDIN
for line in sys.stdin:
    line = line.strip()
    value, feature, click, imp = line.split('\t', 3)

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
    if current_value == value:
        current_click += click
        current_impression += imp
    else:
        if current_value and current_value != 'unknown':
            # write result to STDOUT
            print '%s\t%s\t%s\t%s' % (current_value, current_feature,\
                                    current_click, current_impression)
        current_click = click
        current_impression = imp
        current_value = value
        current_feature = feature

# do not forget to output the last user if needed!
# we also use this to ignore lines where the user information is unknown
if current_value == value and current_value != 'unknown':
    print '%s\t%s\t%s\t%s' % (current_value, current_feature,\
                            current_click, current_impression)