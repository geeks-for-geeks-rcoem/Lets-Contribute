a = []
for i in range(0,10):
    elem = int(input("Enter a number"))
    a.append(elem)
    if a[i]%2 == 0:
        a[i] = a[i]*2 

for i in range(0,10):
    print(f"The new list is {a[i]}")