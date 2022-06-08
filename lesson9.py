from datetime import date
from dataclasses import dataclass
from dataclasses import field


class Car:
    def __init__(self, model, age):
        self.model = model
        self.age = age

    @staticmethod
    def make_a_sound():
        print("sounds")

    @classmethod
    def from_year_of_issue(cls, model, year):
        return cls(model, date.today().year - year)


@dataclass
class Phone:
    price: float
    model: str
    count: int #int = field(default_factory=int)

    @staticmethod
    def total_cost(self):
        pass

phone = Phone(price=400, model="lg")
phone = Phone(price=400, model="lg")



