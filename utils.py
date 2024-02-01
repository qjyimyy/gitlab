import json
import logging
from datetime import datetime, timedelta

import gitlab


class GitLab:
    # Set GitLab API URL and access token
    gitlab_url = 'https://gitlab.com/'
    # access_token = 'glpat-6hdadKF11istc_zenCSB'
    access_token = 'glpat-GVkkAADHrhH8myA2xzQs'
    register_token = 'GR1348941gV8pYxmytcKA2F6vcZJQ'
    
    def __init__(self):
        # Connect to GitLab instance with the access token
        self.gl = gitlab.Gitlab(self.gitlab_url, private_token=self.access_token)
        
    def get_gl(self):
        # Returns the GitLab instance
        return self.gl
    
    def get_projects(self):
        # Returns a list of GitLab projects owned by the authenticated user
        return self.gl.projects.list(owned=True)

class Logger:
    def __init__(self, name, level=logging.INFO):
        """
        Initializes the logger with the specified logger name and logging level.
        :param name:name of the logger.
        :param level:logging level of the logger.
        """
        # create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level=level)
        
        # create log format
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        
        # create console handler
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(level=level)
        self.console_handler.setFormatter(formatter)
        
        # create file handler
        self.file_handler = logging.FileHandler('logfile.log')
        self.file_handler.setLevel(level=level)
        self.file_handler.setFormatter(formatter)
        
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)
        
    def info(self, msg):
        """
        Logs an info message.

        Args:
            msg (str): message to be logged
        """
        self.logger.info(msg=msg)
    
    def warning(self, msg):
        """
        Logs a warning message.

        Args:
            msg (str): message to be logged
        """
        self.logger.warning(msg=msg)
    
    def error(self, msg):
        """
        Logs an error message.

        Args:
            msg (str): message to be logged
        """
        self.logger.error(msg=msg)
   
class Project:
    def __init__(self) -> None:
        self.gl = GitLab().get_gl()
        self.projects = GitLab().get_projects()
         
    def get_all_projects(self):
        # get all the GitLab projects
        projects = []
        for p in self.projects:
            projects.append(p)
        return projects
            
    def query_project(self, project_id):
        # query a specific project
        for p in self.projects:
            if p.id == project_id:
                print("Project found: %s" % p)
                return p
            
    def show_projects(self):
        # display all the project details
        for p in self.get_all_projects():
            # Loop through the projects and print their ID and name
            print("project ID: {} project name: {}".format(p.id, p.name))

