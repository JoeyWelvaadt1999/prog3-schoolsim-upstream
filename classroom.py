import math
import pygame
import simpy

class Table(pygame.sprite.Sprite):

    def __init__(self, screen, image, size, pos):
        self.screen = screen
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.pos = pos

    def draw(self):
        self.screen.blit(self.image, self.pos)


class Classroom():

    def __init__(self, env, screen, left, top, width, height, seat_size, seat_img, student_table_offset, capacity=25, rows=None):
        self.env = env
        self.screen = screen
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.seats = capacity
        self.resource = simpy.Resource(self.env, capacity=capacity)
        self.seat_size = seat_size
        self.tables = []
        self.seat_img = seat_img
        self.student_table_offset = student_table_offset

        # True means there is the spot is open
        self.spots = self.seats*[True]
        # Assuming square design because im lazy
        if rows is None:
            self.rows = int(math.sqrt(capacity))
        else:
            self.rows = rows

        self._set_tables()

    def _set_tables(self):
        table_number = 0
        for row in range(self.rows*2+1):
            if row%2 == 0:
                pass
            else:
                for column in range(self.rows*2+1):
                    if column%2==0:
                        pass
                    else:
                        self.tables.append(Table(self.screen, self.seat_img, self.seat_size, (self.left + self.seat_size*column, self.top+self.seat_size*row)))
                        table_number += 1

    def place_student(self):
        """ Return index of first available table """
        try:
            index = next((index for index, spot in enumerate(self.spots) if spot))
            self.spots[index] = False
            return index, [sum(x) for x in zip(self.tables[index].pos, self.student_table_offset)]
        except ValueError as ve:
            print(f"{ve}\n This error should not occur. Simpy resources should manage spots.")
            return None

    def open_spot(self, table_number) -> bool:
        self.spots[table_number] = True

    def draw(self, width=2):
        for table in self.tables:
            table.draw()