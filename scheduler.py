from typing import List
from student import Student
import numpy as np

class Scheduler ():
    """
        Initialize the scheduler with certain given lessons.
    """
    def __init__(self, lessons: List[str] = [], classes: List[str] = [], students: List[Student] = []):
        self.lessons = lessons
        self.classes = classes

        # First evenly spread the students over the given classes, after which we create a dictionary where the
        # key represents the class name and the value contains the students and their schedule.

        studentsPerClass = len(students) // len(classes)
        restStudents = len(students) % len(classes)
        print(studentsPerClass, restStudents)

        students_copy: List[Student] = students.copy()
        np.random.shuffle(students_copy)
        class_schedules = {}

        self.student_class_mapping = {}
        for i in range(len(classes)):
            current_class = classes[i]
            class_schedule = self.create_schedule(i)
            class_schedules[current_class] = class_schedule
            # Get studentsPerClass amount of random students from the students array

            
            
            for j in range(studentsPerClass):
                student = students_copy.pop((studentsPerClass - 1) - j)
                self.student_class_mapping[student.name] = {
                    "class": current_class,
                    "schedule": class_schedule
                }
        
        # Assign the remaining students to the first index of classes
        for i in range(restStudents):
            print(f"{len(students_copy)}, {i}")
            student = students_copy.pop((len(students_copy) - 1) - i)
            self.student_class_mapping[student.name] = {
                "class": classes[0],
                "schedule": class_schedules[classes[0]]
            }

        print(class_schedules)

    def get_schedule_information(self, name) -> dict:
        print(self.student_class_mapping[name])
        return self.student_class_mapping[name]    

    def create_schedule (self, index) -> List[int]:
        base_schedule = [1,0,1,0,1,1,0,1]
        
        return np.roll(base_schedule, index)


        