class Pipeline:
    def __init__(self):
        # get all the GitLab projects
        self.projects = GitLab().get_projects()
        # create a logger object for logging
        self.log = Logger(__name__).logger
    
    def get_all_pipelines(self):
        # get all the pipelines for all the projects
        pipelines = []
        for p in self.projects:
            # Get all status pipelines for the project
            pipelines.extend(p.pipelines.list(get_all=True))
        return pipelines
    
    def query_pipeline(self, pipeline_id):
        # query a specific pipeline
        for pipeline in self.get_all_pipelines():
            if pipeline.id == pipeline_id:
                # self.log.info("Pipeline found: %s" % pipeline)
                return pipeline
    
    def show_pipelines(self):
        # display all the pipeline details
        for pipeline in self.get_all_pipelines():
            # Loop through the pipelines and print their ID and status
            print("pipeline ID: {} status: {} project ID: {}".format(
                pipeline.id, pipeline.status, pipeline.project_id))

    def get_running_pipelines(self):
        running_pipelines = []
        for pipeline in self.get_all_pipelines():
            running_pipeline = self.query_pipeline(pipeline.id)
            if running_pipeline.status == 'running':
                running_pipelines.append(pipeline)
        if running_pipelines == []:
            print("No running pipelines...")
        else:
            print("running pipelines: {}".format(running_pipelines))
        return running_pipelines
                
    
    def get_pending_pipelines(self):
        
        # pending_pipelines = {}
        pending_pipelines = []
        # for pipeline in self.get_all_pipelines():
        #     if pipeline.status == "pending":
        #         # UTC+8:00
        #         pending_time = self.pending_diff_time(pipeline)
        #         pending_pipelines[pipeline.id] = pending_time
        
        # pending_pipelines = dict(sorted(pending_pipelines.items(), key=lambda x: x[1], reverse=True))
        # print(pending_pipelines)
        # return pending_pipelines
        for pipeline in self.get_all_pipelines():
            pending_pipeline = self.query_pipeline(pipeline.id)
            if pending_pipeline.status == 'pending':
                pending_pipelines.append(pipeline)
        print(pending_pipelines)
        return pending_pipelines
    
    def update_pending_pipeline(self):
        pending_pipelines = self.get_pending_pipelines()
        for k in self.get_pending_pipelines().keys():
            if self.query_pipeline(k).status != "pending":
                del pending_pipelines[k]
            
        
        pending_pipelines = dict(sorted(pending_pipelines.items(), key=lambda x: x[1], reverse=True))
        print(pending_pipelines)
        return pending_pipelines
    
    def pending_diff_time(self, pipeline):
        created_at = datetime.strptime(pipeline.created_at, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=8)
        current_time = datetime.now()
        return current_time - created_at
    
    # TODO: pipeline.id, jobs, difftime
    def get_pipelines_with_pending_jobs(self):
        # get all the pipelines with pending jobs
        pipelines_with_pending_jobs = []
        for pipeline in self.get_all_pipelines():
            for job in pipeline.jobs.list():
                if job.status == "pending":
                    pipelines_with_pending_jobs.append(pipeline.id)
        print("pipelines with pending jobs: {}".format(pipelines_with_pending_jobs))
        return pipelines_with_pending_jobs
    
    def finished_diff_time(self, pipeline_id):
        updated_at = datetime.strptime(self.query_pipeline(pipeline_id).updated_at, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=8)
        current_time = datetime.now()
        print("pipeline ID: {} difftime: {} updated_at: {} current_time: {}".format(pipeline_id, current_time - updated_at, updated_at, current_time))
        return current_time - updated_at
    
    def pipeline_runner_pair(self):
        pipeline_runner_pair = {}
        for pipeline in self.get_all_pipelines():
            if pipeline.status == "running":
                pipeline_runner_pair[pipeline.id] = pipeline.runner['id']
        print("pipeline_runner_pair: {}".format(pipeline_runner_pair))
        return pipeline_runner_pair
            
    
    def isFinished(self, pipeline_id):
        # check if the pipeline is finished
        if pipeline_id in self.pipeline_runner_pair().keys():
            pipeline = self.query_pipeline(pipeline_id)
            if pipeline.status == "success" or pipeline.status == "failed" or pipeline.status == "canceled":
                print("pipeline ID: {} status: {} project ID: {}".format(pipeline_id, pipeline.status, pipeline.project_id) + " has been finished")
            return self.finished_diff_time(pipeline_id)
    
    def remove_failed_pipeline(self):
        # remove the failed pipeline
        threshold_time = timedelta(hours=24)
        for pipeline in self.get_all_pipelines():
            if pipeline.status == "failed":
                if self.pending_diff_time(pipeline) >= threshold_time:
                    pipeline.delete()
                print("pipeline ID: {} status: {} project ID: {}".format(
                    pipeline.id, pipeline.status, pipeline.project_id) + " has been removed")

    def remove_canceled_pipeline(self):
        # remove the canceled pipeline
        threshold_time = timedelta(hours=12)
        for pipeline in self.get_all_pipelines():
            if pipeline.status == "canceled":
                if self.pending_diff_time(pipeline) > threshold_time:
                    pipeline.delete()
                print("pipeline ID: {} status: {} project ID: {}".format(
                    pipeline.id, pipeline.status, pipeline.project_id) + " has been removed")

    def remove_passed_pipeline(self):
        # threshold_time = timedelta(weeks=2)
        for pipeline in self.get_all_pipelines():
            if pipeline.status == "success":
                # if self.pending_diff_time(pipeline) > threshold_time:
                pipeline.delete()
                print("pipeline ID: {} status: {} project ID: {}".format(
                    pipeline.id, pipeline.status, pipeline.project_id) + " has been removed") 
            
