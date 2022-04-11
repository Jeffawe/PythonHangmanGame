import random
import numpy as np

word_list = [
    'Big',
    'Small',
    'Reckless',
    'Night',
    'Random',
]

word_list_description = [
    'Large',
    'tiny',
    'women driving',
    'black man',
    'Anything',
]

word = random.choice(word_list)
index = word_list.index(word)
description = word_list_description[index]

print(word)
print("Can be described as", description)
