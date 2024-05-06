message:str = 'Welcome to beginners-py-learn'
def generator():
    for i in message:
        yield i

def generator_loop():
  while 1:
      for i in message:
          yield i



for i in generator():
    print(i)

# generator in infinite loop
for i in generator_loop():
    print(i)


