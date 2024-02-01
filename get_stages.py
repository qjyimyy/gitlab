import info
from setting import color

for p in info.projects:
    # Get the running or pending pipelines for the project
    pipelines = p.pipelines.list(status='running' or 'pending')
    
    for pipeline in pipelines:
        # Get a list of all stage names in the pipeline
        stage_names = list(set(job.stage for job in pipeline.jobs.list()))
        # Get the current stage and its index in the pipeline
        current_stage_name = None
        current_stage_index = -1
        for index, stage_name in enumerate(stage_names):
            if current_stage_name is not None:
                break
            for job in pipeline.jobs.list():
                if job.stage == stage_name and (job.status == 'running' or job.status == 'pending'):
                    current_stage_name = stage_name
                    current_stage_index = index + 1
                    break
        print(color._blue + "Pipeline ID: " + color._ec + "{}".format(pipeline.id)
              + color._blue + " Status: " + color._ec + "{}".format(pipeline.status)
              + color._blue + " Current Stage: " + color._ec + "{} ({} of {})".format(current_stage_name, current_stage_index, len(stage_names))
              + color._blue + " Project ID: " + color._ec + "{}".format(pipeline.project_id)
              + color._blue + " Project Name: " + color._ec + "{}".format(p.name))