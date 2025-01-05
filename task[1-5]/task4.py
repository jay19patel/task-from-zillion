"""
4) Create a function that accepts single list containing letters or may be words. Total number of
elements in a list may vary. In turn, it counts the number of occurrences in a list for each
element and returns user a dictionary with total number of counts for each element. Please
remember to include case-sensitive match i.e. 'user1' is not equal to 'User1' word.
"""


def counter(input_list):
    store = {}
    
    for i in input_list:
        if i in store:
            store[i] += 1
        else:
            store[i] = 1
    print("store:",store)
    return store

input_list = ['python', 'pyhton3', 'user1', 'assignment', 'user', 'user1', 'python', 'User']
counter(input_list)
