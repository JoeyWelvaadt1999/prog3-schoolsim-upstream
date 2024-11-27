from state import State
from student import Student

import simpy

class WanderingState(State):
    def __init__(self, env: simpy.Environment, student: Student = None) -> None:
        super().__init__()
        self.env = env
        self.student = student

    def enter(self) -> None:
        pass

    def step(self):
        yield self.env.timeout(10)
        from states.classroom_state import ClassroomState
        self.switch_state(ClassroomState(self.env, self.student))

    def leave(self) -> None:
        pass
