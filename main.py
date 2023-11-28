import time
import util

from simulation import Simulation

# init logging
logger = util.logger

if __name__ == "__main__":

    # init config
    conf = util.get_conf()

    simulation = Simulation(conf)

    """
    The simulation runs regardless of the speed at which the graphics can be drawn.
    """
    start = time.time()
    current_time = start
    last_time = start
    frame_time = 1.0 / simulation.fps
    while simulation.simulation_time < simulation.max_end_time:
        current_time = time.time()
        delta_time = current_time - last_time

        if(delta_time >= frame_time):
            simulation.run_for(delta_time * simulation.simulation_speed)
            simulation.draw(delta_time)
            simulation.handle_pygame_events()
            last_time = current_time

    # Currently, the simulation screen terminates automatically when the end time is reached.
    # Uncomment the code below if you want the screen to remain until it is manually closed.
    # while True:
    #     time.sleep(0.01)
