import threading

from utils import GitLab, Job, Logger, Pipeline, Project, Runner


def process_pipeline(runners, jobs, pipeline):
    pending_job = jobs.get_pending_job(pipeline.id)
    if pending_job is None:
        return

    pending_job_tag_list = pending_job.tag_list

    # If idle list is empty, return
    if not runners.idle_list:
        return

    # Get an idle runner, add necessary tags and move it to the active list
    runner_id = runners.idle_list.pop(0)
    original_tag_list = runners.get_tags(runner_id)

    diff_tag_list = list(set(pending_job_tag_list) - set(original_tag_list))

    runners.add_tags(runner_id, diff_tag_list)
    runners.active_list.append(runner_id)
    runners.modified_tags_runner_list.append(runner_id)

def process_modified_runner(runners, jobs):
    if runners.modified_tags_runner_list is None:
        return

    for runner_id in runners.modified_tags_runner_list:
        runner = runners.query_runner(runner_id)
        # print(runner.id, runner.jobs.list())
        if runner.jobs.list() is None:
            continue
        job = runner.jobs.list()[-1]

        if jobs.job_finished_time_until_now(job.id) is not None and \
           jobs.job_finished_time_until_now(job.id).total_seconds() > 60:
            runners.recover_tags(runner_id)
            runners.modified_tags_runner_list.remove(runner_id)

def main():
    # Initialize system components
    gitlab = GitLab()
    runners = Runner()
    projects = Project()
    pipelines = Pipeline()
    jobs = Job()
    log = Logger(__name__).logger

    # Retrieve all pipelines
    pipeline_list = pipelines.get_all_pipelines()

    # Initialize Runner
    runners.init_tags()
    runners.init_idle_list()

    print("============================Monitor  Start============================")
    while True:
        runners.update_idle_list()

        # Check if there are running pipelines with pending jobs
        running_pipelines = pipelines.get_running_pipelines()
        if not running_pipelines:
            process_modified_runner(runners, jobs)
            continue

        # Update active runners list
        runners.update_active_list()

        threads = []
        for pipeline in running_pipelines:
            process_pipeline_thread = threading.Thread(target=process_pipeline, args=(runners, jobs, pipeline))
            process_pipeline_thread.start()
            threads.append(process_pipeline_thread)
            
            process_modified_runner_thread = threading.Thread(target=process_modified_runner, args=(runners, jobs))
            process_modified_runner_thread.start()
            threads.append(process_modified_runner_thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # process_modified_runner(runners, jobs)

if __name__ == '__main__':
    main()
