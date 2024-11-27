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

    def enter(self) -> None:
        self.waiting_patience = np.random.randint(0, 5)

    # TODO: Placeholder, student inserts modelled behaviour here
    def step(self):
        nr_of_drinks = np.random.poisson(self.student.general_thirstiness, size=1)[0]

        coffee_machine = self.student.enter_coffee_machine_queue()

        self.student.text = "Is waiting their turn for drinks"

        with coffee_machine.resource.request() as req:
            yield req
            if(len(coffee_machine.signal.students) < self.waiting_patience):
                
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
            else: 
                print(f"{self.student.name}: Thinks the queue is too long")
                self.student.text = f"What a long queue, i'll find another time to get coffee"

        self.student.leave_coffee_machine_queue(coffee_machine)

        self.student.text = "At the hallway. Walking to the classroom"
        from states.hallway_state import HallwayState
        new_state = HallwayState(self.env, self.student)
        new_state.sprite = 4
        self.switch_state(new_state)

    def leave(self) -> None:
        pass


    import random

# import numpy as np
# import simpy

# from state import State
# from student import Student

# """
# Behaviour of a student at the coffee machine
# """
# class CoffeeState(State):
#     def __init__(self, env: simpy.Environment, student: Student = None):
#         super().__init__()
#         self.env = env
#         self.student = student
#         self.sprite = 10
#         self.animation_speed = max(random.normalvariate(1, 0.25), 0.5)
#         # Arbitrarily chosen
#         self.drink_choice = (["coffee", "tea"], 1, [0.8, 0, 2])

#     def enter(self) -> None:
#         # Determine how long the student wants to wait for coffee
#         self.waiting_patience = np.random.randint(0, 5)

#     # TODO: Placeholder, student inserts modelled behaviour here
#     def step(self):
#         nr_of_drinks = np.random.poisson(self.student.general_thirstiness, size=1)[0]

        
#         coffee_machine = self.student.enter_coffee_machine_queue()
        
#         self.student.text = "Is waiting their turn for drinks"

#         print(f"Queue: {len(coffee_machine.signal.students)}")
#         # if(len(coffee_machine.signal.students) < self.waiting_patience):
#         with coffee_machine.resource.request() as req:
#             yield req
#             print(f"{self.student.name}'s turn!")
#             # TODO: logischer om deze keuze vanuit classroom te maken
#             self.student.text = "What drink to take...\nHm...."

#             yield self.env.timeout(2)

#             self.drink = np.random.choice(*self.drink_choice)[0]
#             self.student.text = f"Today I am taking {nr_of_drinks} {'liter' if nr_of_drinks == 1 else 'liters'} of {self.drink}."
#             yield self.env.timeout(2)
#             self.student.text = f"Admires {self.drink} being made...Incredible device!!"

#             yield self.env.timeout(nr_of_drinks * 2)
#             self.student.text = f"Acquired {self.drink}."
#             # self.student.leave_coffee_machine_queue(coffee_machine, 0)

#         # else:
#         #     self.student.text = f"Wow this queue is way too long i will wander around until i go back to class."
#         #     yield self.env.timeout(1)
#         #     print(f"TEST: {self.student.name} {self.student.position}")
#         self.student.leave_coffee_machine_queue(coffee_machine, self.student.position)
        

        

#         self.student.text = "At the hallway. Walking to the classroom"
#         from states.hallway_state import HallwayState
#         from states.wandering_state import WanderingState
#         new_state = HallwayState(self.env, self.student) if len(coffee_machine.signal.students) < self.waiting_patience else WanderingState(self.env, self.student)
#         new_state.sprite = 4
#         self.switch_state(new_state)

#     def leave(self) -> None:
#         pass