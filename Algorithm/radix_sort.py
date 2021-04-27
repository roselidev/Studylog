
import time
import random

# O(n)
def get_digit(number, d):
    return (number // 10 ** d) % 10

def counting_sort_with_digit(A, d):
    B = [-1] * len(A)
    C = [0] * 10
    for a in A:
        C[get_digit(a, d)] += 1
    for i in range(9):
        C[i+1] += C[i]
    for i in reversed(range(len(A))):
        B[C[get_digit(A[i], d)] - 1] = A[i]
        C[get_digit(A[i], d)] -= 1
    return B

def radix_sort(A):
    max_len = max([len(str(i)) for i in A])

    for i in range(max_len):
        A = counting_sort_with_digit(A, i)
    return A

def compare(arr):
    A = [3, 31, 48, 73, 8, 11, 20, 29, 65, 15] if arr == None else arr
    A_t = A.copy() # to compare with default python sort

    ### My merge sort
    s_time = time.time()
    A = radix_sort(A)
    m_time = time.time() - s_time

    ### Python default sort
    s_time = time.time()
    A_t.sort()
    d_time = time.time() - s_time
    
    if A == A_t:
        print("Correct")
    else:
        print("Incorrect")

    if m_time > d_time:
        print("Faster")
    else:
        print("Slower")

N = 10
compare(random.sample(range(1, 1000), N))