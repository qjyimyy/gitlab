from utils import GitLab, Job, Logger, Pipeline, Project, Runner


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
            # Check if any modified runners have finished their jobs and recover their original tags if they have
            if runners.modified_tags_runner_list is None:
                continue
            for runner_id in runners.modified_tags_runner_list:
                runner = runners.query_runner(runner_id)
                job = runner.jobs.list()[-1]

                if jobs.job_finished_time_until_now(job.id) is not None and \
                jobs.job_finished_time_until_now(job.id).total_seconds() > 30:
                    runners.recover_tags(runner_id)
                    runners.modified_tags_runner_list.remove(runner_id)
            continue

        # Update active runners list
        runners.update_active_list()

        for pipeline in running_pipelines:
            pending_job = jobs.get_pending_job(pipeline.id)
            if pending_job is None:
                continue
            pending_job_tag_list = pending_job.tag_list
            
            # # Ensure that pending_job_tag_list and original_tag_list are not None before creating diff_tag_list
            # if pending_job_tag_list is None:
            #     print("Error: pending_job_tag_list is None")
            #     continue

            # If idle list is empty, break
            if not runners.idle_list:
                break

            # Get an idle runner, add necessary tags and move it to the active list
            runner_id = runners.idle_list.pop(0)
            original_tag_list = runners.get_tags(runner_id)
            
            diff_tag_list = list(set(pending_job_tag_list) - set(original_tag_list))

            runners.add_tags(runner_id, diff_tag_list)
            # runners.add_runner_into_active_list(runner_id)
            runners.active_list.append(runner_id)
            runners.modified_tags_runner_list.append(runner_id)
            break

        # Check if any modified runners have finished their jobs and recover their original tags if they have
        if runners.modified_tags_runner_list is None:
            continue
        for runner_id in runners.modified_tags_runner_list:
            runner = runners.query_runner(runner_id)
            job = runner.jobs.list()[-1]

            if jobs.job_finished_time_until_now(job.id) is not None and \
               jobs.job_finished_time_until_now(job.id).total_seconds() > 30:
                runners.recover_tags(runner_id)
                runners.modified_tags_runner_list.remove(runner_id)


if __name__ == '__main__':
    main()
