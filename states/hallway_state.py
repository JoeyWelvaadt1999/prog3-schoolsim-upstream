import random
from random import randint

import simpy

from state import State
from student import Student


"""
Behaviour of a student in the hallway
"""
class HallwayState(State):
    def __init__(self, env: simpy.Environment, student: Student = None):
        super().__init__()
        self.env = env
        self.student = student
        self.animation_speed = max(random.normalvariate(2, 0.5), 1)

    # TODO: Placeholders, student inserts modelled behaviour here
    def enter(self):
        self.hallway = self.student.kb['hallway']
        self.hallway_spot, position = self.hallway.place_student()
        self.student.change_position(position)

    def step(self):
        yield self.env.timeout(randint(1, 8))
        self.hallway.remove_student(self.hallway_spot)
        self.hallway_spot = -1
        from states.classroom_state import ClassroomState
        from states.coffee_state import CoffeeState
        if isinstance(self.fsm.previous_state, CoffeeState):
            self.switch_state(ClassroomState(self.env, self.student))
        else:
            self.switch_state(CoffeeState(self.env, self.student))

    def leave(self) -> None:
        pass
