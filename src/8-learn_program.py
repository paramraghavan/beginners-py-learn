'''
This program counts how many times words appear in a sentence.
sentence.split() creates a list of words in the sentence,
 see help(str.split) for more info.
'''

# to get help
help(str.split)

'''
Read a string from standard input - which is your keyboard in this case.  
The trailing newline is stripped.
'''
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

'''
item here reads the key value from counts dict,
and we can use the counts[item] to get the value for
key
'''
for key in counts:
    print(f' key: {key} <> value: {counts[key]}')

'''
counts.items() here returns a list of (key,value) pairs
'''
for word, count in counts.items():
    if count == 1:
        # "1 times" looks weird
        print(word, "appears once in the sentence")
    else:
        print(word, "appears", count, "times in the sentence")