#!/usr/bin/env python
#Team 11: Predictive Analytics
#Author: Jessica Li & David San Juan

import sys
import os.path
sys.path.append(os.path.dirname(__file__))
#The following lines allow for us to import the supplemental data text files
from userid_profile import user_data
user_data = user_data.split('\n')[1:-1]

'User Demographic Feature'
# Created a dictionary outside of the function so it would not have be
# be repeatedly called upon
user_lookup = {}
for instance in user_data:
        #Split instances into ID and user data 
        temp = instance.split()
        #In the dictionary, key is userID and the gender and age are values
        user_lookup[temp[0]] = (int(temp[1]),int(temp[2]))

def get_user_info(user_id):
    return user_lookup[user_id]

def get_demographic(user_id):
    """We will assign a value to each combination of gender and age group
    where the demographic  are denoted by '(gender)(age range)'. 
    If the gender or age group is not provided for a user, 
    'unknown' will be returned.
    The age ranges are denoted by numbers as follows:
        1 - (0,12]
        2 - (12-18]
        3 - (18-24]
        4 - (24-30]
        5 - (30-40]
        6 - 40+
    EX: 'M3' would indicate a male that is between 18-24 years old
        'F6' would indicate a femal that is greater than 40 years old
    """
    #This is how we chose to identify and denominate the feature values
    demographics = {(1,1):'M1', (1,2):'M2', (1,3):'M3',\
                (1,4):'M4', (1,5):'M5', (1,6):'M6',\
                (2,1):'F1', (2,2):'F2', (2,3):'F3',\
                (2,4):'F4', (2,5):'F5', (2,6):'F6'}
    #check to make sure there are valid inputs, and if not return 'unknown'
    try:
        user_info = get_user_info(user_id)
        return demographics[user_info]
    except:
        return 'unknown'


'Relative Ad Placement'

def get_placement(depth, position):
    """We will assign a value to each combination of (depth, placement)
    where depth refers to how many ads are on the page and position is 
    the ad's placement within that. 
        A - (1,1)
        B - (2,1) #2 ads impressed, ad is first one of the two
        C - (2,2) #2 ads impressed, ad is second one of the two
        D - (3,1)
        E - (3,2)
        F - (3,3)
    *Note, depth >= position because cannot have an ad in a position 
    that is greater than the number of ads being impressed.
    EX: If depth = 2, ad can only either be in the position 1 or 2.
    """
    #This is how we chose to identify and denominate the feature values
    placement = {(1,1):'A',(2,1):'B',(2,2):'C',(3,1):'D',(3,2):'E',(3,3):'F'}
    #check to make sure there are valid inputs
    try:
        place = (int(depth), int(position))
        return placement[place]
    except:
        return None

