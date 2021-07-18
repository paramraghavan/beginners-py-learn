'''
This program counts how many times words appear in a sentence.
sentence.split() creates a list of words in the sentence,
 see help(str.split) for more info.
'''

# to get help
help(str.split)

import random

x= ''
while x != 'xit':
    print(random.randint(1, 6))
    x= input('Roll the dice again, xit to Exit')


sentence = input("Enter a sentence: ")

counts = {}     # {word: count, ...}
for word in sentence.split():
    if word in counts:
        # we have seen this word before
        counts[word] += 1
    else:
        # this is the first time this word occurs
        counts[word] = 1

print()     # display an empty line

for item in counts:
    print(item)

for word, count in counts.items():
    if count == 1:
        # "1 times" looks weird
        print(word, "appears once in the sentence")
    else:
        print(word, "appears", count, "times in the sentence")