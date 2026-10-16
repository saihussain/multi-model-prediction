"""
a=int(input("enter number:"))
print("factors:")
for i in range(1,a+1):
    if a%i==0:
        print(i)
"""

def f(n):
    if n<=1:
        return n
    else:
        return f(n-1)+f(n-2)
limit=100
i=0
while True:
    val=f(i)
    if val>limit:
        break
    print(val,end="")
    i+=1
    print()
