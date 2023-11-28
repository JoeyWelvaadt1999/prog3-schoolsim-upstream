# Source: https://www.pygame.org/wiki/Spritesheet

import pygame

class Spritesheet(object):

    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(message)

    def image_at(self, rectangle, colorkey = None):
        """
        Loads image from x,y,x+offset,y+offset.
        Use colorkey=-1 to use topleft pixel color as key.
        """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """
        Loads multiple images, supply a list of coordinates
        """
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_grid(self, rect, cols, rows, colorkey = None):
        """
        Loads a strip of images and returns them as a 2D list
        """
        rects = []
        for y in range(rows):
            for x in range(cols):
                rects.append((rect[0]+rect[2]*x, rect[1]+rect[3]*y, rect[2], rect[3]))
        return self.images_at(rects, colorkey)