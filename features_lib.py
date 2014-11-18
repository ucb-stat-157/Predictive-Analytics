#!/usr/bin/env python
#Team 11: Predictive Analytics
#Author: Jessica Li

import sys
import os.path
sys.path.append(os.path.dirname(__file__))
#The following lines allow for us to import the supplemental data text files
from userid_profile import user_data
user_data = user_data.split('\n')[1:-1]

'''These lines will be implemented for the final project when we 
incorporate the Search Relevance Feature'''
#from queryid_tokensid.py import query_data
#from titleid_tokensid.py import title_data
#from purchasedkeywordid_tokensid.py import keyword_data
#from descriptionid_tokensid.py import description_data

#query_data = query_data.split('\n')[1:-1]
#title_data = title_data.split('\n')[1:-1]
#keyword_data = keyword_data.split('\n')[1:-1]
#description_data = description_data.split('\n')[1:-1]

'User Demographic Feature'

user_lookup = {}
for instance in user_data:
        #Split instances into ID and user data
        temp = instance.split()
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
    #This is how we chose to identify and deonimnate the feature values
    placement = {(1,1):'A',(2,1):'B',(2,2):'C',(3,1):'D',(3,2):'E',(3,3):'F'}
    #check to make sure there are valid inputs
    try:
        place = (int(depth), int(position))
        return placement[place]
    except:
        return None



'Search Relevance Feature'

def get_tokens(id_val, filename):
    """ Given (ID, filename), return the list of tokens associated with it"""
    id_token_list = filename

    for instance in id_token_list:
        #Split instances into ID and tokens
        temp = instance[0].split("\t")
        #Search to see if ID matches
        if id_val == temp[0]:
            #then splitting the tokens into a list of individual tokens
            ans = temp[1].split("|")
    return ans

def get_all_ad_tokens(ad_id):
    """Given an ad ID, find the combined list of all tokens in its
    keyword, title and description"""

    instance_list = instances
    ans = []
    #go through each instance within the file
    for instance in instance_list:
        #split each line into it's individual fields
        temp = instance.split("\t")
        #look up the ad_id in the other files to get keyword, title, description
        #get tokens for each of the respective id's
        if ad_id == temp[3]:
            ans.extend(get_tokens(temp[8], keyword_data))
            ans.extend(get_tokens(temp[9], title_data))
            ans.extend(get_tokens(temp[10], description_data))
    return ans

def get_similarity_index(query_id, ad_id):
    """Given a query_id, adID find the SimilarityIndex"""
    #getting the query tokens and then keyword/title/description tokens
    query_tok = get_tokens(query_id, query_data)
    others_tok = get_all_ad_tokens(ad_id)
    #created a counter to check how many times query tokens show up
    count = 0
    for query in query_tok:
        if query in others_tok:
            count += 1
    return count/float(len(query_tok))
