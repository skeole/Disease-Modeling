with open("Names.txt") as file:
    l = list(file)
print(l)
d = []
for i in l:
    temp = i
    temp.strip()
    temp = temp.split("\t")
    print(temp)
    d.append(temp[1])
    d.append(temp[3])

print(d)