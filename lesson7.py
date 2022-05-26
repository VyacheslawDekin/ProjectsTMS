import time


class Auto:

    def __init__(self, brand: str, age: int, mark: str, color: str = "", weight: float = 0.0):
        self.brand = brand
        self.age = age
        self.mark = mark
        self.color = color
        self.weight = weight

    @staticmethod
    def move() -> None:
        print("move")

    @staticmethod
    def stop():
        print("stop")

    def birthday(self):
        self.age += 1


class Truck(Auto):

    def __init__(self, brand: str, age: int, mark: str, max_load: int, color: str = "", weight: float = 0.0):
        super().__init__(brand, age, mark, color, weight)
        self.max_load = max_load

    @staticmethod
    def move():
        print("attention")
        super().move()

    @staticmethod
    def load():
        time.sleep(1)
        print("load")
        time.sleep(1)


class Car(Auto):

    def __init__(self, brand: str, age: int, mark: str, max_speed: int, color: str = "", weight: float = 0.0):
        super().__init__(brand, age, mark, color, weight)
        self.max_speed = max_speed

    def move(self):
        super().move()
        print(f'max speed is {self.max_speed}')


truck1 = Truck("volvo", 2, "342", 4, "black", 10000)
truck2 = Truck("reno", 3, "8yr", 2, "black", 7000)

print('truck 1: ')
truck1.move()
truck1.birthday()
truck1.stop()
print(truck1.brand)
print(truck1.age)
print(truck1.mark)
print(truck1.max_load)
print(truck1.color)
print(truck1.weight)

print('\ntruck 2: ')
truck2.move()
truck2.birthday()
truck2.stop()
print(truck2.brand)
print(truck2.age)
print(truck2.mark)
print(truck1.max_load)
print(truck2.color)
print(truck2.weight)

car1 = Car("mazda", 3, "3", 197, "black", 1487)
car2 = Car("honda", 2, "civic", 190, "black", 1500)

print('\ncar 1: ')
car1.move()
car1.birthday()
car1.stop()
print(car1.brand)
print(car1.age)
print(car1.mark)
print(car1.max_speed)
print(car1.color)
print(car1.weight)

print('\ncar 2: ')
car2.move()
car2.birthday()
car2.stop()
print(car2.brand)
print(car2.age)
print(car2.mark)
print(car2.max_speed)
print(car2.color)
print(car2.weight)
