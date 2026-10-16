"""
f=open("ex.txt","x")
with open("ex.txt","w")as f:
    f.write("HELLO WORLD")
with open("ex.txt","r")as f:
    con=f.read()
    print(con)



with open("ex.txt","r")as f:
    a=f.read()
a=a.replace("H","s")
f=open("exa.txt","x")
with open("exa.txt","w")as f1:
    f1.write(a)
with open("exa.txt","r")as f:
    con=f.read()
    print(con)
"""

with open("ex.txt","r")as f:
    a=f.read()
a=a.count("L")
print("count of L is",a)
