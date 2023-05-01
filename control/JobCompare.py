class JobCompare():
    """

    """

    def __init__(self, source_job_list: dict, dest_job_list: dict):
        self.source_job:dict = source_job_list
        self.dest_job:dict =dest_job_list

    def doCompare(self):
        for source_element in self.source_job:
            source: dict = source_element
            match:dict= self._get_element_by_path(source.get("path"))
            if match:
                return

    def _get_element_by_path(self, str_path: str) -> dict:
        for dest_element in self.dest_job:
            dest: dict =dest_element
            if dest.get("path").__eq__(str_path):
                 return dest

    def _get_diff(self, source: dict, dest: dict):
        # Vergleichen der Attribute
        keys:list= source.items()