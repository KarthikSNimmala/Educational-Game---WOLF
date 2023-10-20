
class Foo():
    def __init__(self,name):
        self.name = name

    def go(self,distance):
        print(distance)

class Thing(Foo):
    def __init__(self,name,age):
        Foo.__init__(self,name)
        self.age = age

    def go(self):
        Foo.go(self,self.age)

something = Thing("Joe",12)
something.go()
