import os.path
from control.Application import Application
from control.JobHandler import JobHandler

app : Application = Application(os.path.dirname(__file__))

# Erstellung eines neuen Jobs für den Scan
JobHandler: JobHandler = JobHandler(app)
JobHandler.execute_job()

