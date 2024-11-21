from state import State
from student import Student
import simpy

class WanderingState(State):
    def __init__(self, env: simpy.Environment, student: Student) -> None:
        super().__init__()
