from typing import List
from student import Student
import matplotlib.pyplot as plt
import numpy as np

class DataViewer():
    def __init__(self, students: List[Student]) -> None:
        self.students: List[Student] = students

    """
        Proof that the poisson distribution is correctly implemented
    """
    def plotThirstDistribution (self) -> None:
        thirsts: list = [s.general_thirstiness for s in self.students]
        plt.hist(thirsts, len(list(map(np.unique, thirsts))), density=True, stacked=True)
        plt.show()