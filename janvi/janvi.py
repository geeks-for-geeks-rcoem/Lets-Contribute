
a=[]
for i in range(10):
    val=int(input("enter"))
    a.append(val)
for i in range(0,10,2):
    a[i]=a[i]*2
    print(a[i])

# Please dont be offended I did this
# what is someone enters a string?
a = []
for i in range(10):
    try:
        val = int(input("enter an integer"))
        a.append(val)
    except ValueError:
        print("please enter an Integer")
for i in range(0, 10, 2):
    a[i] = a[i]*2
    print(a[i])

"""
the adjustment i made makes it possible for someone not to input a string but it only
works between range(2-10). If you input a string at the beginning of the code, it will 
terminae the code after the exception but if its betweeen range 2-10, the loop continues.
Again, sorry for doing this.
"""
