import info
from setting import color

for p in info.projects:
    # Get the running or pending pipelines for the project
    pipelines = p.pipelines.list(status='running' or 'pending')
    # Get the successful pipelines for the project
    pipelines = p.pipelines.list(status='success')
    
    # Loop through the pipelines and print their ID and status
    for pipeline in pipelines:
        print(color._blue + "Pipeline ID: " + color._ec + "{}".format(pipeline.id) 
          + color._blue + " Status: " + color._ec + "{}".format(pipeline.status)
          + color._blue + " Project ID: " + color._ec + "{}".format(pipeline.project_id)
          + color._blue + " Project Name: " + color._ec + "{}".format(p.name))
