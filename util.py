import logging
from pathlib import Path
from box import Box
import yaml


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


def get_conf():
    CONFIG = Path("config.yaml")
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
conf = get_conf()

# init logging
logger = init_logger(conf)