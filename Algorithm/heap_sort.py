
import time
import random

# O(n*lg(n))
def swap(A, i, j):
    tmp = A[i]
    A[i] = A[j]
    A[j] = tmp

def heapify(A, i):
    root = A[i]
    left = A[2*i + 1] if len(A) > 2*i + 1 else None
    right = A[2*i + 2] if len(A) > 2*i + 2 else None
    if left == None and right == None: return
    smaller_idx = 2*i + 1 if right==None or min(left, right) == left else 2*i + 2
    if root > A[smaller_idx]:
        swap(A, i, smaller_idx)
        heapify(A, smaller_idx)
    return

def build_heap(A):
    for i in reversed(range(int(len(A)/2))):
        heapify(A, i)
    return A

def heap_sort(A):
    result = []
    A = build_heap(A)
    for i in range(len(A)):
        swap(A, 0, -1)
        result.append(A.pop())
        if A: heapify(A, 0)
    return result

def compare(arr):
    A = [3, 31, 48, 73, 8, 11, 20, 29, 65, 15] if arr == None else arr
    A_t = A.copy() # to compare with default python sort

    ### My merge sort
    s_time = time.time()
    A = heap_sort(A)
    m_time = time.time() - s_time

    ### Python default sort
    s_time = time.time()
    A_t.sort()
    d_time = time.time() - s_time
    
    if A == A_t:
        print("Correct")
    else:
        print("Incorrect")

    if s_time > d_time:
        print("Faster")
    else:
        print("Slower")

N = 10
compare(random.sample(range(1, 1000), N))