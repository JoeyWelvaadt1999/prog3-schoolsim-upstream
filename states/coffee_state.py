import random

import numpy as np
import simpy

from state import State
from student import Student

"""
Behaviour of a student at the coffee machine
"""
class CoffeeState(State):
    def __init__(self, env: simpy.Environment, student: Student = None):
        super().__init__()
        self.env = env
        self.student = student
        self.sprite = 10
        self.animation_speed = max(random.normalvariate(1, 0.25), 0.5)
        # Arbitrarily chosen
        self.drink_choice = (["coffee", "tea"], 1, [0.8, 0, 2])
        self.coffee_machine = ""

    def enter(self):
        self.coffee_machine = self.student.enter_coffee_machine_queue()

    # TODO: Placeholder, student inserts modelled behaviour here
    def step(self):
        nr_of_drinks = np.random.poisson(self.student.general_thirstiness, size=1)[0]



        self.student.text = "Is waiting their turn for drinks"

        with self.coffee_machine.resource.request() as req:
            yield req
            print(f"{self.student.name}'s turn!")
            # TODO: logischer om deze keuze vanuit classroom te maken
            self.student.text = "What drink to take...\nHm...."

            yield self.env.timeout(2)

            self.drink = np.random.choice(*self.drink_choice)[0]
            self.student.text = f"Today I am taking {nr_of_drinks} {'liter' if nr_of_drinks == 1 else 'liters'} of {self.drink}."
            yield self.env.timeout(2)
            self.student.text = f"Admires {self.drink} being made...Incredible device!!"

            yield self.env.timeout(nr_of_drinks * 2)
            self.student.text = f"Acquired {self.drink}."

        self.student.leave_coffee_machine_queue(self.coffee_machine)

        self.student.text = "At the hallway. Walking to the classroom"
        from states.hallway_state import HallwayState
        new_state = HallwayState(self.env, self.student)
        new_state.sprite = 4
        self.switch_state(new_state)

    def leave(self):
        pass