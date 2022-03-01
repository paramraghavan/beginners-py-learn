# Sequence (Python)
In Python, sequence is the generic term for an ordered set. There are several types of sequences in Python, 
the following three are the most important.
- Lists are the **most versatile sequence type**. The elements of a list can be any object, 
  and lists are mutable - they can be changed. Elements can be reassigned or removed, and new elements can be inserted.
- Tuples are like lists, but they are immutable - they can't be changed.
- Strings are a special type of sequence that can only store characters, and they have a special notation.

# Sequence Operations
- combines two sequences in a process called concatenation. For example, [1,2,3]+[4,5] will evaluate to [1,2,3,4,5].
- repeats a sequence a (positive integral) number of times. For example, [1,11]*3 will evaluate to [1,11,1,11,1,11].
- x in mySeq will return True if x is an element of mySeq, and False otherwise. You can negate this statement with either not (x in mySeq) or x not in mySeq.
- mySeq[i] will return the i'th character of mySeq. Sequences in Python are zero-indexed, so the first element has index 0, the second has index 1, and so on.
- mySeq[-i] will return the i'th element from the end of mySeq, so mySeq[-1] is the last element of mySeq, mySeq[-2] is the second-to-last element, etc.
- All sequences can be sliced.

# Useful Functions
- len(mySeq), short for length, returns the number of elements in the sequence mySeq.
# Searching
- mySeq.index(x) returns the index of the first occurrence of x in mySeq. Note that if x isn't in mySeq index will return an error. (Use in with an if statement first to avoid this.)
- min(mySeq) and max(mySeq) return the smallest and largest elements of mySeq, respectively. If the elements are strings this would be the first and last elements 
  in lexicographic order (the order of words in a dictionary). Note that if any two elements in mySeq are incomparable (a string and a number, for example), min and max will return errors.
- mySeq.count(x) returns the number of occurrences of x in mySeq (that is, the number of elements in mySeq that are equal to x).

ref: https://artofproblemsolving.com/wiki/index.php/Sequence_(Python)