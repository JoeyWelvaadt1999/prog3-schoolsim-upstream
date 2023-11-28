from typing import List
import pygame
from itertools import chain

from coffee_machine import CoffeeMachine


class CoffeeCorner(pygame.Rect):

    def __init__(self, env, screen, left, top, width, height):
        self.env = env
        self.screen = screen
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.coffee_machines: List[CoffeeMachine] = []

    def draw(self, width=2):
        for cm in self.coffee_machines:
            cm.draw()

    def add_coffee_machines(self, *coffee_machines):
        for cm in chain.from_iterable(coffee_machines):
            self.coffee_machines.append(cm)





