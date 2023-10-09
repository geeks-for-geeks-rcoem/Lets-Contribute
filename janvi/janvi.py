
a=[]
for i in range(10):
    val=int(input("enter"))
    a.append(val)
for i in range(0,10,2):
    a[i]=a[i]*2
    print(a[i])