# Pipeline().get_running_pipelines()
# Pipeline().remove_passed_pipeline()

class Job:
    def __init__(self):
        self.pipelines = Pipeline()
        self.log = Logger(__name__).logger
        
    def get_all_jobs(self):
        # get all the jobs for all the pipelines
        all_jobs = []
        for pipeline in self.pipelines.get_all_pipelines():
            for job in pipeline.jobs.list():
                all_jobs.append(job)
        return all_jobs
    
    def query_job(self, job_id):
        # query the job by job id
        for job in self.get_all_jobs():
            if job.id == job_id:
                # print(job.stage)
                # self.log.info("job ID: {} status: {} pipeline ID: {}".format(job_id, job.status, job.pipeline_id))
                return job
    
    def show_jobs(self):
        # display all the jobs for all the pipelines
        # Loop through the pipelines and print job status information
        for pipeline in self.pipelines.get_all_pipelines():
            # create a dictionary to store the job status information
            # Get a list of all stage names in the pipeline
            job_status = {"created": 0, "running": 0, "pending": 0, 
                          "failed": 0, "success": 0, "canceled": 0, "skipped": 0}

            # loop through all the jobs in the pipeline and update the job status dictionary
            for job in pipeline.jobs.list():
                    job_status[job.status] += 1
            
            # self.show_pipelines()
            print("pipeline ID: {} status: {} project ID: {}".format(
                pipeline.id, pipeline.status, pipeline.project_id) + "\n    Jobs status information:\n" 
                          + "       Total Jobs: {} job status: {}".format(len(pipeline.jobs.list()), job_status))
            # print(" Jobs status information:")
            # print("     Total Jobs: {} job status: {}".format(len(pipeline.jobs.list()), job_status))
    
    def job_finished_time_until_now(self, job_id):
        job = self.query_job(job_id)
        # runner_id = job.runner['id']
        if job.status == "success" or job.status == "failed" or job.status == "canceled" or job.status == "skipped":
            finished_at = datetime.strptime(job.finished_at, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=8)
            current_time = datetime.now()
            # self.log.info("job ID: {} difftime: {} finished_at: {} current_time: {}".format(job_id, current_time - finished_at, finished_at, current_time))
            return current_time - finished_at

    def pipeline_all_stages(self, pipeline_id):
        pipeline =  self.pipelines.query_pipeline(pipeline_id)
        stage_list = []
        for job in pipeline.jobs.list():
            # print(job.id)
            job = self.query_job(job.id)
            stage_list.append(job.stage)
            # print(job.stage)
        stage_list = list(set(stage_list))
        print(stage_list)
        return stage_list
    
    def job_in_stage(self, job_id, stage_list):
        total_stage_nums = len(stage_list)
        job = self.query_job(job_id)
        count = 1
        for stage in stage_list:
            if job.stage == stage:
                print("current stage: {} / total stage: {}".format(count, total_stage_nums))
                return count
            else:
                count += 1
                
    # def get_pending_job_tag_list(self, pipeline_id):
    #     pipeline = self.pipelines.query_pipeline(pipeline_id)
    #     for job in pipeline.jobs.list():
    #         job = self.query_job(job.id)
    #         if job.status == 'pending':
    #             return job.tag_list
    #     return None 
    
    def get_pending_job(self, pipeline_id):
        pipeline = self.pipelines.query_pipeline(pipeline_id)
        for job in pipeline.jobs.list():
            job = self.query_job(job.id)
            if job.status == 'pending':
                return job
        return None 
        
            

# Job().query_job(4292847921)
# Job().show_jobs()
# Job().get_job_runner_pair(4292847921)
# Job().job_finished_time_until_now(4292847921)
# job = Job()
# stage_list = job.pipeline_all_stages(868853761)
# job.job_in_stage(4292847921, stage_list)
# Job().isPending(868853761)

