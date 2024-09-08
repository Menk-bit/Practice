dna = str(input())
dna_list = [char for char in dna]
length = 1
largest_length = 1
for x in range(len(dna_list)):
    if x+1 != len(dna_list) and dna_list[x] == dna_list[x+1]:
        length = length + 1
        if largest_length < length:
            largest_length = length
    else: length = 1
print(largest_length)