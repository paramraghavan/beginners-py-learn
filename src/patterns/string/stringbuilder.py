from io import StringIO

mylist = ["hello ", "here ", "is ", "a an example ", "of ", "Stringbuilder"]
file_str = StringIO()
for i in range(len(mylist)):
    file_str.write(mylist[i])
print(file_str.getvalue())