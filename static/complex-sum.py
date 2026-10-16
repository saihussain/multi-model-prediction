"""
#sum of complex numbers

class complex:
    def __init__(self,real,imag):
        self.real=real
        self.imag=imag
    def add(self,other):
        real_part=self.real+other.real
        imag_part=self.imag+other.imag
        return complex(real_part,imag_part)
    def display(self):
        print(self.real,"+",self.imag,"i")
r1=int(input("Enter first real number:"))
i1=int(input("Enter first imaginary number:"))
r2=int(input("Enter second real number:"))
i2=int(input("Enter second imaginary number:"))
c1=complex(r1,i1)
c2=complex(r2,i2)
result=c1.add(c2)
print("sum:")
result.display()

"""
#sub of complex numbers
class complex:
    def __init__(self,real,imag):
        self.real=real
        self.imag=imag
    def sub(self,other):
        real_part=self.real-other.real
        imag_part=self.imag-other.imag
        return complex(real_part,imag_part)
    def display(self):
        print(self.real,"+",self.imag,"i")
r1=int(input("Enter 1st real number:"))
i1=int(input("Enter 1st imaginary number:"))
r2=int(input("Enter 2nd real number:"))
i2=int(input("Enter 2nd imaginary number:"))
c1=complex(r1,i1)
c2=complex(r2,i2)
result=c1.sub(c2)
print("sum:")
result.display()
