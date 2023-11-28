from pathlib import Path
from typing import Tuple
import simpy
import pygame
import util


class CoffeeMachine:

    def __init__(self, env: simpy.Environment, screen: pygame.surface.Surface, image: Path, image_size: Tuple[int,int],
                 position: Tuple[int,int], capacity=1):
        self.env = env
        self.screen = screen
        self.img = pygame.image.load(image)
        self.img = pygame.transform.scale(self.img, image_size)
        self.image_size = image_size
        self.position = position
        # The signal is used to signal to students in the queue when they can step forward
        self.signal = util.QueueSignal()
        # A simpy resource makes sure only one student can use a coffee machine at the same time
        self.resource = simpy.Resource(env, capacity=1)

    def place_student(self, student) -> Tuple[int, int]:
        queue_length = len(self.resource.queue) + len(self.resource.users)
        print(f"{student.name} starts {queue_length}th in queue ")
        return self.position[0], self.position[1] + self.image_size[1] + queue_length * student.image_size[1]

    def draw(self):
        self.screen.blit(self.img, self.position)
