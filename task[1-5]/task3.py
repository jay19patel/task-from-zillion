"""
3) We have a count 35 heads and 94 legs among the chickens and rabbits in a farm. How many
rabbits and how many chickens do we have? Write a program to get the answer,
"""


total_head  = 35
total_leg = 94

# 1 Chickens + 1 Rabbits = Head 35
# 2 Chickens+ 4 Rabbits= Leg 94

# Chickens = 35 - Rabbits
# 2 * (35 - Rabbits) + 4 * Rabbits = 94
# 70 - 2 * Rabbits + 4 * Rabbits = 94
# 2 * Rabbits = 94 - 70
# Rabbits = 24 / 2 
# Rabbits = 12
35-12

Rebit = (total_leg - (2 * total_head)) // 2
Cat = total_head - Rebit
print(Cat,Rebit)