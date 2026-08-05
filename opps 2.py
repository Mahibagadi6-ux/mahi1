#__init__ funtion is the cconstuctuter as like a house  the house consist of the more things like ,the house is the conscrture aslik
# init__ funtion is the intialix=zation methe=ode in python you seee very oops topic  inhit funtion must called and class
#purpose use to defining object
#self kannada(swayam)own
class human:
    def __init__(self,name,age,lover="he dont had girlfriend and still no  friend still no "):
        self.name = name
        self.age = age
        self.lover = lover
    def walk(self):
        print(f"{self.name} is walking and his age is {self.age}")
chandan = human("chandan",18,lover="shweta")
chandan.walk()
mahesh = human("mahesh",17)
mahesh.walk()
print(mahesh.age)
print(mahesh.lover)
