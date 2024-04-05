#  count the number of files pattern process_*_ready.txt

directory = /Users/paramraghavan/dev/beginners-py-learn/src/advance_stuff/file_filter
pattern = "*processA_ABC-DEF*_ready.txt"

- To find the number of file(s) which have the above pattern in folder specified in directory
- Files should be ordered by "123457" of 123456_ready.txt
```shell
touch pid123_processA_ABC-DEF_123456_ready.txt
touch pid124_processA_ABC-DEF_123457_ready.txt
touch pid125_processA_ABC-DEF_123458_ready.txt

touch pid126_processB_GHI_JKF_123456_ready.txt
touch pid127_processB_GHI_JKF_123457_ready.txt



touch pid128_processA_ABC-DEF_123459_ready.txt



```