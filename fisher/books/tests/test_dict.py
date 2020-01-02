# _*_ coding: utf-8 _*_
__author__ = 'john'


class A:
    def __init__(self):
        self.a = 1
        self.b = 2

d = A()
print(hasattr(d, 'a'))
