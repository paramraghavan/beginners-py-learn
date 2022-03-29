'''
InsertionSort - one of the easiest sort algorithms and MergeSort - Divide and Conquer, the following:
61,109,149,111,34,2,24,119,122,125,27,145


Prove time complexity
Insertion Sort	Ω(n)	θ(n^2)	O(n^2)          Space O(1)  Quadratic
Merge Sort	Ω(n log(n))	θ(n log(n))	O(n log(n)) Space O(n)  Linear-Logarithmic

Notes::
    Binary Search - Linear search to logarithmic search for sorted list
    https://www.geeksforgeeks.org/insertion-sort/
'''

def merge_sort(arr):
    L = None
    R = None
    if len(arr) > 1:
        global iteration_count
        iteration_count +=1
        # Finding the mid of the array, note using double divisior '//'
        mid = len(arr) // 2

        # Dividing the array elements
        L = arr[:mid]

        # into 2 halves
        R = arr[mid:]

        # Sorting the first half
        merge_sort(L)

        # Sorting the second half
        merge_sort(R)

    # merge back all nodes
    if L is None  and R is not None:
        merge(arr, L, R)

    return arr

def merge(arr, L, R):
    global iteration_count
    # init all the index positions to 0
    left_idx = right_idx = curr_idx = 0

    # Copy data to temp arrays L[] and R[]
    while left_idx < len(L) and right_idx < len(R):
        if L[left_idx] < R[right_idx]:
            arr[curr_idx] = L[left_idx]
            left_idx += 1
        else:
            arr[curr_idx] = R[right_idx]
            right_idx += 1
        curr_idx += 1
        iteration_count +=1

    # Checking if any element was left
    while left_idx < len(L):
        arr[curr_idx] = L[left_idx]
        left_idx += 1
        curr_idx += 1
        iteration_count +=1

    while right_idx < len(R):
        arr[curr_idx] = R[right_idx]
        right_idx += 1
        curr_idx += 1
        iteration_count +=1


str_num_list_worst_case ='12,11,10,9,8,7,6,5,4,3,2,1' #worst case
str_num_list_best_case ='1,2,3,4,5,6,7,8,9,10,11,12'  #best case

iteration_count = 0

if __name__ == '__main__':
    print(f'input: {str_num_list_best_case}')
    str_list= str_num_list_best_case.split(",")
    int_num_list = list(map(int, str_list))
    merge_sort(int_num_list)
    print(f'sorted list best case: {int_num_list}, iteration count: {iteration_count}')
    print(80*'-')
    print(f'input: {str_num_list_worst_case}')
    str_list= str_num_list_worst_case.split(",")
    int_num_list = list(map(int, str_list))
    merge_sort(int_num_list)
    print(f'unsorted list worst case: {int_num_list}, iteration count: {iteration_count}')

