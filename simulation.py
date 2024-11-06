import random
import pygame
import simpy
from pathlib import Path
import time
import sys
from box import Box

from classroom import Classroom
from coffee_corner import CoffeeCorner
from coffee_machine import CoffeeMachine
from hallway import Hallway
from name_generator import NameGenerator
from states.hallway_state import HallwayState
from student import Student
from ui import UI, Legend
from pygame.locals import *


class Simulation:

    def __init__(self, conf: Box):
        """
        Initialize all attributes without declaring their values, then use reset() to declare values.
        :param conf: configuration for the simulation
        """
        self.real_screen = None
        self.screen = None
        self.background = None
        self.env = None
        self.paused = None
        self.fps = None
        self.max_end_time = None
        self.last_frame_time = None
        self.simulation_time = None
        self.simulation_speed = None
        self.legend = None
        self.ui = None
        self.coffee_corner = None
        self.coffee_machines = None
        self.classroom = None
        self.hallway = None
        self.students = None
        self.conf = conf

        self.reset(conf)

    def reset(self, conf):
        """
        Reset the simulation. Set all attributes of the simulation to their initial values
        :param conf: configuration for the simulation
        :return:
        """
        # initialize pygame
        self.real_screen, self.screen, self.background = self.setup_pygame(conf)
        self.calculate_screen_transform()

        # initialize simpy
        self.env = simpy.Environment()
        self.paused = not conf.headless

        # initialize time settings
        self.simulation_speed = 10 if not conf.headless else 999999999 # dirty fix for headless
        self.fps = 20
        self.max_end_time = 5000000
        self.last_frame_time = time.time()
        self.simulation_time = 0

        # UI
        self.legend = Legend(conf.ui.legend.left, conf.ui.legend.top, conf.ui.legend.width, conf.ui.legend.height,
                             self.paused, self.simulation_speed, self.simulation_time)
        self.ui = UI(self.screen, conf.ui.font_filename, conf.ui.font_size, conf.ui.position[0], conf.ui.position[1],
                     conf.ui.width, conf.ui.height, self.legend)

        # Coffee Corner
        self.coffee_corner = CoffeeCorner(self.env, self.screen,
                                          conf.coffee_corner.position[0], conf.coffee_corner.position[1],
                                          conf.coffee_corner.width, conf.coffee_corner.height)

        # TODO: When you want more or less coffee machines you could remove amount in the configuration and in the logic
        #  below make use of all the "positions" in the configuration for a more generic approach.
        self.coffee_machines = []
        for i in range(conf.coffee_machine.amount):
            self.coffee_machines.append(CoffeeMachine(self.env, self.screen,
                                                 Path(conf.coffee_machine.image),
                                                 image_size=(conf.coffee_machine.width, conf.coffee_machine.height),
                                                 position=(
                                                     conf.coffee_machine.position[i][0],
                                                     conf.coffee_machine.position[i][1])))
        self.coffee_corner.add_coffee_machines(self.coffee_machines)

        # Classroom
        self.classroom = Classroom(self.env, self.screen, conf.classroom.position[0],
                              conf.classroom.position[1], conf.classroom.width, conf.classroom.height,
                              conf.classroom.seat_size, conf.classroom.seat_image, conf.classroom.student_table_offset,
                              capacity=conf.classroom.seats)

        # Hallway
        self.hallway = Hallway(self.env, self.screen, conf.hallway.position[0], conf.hallway.position[1], conf.hallway.width,
                          conf.hallway.height, conf.hallway.spot_size, conf.hallway.rows)

        # Students
        # TODO: You might want to change the way students are spawned
        NUM_STUDENTS = 1
        self.students = []
        image_size = conf.student.size
        image_grid_size = conf.student.grid_size
        student_names = NameGenerator().randomNames(NUM_STUDENTS)
        # If you uncomment the line below, the students each get a unique character as a name,
        # which is arguably easier to read for debugging.
        # student_names = [chr(i) for i in range(65, 65+NUM_STUDENTS)]
        for i in range(NUM_STUDENTS):
            image_path = random.choice(list(Path(conf.student.images_path).glob("*.png")))
            student = Student(student_names[i], self.env, self.screen, Path(image_path), image_size, image_grid_size,
                        coffee_machines=self.coffee_machines,
                        classroom=self.classroom, hallway=self.hallway)
            student.start_state(HallwayState(self.env, student))
            self.students.append(student)

    def draw(self, delta_time):
        """
        Draw everything and update screen
        :return:
        """
        self.screen.blit(self.background, (0, 0))
        self.coffee_corner.draw()
        self.classroom.draw()
        self.hallway.draw()
        self.ui.draw()
        for student in self.students:
            student.draw(delta_time)

        self.real_screen.blit(pygame.transform.smoothscale(self.screen, self.target_rect.size), self.target_rect)
        pygame.display.flip()

    def handle_pygame_events(self):
        """
        Handles events like mouse clicks and keyboard presses
        :return:
        """
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.QUIT
                sys.exit()
            # mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                # select agent
                if event.button == 1:
                    found = False
                    old = self.ui.object
                    for student in self.students:
                        if student.rect.collidepoint(event.pos) and self.ui.object != student:
                            self.ui.object = student
                            student.select()
                            found = True
                    if not found:
                        self.ui.object = ""
                    if self.ui.object != old and isinstance(old, Student):
                        old.deselect()
            # hot keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.realtime_start = time.time() - self.simulation_time
                    self.paused = not self.paused
                    self.ui.legend.paused = self.paused
                elif event.key == pygame.K_w:
                    # based on the speed of your sim you can't speed up with graphics past a certain speed (6 for me)
                    self.simulation_speed = int(self.simulation_speed + 1)
                    self.realtime_start = time.time() - self.simulation_time
                elif event.key == pygame.K_s:
                    self.simulation_speed = max(self.simulation_speed -1, 0.1)
                    self.realtime_start = time.time() - self.simulation_time
                elif event.key == pygame.K_r:
                    self.reset(self.conf)
                elif event.key == pygame.K_t:
                    self.simulation_speed = 1
            # resizable window
            elif event.type == VIDEORESIZE:
                self.real_screen = pygame.display.set_mode(event.size, HWSURFACE | DOUBLEBUF | RESIZABLE)
                self.calculate_screen_transform()

        self.simulation_speed = round(self.simulation_speed, 2)
        self.ui.legend.speed = self.simulation_speed

    def run_for(self, delta_time):
        """
        Our simulation is allowed to check for all events up to the moment defined by simulation_time, after that we will
        sleep for a time based on our sim speed
        :return:
        """
        if self.paused:
            return
        self.simulation_time += delta_time
        self.ui.legend.sim_time = self.simulation_time
        if not self.conf.headless:
            self.ui.draw()

        # env.peek() gives the time of the next event in the simpy environment
        while self.env.peek() < self.simulation_time:
            self.env.step()

    def calculate_screen_transform(self):
        screen_rect = self.screen.get_rect()
        buffer_rect = self.real_screen.get_rect()
        source_aspect = screen_rect.w / screen_rect.h
        target_aspect = buffer_rect.w / buffer_rect.h
        if(source_aspect < target_aspect):
            target_w = buffer_rect.h * source_aspect
            self.target_rect = Rect((buffer_rect.w - target_w) / 2, 0, target_w, buffer_rect.h)
        else:
            target_h = buffer_rect.w / source_aspect
            self.target_rect = Rect(0, (buffer_rect.h - target_h) / 2, buffer_rect.w, target_h)

    @staticmethod
    def setup_pygame(conf):
        """ Wrapper for setting up pygame in our program """
        pygame.init()
        pygame_screen = pygame.display.set_mode((conf.screen.width, conf.screen.height), HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption("School Sim")
        buffer_screen = pygame_screen.copy()
        background = pygame.image.load(Path(conf.background)).convert()
        buffer_screen.blit(background, (0, 0))
        pygame.font.init()
        return pygame_screen, buffer_screen, background
