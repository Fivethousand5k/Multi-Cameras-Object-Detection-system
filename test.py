class A():
    def __init__(self):
        self.a="aa"

class B():
    def __init__(self):
        self.b="bb"

class C(A,B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)

if __name__ == "__main__":
    C=C()
    print(C.a)
    print(C.b)