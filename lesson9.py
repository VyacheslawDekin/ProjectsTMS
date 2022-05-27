from datetime import date


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
