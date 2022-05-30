from datetime import date
from dataclasses import dataclass


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


phone = Phone(price=400, model="lg")



