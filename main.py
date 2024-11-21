import time
import util
import sys

from simulation import Simulation
from visualization.data_viewer import DataViewer

# init logging
logger = util.logger

if __name__ == "__main__":

    # init config
    conf = util.get_conf()

    simulation = Simulation(conf)

    dataViewer = DataViewer(simulation.students)
    # dataViewer.plotThirstDistribution()

    """
    The simulation runs regardless of the speed at which the graphics can be drawn,
    unless headless is set to true in config.yaml, in which case it runs as fast as possible without graphics.
    """
    start = time.time()
    current_time = start
    last_time = start
    frame_time = 1.0 / simulation.fps
    while simulation.simulation_time < simulation.max_end_time:
        current_time = time.time()
        delta_time = current_time - last_time

        if delta_time >= frame_time:
            simulation.run_for(delta_time * simulation.simulation_speed)
            if not conf.headless:
                simulation.draw(delta_time)
                simulation.handle_pygame_events()
            last_time = current_time

    # Currently, the simulation screen terminates automatically when the end time is reached.
    # Uncomment the code below if you want the screen to remain until it is manually closed.
    # while True:
    #     time.sleep(0.01)


