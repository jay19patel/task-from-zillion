"""
Write a program that accepts a sequence of whitespace separated words as input and prints
the words after removing all duplicate words and sorting them alphanumerically.

Suppose the following input is supplied to the program:

hello world and practice makes perfect and hello world again
Then, the output should be:
again and hello makes perfect practice world

"""


def test(text):
    if not isinstance(text,str):
        print("Please eneter valid string input")
    
    stack = list()
    new_stack = list()
    for i in text.split(" "): # Remove duplicate
        if i not in stack:
            stack.append(i)

    n = len(stack)
    for i in range(n): # sorting
        for j in range(0, n-i-1):
            print(f"I :{i} {stack[j]}     J:{j} {stack[j+1]}")
            if stack[j] > stack[j+1]:
                stack[j], stack[j+1] = stack[j+1], stack[j]

    print(" ".join(stack))
test("hello world and practice makes perfect and hello world again")