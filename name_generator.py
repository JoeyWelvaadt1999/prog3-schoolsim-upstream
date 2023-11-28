import random


class NameGenerator():
    def __init__(self):
        with open("names/LastNames.txt", "r") as names:
            self.lastNames = [name.strip() for name in names.readlines()]
        with open("names/FemaleNames.txt", "r") as names:
            self.femaleNames = [name.strip() for name in names.readlines()]
        with open("names/MaleNames.txt", "r") as names:
            self.maleNames = [name.strip() for name in names.readlines()]

    def randomLastNames(self, count: int):
        return random.sample(self.lastNames, count)

    def randomFemaleFirstNames(self, count: int):
        return random.sample(self.femaleNames, count)

    def randomMaleFirstNames(self, count: int):
        return random.sample(self.maleNames, count)

    def randomFirstNames(self, count: int):
        return random.sample(self.maleNames + self.femaleNames, count)

    def randomNames(self, count: int):
        return [f"{first} {last}" for (first, last) in zip(self.randomFirstNames(count), self.randomLastNames(count))]