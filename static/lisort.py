li=[5,8,2,89,31,58,65,97,82,3,9,1,8,]
print("original list:",li)
li.sort()
print("sorted:",li)
li.sort(reverse=True)
print("sorted using sort(reverse=true):",li)
li.reverse()
print("reversed:",li)

co=li.count(8)
print("count of number 8 in the list:",co)
c=len(li)
print("no.of elements in list are:",c)
print()
a=[2,5,-3,6,8]
print("another list a:",a)
a.sort(key=abs)
print("sorted using key:",a)
