size = int(input())
if size == 2 or size == 3:
    print("NO SOLUTION")
else:
    for i in range(2, size+1, 2):
        print(i, end=" ")
    for i in range(1, size+1, 2):
        print(i, end=" ")