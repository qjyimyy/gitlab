import allocator
import utils


def main():
    # init system
    GL = utils.GitLab()
    RUNNERS = utils.Runner()
    PROJECTS = utils.Project()
    PIPELINES = utils.Pipeline()
    JOBS = utils.Job()
    log = utils.Logger(__name__).logger
    
    # TODO: init allocator
    
    pipelines = PIPELINES.get_all_pipelines() # pipeline list
    
    # init Runner
    RUNNERS.init_tags()
    RUNNERS.init_idle_list()
    # RUNNERS.init_idle_time()
    
    print("============================Monitor  Start============================")
    while (True):
        # TODO: main operations
        RUNNERS.update_idle_list()
        # check whether there is a running pipeline with some pending jobs
        running_pipelines = PIPELINES.get_running_pipelines()
        if len(running_pipelines) == 0:
            continue
        # if there is a such pipeline, copy the tag of pending jobs need
        # RUNNERS.update_idle_list()
        RUNNERS.update_active_list()
        for pipeline in running_pipelines:
            pending_job_tag_list = JOBS.get_pending_job_tag_list(pipeline.id)
            # if idle list is empty, break
            if RUNNERS.idle_list == []:
                break
            # if there is a idle runner, add copied tag to it
            # RUNNERS.update_active_list()
            runner_id = RUNNERS.idle_list.pop(0)
            # RUNNERS.active_list.append(runner_id)
            original_tag_list = RUNNERS.get_tags(runner_id)
            diff_tag_list = list(set(pending_job_tag_list)-set(original_tag_list))
            if diff_tag_list != []:
                RUNNERS.add_tags(runner_id, diff_tag_list)
            RUNNERS.add_runner_into_active_list(runner_id)
            RUNNERS.modified_tags_runner_list.append(runner_id)
            break
        
        for runner_id in RUNNERS.modified_tags_runner_list:
            runner = RUNNERS.query_runner(runner_id)
            job = runner.jobs.list()[-1]
            if JOBS.job_finished_time_until_now(job.id) is not None and JOBS.job_finished_time_until_now(job.id).total_seconds() > 60:
                RUNNERS.recover_tags(runner_id)
                RUNNERS.modified_tags_runner_list.remove(runner_id)
            

if __name__ == '__main__':
    main()
    
