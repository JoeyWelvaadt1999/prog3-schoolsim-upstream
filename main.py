import time
import util
import sys

from simulation import Simulation
from visualization.data_viewer import DataViewer
from visualization.data_storage import DataStorage
import argparse

# init logging
logger = util.logger

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script that adds 3 numbers from CMD"
    )
    parser.add_argument("--batch", required=True, type=bool)
    args = parser.parse_args()

    batch_run = args.batch

    # init config
    conf = util.get_conf("config.yaml")
    batch_conf = util.get_conf("batch_config.yaml")
    print(batch_conf)

    store = DataStorage()
    # dataViewer = DataViewer(simulation.students)
    # dataViewer.plotThirstDistribution()

    base_configuration = {
        "schedule": True,
        "characteristics": False,
        "coffee_machines": 4,
        "students": 60
    }

    batch_configurations = [batch_conf.configurations[key] for key in list(batch_conf.configurations.keys())]
    print(batch_configurations)

    configurations = [base_configuration]

    if(batch_run):
        conf.headless = True
        configurations = batch_configurations

    simulation = Simulation(conf, store, configurations[0])
    for i in range(len(configurations)): 
        store.open_new_conf()
        for j in range(configurations[i].run_times):
            store.start_run()
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
                if simulation.simulation_time > simulation.max_end_time:
                    break
                
            store.end_run()
            simulation.reset(conf, configurations[i])
            util.Clock.reset_clock()
        if(i + 1 < len(configurations)):
            simulation.reset(conf, configurations[i + 1])

    # Currently, the simulation screen terminates automatically when the end time is reached.
    # Uncomment the code below if you want the screen to remain until it is manually closed.
    # while True:
    #     time.sleep(0.01)


