<pre>
Insertsort the following:
61,109,149,111,34,2,24,119,122,125,27,145
</pre>

# Insertsort
To sort an array of size n in ascending order: 
- Iterate from arr[1] to arr[n] over the array. 
- Compare the current element (key) to its predecessor. 
- If the key element is smaller than its predecessor, compare it to the elements before. 
   Move the greater elements one position up to make space for the swapped element.
- ![img_2.png](img_2.png)
- [ref](https://www.geeksforgeeks.org/insertion-sort/)



# MergeSort - a Divide and Conquer algorithm
- divide  elements to leaf nodes adn merge them back
  ![img.png](img.png)
-  MergeSort(arr[], l,  r)
   <pre>
    If r > l
         1. Find the middle point to divide the array into two halves:  
                 middle m = l+ (r-l)/2
         2. Call mergeSort for first half:   
                 Call mergeSort(arr, l, m)
         3. Call mergeSort for second half:
                 Call mergeSort(arr, m+1, r)
         4. Merge the two halves sorted in step 2 and 3:
                 Call merge(arr, l, m, r)
   </pre>
- [ref](https://www.geeksforgeeks.org/merge-sort/)