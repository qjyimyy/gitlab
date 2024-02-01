import time

import utils


class Scheduler:
    def __init__(self):
        self.gl = utils.GitLab()
        self.runner = utils.Runner()
        self.info = utils.Pipeline()
        self.log = utils.Logger()
        
    
    # TODO: implement
    def period(self):
        pass
    
    # TODO: implement
    def monitoring(self):
        # 查询所有正在运行的pipeline
        # 如果没有pending状态的pipeline，那么就break
        # 如果有pending状态的pipeline，查询这个pipeline的创建时间
        pass
    
    def pending_pipelines_jobs(self):
        pass
    
    def pending_jobs_pipelines(self):
        pass