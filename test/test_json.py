import json

# a Python object (dict):
"""
x: list= []
x.append(dict(name="Max", age=25, city="Berlin"))
x.append(dict(name="John", age=30, city="New York"))
"""

x= [{"id_job":1,"dt_start_job":"2023-04-07T14:24:30","dt_end_job":"2023-04-07T14:24:30","int_processed_dir":201,"int_processed_file":783},{"id_job":2,"dt_start_job":"2023-04-07T15:00:09","dt_end_job":"2023-04-07T15:00:09","int_processed_dir":201,"int_processed_file":783},{"id_job":3,"dt_start_job":"2023-04-09T12:41:46","dt_end_job":"2023-04-09T12:41:47","int_processed_dir":201,"int_processed_file":783},{"id_job":4,"dt_start_job":"2023-04-09T12:41:59","dt_end_job":"2023-04-09T12:41:59","int_processed_dir":201,"int_processed_file":783},{"id_job":5,"dt_start_job":"2023-04-09T12:42:13","dt_end_job":"2023-04-09T12:42:14","int_processed_dir":201,"int_processed_file":783},{"id_job":6,"dt_start_job":"2023-04-09T12:43:07","dt_end_job":"2023-04-09T12:43:07","int_processed_dir":201,"int_processed_file":783},{"id_job":7,"dt_start_job":"2023-04-09T12:52:37","dt_end_job":"2023-04-09T12:52:37","int_processed_dir":201,"int_processed_file":783}]

# convert into JSON:
y = json.dumps(x)

# the result is a JSON string:
print(y)

z = json.loads(y)

# the result is a Python dictionary:
for m in z:
    print(m["id_job"])