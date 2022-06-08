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


if __name__ == '__main__':
    lesson1 = Lesson1(4, 7)
    print(lesson1.sum())
    print(lesson1.difference())
    print(lesson1.multiplication())
    print(lesson1.raised_to_the_power())
    print(lesson1.division())
    print(lesson1.ost())

