size = int(input())
array_string = input()
array = [int(s) for s in array_string.split()]
moves = 0
for index in range(1, len(array)):
    if array[index] < array[index-1]:
        moves = moves + array[index-1] - array[index]
        array[index] = array[index-1]
print(moves)
