import os
import pandas as pd
from student import Student

class DataStorage():
    def __init__(self):
        batch_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.join(__file__, ".."))), "batches") 
        if(not os.path.exists(batch_dir)):
            os.mkdir(batch_dir)

        self.create_dir_name = lambda name, number: f"{name}{number}"
        self.current_batch_dir = os.path.join(batch_dir, self.create_dir_name("batch", len(os.listdir(batch_dir))))
        if(not os.path.exists(self.current_batch_dir)):
            os.mkdir(self.current_batch_dir)

        self.start_run()



    def start_run(self) -> None:
        self.current_run_dir = os.path.join(self.current_batch_dir, self.create_dir_name("runs", len(os.listdir(self.current_batch_dir))))
        os.mkdir(self.current_run_dir)

        self.current_run_csv = os.path.join(self.current_run_dir, "data.csv")
        self.current_run_data = []

    def add_data_entry(self, timestamp: int, student: Student, action: str, duration: int) -> None:
        pass

    def end_run(self) -> None:
        data_frame = pd.DataFrame(self.current_run_data, columns=["Timestamp", "Name", "Action", "Duration"])
        data_frame.to_csv(self.current_run_csv)
        pass
