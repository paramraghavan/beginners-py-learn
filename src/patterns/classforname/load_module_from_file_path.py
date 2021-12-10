'''
importing from file
'''

import  importlib

spec = importlib.util.spec_from_file_location("sample.py",
                                               r"C:\Users\padma\github\python-from-a-java-developer\src\classforname\level1\level2\sample.py")
sample = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sample)

sample.printName('Aaron')