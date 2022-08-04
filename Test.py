class Test:
    def f(self):
        self.k()

    def k(self):
        print(123)

class Test2(Test):
    def k(self):
        print(234)

Test2().f()
