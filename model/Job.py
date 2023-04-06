from datetime import datetime
from model import SQLConntect
class Job():

    def __init__(self):
        self.job_id: int = 0
        self.dt_job_start: datetime = None
        self.dt_job_end: datetime = None
        self.int_processed_dir: int = 0
        self.int_processed_file: int= 0

    def createJob(self):

        self.job_ts_start= datetime.timestamp()

    def endJob(self):
        self.job_ts_end = datetime.timestamp()
        

