from random import randint
from typing import List

import pygame

class Hallway(pygame.Rect):

    def __init__(self, env, screen, left, top, width, height, spot_size, rows=None):
        self.env = env
        self.screen = screen
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.spot_size = spot_size
        self.rows = rows
        self.spots: List[pygame.Rect] = self._create_spots()

    def place_student(self):
        index = 0
        while True:
            index = randint(0, len(self.spots)-1)
            if not self.spots[index][1]:
                break
        self.spots[index][1] = True
        return index, (self.spots[index][0].left, self.spots[index][0].top)

    def remove_student(self, index):
        self.spots[index][1] = False

    def _create_spots(self):
        # Custom amount of rows, or calculated based on available space
        if self.rows is None:
            rows = int(self.height/self.spot_size)
        else:
            rows = self.rows

        columns = int(self.width/self.spot_size)
        result = []
        for i in range(columns):
            for j in range(rows):
                result.append([pygame.Rect(self.left+i*self.spot_size, self.top+j*self.spot_size, self.spot_size, self.spot_size), False])
        return result

    def draw(self):
        pass

