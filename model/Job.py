from datetime import datetime
class Job():

    def __init__(self):
        self.job_id: int = 0
        self.job_ts_start: float = 0
        self.job_ts_end: float = 0

    def createJob(self):
        self.job_ts_start= datetime.timestamp()

    def endJob(self):
        self.job_ts_end = datetime.timestamp()
        

