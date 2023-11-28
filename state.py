from abc import ABC

"""
Superclass for all states
"""
class State(ABC):
    def __init__(self):
        self.sprite = 1
        self.animation = 0
        self.frames = [0, -1, 0, 1]
        self.animation_speed = 0

    def sprite_index(self, delta_time):
        self.animation += self.animation_speed * delta_time
        if (self.animation > len(self.frames)):
            self.animation = 0
        return self.sprite + self.frames[int(self.animation)]

    def enter(self):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError

    def leave(self):
        raise NotImplementedError

    def switch_state(self, new_state):
        self.next_state = new_state

    def __str__(self):
        return self.__class__.__name__