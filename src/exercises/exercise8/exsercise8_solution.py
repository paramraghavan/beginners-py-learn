'''
InsertionSort - one of the easiest sort algorithms and MergeSort - Divide and Conquer, the following:
61,109,149,111,34,2,24,119,122,125,27,145


Prove time complexity
Insertion Sort	Ω(n)	θ(n^2)	O(n^2)          Space O(1)
Merge Sort	Ω(n log(n))	θ(n log(n))	O(n log(n)) Space O(n)

Notes::
    Binary Search - Linear search to logarithmic search for sorted list
    https://www.geeksforgeeks.org/insertion-sort/
'''


# str_num_list ='61,109,149,111,34,2,24,119,122,125,27,145'
str_num_list_worst_case ='12,11,10,9,8,7,6,5,4,3,2,1' #worst case
str_num_list_best_case ='1,2,3,4,5,6,7,8,9,10,11,12'  #best case

iteration_count = 0
def insertion_sort(arr):
    global iteration_count

    for i in range(1, len(arr)):
        iteration_count +=1

        # current loop value
        curr_value = arr[i]
        j= i-1  # prev index

        # if curr value less than previous value, swap
        while j>= 0 and curr_value < arr[j]:
            iteration_count += 1
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = curr_value

    return arr


if __name__ == '__main__':
    print(f'input: {str_num_list_best_case}')
    str_list= str_num_list_best_case.split(",")
    int_num_list = list(map(int, str_list))
    insertion_sort(int_num_list)
    print(f'sorted list best case: {int_num_list}, iteration count: {iteration_count}')
    print(80*'-')
    print(f'input: {str_num_list_worst_case}')
    str_list= str_num_list_worst_case.split(",")
    int_num_list = list(map(int, str_list))
    insertion_sort(int_num_list)
    print(f'unsorted list worst case: {int_num_list}, iteration count: {iteration_count}')