class Runner:
    def __init__(self):
        self.gl = GitLab().get_gl()
        
        self.runners = self.gl.runners
        self.runner_list = self.runners.list()
        
        self.pipelines = Pipeline()
        
        self.jobs = Job()
        
        self.log = Logger(__name__).logger
        
        self.idle_list = []
        self.idle_time = {}
        
        self.active_list = []

        self.modified_tags_runner_list = []
    
    def nums(self):
        print("Total runners: {}".format(len(self.runner_list)))
        return len(self.runner_list)
    
    def info(self):
        """
        Prints information about each runner in the runner list to the console.
    
        This method iterates over each runner in the runner list and prints its ID, description, and status 
        to the console in a formatted string. 
    
        Args:
            None
    
        Returns:
            None
        """
        for runner in self.runner_list:
            print("runner ID: {} runner description: {:<15} status:{}".format(
                runner.id, runner.description, runner.status))
    
    def query_runner(self, runner_id):
        runner = self.runners.get(runner_id)
        # self.log.info("runner ID: {} runner description: {:<15} status:{}".format(runner_id, runner.description, runner.status))
        return runner
    
    def init_tags(self):
        """
        This method initializes tags for all runners and saves them to a JSON file named 'runner_tags.json'.
    
        :return: None
        """
        # A dictionary to store runner tags
        runner_tags = {}
        for i in range(self.nums()): # Iterate over all runners
            # Get the ID of the current runner
            runner_id = self.runner_list[i].id
            # Get the GitLab Runner object for the current runner
            runner =  self.runners.get(runner_id)
            # Add the current runner's tag list to the runner_tags dictionary
            runner_tags[runner_id] = runner.tag_list
            
            # print("runner ID: {} runner tags: {}".format(
            #     runner_id, runner.tag_list))
        
            # Write the runner_tags dictionary to a JSON file named 'runner_tags.json'
            with open('runner_tags.json', 'w') as f:
                json.dump(runner_tags, f)
        print("+++++Runner tags initialized and saved to 'runner_tags.json' file+++++")
    
    def get_tags(self, runner_id):
        """
        This method returns the tag list for the specified runner ID.
    
        :param runner_id: the ID of the runner whose tag list needs to be returned
        :return: the tag list for the specified runner ID
        """
        # Get the runner object for the specified runner ID
        runner = self.query_runner(runner_id)
        # Get the tag list for the specified runner ID
        tag_list = runner.tag_list
        print("runner ID: {} runner tags: {}".format(runner_id, tag_list))
        return tag_list
    
    def add_tags(self, runner_id, new_tags):
        """
        Adds one or more tags to a runner's tag list and saves the updated tag list to a JSON file.
    
        This method takes a runner ID and a list of new tags to add, finds the runner with that ID in the runner list, 
        and adds the new tags to its tag list. It then saves the updated tag list for that runner to a JSON file named 
        "temp_tags.json".
    
        Args:
            runner_id (int): The ID of the runner to add tags to.
            new_tags (list): A list of tags to add to the runner's tag list.
    
        Returns:
            None
        """
        for runner in self.runner_list:
            # Check if current runner is the one to add tags to
            if runner.id == runner_id:
                # Get the runner from the runners dictionary
                runner = self.runners.get(runner_id)
                # Add new tags to the runner's tag list
                current_tags = runner.tag_list 
                current_tags += new_tags
                # current_tags.append(new_tags)
                runner.tag_list = current_tags
                runner.save()

                # Save updated tag list for the runner to a JSON file
                with open("temp_tags.json", "w") as f:
                    tag_dict = {}
                    # counter = {}
                    tag_dict[runner.id] = runner.tag_list 
                    json.dump(tag_dict,f)
                
        print("Tags added to runner ID {}: {}".format(runner_id, new_tags))
    
    def recover_tags(self, runner_id):
        """
        This method recovers the tag list for the specified runner ID by reading the runner_tags.json file,
        which contains a dictionary of runner IDs and their corresponding tag lists.

        :param runner_id: the ID of the runner whose tag list needs to be recovered
        """
        # Get the runner object for the specified runner ID
        runner = self.runners.get(runner_id)
        
        # Load the runner tags dictionary from the runner_tags.json file
        with open("runner_tags.json", "r") as f:
            runner_tags = json.load(f)
        # print(runner_tags)
            
        # Find the tag list for the specified runner ID in the runner tags dictionary
        for k, v in runner_tags.items():
            if k == str(runner_id):
                # print(k, v)
                current_tags = v
                runner.tag_list=current_tags
                runner.save()
        
        print("Tags recovered to runner ID {}: {}".format(runner_id, runner.tag_list))
    
    def isOnline(self, runner_id):
        """
        Checks whether a runner is online.

        Args:
            runner_id (int): The ID of the runner to check.

        Returns:
            bool: True if the runner is online, False otherwise.
        """
        # Get the runner by its ID
        runner = self.runners.get(runner_id)
        # Check if the runner status is "online"
        if runner.status == "online":
            return True
        
    def online_usable(self):
        """
        Counts the number of online runners and returns the count
        """
        count = 0
        online_runners = {}
        for runner in self.runner_list:
            if self.isOnline(runner.id):
                online_runners[runner.id] = self.difftime(runner.id)
                count += 1
        print("There are {} online runner(s)".format(count))
        return count, online_runners
    
    def init_idle_list(self):
        for runner in self.runner_list:
            if runner.status == 'online':
                print(runner)
                self.idle_list.append(runner.id)
        print(self.idle_list)
    
    def init_idle_time(self):
        for runner in self.runner_list:
            self.idle_time[runner.id] = datetime.utcnow()
        print("idle runner available: {}".format(self.idle_time))
    
    def update_idle_time(self):
        for runner in self.runner_list:
            if runner.jobs.list() != []:
                finished_at = datetime.strptime(runner.jobs.list()[-1].finished_at, "%Y-%m-%dT%H:%M:%S.%fZ") #+ timedelta(hours=8)
                # print(" job ID: {} finished_at: {}".format(runner.jobs.list()[-1].id, finished_at))
                self.idle_time[runner.id] = (datetime.utcnow() - finished_at).seconds
            else:
                self.idle_time[runner.id] = (datetime.utcnow() - self.idle_time[runner.id]).seconds
            
            # self.idle_time = dict(sorted(self.idle_time.items(), key=lambda x: x[1], reverse=True))
            # sorted_dict = dict(sorted(self.idle_time.items(), key=operator.itemgetter(1)))
            
            print("runner ID: {} idle time: {}".format(runner.id, self.idle_time[runner.id]))
    
    def update_active_list(self):
        if self.idle_list == []:
            return
        
        for runner_id in self.idle_list:
            runner = self.query_runner(runner_id)
            if runner.jobs.list() == []:
                continue
            job = runner.jobs.list()[-1]
            if job.status == 'running':
                self.active_list.append(runner.id)
                self.idle_list= list(set(self.idle_list)-set(self.active_list))
        
        print("active list: {} idle list: {}".format(self.active_list, self.idle_list))
        
    def add_runner_into_active_list(self, runner_id):
        self.active_list.append(runner_id)
        # self.idle_list = list(set(self.idle_list)-set(self.active_list))
        print("active list: {} idle list: {}".format(self.active_list, self.idle_list))
    
    def update_idle_list(self):
        if self.active_list == []:
            return
        
        for runner_id in self.active_list:
            runner = self.query_runner(runner_id)
            if runner.jobs.list() == []:
                continue
            job = runner.jobs.list(get_all=True)[-1]
            if job.status != 'running':
                self.idle_list.append(runner.id)
                self.active_list = list(set(self.active_list)-set(self.idle_list))
                
        print("active list: {} idle list: {}".format(self.active_list, self.idle_list))
                
    
    def test(self):
        for runner in self.runner_list:
           print(runner.jobs.list()) 
            
        

# Runner().isActive(22789374)
# Runner().info()
# runner = Runner()
# runner.init_idle_time()
# runner.update_idle_time()
# Runner().test()
# Runner().init_idle_list()
# Runner().get_tags(22789374)
# Runner().add_tags(22789374, ['ragemule'])
# Runner().test()