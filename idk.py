class a(object):
    def __init__(self, name):
        self.name = name
    def p(self):
        print(self.name)

class b(object):
    def __init__(self, name):
        self.name = name
    def p(self):
        print(self.name + " sucks")

l = [a, b]

for i in l:
    c = i("shaan")
    c.p()