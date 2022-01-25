'''
Tower of Hanoi is a mathematical puzzle where we have three rods and n disks.
 The objective of the puzzle is to move the entire stack to another rod,
 obeying the following simple rules:
1) Only one disk can be moved at a time.
2) Each move consists of taking the upper disk from one of the stacks and placing it
on top of another stack i.e. a disk can only be moved if it is the uppermost disk on a stack.
3) No disk may be placed on top of a smaller disk

So,first we have to move those n − 1 smaller disks to the spare peg. Once that’s
done, we can move the largest disk directly to its destination. Finally, to finish
the puzzle, we have to move the n − 1 smaller disks from the spare peg to their
destination.

We’ve successfully reduced the n-disk Tower of Hanoi
problem to two instances of the (n − 1)-disk Tower of Hanoi problem, which
we can gleefully hand off to the Recursion

The algorithm moves a stack of n disks from a source peg (src) to a destination
peg (dst) using a third temporary peg (tmp) as a placeholder. Notice that the
algorithm correctly does nothing at all when n = 0.
Hanoi(n,src, dst,tmp):
if n > 0
Hanoi(n − 1,src,tmp, dst) 〈〈Recurse!〉〉
move disk n from src to dst
Hanoi(n − 1,tmp, dst,src) 〈〈Recurse!〉〉

Let T(n) denote the number of moves required to transfer n disks—the
running time of our algorithm. Our vacuous base case implies that T(0) = 0,
and the more general recursive algorithm implies that T(n) = 2T(n − 1) + 1
for any n ≥ 1. By writing out the first several values of T(n), we can easily
guess that T(n) = 2^n − 1; a straightforward induction proof implies that this
guess is correct. In particular, moving a tower of 64 disks requires 2^64 − 1 =18,446,744,073,709,551,615
individual moves. Thus, even at the impressive rate
of one move per second, the monks at Benares will be at work for approximately
585 billion years (“plus de cinq milliards de siècles”) before tower, temple, and
Brahmins alike will crumble into dust, and with a thunderclap the world will
vanish. ref: Algorithms by Jeff Erickson


ref: https://www.geeksforgeeks.org/python-program-for-tower-of-hanoi/
'''


# Recursive Python function to solve the tower of hanoi

def Hanoi(n, source, destination, tmp):
    if n == 1:
        print("Move disk 1 from source", source, "to destination", destination)
        return
    Hanoi(n - 1, source, tmp, destination)
    print("Move disk", n, "from source", source, "to destination", destination)
    Hanoi(n - 1, tmp, destination, source)


# Driver code
n = 4
Hanoi(n,'Start','End','Tmp')



# not recursiev, iterative
def nr_Hanoi(n, source, destination, tmp):
    pass # todo