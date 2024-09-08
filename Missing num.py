# Function to find the missing number from 1 to N
def solve(N, arr):
    # Variable to store the value of XOR
    XOR = 0
    for i in range(N - 1):
        # XOR of all elements in arr[]
        XOR ^= arr[i]
        # XOR of all numbers from 1 to N - 1
        XOR ^= (i + 1)
    XOR ^= N
    return XOR
 
 
N = int(input())
arr = [int(x) for x in input().split()]
 
print(solve(N, arr))
