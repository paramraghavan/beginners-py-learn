how to convert following comma separated string into dataframe

file1.zip,12/5/24 7:15:20 AM, 1.38 MB
file2.zip,12/5/24 7:12:20 AM, 0.21 KB
file3.zip,11/27/24 8:31:00 PM, 22.18 MB
file3.zip,7/2/24 3:31:00 PM, 0.78 KB

add header 
first column is filename
second is intime of file
third is filesize
convert file size to KB

read above into dataframe,

limit the rows rows for last X minutes, lets say 30 minutes
and then order the dataframe in ascending order of intime