import random
import simpy

from state import State
from student import Student
from util import print_stats

"""
Behaviour of a student in the classroom
"""
class ClassroomState(State):
    def __init__(self, env: simpy.Environment, student: Student = None):
        super().__init__()
        self.env = env
        self.student = student
        self.sprite = 10
        self.animation_speed = max(random.normalvariate(0.5, 0.05), 0.25)

    def enter(self):
        pass

    # TODO: Placeholder, student inserts modelled behaviour here
    def step(self):
        _classroom = self.student.kb['classroom']
        print_stats(_classroom.resource)

        if _classroom.resource.count >= _classroom.resource.capacity:
            self.student.text = "Standing in front of a full classroom"

        with _classroom.resource.request() as req:
            self.student.text = "before req in classroom"
            yield req
            self.table_number, position = _classroom.place_student()
            self.student.change_position(position)
            self.student.text = "At the classroom. Learning incredible things about Discrete Event Systems"
            print(f"time cr before timeout {self.env.now}")
            yield self.env.timeout(10)
            print(f"time cr after timeout {self.env.now}")

        _classroom.open_spot(self.table_number)

        self.student.text = "Walking from the classroom via the hallway to the coffee corner to get a drink"
        from states.hallway_state import HallwayState
        new_state = HallwayState(self.env, self.student)
        new_state.sprite = 7
        self.switch_state(new_state)


    def leave(self):
        pass
