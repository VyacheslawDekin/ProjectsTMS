class Lesson1:

    def __init__(self, a, b):
        self._a = a
        self._b = b

        x1 = ((17 / 2) * 3) + 2
        x2 = 2 + ((17 / 2) * 3)
        x3 = ((19 % 4) + ((15 / 2) * 3))
        x4 = (15 + 6) - (10 * 4)
        x5 = (((17 / 2) % 2) * (3 ** 3))

    def sum(self):
        return self._a + self._b


    def difference(self):
        return self._a - self._b


    def multiplication(self):
        return self._a * self._b

    def raised_to_the_power(self):
        return self._a ** self._b


    def division(self):
        return self._a // self._b


    def ost(self):
        return self._a % self._b

class R:
    def __init__(self, radius):
        self.radi = radius


    @property
    def radius(self):
        return self.radi

if __name__ == '__main__':

    r = R(5)
    print(r.radius)

