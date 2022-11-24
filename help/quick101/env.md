```
import os

# Print the list of user's
# environment variables
print("User's Environment variable:")
print(dict(os.environ))

# Get the value of
# 'foo' environment variable
export foo=bar #in the Local Operating System
foo = os.environ['foo']
foo = os.environ.get('foo')

# Modify the value of
# 'foo'  environment variable 
os.environ['foo'] = 'tar'

# Add a new environment variable 
os.environ['learnSpark1'] = 'www.learn-spark.info'

# If the key does not exists
# it will produce an error
 os.environ['env_does_not_exist']
```
