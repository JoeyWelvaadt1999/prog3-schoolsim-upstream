import uuid
import pygame
import simpy
from pathlib import Path
import numpy as np

from simpy_fsm import SimpyFSM
from spritesheet import Spritesheet
from state import State
from visualization.data_storage import DataStorage

class Student():

    def __init__(self, name: str, env: simpy.Environment, screen: pygame.surface.Surface,
                 image: Path, image_size: (int, int), image_grid_size: (int, int), 
                 store: DataStorage, **knowledge_base):
        self.name = name
        self.uid = uuid.uuid4()
        self.selected = False

        self.store: DataStorage = store
        self.env = env

        self.spritesheet = Spritesheet(image)
        self.sprites = self.spritesheet.load_grid((0, 0, image_grid_size[0], image_grid_size[1]), 3, 4, -1)
        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.scale(self.sprites[i], image_size)
        self.screen = screen
        self.image_size = image_size
        self.position = (0, 0)
        self.rect = pygame.Rect(0, 0, image_size[0], image_size[1])

        # The knowledge base (kb) is knowledge the object has about other parts of the simpy simulation and pygame
        # environment. Most likely information about where to draw/blit the object. So also info on other objects
        self.kb = {}
        for k, v in knowledge_base.items():
            self.kb[k] = v

        # This is a way to introduce randomness properly (part of the Math course later on)
        self.general_thirstiness = np.random.poisson(lam=2, size=1)
        
        # Another student
        self.friend: Student = None
        self.total_drinks = 0

        self.drink = ""
        self.text = ".."
        self.table_number = -1

    def start_state(self, initial_state: State):
        self.fsm = SimpyFSM(initial_state, self.env)

    def reset(self):
        self.total_drinks = 0

    def draw(self, delta_time):
        if self.selected:
            pygame.draw.circle(self.screen, pygame.color.Color(255, 128, 0, 255), self.rect.center, self.rect.width / 2)
        self.screen.blit(self.sprites[self.fsm.state.sprite_index(delta_time)], self.position)

    def __eq__(self, rhs):
        return rhs is Student and self.uid == rhs.uid and isinstance(rhs, Student)

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"State: {self.fsm.state}\n" \
               f"Thoughts: {self.text}\n" \
               f"Friend: {self.friend.name}\n" \


    def _get_shortest_queue(self, coffee_machines):
        return sorted(coffee_machines, key=lambda x: len(x.resource.queue) + len(x.resource.users))[0]

    def enter_coffee_machine_queue(self):
        coffee_machine = self._get_shortest_queue(self.kb['coffee_machines'])
        self.change_position(coffee_machine.place_student(self))
        coffee_machine.signal.connect(self)
        return coffee_machine

    def leave_coffee_machine_queue(self, coffee_machine):
        coffee_machine.signal.disconnect(self)
        # Tell everyone you left the queue so they can move up a spot
        coffee_machine.signal.emit()

    # Use this function to set a friend for the current student, but only if they do not have a friend yet.
    def set_friend(self, friend):
        if(self.friend == None):
            self.friend = friend

    def move_up(self):
        # print(self.position[0], self.position[1], fromPosition)
        # if(fromPosition[1] < self.position[1]+self.image_size[1]):
        #     print(f"{self.name}: Needs to move up")
        self.change_position((self.position[0], self.position[1]-self.image_size[1]))

    def change_position(self, pos):
        self.position = pos
        self.rect.left = pos[0]
        self.rect.top = pos[1]

    def select(self):
        print(f"Select {self.name}")
        self.selected = True

    def deselect(self):
        print(f"Deselect {self.name}")
        self.selected = False