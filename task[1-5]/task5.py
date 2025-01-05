"""
5) Create a function that accepts a list containing integers. Total number of elements in list may
vary. Your method should return back the list removing duplicates from list. So lets say if user
passes a following list to your function as input:

[1,2,55,1,3,2,34,55]
it's output should be:[1, 2, 55, 3, 34]
"""


def remover(input_list):
    stack = []
    
    for element in input_list:
        if element not in stack:
            stack.append(element)
    
    return stack

print(remover([1, 2, 55, 1, 3, 2, 34, 55]))
