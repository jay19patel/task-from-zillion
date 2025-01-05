"""
Write a program that accepts multiple number of sentences as input and prints the lines after
making all characters in the sentence capitalized.
"""

def convert_into_capital(text):
    new_text = ""
    if not isinstance(text,str):
        print("Please eneter valid string input")
    for i in text:
        if 'a' <= i <= 'z':
            print("Find",i)
            converted_char1 = ord(i)-32
            print(converted_char1)
            converted_char2 = chr(converted_char1)
            print(converted_char2)
            new_text += converted_char2
        else:
            new_text += i
    print("Converted Sting is :",new_text)
convert_into_capital("Jay Patel")