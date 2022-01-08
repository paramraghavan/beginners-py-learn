'''
ref: https://stackoverflow.com/questions/452969/does-python-have-an-equivalent-to-java-class-forname

We're using __import__ to import the module that holds the class, which required that we first extract the module name
from the fully qualified name. Then we import the module:

m = __import__( module )
In this case, m will only refer to the top level module,

For example, if your class lives in foo.baz module, then m will be the module foo
We can easily obtain a reference to foo.baz using getattr( m, 'baz' )

To get from the top level module to the class, have to recursively use gettatr on the parts of the class name

Say for example, if you class name is foo.baz.bar.Model then we do this:

m = __import__( "foo" ) #m is package foo
m = getattr( m, "baz" ) #m is package baz
m = getattr( m, "bar" ) #m is module bar
m = getattr( m, "Model" ) #m is class Model
This is what's happening in this loop:

for comp in parts[1:]:
    m = getattr(m, comp)
At the end of the loop, m will be a reference to the class. This means that m is actually the class itslef, you can do for instance:
'''

def get_class( kls ):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m

# example 1
D = get_class("datetime.datetime")
print(D)
print(D.now())
a = D( 2010, 4, 22 )
print(a)

# example 2
printName = get_class("level1.level2.sample.printName")
printName('Test2')