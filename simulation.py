import random
import pygame
import simpy
from pathlib import Path
import numpy as np
import time
import sys
from box import Box
from typing import List
import util

from classroom import Classroom
from scheduler import Scheduler
from coffee_corner import CoffeeCorner
from coffee_machine import CoffeeMachine
from hallway import Hallway
from name_generator import NameGenerator
from states.hallway_state import HallwayState
from student import Student
from ui import UI, Legend
from pygame.locals import *
from visualization.data_storage import DataStorage


class Simulation:

    def __init__(self, conf: Box, store: DataStorage, batch_configuration: Box):
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
        self.batch_configuration = batch_configuration

        self.store = store

        self.reset(conf, batch_configuration)

    """
        I changed the values in the config to be ratios instead of fixed values, this function returns the value it was supposed to be taking the width and height of the simulation
    """
    def get_real_from_ratio(self, ratio: float, isWidth: bool) -> int:
        otherNumber = self.conf.screen.width if isWidth else self.conf.screen.height
        return int(otherNumber * ratio)

    def reset(self, conf: Box, batch_configuration: Box):
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
        self.simulation_speed = 1 if not conf.headless else 99999*3 # dirty fix for headless
        self.fps = 20
        self.max_end_time = 500000 if not conf.headless else 1
        self.last_frame_time = time.time()
        self.simulation_time = 0

        # UI
        self.legend = Legend(self.get_real_from_ratio(conf.ui.legend.left, True), 
                                self.get_real_from_ratio(conf.ui.legend.top, False), 
                                self.get_real_from_ratio(conf.ui.legend.width, True), 
                                self.get_real_from_ratio(conf.ui.legend.height, False),
                             self.paused, self.simulation_speed, self.simulation_time)
        
        self.ui = UI(self.screen, conf.ui.font_filename, conf.ui.font_size, 
                        self.get_real_from_ratio(conf.ui.position[0], True), 
                        self.get_real_from_ratio(conf.ui.position[1], False),
                        self.get_real_from_ratio(conf.ui.width, True), 
                        self.get_real_from_ratio(conf.ui.height, False), 
                    self.legend)

        # Coffee Corner
        self.coffee_corner = CoffeeCorner(self.env, self.screen,
                                            self.get_real_from_ratio(conf.coffee_corner.position[0], True), 
                                            self.get_real_from_ratio(conf.coffee_corner.position[1], False),
                                            self.get_real_from_ratio(conf.coffee_corner.width, True), 
                                            self.get_real_from_ratio(conf.coffee_corner.height, False)
                                        )

        # TODO: When you want more or less coffee machines you could remove amount in the configuration and in the logic
        #  below make use of all the "positions" in the configuration for a more generic approach.
        self.coffee_machines = []
        clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
        for i in range(clamp(batch_configuration.coffee_machines, 1, 5)):
            self.coffee_machines.append(CoffeeMachine(self.env, self.screen,
                                                 Path(conf.coffee_machine.image),
                                                 image_size=(self.get_real_from_ratio(conf.coffee_machine.width, True), self.get_real_from_ratio(conf.coffee_machine.height, False)),
                                                 position=(
                                                     self.get_real_from_ratio(conf.coffee_machine.position[i][0], True),
                                                     self.get_real_from_ratio(conf.coffee_machine.position[i][1], False))))
        self.coffee_corner.add_coffee_machines(self.coffee_machines)

        # Classroom
        self.classroom = Classroom(self.env, self.screen, 
                                    self.get_real_from_ratio(conf.classroom.position[0], True), # position X
                                    self.get_real_from_ratio(conf.classroom.position[1], False), # Position Y
                                    self.get_real_from_ratio(conf.classroom.width, True), 
                                    self.get_real_from_ratio(conf.classroom.height, False),
                                    self.get_real_from_ratio(conf.classroom.seat_size, True), 
                                    conf.classroom.seat_image, 
                                    conf.classroom.student_table_offset,
                                    capacity=conf.classroom.seats
                                )

        # Hallway
        self.hallway = Hallway(self.env, self.screen, 
                                self.get_real_from_ratio(conf.hallway.position[0], True), 
                                self.get_real_from_ratio(conf.hallway.position[1], False),
                                self.get_real_from_ratio(conf.hallway.width, True),
                                self.get_real_from_ratio(conf.hallway.height, False),
                                self.get_real_from_ratio(conf.hallway.spot_size, True), 
                                conf.hallway.rows
                            )

        # Students
        # TODO: You might want to change the way students are spawned
        NUM_STUDENTS = batch_configuration.students
        self.students = []
        image_size = (self.get_real_from_ratio(conf.student.size[0], True), self.get_real_from_ratio(conf.student.size[1], False))
        image_grid_size = (self.get_real_from_ratio(conf.student.grid_size[0], True), self.get_real_from_ratio(conf.student.grid_size[1], False))
        student_names = NameGenerator().randomNames(NUM_STUDENTS)
        # If you uncomment the line below, the students each get a unique character as a name,
        # which is arguably easier to read for debugging.
        student_names = [chr(i) for i in range(65, 65+NUM_STUDENTS)]
        for i in range(NUM_STUDENTS):
            image_path = random.choice(list(Path(conf.student.images_path).glob("*.png")))
            student = Student(student_names[i], self.env, self.screen, Path(image_path), image_size, image_grid_size, self.store, batch_configuration.schedule, batch_configuration.characteristics,
                        coffee_machines=self.coffee_machines,
                        classroom=self.classroom, hallway=self.hallway)
            student.start_state(HallwayState(self.env, student))
            self.students.append(student)
        
        # After creating the students array we assign a schedule to each student
        scheduler: Scheduler = Scheduler(students=self.students, lessons=[], classes=["V1A", "V1B", "V2A", "V2B"])

        [student.set_schedule_information(scheduler.get_schedule_information(student.name)) for student in self.students]

        # Split the array in to two equal parts. Where each index is a student pair. This student pair will be assigned as friends of each other
        # So for example a student in the left array on index 0 would be friends with the students on the right array on index 0.
        half_array_size = (int)(len(self.students) / 2)

        left_student_array: List[Student] = self.students[half_array_size:]
        right_student_array: List[Student] = self.students[:half_array_size]

        for i in range(half_array_size):
            left_student_array[i].set_friend(right_student_array[i])
            right_student_array[i].set_friend(left_student_array[i])

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
                
                self.store.end_run()
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
        # total = 0
        # current = 0
        
        # env.peek() gives the time of the next event in the simpy environment
        while self.env.peek() < self.simulation_time:
            util.Clock.update_clock(self.env, lambda s=self.students: [student.reset() for student in s])
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
        background = pygame.transform.scale(background, (conf.screen.width, conf.screen.height))
        buffer_screen.blit(background, (0, 0))
        pygame.font.init()
        return pygame_screen, buffer_screen, background
