import os
import pandas as pd

class DataStorage():
    def __init__(self):
        batch_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.join(__file__, ".."))), "batches") 
        if(not os.path.exists(batch_dir)):
            os.mkdir(batch_dir)

        self.create_dir_name = lambda name, number: f"{name}{number}"
        self.current_batch_dir = os.path.join(batch_dir, self.create_dir_name("batch", len(os.listdir(batch_dir))))
        if(not os.path.exists(self.current_batch_dir)):
            os.mkdir(self.current_batch_dir)

        self.current_run_data = None

        self.start_run()



    def start_run(self) -> None:
        self.current_run_dir = os.path.join(self.current_batch_dir, self.create_dir_name("runs", len(os.listdir(self.current_batch_dir))))
        os.mkdir(self.current_run_dir)

        self.current_run_csv = os.path.join(self.current_run_dir, "data.csv")
        self.current_run_data = []

    # Cant give student type because of circular imports
    def add_data_entry(self, timestamp: int, student, action: str, duration: int) -> None:
        if self.current_run_data != None:
            self.current_run_data.append([timestamp, student.name, action, duration, timestamp // (360 * 8), student.total_drinks])

    def end_run(self) -> None:
        data_frame = pd.DataFrame(self.current_run_data, columns=["Timestamp", "Name", "Action", "Duration", "Day", "Total Drinks"])
        data_frame.to_csv(self.current_run_csv, index_label="ID")

        self.current_run_data = None
        

