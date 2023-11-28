import simpy
from state import State


class SimpyFSM():

    def __init__(self, initial_state: State, env: simpy.Environment):
        self.env = env
        self.state = initial_state
        self.previous_state = None

        self.state.enter()
        self.process = env.process(self.run())

    def run(self):
        cnt = 0
        while True:
            print(f"{self.state.student.name} @{cnt}: {self.state.__class__.__name__}")
            cnt += 1
            self.state.fsm = self
            yield self.env.process(self.state.step())
            if(hasattr(self.state, "next_state") and self.state.next_state != self.state):
                print(f"{self.state.student.name}: {self.state} -> {self.state.next_state}")
                self.state.leave()
                self.previous_state = self.state
                self.state = self.state.next_state
                self.state.enter()
