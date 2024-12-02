import logging
from pathlib import Path
from box import Box
import yaml
import simpy

class Clock(object):
    total = 0
    current = 0
    day = 0
    hour = 0
    @staticmethod
    def update_clock(env: simpy.Environment, callback: callable) -> None:
        Clock.current = env.now - Clock.total
        if(Clock.current // (360 * (Clock.hour + 1)) == 1):
            Clock.hour += 1
        if(Clock.current // (360 * 8) == 1):
            callback()
            Clock.total = env.now
            Clock.hour = 0
            Clock.day +=1
    
    @staticmethod
    def reset_clock() -> None:
        Clock.total = 0
        Clock.current = 0
        Clock.day = 0
        Clock.hour = 0

class QueueSignal:
    def __init__(self):
        self.students = []

    def connect(self, student):
        self.students.append(student)

    def disconnect(self, student):
        self.students.remove(student)

    def emit(self):
        for student in self.students:
            student.move_up()


def print_stats(res):
    print(f'{res.count} of {res.capacity} slots are allocated.')
    print(f'  Users: {res.users}')
    print(f'  Queued events: {res.queue}')


def get_conf(path):
    CONFIG = Path(path)
    conf: Box = Box.from_yaml(filename=CONFIG, Loader=yaml.FullLoader)
    return conf


def init_logger(conf):
    logger = logging.getLogger(__name__)
    logger.setLevel(conf.logging.level)  # 0: not set, 10: debug, 20: info, 30: warning, 40: error, 50: critical

    file_handler = logging.FileHandler(filename=conf.logging.file)
    file_handler.setLevel(conf.logging.level)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(conf.logging.level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


# init config
conf = get_conf("config.yaml")

# init logging
logger = init_logger(conf)