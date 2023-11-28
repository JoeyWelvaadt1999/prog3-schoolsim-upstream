import pygame
from simpy_fsm import SimpyFSM


class Legend(pygame.rect.Rect):

    def __init__(self, left, top, width, height, paused, sim_speed, sim_time):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.paused = paused
        self.speed = sim_speed
        self.sim_time = sim_time

    def __str__(self):
        return f"Pause: SPACE ({self.paused})\n" \
               f"Faster: W\n" \
               f"Slower: S\n" \
               f"Reset: R\n" \
               f"Reset to 0: T\n" \
               f"Sim Speed: {self.speed}\n" \
               f"Sim Time: {self.sim_time:.1f}\n"


class UI(pygame.rect.Rect):

    def __init__(self, screen, font_filename, font_size, left, top, width, height, legend):
        self.screen = screen
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.font: pygame.font = pygame.font.Font(font_filename, font_size)
        self.object = "Click any student for more info."
        self.legend = legend

    def draw(self):
        match self.object:
            case SimpyFSM():
                image = self.object.image
                text_surface = self.font.render(self.object.__str__(), False, (0,0,0), wraplength=self.width)
                self.screen.blit(image, (self.left, self.top))
                self.screen.blit(text_surface, (self.left, self.top+self.object.image_size+5))
            case _:
                text_surface = self.font.render(str(self.object), True, (0, 0, 0), wraplength=self.width)
                self.screen.blit(text_surface, (self.left, self.top))

        text_surface = self.font.render(self.legend.__str__(), True, (0,0,0))
        self.screen.blit(text_surface, (self.legend.left, self.legend.top))
