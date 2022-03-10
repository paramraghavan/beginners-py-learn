# loop over string
s = 'Buzz'

for char in s:
    print(char)

print('basic for loop')
# for (i=0; i <10; i++)
for i in range(10):
    print(f'counter {i}')

print('for loop with skip count')
# for (i=2; i <10; i=i+2)
for i in range(2,10,2):
    print(f'counter {i}')

# reverse Buzz

reversed_string = ''
for c in s:
    reversed_string = c + reversed_string  # appending chars in reverse order
print(reversed_string)


# while loop