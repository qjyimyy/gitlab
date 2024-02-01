import info
from setting import color

for p in info.projects:
    # Get the running or pending pipelines for the project
    # pipelines = p.pipelines.list(status='running' or 'pending')
    
    # if len(pipelines) == 0:
    #     print("There is no running or pending pipeline in project {}.".format(p.name))
    #     continue
    
    pipelines = p.pipelines.list(status='success' )
    
    # Loop through the pipelines and print job status information
    for pipeline in pipelines:
        # Get a list of all stage names in the pipeline
        job_status = {"created": 0, "running": 0, "pending": 0, "failed": 0, "success": 0, "canceled": 0, "skipped": 0}

        for job in pipeline.jobs.list():
            job_status[job.status] += 1
                
        print(color._blue + "Pipeline ID: " + color._ec + "{}".format(pipeline.id)
            + color._blue + " Status: " + color._ec + "{}".format(pipeline.status)
            + color._blue + " Project ID: " + color._ec + "{}".format(pipeline.project_id)
            + color._blue + " Project Name: " + color._ec + "{}".format(p.name))
        print(" Jobs status information:")
        print(color._blue + "   Total Jobs: " + color._ec + "{}".format(len(pipeline.jobs.list()))
            + color._blue + " Created Jobs: " + color._ec + "{}".format(job_status["created"])
            + color._blue + " Running Jobs: " + color._ec + "{}".format(job_status["running"])
            + color._blue + " Pending Jobs: " + color._ec + "{}".format(job_status["pending"])
            + color._blue + " Success Jobs: " + color._ec + "{}".format(job_status["success"])
            + color._blue + " Failed Jobs: " + color._ec + "{}".format(job_status["failed"])
            + color._blue + " Canceled Jobs: " + color._ec + "{}".format(job_status["canceled"])
            + color._blue + " Skipped Jobs: " + color._ec + "{}".format(job_status["skipped"]))
